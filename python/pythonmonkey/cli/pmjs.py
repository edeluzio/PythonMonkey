#! /usr/bin/env python3
# @file         pmjs - PythonMonkey REPL
# @author       Wes Garland, wes@distributive.network
# @date         June 2023

import sys, os, readline, signal
import pythonmonkey as pm

def main():
    globalThis = pm.eval("globalThis;")
    globalThis.python.write = sys.stdout.write
    pm.createRequire(__file__)('./pmjs-require')
    
    pm.eval("""'use strict';
    const cmds = {};
    
    cmds.help = function help() {
      return '' +
    `.exit     Exit the REPL
    .help     Print this help message
    .load     Load JS from a file into the REPL session
    .save     Save all evaluated commands in this REPL session to a file
    
    Press Ctrl+C to abort current expression, Ctrl+D to exit the REPL`
    };
    
    cmds.exit = python.exit;
    
    /**
     * Handle a .XXX command. Invokes function cmds[XXX], passing arguments that the user typed
     * as the function arguments. The function arguments space-delimited arguments; arguments
     * surrounded by quotes can include spaces, similar to how bash parses arguments. Argument
     * parsing cribbed from stackoverflow user Tsuneo Yoshioka, question 4031900.
     *
     * @param {string} cmdLine     the command the user typed, without the leading .
     * @returns {string} to display
     */
    globalThis.replCmd = function replCmd(cmdLine)
    {
      const cmdName = (cmdLine.match(/^[^ ]+/) || ['help'])[0];
      const args = cmdLine.slice(cmdName.length).trim();
      const argv = args.match(/\\\\?.|^$/g).reduce((p, c) => {
            if (c === '"')
              p.quote ^= 1;
            else if (!p.quote && c === ' ')
              p.a.push('');
            else
              p.a[p.a.length-1] += c.replace(/\\\\(.)/,"$1");
            return  p;
        }, {a: ['']}).a;
    
      if (!cmds.hasOwnProperty(cmdName))
        return `Invalid REPL keyword`;
      return cmds[cmdName].apply(null, argv);
    }
    
    /** Return String(val) surrounded by appropriate ANSI escape codes to change the console text colour. */
    function colour(colourCode, val)
    {
      const esc=String.fromCharCode(27);
      return `${esc}[${colourCode}m${val}${esc}[0m`
    }
    
    /** 
     * Format result more intelligently than toString. Inspired by Node.js util.inspect, but far less 
     * capable.
     */
    globalThis.formatResult = function formatResult(result)
    {
      switch (typeof result)
      {
        case 'undefined':
          return colour(90, result);
        case 'function':
          return colour(36, result);
        case 'string':
          return colour(32, `'${result}'`);
        case 'boolean':
        case 'number':
          return colour(33, result);
        case 'object':
          if (result instanceof Date)
            return colour(35, result.toISOString());
          if (result instanceof Error)
          {
            const error = result;
            const LF = String.fromCharCode(10);
            const stackEls = error.stack
                             .split(LF)
                             .filter(a => a.length > 0)
                             .map(a => `    ${a}`);
            return (`${error.name}: ${error.message}` + LF
              + stackEls[0] + LF
              + colour(90, stackEls.slice(1).join(LF))
            );
          }
          return JSON.stringify(result);
        default:
          return colour(31, `<unknown type ${typeof result}>${result}`);
      }
    }
    
    /**
     * Evaluate a complete statement, built by the Python readline loop.
     */
    globalThis.replEval = function replEval(statement)
    {
      const indirectEval = eval;
      try
      {
        const result = indirectEval(`${statement}`);
        return formatResult(result);
      }
      catch(error)
      {
        return formatResult(error);
      }
    }
    """);
    
    readline.parse_and_bind('set editing-mode emacs')
    histfile = os.path.expanduser('~/.pmjs_history')
    if (os.path.exists(histfile)):
        readline.read_history_file(histfile)
    
    print('Welcome to PythonMonkey v' + pm.__version__ +'.')
    print('Type ".help" for more information.')
    
    def quit():
         readline.write_history_file(histfile)
         sys.exit(0)
    globalThis.python.exit = quit
    
    got_sigint = 0
    building_statement = False
    
    # Try to handle ^C by aborting the entry of the current line and quitting when double-struck. Note that
    # does not currently work properly because there doesn't seem to be an easy way to abort data entry via
    # input() via gnu readline in Python.
    def sigint_handler(signum, frame):
        global got_sigint
        global building_statement
        got_sigint = got_sigint + 1
        if (got_sigint == 1 and building_statement == False):
            print('(To exit, press Ctrl+C again or Ctrl+D or type .exit)')
        if (got_sigint > 1 and building_statement == False):
            quit()
        readline.redisplay()
    signal.signal(signal.SIGINT, sigint_handler)
    
    # Main Program Loop #####
    #
    # Read lines entered by the user and collect them in a statement. Once the statement is a candiate for
    # JavaScript evaluation (determined by pm.isCompilableUnit(), send it to replEval(). Statement beginning
    # with a . are interpreted as REPL commands and sent to replCmd().
    while got_sigint < 2:
        try:
            building_statement = False
            statement = input('> ')
    
            if (len(statement) == 0):
                continue
            if (statement[0] == '.'):
                print(globalThis.replCmd(statement[1:]))
                continue
            if (pm.isCompilableUnit(statement)):
                print(globalThis.replEval(statement))
                got_sigint = 0
            else:
                building_statement = True
                got_sigint = 0
                while (got_sigint == 0):
                    more = input('... ')
                    statement = statement + '\n' + more
                    if (pm.isCompilableUnit(statement)):
                        print(globalThis.replEval(statement))
                        break
                got_sigint = 0
                building_statement = False
        except EOFError:
            print()
            quit()

if __name__ == "__main__":
    main()
