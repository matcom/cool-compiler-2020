(* A class is a list of features *)

CLaSS Main {
    main(): Object {
        (new Alpha).print()
    };
};

CLaSS Test {
    testing(): Int {
        2 + 2
    };
};

-- Type names must begin with uppercase letters
CLaSS Alpha iNHeRiTS iO {
    print() : Object {
        out_string("reached!!\n")
    };
};
