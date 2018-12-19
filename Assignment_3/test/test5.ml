open test1 test2
open test3 test4

let function_test5 =
	begin
	let int a = 10 int b = 20 in
	let int d <- (module_func_call a) in
	let int e <- (function_test3 a b) in
	print_int(d + e);
	end
return 0
;;
