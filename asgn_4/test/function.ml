
let foo =
begin
  let int i = 1 in
	print_int(i);
end
;;

let main =
begin
  foo();
  return 0;
end
;;
