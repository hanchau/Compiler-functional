(*Nested Begin End with mod*)


let Function_test4 int a int b =
	if a >= 100 and b <= 100 
	then 
		begin
			a <- a + b;
			b <- b--;
			begin
				let int c = 1500 in
				c <- a * b;
				if (c mod 4 <= 0 ) then c <- c + b; else c <- c + a;
			end
			print_int(a);
			print_int(b);
			print_int(c);
		end
	else
		begin
			let int c = 1000 in
			print_int(a);
			print_int(b);
			print_int(c);
		end
	;;
