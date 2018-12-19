
let Main int r =
begin
    let int num = 50 int sum = 0 in
    print_str("Enter a Number : ") ;

    while num != 0 do
    begin
        r <- num mod 10;
        num = num / 10;
        sum = sum + r;
    end
    done

    for r = 1 upto 100 do
    begin
        sum = sum - sum/100;
    end
    done

    print_str("Sum of Digits of the Number :");
    print_int(sum);
end
return 0;
;;
