class Main inherits IO {
    main() : Int {
        {
            let x : Int <- 1, y : Int <- x + 1 in new SELF_TYPE;
            out_string(x);
            1;
        }
    };
};