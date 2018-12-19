open test2 test3 test4

let function_test5 = 
	let int a = 10 int b = 20 in
		let int d <- (module_func_call a) and int e <- (function_test3 a b) in 
			print_int(d + e);
		function_test4 a b;;
	
