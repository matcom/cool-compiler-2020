
class A {

message() : String{
	"A\n"
};

};


class B inherits A {

message() : String{
	"B\n"
};

};


class Main inherits IO {

	main() : IO {
	out_string((new B).message())
};

};



