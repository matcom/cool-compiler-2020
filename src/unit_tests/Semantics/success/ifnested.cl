class Foo {

};

class Test {
  foo:Test;
  bar(x: Int, baz : Foo):Object 
  { 
    if x = 3 then 
    {
      if x < 2 then 
        new Foo 
      else 
        isvoid baz 
      fi;
    }
    else 
      false 
    fi
  };
};

class Main {
	main() : Int {
		1
	};
};