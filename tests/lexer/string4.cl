class Main {
    str <- "The big brown fox
            jumped over the fence";
	main() : Object {
        {
            out_string("Yay! This is the newest shites );
        }
    };
};

(*
#1 CLASS
#1 TYPEID Main
#1 '{'
#2 OBJECTID str
#2 ASSIGN
#3 ERROR "Unterminated string constant"
#3 OBJECTID jumped
#3 OBJECTID over
#3 OBJECTID the
#3 OBJECTID fence
#4 ERROR "Unterminated string constant"
#4 OBJECTID main
#4 '('
#4 ')'
#4 ':'
#4 TYPEID Object
#4 '{'
#5 '{'
#6 OBJECTID out_string
#6 '('
#7 ERROR "Unterminated string constant"
#7 '}'
#8 '}'
#8 ';'
#9 '}'
#9 ';'
*)