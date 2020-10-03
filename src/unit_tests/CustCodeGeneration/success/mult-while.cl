class Main inherits IO {
    x : Int;

    main() : Object {
        let y:Int, z:Int <- new Int in {
            while x < 5 loop {
                y <- 0;
                while y < 5 loop {
                    z <- 0;
                    while z < 5 loop {
                        out_int(x);
                        out_int(y);
                        out_int(z);
                        z <- z + 1;
                    } pool;
                    y <- y + 1;
                } pool;
                x <- x + 1;
            } pool;

            x <- 0;
            while x < 5 loop {
                y <- x + 1;
                while y < 5 loop {
                    z <- y + 1;
                    while z < 5 loop {
                        out_int(x);
                        out_int(y);
                        out_int(z);
                        z <- z + 1;
                    } pool;
                y <- y + 1;
                } pool;
            x <- x + 1;
            } pool;
        }
    };
};