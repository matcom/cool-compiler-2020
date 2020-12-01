(* A class is a list of features *)

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

-- Class names must begin with uppercase letters
class alpha inherits IO {
    print() : Object {
        out_string("reached!!\n")
    };
};
