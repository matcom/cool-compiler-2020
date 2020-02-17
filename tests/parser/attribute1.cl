(* An attribute of class A specifies a variable that is part of the state of objects of class A *)

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

    -- Attributes names must begin with lowercase letters
    Test2: Int <- 1;

    test3: String <- "1";

    testing2(a: Alpha, b: Int): Int {
        2 + 2
    };

    testing3(): String {
        "2 + 2"
    };
};

class Alpha inherits IO {
    print() : Object {
        out_string("reached!!\n")
    };
};