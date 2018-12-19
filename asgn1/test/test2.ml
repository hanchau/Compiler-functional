let main = 
	let int a = 959 in
	foo a;;
	
(*Function as asked in Assignment*)

(*functions with no arguments*)	
let main_int_array =
	let int a = [|2, 3, 5, 7, 10|] in
	let int b = a.(4)++ in
	print_int(b--);;
	
let main_float_array =
	let float a = [|2.3, 3.5, 5.6, 7.5, 10.45|] in
	let float b = a.(5) in
	print_float(b);;
	
let main_char_string =
	let char a = 'A' in
	let string b = "First String in Lexer" in
	print_char(a);
	print_string(b);;	
	
let main_bool =
	let bool a = true in
	let bool b = false in 
	print_string(a);
	print_strint(b);; 

(*function with one argument used in test5.ml *)	
let module_func_call int c =
	let int a = [|2, 3, 5, 7, 10|] in
	let int b = a.(4)++ in
	b + c;; (*This is the return value of Function*)

(*Functions*)
