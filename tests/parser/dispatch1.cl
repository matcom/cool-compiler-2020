(* There are three forms of dispatch (i.e. method call) in Cool. The three forms differ only in how the called method is selected *)

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

    testing4(x: Int, y: Int): Test {
        self
    };
};

class Test2 {
    test1: Test <- new Test;

    testing1(): Test {
        Test1.testing4(1, 2).testing4(3, 4).testing4(5, 6) -- Objet identifiers begin with a lower case letter
    };
}

class Alpha inherits IO {
    print() : Object {
        out_string("reached!!\n")
    };
};