let int CONST1 = 440 in
let int CONST2 = 44 in

let EXP =
begin
	let int a in
	for a = 6 to 10000
	do
		begin
				a = a + CONST2;
				CONST2  = CONST2 + CONST1;
				a = a * 2 + CONST2;
		end
	done
end
;;
