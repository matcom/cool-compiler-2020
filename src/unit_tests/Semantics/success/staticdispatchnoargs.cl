class Test {
  foo:Int;
  bar():Object{self@Test.bar()};
};

class Main {
  main() : Object {
    (new Test).bar()
  };
};