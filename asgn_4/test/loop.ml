let Main =
begin
  let int i = 0 in
  let int j = 0 in
  let int k = 0 in
  let int res = 0 in
  for i = 0 to 10
  do
    for j = 0 to 10
    do
      for k = 0 to 10
      do begin res = res + 1; end
      done
    done
  done
  print_int(res) ;
end
;;
