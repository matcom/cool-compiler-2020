(* A method of class A is a procedure that may manipulate the variables and objects of class A *)

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

    -- Missing paremeter
    testing3(x: Int,): String {
        "2 + 2"
    };
};

class Alpha inherits IO {
    print() : Object {
        out_string("reached!!\n")
    };
};