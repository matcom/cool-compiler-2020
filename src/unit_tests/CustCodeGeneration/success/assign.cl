class Main inherits IO {
    main() : SELF_TYPE {
        let x:Int, y:Int, z:Int in {
            x <- y <- z <- 5;
            out_int(x);
            out_int(y);
            out_int(z);
        }
    };
};