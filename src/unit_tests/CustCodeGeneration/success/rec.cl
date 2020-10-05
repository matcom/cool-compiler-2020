class Math {
    factorial(n : Int) : Int {
        if n = 0 then
            1
        else n * factorial(n - 1) fi
    };

    fib(n : Int) : Int {
        if n <= 2 then
            1
        else fib(n - 1) + fib(n - 2) fi
    };
};

class Main inherits IO {
    math : Math <- new Math;

    main() : SELF_TYPE {{
        out_int(math.factorial(12));
        out_int(math.fib(10));
    }};
};