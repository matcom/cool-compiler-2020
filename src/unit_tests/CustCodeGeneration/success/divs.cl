(*
    Program that given n find its divisors in lineal time.
*)

class Main inherits IO {
    n : Int;

    main() : Int {
        {
            out_string("Enter number n\n");
            n <- 321;

            out_string("You entered: ");
            out_int(n);
            out_string("\n");

            let d : Int <- 1 in {
                while d <= n loop {
                    if n - (n / d) * d = 0 then {
                        out_int(d);
                        out_string("\n");
                    }

                    else 1
                    fi;

                    d <- d + 1;
                } pool;
            };

            1;
        }
    };
};