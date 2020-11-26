-- It is an error to inherit from or redefine String.

class Main inherits IO {
	main(): IO { out_string("Hello World!")};
}; 
 
class String {
	is_palindrome(): Bool { false };
};