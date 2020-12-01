(* An assignment has the form <id> <- <expr> *)

class Main {
    main(): Object {
        (new Alpha).print()
    };
};

class Test {
    test1: Object;
    
    testing1(): Int {
        2 + 2
    };

    test2: Int <- 1;

    test3: String <- "1";

    testing2(a: Alpha, b: Int): Int {
        2 + 2
    };

    testing3(): String {
        "2 + 2"
    };

    testing4(): String {
        Test1 <- "Hello World" -- Identifiers begin with a lower case letter
    };
};

class Alpha inherits IO {
    print() : Object {
        out_string("reached!!\n")
    };
};