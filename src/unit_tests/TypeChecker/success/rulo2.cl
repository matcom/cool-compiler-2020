class Main { main() : Int {1}; };

class B {
    y : SELF_TYPE;
    
    foo() : SELF_TYPE {{
        y <- (new SELF_TYPE).copy();
        y;
    }};
};