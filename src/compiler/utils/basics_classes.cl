class Object {
    abort(): Object { self };
    copy(): Object { self };
    type_name(): String { "" };
};

class IO {
    in_int(): Int { 0 };
    in_string(): String { "" };
    out_int(x: Int): IO { self };
    out_string(x: String): IO { self };
};

class Int {
};

class Bool {
};

class String {
    length(): Int { 0 };
    concat(s: String): String { "" };
    substr(i: Int, l: Int): String { "" };
};




