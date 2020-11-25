class Main inherits IO {
    a : Bool;
    b : Bool <- new Bool;
    c : Bool <- true;
    d : Int <- 7;
    e : Int <- 20;

    main() : Bool {{
        1 < 2;
        2 <= 2;
        3 < 2;
        3 <= 2;
        d < e;
        d = e;
    }};
};