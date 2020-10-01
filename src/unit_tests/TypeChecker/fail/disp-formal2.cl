class Main { main() : Int {1}; };

class A {
    obj : A <- fun(new A);
    
    fun(obj : SELF_TYPE) : SELF_TYPE { obj };
};