(*
For, While, If-then-else
*)
(*
open test2 is in comments so we are using test2.(<function arg1 ..>) 
for calling function from different module
*)
let Function_test3 int n1 int n2=
	let int result = 1 in
	for i = 1 to n1 do (result <- n1*result) done;
	if n2 > 50 and n2<100 then
		begin
		for int i = 0 to n2 do result <- result + (test2.(module_func_call 54)); (* Checking loops and if statements *)
	  	end
	else
		begin 
		if n2 > 100 then
			begin
			while result <= 1000 do (result <- result + n1); result++; done 
			end
		else
			begin
			for int i = 120 downto 1 do (result <- result + n1);	done 
			end
	print_int(result);;



