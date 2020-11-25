class Main inherits IO {
    main(): Int {
        1
    };
};

class A {};
class B {};
class C {};
class D inherits C {};
class E inherits C {};
class F inherits D {};
class G inherits F {};
class H inherits B {};
class I inherits E {};
class W inherits Z {};
class Z inherits X {};
class X inherits Y {};
class Y inherits W {};
class Q inherits Y {};