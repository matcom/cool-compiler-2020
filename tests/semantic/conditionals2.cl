(*
Let T and F be the static types of the branches of the conditional. Then the static type of the
conditional is T t F. (think: Walk towards Object from each of T and F until the paths meet.)
*)

class A { };
class B inherits A { };
class C inherits B { };
class D inherits B { };
class E inherits B { }; 
class F inherits A { }; 

class Main inherits IO {
	main(): IO { out_string("Hello World!")};

	b: B <- if true then 
				new C 
			else 
				if false then new D 
				else new E fi
			fi;

	test: B <- if not true then new F else new E fi;
}; 
