import pythonmonkey as pm

def test_assign():
    items = [1,2,3]
    pm.eval("(arr) => {arr[0] = 42}")(items)
    assert items[0] == 42

def test_get():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr[1]}")(result, items)
    assert result[0] == 2

def test_get_length():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.length}")(result, items)
    assert result[0] == 3    

def test_missing_func():
    items = [1,2,3]
    try:
        pm.eval("(arr) => {arr.after()}")(items)         
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'pythonmonkey.SpiderMonkeyError'>"
        assert str(e).__contains__('TypeError: arr.after is not a function')        

#reverse
def test_reverse():
    items = [1,2,3]
    pm.eval("(arr) => {arr.reverse()}")(items)
    assert items == [3,2,1]   

def test_reverse_size_one():
    items = [1]
    pm.eval("(arr) => {arr.reverse()}")(items)
    assert items == [1]  

def test_reverse_size_zero():
    items = []
    pm.eval("(arr) => {arr.reverse()}")(items)
    assert items == []          

def test_reverse_returns_reference():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reverse(); result[0][0] = 4}")(result, items)
    assert result[0] == [4,2,1]
    assert items == [4,2,1]      

def test_reverse_ignores_extra_args():
    items = [1,2,3]
    pm.eval("(arr) => {arr.reverse(9)}")(items)
    assert items == [3,2,1]   

#pop
def test_pop():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.pop()}")(result, items)
    assert items == [1,2]
    assert result[0] == 3      

def test_pop_empty():
    items = []
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.pop()}")(result, items)
    assert items == []
    assert result[0] is None       

def test_pop_ignore_extra_args():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.pop(1)}")(result, items)
    assert items == [1,2]
    assert result[0] == 3      

#join
def test_join_no_arg():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.join()}")(result, items)
    assert result[0] == '1,2,3'     

def test_join_empty_array():
    items = []
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.join()}")(result, items)
    assert result[0] == ''       

def test_join_no_arg_diff_types():
    items = [1,False,"END"]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.join()}")(result, items)
    assert result[0] == '1,false,END'     

def test_join_no_arg_with_embedded_list_type():
    items = [1,[2,3],"END"]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.join()}")(result, items)
    assert result[0] == '1,2,3,END'   

def test_join_with_sep():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.join('-')}")(result, items)
    assert result[0] == '1-2-3'

def test_join_none():
    items = [None,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.join()}")(result, items)
    assert result[0] == ',2,3'    

def test_join_null():
    items = [pm.null,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.join()}")(result, items)
    assert result[0] == ',2,3'  

def test_join_utf8():
    prices = ["￥7", 500, 8123, 12]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.join()}")(result, prices)
    assert result[0] == '￥7,500,8123,12'               

#toString
def test_toString():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.toString()}")(result, items)
    assert result[0] == '1,2,3'
    
#push
def test_push():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.push(4)}")(result, items)
    assert items == [1,2,3,4]
    assert result[0] == 4       

def test_push_no_arg():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.push()}")(result, items)
    assert items == [1,2,3,]
    assert result[0] == 3 

def test_push_two_args():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.push(4,false)}")(result, items)
    assert items == [1,2,3,4,False]
    assert result[0] == 5   

def test_push_list():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.push([4,5])}")(result, items)
    assert items == [1,2,3,[4,5]]
    assert result[0] == 4   

#shift
def test_shift():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.shift()}")(result, items)
    assert items == [2,3]
    assert result[0] == 1    

def test_shift_empty():
    items = []
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.shift()}")(result, items)
    assert items == []
    assert result[0] is None   

#unshift     
def test_unshift_zero_arg():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.unshift()}")(result, items)
    assert items == [1,2,3]
    assert result[0] == 3

def test_unshift_one_arg():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.unshift(6)}")(result, items)
    assert items == [6,1,2,3]
    assert result[0] == 4    

def test_unshift_two_args():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.unshift(6,7)}")(result, items)
    assert items == [6,7,1,2,3]
    assert result[0] == 5      

#concat
def test_concat_primitive():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.concat(4)}")(result, items)
    assert items == [1,2,3]
    assert result[0] == [1,2,3,4]

def test_concat_array():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.concat([4,5])}")(result, items)
    assert items == [1,2,3]
    assert result[0] == [1,2,3,4,5]    

def test_concat_empty_arg():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.concat()}")(result, items)
    assert items == [1,2,3]
    assert result[0] == [1,2,3]  
    assert items is not result[0]

def test_concat_two_arrays():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.concat([7,8], [0,1])}")(result, items)
    assert items == [1,2,3]
    assert result[0] == [1,2,3,7,8,0,1]         

def test_concat_mix():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.concat([7,8], true, [0,1])}")(result, items)
    assert items == [1,2,3]
    assert result[0] == [1,2,3,7,8,True,0,1]    

def test_concat_object_element():
    d = {"a":1}
    items = [1, 2, d]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.concat()}")(result, items)
    assert items == [1, 2, d]
    assert result[0] == [1, 2, d]
    assert items is not result[0]
    assert d is items[2]
    assert d is result[0][2]    

#slice
def test_slice():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.slice(1,2)}")(result, items)
    assert items == [1,2,3]
    assert result[0] == [2]   

def test_slice_copy():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.slice(0,3)}")(result, items)
    assert items == [1,2,3]
    assert result[0] == [1,2,3]
    assert items is not result[0]    

def test_slice_start_zero():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.slice(0,2)}")(result, items)
    assert items == [1,2,3]
    assert result[0] == [1,2]      

def test_slice_stop_length():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.slice(1,3)}")(result, items)
    assert items == [1,2,3]
    assert result[0] == [2,3]     

def test_slice_stop_beyond_length():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.slice(1,4)}")(result, items)
    assert items == [1,2,3]
    assert result[0] == [2,3]   

def test_slice_start_negative():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.slice(-3,-1)}")(result, items)
    assert result[0] == [1,2]      

#indexOf
def test_indexOf():
    items = [1,2,3,1]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.indexOf(1)}")(result, items)
    assert result[0] == 0     

def test_indexOf_with_start():
    items = [1,2,3,4,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.indexOf(3, 3)}")(result, items)
    assert result[0] == 4

def test_indexOf_with_negative_start():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.indexOf(3, -2)}")(result, items)
    assert result[0] == 2 

def test_indexOf_zero_size():
    items = []
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.indexOf(1)}")(result, items)
    assert result[0] == -1    

def test_indexOf_start_beyond_length():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.indexOf(1, 10)}")(result, items)
    assert result[0] == -1    

def test_indexOf_not_found():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.indexOf(10)}")(result, items)
    assert result[0] == -1   

#lastIndexOf
def test_lastIndexOf():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.lastIndexOf(1)}")(result, items)
    assert result[0] == 0    

def test_lastIndexOf_dup():
    items = [1,2,3,1]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.lastIndexOf(1)}")(result, items)
    assert result[0] == 3    

def test_lastIndexOf_with_from_index():
    items = [1,2,3,1]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.lastIndexOf(1, 2)}")(result, items)
    assert result[0] == 0       

def test_lastIndexOf_with_from_index_greater_than_size():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.lastIndexOf(1, 10)}")(result, items)
    assert result[0] == 0    

def test_lastIndexOf_with_negative_from_index():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.lastIndexOf(1, -2)}")(result, items)
    assert result[0] == 0                     

def test_lastIndexOf_not_found():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.lastIndexOf(3, 0)}")(result, items)
    assert result[0] == -1   

#splice
def test_splice_no_args():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.splice()}")(result, items)
    assert items == [1,2,3]
    assert result[0] == []     

def test_splice_one_arg():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.splice(1)}")(result, items)
    assert items == [1]
    assert result[0] == [2,3]      

def test_splice_one_arg_negative():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.splice(-2)}")(result, items)
    assert items == [1]
    assert result[0] == [2,3]    

def test_splice_two_args_negative_count():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.splice(1, -1)}")(result, items)
    assert items == [1,2,3]
    assert result[0] == []  

def test_splice_two_args_zero_count():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.splice(1, 0)}")(result, items)
    assert items == [1,2,3]
    assert result[0] == []       

def test_splice_two_args_one_count():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.splice(1, 1)}")(result, items)
    assert items == [1,3]
    assert result[0] == [2]   

def test_splice_two_args_two_count():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.splice(1, 2)}")(result, items)
    assert items == [1]
    assert result[0] == [2,3]      

def test_splice_three_args_zero_count():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.splice(1,0,5)}")(result, items)
    assert items == [1,5,2,3]
    assert result[0] == []   

def test_splice_three_args_one_count():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.splice(1,1,5)}")(result, items)
    assert items == [1,5,3]
    assert result[0] == [2] 

def test_splice_three_args_two_count():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.splice(1,2,5)}")(result, items)
    assert items == [1,5]
    assert result[0] == [2,3]     

def test_splice_four_args_zero_count():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.splice(1,0,5,6)}")(result, items)
    assert items == [1,5,6,2,3]
    assert result[0] == []   

def test_splice_four_args_one_count():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.splice(1,1,5,6)}")(result, items)
    assert items == [1,5,6,3]
    assert result[0] == [2] 

def test_splice_four_args_two_count():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.splice(1,2,5,6)}")(result, items)
    assert items == [1,5,6]
    assert result[0] == [2,3]                               

#fill
def test_fill_returns_ref_to_self():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.fill(8)}")(result, items)
    assert items == [8,8,8]
    assert items is result[0]

def test_fill_other_type():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.fill(false)}")(result, items)
    assert items == [False,False,False]  

def test_fill_with_start():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.fill(8,1)}")(result, items)
    assert items == [1,8,8] 

def test_fill_with_start_negative():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.fill(8,-2)}")(result, items)
    assert items == [1,8,8]    

def test_fill_with_start_too_high():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.fill(8,7)}")(result, items)
    assert items == [1,2,3]      

def test_fill_with_stop():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.fill(8,1,2)}")(result, items)
    assert items == [1,8,3]    

def test_fill_with_negative_stop():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.fill(8,1,-1)}")(result, items)
    assert items == [1,8,3]    

def test_fill_with_stop_too_high():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.fill(8,1,10)}")(result, items)
    assert items == [1,8,8]  

#copyWithin

def test_copyWithin():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.copyWithin(0,1)}")(result, items)
    assert items == [2,3,3]
    assert result[0] == [2,3,3]
    result[0][0] = 9
    assert items == [9,3,3]    

def test_copyWithin_no_args():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.copyWithin()}")(result, items)
    assert items == [1,2,3]     

def test_copyWithin_target_only_overwrite_all():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.copyWithin(0)}")(result, items)
    assert items == [1,2,3]  

def test_copyWithin_target_only():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.copyWithin(1)}")(result, items)
    assert items == [1,1,2]     

def test_copyWithin_negative_target_only():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.copyWithin(-1)}")(result, items)
    assert items == [1,2,1] 

def test_copyWithin_target_too_large():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.copyWithin(10)}")(result, items)
    assert items == [1,2,3]     

def test_copyWithin_target_and_start():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.copyWithin(1, 2)}")(result, items)
    assert items == [1,3,3]   

def test_copyWithin_target_and_start_too_large():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.copyWithin(1, 2)}")(result, items)
    assert items == [1,3,3]       

def test_copyWithin_target_and_negative_start():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.copyWithin(1, -1)}")(result, items)
    assert items == [1,3,3]   

def test_copyWithin_target_and_start_and_end():
    items = [1,2,3,4,5]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.copyWithin(1,2,3)}")(result, items)
    assert items == [1,3,3,4,5]    

def test_copyWithin_target_and_start_and_negative_end():
    items = [1,2,3,4,5]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.copyWithin(1,2,-2)}")(result, items)
    assert items == [1,3,3,4,5]    

#includes
def test_includes():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.includes(1)}")(result, items)
    assert result[0] == True   

def test_includes_other_type():
    items = [1,2,'Hi']
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.includes('Hi')}")(result, items)
    assert result[0] == True         

def test_includes_not():
    items = [1,2,3]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.includes(5)}")(result, items)
    assert result[0] == False   

def test_includes_not_other_type():
    items = [1,2,'Hi']
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.includes('Joe')}")(result, items)
    assert result[0] == False   

def test_includes_too_few_args():
    items = [4,2,6,7]
    try:
        pm.eval("(arr) => {arr.includes()}")(items)      
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'pythonmonkey.SpiderMonkeyError'>"
        assert str(e).__contains__("TypeError: includes: At least 1 argument required, but only 0 passed")   

#sort
def test_sort_empty():
    items = []
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.sort()}")(result, items)
    assert result[0] == items
    assert items == []

def test_sort_numbers():
    items = [4,2,6,7]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.sort()}")(result, items)
    assert result[0] == items
    assert items == [2,4,6,7]

def test_sort_strings():
    items = ['Four', 'Three', 'One']   
    pm.eval("(arr) => {arr.sort()}")(items)
    assert items == ['Four', 'One', 'Three']    

def test_sort_with_two_args_keyfunc():
    items = [4,2,6,7]
    def myFunc(e,f):
        return len(e) - len(f)  
    try:
        pm.eval("(arr, compareFun) => {arr.sort(compareFun)}")(items, myFunc)      
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'TypeError'>"
        assert str(e).__contains__("myFunc() missing 1 required positional argument: 'f'")   

def test_sort_with_one_arg_keyfunc():
    items = ['Four', 'Three', 'One']   
    def myFunc(e):
        return len(e)  
    pm.eval("(arr, compareFun) => {arr.sort(compareFun)}")(items, myFunc)
    assert items == ['One', 'Four', 'Three']

def test_sort_with_builtin_keyfunc():
    items = ['Four', 'Three', 'One']   
    pm.eval("(arr, compareFun) => {arr.sort(compareFun)}")(items, len)
    assert items == ['One', 'Four', 'Three']

def test_sort_with_builtin_keyfunc_wrong_data_type():
    items = [4,2,6,7]  
    try:
        pm.eval("(arr, compareFun) => {arr.sort(compareFun)}")(items, len)      
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'TypeError'>"
        assert str(e).__contains__("object of type 'int' has no len()")   

def test_sort_with_js_func():
    items = ['Four', 'Three', 'One']  
    result = [None]
    myFunc = pm.eval("((a, b) => a.toLocaleUpperCase() < b.toLocaleUpperCase() ? -1 : 1)")
    pm.eval("(result, arr, compareFun) => {result[0] = arr.sort(compareFun)}")(result, items, myFunc)
    assert result[0] == items
    assert items == ['Four', 'One', 'Three'] 

#def test_sort_numbers_tricky():
#    items = [1, 30, 4, 21, 100000]
#    result = [None]
#    pm.eval("(result, arr) => {result[0] = arr.sort()}")(result, items)
#    assert result[0] is items
#    assert items == [1, 100000, 21, 30, 4]    

def test_sort_with_js_func_wrong_data_type():
    items = [4,2,6,7]
    myFunc = pm.eval("((a, b) => a.toLocaleUpperCase() < b.toLocaleUpperCase() ? -1 : 1)")
    try:
        pm.eval("(arr, compareFun) => {arr.sort(compareFun)}")(items, myFunc)      
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'pythonmonkey.SpiderMonkeyError'>"
        assert str(e).__contains__("TypeError: a.toLocaleUpperCase is not a function")   

#forEach
def test_forEach():
    items = ['Four', 'Three', 'One'] 
    result = ['']
    returnResult = [0]
    pm.eval("(returnResult, result, arr) => {returnResult[0] = arr.forEach((element) => result[0] += element)}")(returnResult, result, items)
    assert items == ['Four', 'Three', 'One']   
    assert result == ['FourThreeOne'] 
    assert returnResult == [None] 

def test_forEach_check_index():
    items = ['Four', 'Three', 'One'] 
    result = ['']
    pm.eval("(result, arr) => {arr.forEach((element, index) => result[0] += index)}")(result, items) 
    assert result == ['012']    

def test_forEach_check_array():
    items = ['Four', 'Three', 'One'] 
    result = ['']
    pm.eval("(result, arr) => {arr.forEach((element, index, array) => result[0] = array)}")(result, items)
    assert result == [items]        

def test_forEach_check_this_arg():
    items = ['Four', 'Three', 'One'] 
    result = [None]
    pm.eval("(result, arr) => {class Counter { constructor() { this.count = 0;} add(array) { array.forEach(function countEntry(entry) { ++this.count; }, this);}} const obj = new Counter(); obj.add(arr); result[0] = obj.count;}")(result, items)  
    assert result == [3]  

def test_forEach_check_this_arg_wrong_type():
    items = ['Four', 'Three', 'One'] 
    result = [None]
    a = 9
    try:
        pm.eval("(result, arr, a) => {class Counter { constructor() { this.count = 0;} add(array) { array.forEach(function countEntry(entry) { ++this.count; }, a);}} const obj = new Counter(); obj.add(arr); result[0] = obj.count;}")(result, items, a)       
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'pythonmonkey.SpiderMonkeyError'>"
        assert str(e).__contains__("TypeError: 'this' argument is not an object or null")         

# TODO should not pass
def test_forEach_check_this_arg_null():
    items = ['Four', 'Three', 'One'] 
    result = [None]
    try:
        pm.eval("(result, arr) => {class Counter { constructor() { this.count = 0;} add(array) { array.forEach(function countEntry(entry) { ++this.count; }, null);}} const obj = new Counter(); obj.add(arr); result[0] = obj.count;}")(result, items)       
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'pythonmonkey.SpiderMonkeyError'>"
        assert str(e).__contains__("TypeError: this is null")              

def test_forEach_too_few_args():
    items = [4,2,6,7]
    try:
        pm.eval("(arr) => {arr.forEach()}")(items)      
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'pythonmonkey.SpiderMonkeyError'>"
        assert str(e).__contains__("TypeError: forEach: At least 1 argument required, but only 0 passed")          

#map   
def test_map():
    items = [4,2,6,7]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.map((x) => x * x)}")(result, items)
    assert items == [4,2,6,7]
    assert result[0] == [16,4,36,49]

def test_map_too_few_args():
    items = [4,2,6,7]
    try:
        pm.eval("(arr) => {arr.map()}")(items)      
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'pythonmonkey.SpiderMonkeyError'>"
        assert str(e).__contains__("TypeError: map: At least 1 argument required, but only 0 passed")     

def test_map_arg_wrong_type():
    items = [4,2,6,7]
    try:
        pm.eval("(arr) => {arr.map(8)}")(items)      
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'pythonmonkey.SpiderMonkeyError'>"
        assert str(e).__contains__("TypeError: map: callback is not a function")            

def test_map_check_index():
    items = ['Four', 'Three', 'One'] 
    result = ['']
    pm.eval("(result, arr) => {arr.map((element, index) => result[0] += index)}")(result, items) 
    assert result == ['012']    

def test_map_check_array_mutation():
    items = ['Four', 'Three', 'One'] 
    result = ['']
    pm.eval("(result, arr) => {arr.map((element, index, array) => {array[0] = 'Ten'; result[0] = array})}")(result, items)
    assert result[0] == ['Ten', 'Three', 'One']
    assert items == ['Ten', 'Three', 'One']
    
#filter
def test_filter():
    words = ['spray', 'elite', 'exuberant', 'destruction', 'present']
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.filter((word) => word.length > 6)}")(result, words)
    assert words == ['spray', 'elite', 'exuberant', 'destruction', 'present']
    assert result[0] == ['exuberant', 'destruction', 'present']

def test_filter_too_few_args():
    items = [4,2,6,7]
    try:
        pm.eval("(arr) => {arr.filter()}")(items)      
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'pythonmonkey.SpiderMonkeyError'>"
        assert str(e).__contains__("TypeError: filter: At least 1 argument required, but only 0 passed")         

#reduce  index, array param, wrong arg type, too few args same impl as previous few for all below
def test_reduce():
    items = [1,2,3,4,5]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reduce((accumulator, currentValue) => accumulator + currentValue, 0)}")(result, items)
    assert items == [1,2,3,4,5]
    assert result[0] == 15

def test_reduce_empty_array_no_accumulator():
    items = []
    try:
        pm.eval("(arr) => {arr.reduce((accumulator, currentValue) => accumulator + currentValue)}")(items)    
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'pythonmonkey.SpiderMonkeyError'>"
        assert str(e).__contains__("TypeError: reduce of empty array with no initial value")          

def test_reduce_float():
    items = [1.9, 4.6, 9.3, 16.5]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reduce((accumulator, currentValue) => accumulator + currentValue, 0)}")(result, items)
    assert result[0] == 32.3    

def test_reduce_string():
    items = ['Hi', 'There']
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reduce((accumulator, currentValue) => accumulator + currentValue, "")}")(result, items)
    assert result[0] == 'HiThere'    

def test_reduce_initial_value_not_zero():
    items = [1,2,3,4,5]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reduce((accumulator, currentValue) => accumulator + currentValue, 5)}")(result, items)
    assert items == [1,2,3,4,5]
    assert result[0] == 20  

def test_reduce_no_initial_value():
    items = [1,2,3,4,5]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reduce((accumulator, currentValue) => accumulator + currentValue)}")(result, items)
    assert items == [1,2,3,4,5]
    assert result[0] == 15  

def test_reduce_length_one_with_initial_value():
    items = [1]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reduce((accumulator, currentValue) => accumulator + currentValue, 2)}")(result, items)
    assert result[0] == 3       

def test_reduce_length_one_no_initial_value():
    items = [1]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reduce((accumulator, currentValue) => accumulator + currentValue)}")(result, items)
    assert result[0] == 1      

def test_reduce_list_meaningless():
    items = [['Hi', 'There']]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reduce((x) => x * 2)}")(result, items)
    assert result[0] == ['Hi', 'There']  

#reduceRight
def test_reduceRight_list_concat():
    items = [[0, 1],[2, 3],[4, 5]]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reduceRight((accumulator, currentValue) => accumulator.concat(currentValue))}")(result, items)
    assert result[0] == [4, 5, 2, 3, 0, 1]

def test_reduceRight_list_concat_with_initial_value():
    items = [[0, 1],[2, 3],[4, 5]]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reduceRight((accumulator, currentValue) => accumulator.concat(currentValue), [7,8])}")(result, items)
    assert result[0] == [7, 8, 4, 5, 2, 3, 0, 1]

def test_reduceRight():
    items = [0,1,2,3,4]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reduceRight((accumulator, currentValue, index, array) => accumulator + currentValue)}")(result, items)
    assert result[0] == 10  

def test_reduceRight_with_initial_value():
    items = [0,1,2,3,4]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reduceRight((accumulator, currentValue, index, array) => accumulator + currentValue, 5)}")(result, items)
    assert result[0] == 15        

def test_reduceRight_float():
    items = [1.9, 4.6, 9.3, 16.5]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.reduceRight((accumulator, currentValue, index, array) => accumulator + currentValue)}")(result, items)
    assert result[0] == 32.3    

#some
def test_some_true():
    items = [1, 2, 3, 4, 5]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.some((element) => element % 2 === 0)}")(result, items)
    assert items == [1, 2, 3, 4, 5]
    assert result[0] == True    

def test_some_false():
    items = [1,3,5]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.some((element) => element % 2 === 0)}")(result, items)
    assert result[0] == False    

def test_some_truthy_conversion():
    result = [None]
    pm.eval('(result) => {const TRUTHY_VALUES = [true, "true", 1];  function getBoolean(value) { if (typeof value === "string") { value = value.toLowerCase().trim(); } return TRUTHY_VALUES.some((t) => t === value);} result[0] = getBoolean(1);}')(result)
    assert result[0] == True   

#every        
def test_every_true():
    items = [2,4,6]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.every((element) => element % 2 === 0)}")(result, items)
    assert items == [2,4,6]
    assert result[0] == True    

def test_every_false():
    items = [1,2,4,6]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.every((element) => element % 2 === 0)}")(result, items)
    assert result[0] == False    

#find
def test_find_found_once():
    items = [5, 12, 8, 130, 44]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.find((element) => element > 100)}")(result, items)
    assert items == [5, 12, 8, 130, 44]
    assert result[0] == 130  

def test_find_found_twice():
    items = [5, 12, 8, 130, 4]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.find((element) => element > 10)}")(result, items)
    assert result[0] == 12   

def test_find_not_found():
    items = [5, 12, 8, 130, 44]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.find((element) => element > 1000)}")(result, items)
    assert result[0] == None  

#findIndex
def test_findIndex_found_once():
    items = [5, 12, 8, 130, 44]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.findIndex((element) => element > 100)}")(result, items)
    assert items == [5, 12, 8, 130, 44]
    assert result[0] == 3  

def test_findIndex_found_twice():
    items = [5, 12, 8, 130, 4]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.findIndex((element) => element > 10)}")(result, items)
    assert result[0] == 1    

def test_findIndex_not_found():
    items = [5, 12, 8, 130, 4]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.findIndex((element) => element > 1000)}")(result, items)
    assert result[0] == -1        

#flat
def test_flat():
    items = [0, 1, 2, [3, 4]]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.flat()}")(result, items)
    assert items == [0, 1, 2, [3, 4]]
    assert result[0] == [0, 1, 2, 3, 4]

def test_flat_with_js_array():
    items = [0, 1, 2, [3, 4]]
    result = [0]
    pm.eval("(result, arr) => {arr[1] = [10,11]; result[0] = arr.flat()}")(result, items)
    assert items == [0, [10, 11], 2, [3, 4]]
    assert result[0] == [0, 10, 11, 2, 3, 4]

def test_flat_depth_zero():
    items = [0, 1, [2, [3, [4, 5]]]]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.flat(0)}")(result, items)
    assert result[0] == [0, 1, [2, [3, [4, 5]]]]

def test_flat_depth_one():
    items = [0, 1, [2, [3, [4, 5]]]]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.flat(1)}")(result, items)
    assert items == [0, 1, [2, [3, [4, 5]]]]
    assert result[0] == [0, 1, 2, [3, [4, 5]]]    

def test_flat_depth_two():
    items = [0, 1, [2, [3, [4, 5]]]]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.flat(2)}")(result, items)
    assert items == [0, 1, [2, [3, [4, 5]]]]
    assert result[0] == [0, 1, 2, 3, [4, 5]]    

def test_flat_depth_large():
    items = [0, 1, [2, [3, [4, 5]]]]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.flat(10)}")(result, items)
    assert result[0] == [0, 1, 2, 3, 4, 5]      

#flatMap
def test_flatMap():
    items = [1, 2, 1]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.flatMap((num) => (num === 2 ? [2, 2] : 1))}")(result, items)
    assert items == [1,2,1]
    assert result[0] == [1,2,2,1]

def test_flatMap_with_js_array():
    items = [1,2,2,1]
    result = [0]
    pm.eval("(result, arr) => {arr[1] = [10,11]; result[0] = arr.flatMap((num) => (num === 2 ? [2, 2] : 1))}")(result, items)
    assert items == [1, [10, 11], 2, 1]
    assert result[0] == [1, 1, 2, 2, 1]  

def test_flatMap_no_replace():
    items = [1,2,[4,5]]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.flatMap((num) => (num === 2 ? [2, 2] : 1))}")(result, items)
    assert items == [1, 2, [4, 5]]
    assert result[0] == [1, 2, 2, 1]    

def test_flatMap_no_replace_depth_one():
    items = [1,2,[4,5]]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.flatMap((num) => (num === 2 ? [2, [2, 2]] : 1))}")(result, items)
    assert items == [1, 2, [4, 5]]
    assert result[0] == [1, 2, [2, 2], 1]       
 
def test_flatMap_equivalence():
    items = [1, 2, 1]
    result = [0]
    result2 = [0]
    pm.eval("(result, arr) => {result[0] = arr.flatMap((num) => (num === 2 ? [2, 2] : 1))}")(result, items)
    pm.eval("(result, arr) => {result[0] = arr.map((num) => (num === 2 ? [2, 2] : 1)).flat()}")(result2, items)
    assert result[0] == result2[0]   

#valueOf
def test_valueOf():
    items = [1, 2, 1]
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.valueOf()}")(result, items)
    assert result[0] == [1,2,1] 
    result[0][1] = 5
    assert result[0] == [1,5,1]
    assert items == [1,5,1]

#toLocaleString
def test_toLocaleString():
    prices = ["￥7", 500, 8123, 12]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.toLocaleString('ja-JP', { style: 'currency', currency: 'JPY' })}")(result, prices)
    assert result[0] == '￥7,￥500,￥8,123,￥12'   

def test_toLocaleString_no_args():
    prices = ["￥7", 500, 8123, 12]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.toLocaleString()}")(result, prices)
    assert result[0] == '￥7,500,8,123,12'     

def test_toLocaleString_one_arg_():
    prices = ["￥7", 500, 8123, 12]
    result = [None]
    pm.eval("(result, arr) => {result[0] = arr.toLocaleString('ja-JP')}")(result, prices)
    assert result[0] == '￥7,500,8,123,12'     

def test_toLocaleString_one_arg_invalid_locale():
    prices = ["￥7", 500, 8123, 12]
    result = [None]
    try:
        pm.eval("(result, arr) => {result[0] = arr.toLocaleString('asfasfsafsdf')}")(result, prices)   
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'pythonmonkey.SpiderMonkeyError'>"
        assert str(e).__contains__("RangeError: invalid language tag:")       

def test_toLocaleString_two_args_invalid_currency():
    prices = ["￥7", 500, 8123, 12]
    result = [None]
    try:
        pm.eval("(result, arr) => {result[0] = arr.toLocaleString('ja-JP', { style: 'currency', currency: 'JPYsdagasfgas' })}")(result, prices)    
        assert (False)
    except Exception as e:    
        assert str(type(e)) == "<class 'pythonmonkey.SpiderMonkeyError'>"
        assert str(e).__contains__("RangeError: invalid currency code in NumberFormat():")       

#entries
def test_entries_next():
    items = ['a', 'b', 'c']
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.entries(); result[0] = result[0].next().value}")(result, items)
    assert items == ['a', 'b', 'c']
    assert result[0] == [0, 'a']      

def test_entries_next_next():
    items = ['a', 'b', 'c']
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.entries(); result[0].next(); result[0] = result[0].next().value}")(result, items)
    assert result[0] == [1, 'b']    

def test_entries_next_next_undefined():
    items = ['a']
    result = [0]
    pm.eval("(result, arr) => {result[0] = arr.entries(); result[0].next(); result[0] = result[0].next().value}")(result, items)
    assert result[0] == None    

#keys
def test_keys_iterator():
    items = ['a', 'b', 'c']
    result = [7,8,9]
    pm.eval("(result, arr) => { index = 0; iterator = arr.keys(); for (const key of iterator) { result[index] = key; index++;} }")(result, items)
    assert result == [0,1,2]    

#values
def test_values_iterator():
    items = ['a', 'b', 'c']
    result = [7,8,9]
    pm.eval("(result, arr) => { index = 0; iterator = arr.values(); for (const key of iterator) { result[index] = key; index++;} }")(result, items)
    items[0] = 'd'
    assert result == ['a', 'b', 'c']

#constructor property
def test_constructor_creates_array():
    items = [1,2]
    result = [0]
    pm.eval("(result, arr) => { result[0] = arr.constructor; result[0] = new result[0]; result[0][0] = 9}")(result, items)
    assert result[0] == [9]     

#length property
def test_constructor_creates_array():
    items = [1,2]
    result = [0]
    pm.eval("(result, arr) => { result[0] = arr.length}")(result, items)
    assert result[0] == 2      

#iterator symbol property
def test_iterator_type_function():
    items = [1,2]
    result = [0]
    pm.eval("(result, arr) => { result[0] = typeof arr[Symbol.iterator]}")(result, items)
    assert result[0] == 'function'         

def test_iterator_first_next():
    items = [1,2]
    result = [0]
    pm.eval("(result, arr) => { result[0] = arr[Symbol.iterator]().next()}")(result, items)
    assert result[0].value == 1    
    assert result[0].done == False     

def test_iterator_second_next():
    items = [1,2]
    result = [0]
    pm.eval("(result, arr) => { let iterator = arr[Symbol.iterator](); iterator.next(); result[0] = iterator.next()}")(result, items)
    assert result[0].value == 2    
    assert result[0].done == False 

def test_iterator_last_next():
    items = [1,2]
    result = [0]
    pm.eval("(result, arr) => { let iterator = arr[Symbol.iterator](); iterator.next(); iterator.next(); result[0] = iterator.next()}")(result, items)
    assert result[0].value == None
    assert result[0].done == True                    