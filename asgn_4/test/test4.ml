open test2
let int a in
let int b in
let Function_test4A =
begin
a = 0;
b = 50;
	for r = 1 to 100 do
	begin
	if a > 100 and b < 100
	then
		begin
			a = a + b;
			b = --b;
			print_int(a);
			print_int(b);
		end
	else
		begin
			let int c = 1000 in
			print_int(a);
			print_int(b);
			print_int(c);
		end
	end
	done
	return a;
end
;;
