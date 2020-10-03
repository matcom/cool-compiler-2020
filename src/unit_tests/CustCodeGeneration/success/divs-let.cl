(*
    Program that given n find its divisors in lineal time.
*)

class Main inherits IO {
    n : Int;

    main() : Int {
        {
            n <- 232;

            let d : Int <- 1 in {
                while d <= n loop {
                    if n - (n / d) * d = 0 then {
                        out_int(d);
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