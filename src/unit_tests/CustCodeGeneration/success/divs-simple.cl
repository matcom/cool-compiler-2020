(*
    Program that given n find its divisors in lineal time.
*)

class Main inherits IO {
    n : Int;
    d : Int <- 1;

    main() : Object {{
        n <- 100;

        while d <= n loop {
            if n - (n / d) * d = 0 then
                out_int(d)
            else 1 fi;

            d <- d + 1;
        } pool;
    }};
};