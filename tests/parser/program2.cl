(* Cool programs are sets of classes *)

class Main {
    main(): Object {
        (new Alpha).print()
    };
};

-- Missing semicolon
class Test {
    testing(): Int {
        2 + 2
    };
}

class Alpha inherits IO {
    print() : Object {
        out_string("reached!!\n")
    };
};
