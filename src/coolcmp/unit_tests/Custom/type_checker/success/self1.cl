class Main {
    main() : Int { 1 };
};

class C inherits Main {
    obj : Main <- new SELF_TYPE;
};
