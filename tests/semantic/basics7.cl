-- It is an error to inherit from or redefine Bool.

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
}; 
 
class Bool {
	xor(b: Bool): Bool { false };
};