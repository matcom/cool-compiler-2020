class Main inherits PP {
   main(): SELF_TYPE {
	out_string("Hello, World.\n")
   };
};

class PP inherits Main{
    main(): String {
        out_string("Hello, World.\n")
    };
};