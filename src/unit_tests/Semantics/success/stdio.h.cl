class Stdio inherits IO {

    scanfInt() : Int {
        in_int()
    };

    scanfString() : String {
        in_string()
    };

    printInt(n : Int) : IO {
        out_int(n)
    };

    printString(s : String) : IO {
        out_string(s)
    };
};

class Main inherits Stdio {

    a: Int <- 1;
    b: Int <- 2;
    s : String <- "hola";

    main(): IO {
        {
            a <- scanfInt();
            s <- scanfString();
            
            printInt(a);
            printString(s);
            
            printInt(1+1*5);
            printString("Hello World\n");
        }
    };
};