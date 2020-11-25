class Main inherits IO {
    x : Int;

    main() : Object {
        while x < 30 loop {
            out_int(x);
            x <- x + 1;
        } pool
    };
};