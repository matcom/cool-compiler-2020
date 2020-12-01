(* Cool programs are sets of classes *)

class Main {
    main(): Object {
        (new Alpha).print()
    };
};

class Test {
    testing(): Int {
        2 + 2
    };
};

-- Only classes
suma(a: Int, b: Int) int {
    a + b
};

class Alpha inherits IO {
    print() : Object {
        out_string("reached!!\n")
    };
};
