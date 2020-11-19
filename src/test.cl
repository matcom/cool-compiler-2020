class A {
    i : Int;

     geti() : Int {
	i
};
};

class Main inherits IO {
    main() : IO {
	let x : A <- new A in out_int(x.geti())
    };
};
