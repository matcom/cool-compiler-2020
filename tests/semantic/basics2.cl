-- It is an error to inherit from or redefine Int.

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
}; 
 
class A inherits Int {
	is_prime(): Bool { false };
};
