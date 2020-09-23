class Main {

    main(): Object {
        (new Alpha).print()
    };
};

class Test {
    test1: Int;
    test2: Int <- test3;
    
    testing1(): Int {
        2 - 2
    };


    test3: String <- "1";

    testing2(a: Alpha, b: Int): Int {
        let count: Int, pow: Int <- 1 -- Initialization must be an expression
        in {
            count <- 0;
        }
    };

    testing3(): Int {
        testing2(new Alpha, 2)
    };

    testing4(): Int {
        test1 <- ~(1 + 2 + 3 + 4 + 5) -- The left side must be an expression
    };
};

class Alpha inherits IO {
    x : Int <- 0;
    print() : Object {
        out_string("reached!!\n")
    };
};