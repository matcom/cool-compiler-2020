class Main { main() : Int {1}; };

class A {
    obj : A <- fun(new A);
    
    fun(obj : A) : SELF_TYPE { obj };
};