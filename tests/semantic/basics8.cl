-- It is an error redefine Object.

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
}; 
 
class Object {
	xor(b: Bool): Bool { false };
};