(* A class is a list of features *)

CLaSS Main {
    main(): Object {
        (new Alpha).print()
    };
};

-- Missing '}'
CLaSS Test {
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
;

CLaSS Alpha iNHeRiTS IO {
    print() : Object {
        out_string("reached!!\n")
    };
};
