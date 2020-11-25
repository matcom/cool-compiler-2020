class A {
    f() : Object {
        {
            -- valid
            while 1=1 loop 1 pool;
            while 1=1 loop while 2=2 loop 2 pool pool;
        }
    };
};

class Main {
	main() : Int {
		1
	};
};