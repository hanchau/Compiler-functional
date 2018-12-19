
let Main =
begin
    let int num = 50 in
    let int sum = 0 in
    let int r = 0 in

    while num != 0 do
    begin
        r = num mod 10;
        num = num / 10;
        sum = sum + r;
    end
    done

    for r = 1 to 100 do
    begin
        sum = sum - sum/100;
    end
    done

    print_int(sum);
    return 0;
end
;;
