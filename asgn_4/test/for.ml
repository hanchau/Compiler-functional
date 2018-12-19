let Main =
begin
  let int i = 6 in
  for i = 6 to 8
  do
      if i > 0 and i != 7
      then begin
        print_int(i-100) ; end
      else begin
        print_int(i+100) ; end
  done
end
;;
