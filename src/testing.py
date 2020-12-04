from build.compiler_struct import LEXER, PARSER
from cil.nodes import CilProgramNode
from travels.ciltomips import MipsCodeGenerator
from typecheck.evaluator import evaluate_right_parse
from comments import find_comments
from travels.ctcill import CilDisplayFormatter, CoolToCILVisitor
import sys


def report(errors: list):
    for error in set(errors):
        print(error)


def pipeline(program: str, deep: int) -> None:
    try:
        program = find_comments(program)
        program = program.replace('\t', ' ' * 4)
    except AssertionError as e:
        print(e)
        sys.exit(1)

    # Right now, program has no comments, so is safe to pass it to the LEXER
    try:
        tokens = LEXER(program)
    except Exception as e:
        print(e)
        sys.exit(1)

    # Parse the tokens to obtain a derivation tree
    try:
        parse = PARSER(tokens)
    except Exception as e:
        print(e)
        sys.exit(1)
    # build the AST from the obtained parse
    # try:
    ast = evaluate_right_parse(parse, tokens[:-1])
    # except Exception as e:
    #     print(e)
    #     sys.exit(1)
    #####################
    # Start the visitors #
    ######################

    # Run type checker visitor
    errors, context, scope = ast.check_semantics(deep)
    if errors:
        report(errors)
        sys.exit(1)

    cil_travel = CoolToCILVisitor(context)
    cil_program_node = cil_travel.visit(ast, scope)
    # formatter = CilDisplayFormatter()
    # print(formatter(cil_program_node))

    mips_gen = MipsCodeGenerator()
    assert isinstance(cil_program_node, CilProgramNode)
    source = mips_gen(cil_program_node)
    print(source)


text = r"""(*
 *  This file shows how to implement a list data type for lists of integers.
 *  It makes use of INHERITANCE and DYNAMIC DISPATCH.
 *
 *  The List class has 4 operations defined on List objects. If 'l' is
 *  a list, then the methods dispatched on 'l' have the following effects:
 *
 *    isNil() : Bool		Returns true if 'l' is empty, false otherwise.
 *    head()  : Int		Returns the integer at the head of 'l'.
 *				If 'l' is empty, execution aborts.
 *    tail()  : List		Returns the remainder of the 'l',
 *				i.e. without the first element.
 *    cons(i : Int) : List	Return a new list containing i as the
 *				first element, followed by the
 *				elements in 'l'.
 *
 *  There are 2 kinds of lists, the empty list and a non-empty
 *  list. We can think of the non-empty list as a specialization of
 *  the empty list.
 *  The class List defines the operations on empty list. The class
 *  Cons inherits from List and redefines things to handle non-empty
 *  lists.
 *)


class List {
   -- Define operations on empty lists.

   isNil() : Bool { true };

   -- Since abort() has return type Object and head() has return type
   -- Int, we need to have an Int as the result of the method body,
   -- even though abort() never returns.

   head()  : Int { { abort(); 0; } };

   -- As for head(), the self is just to make sure the return type of
   -- tail() is correct.

   tail()  : List { { abort(); self; } };

   -- When we cons and element onto the empty list we get a non-empty
   -- list. The (new Cons) expression creates a new list cell of class
   -- Cons, which is initialized by a dispatch to init().
   -- The result of init() is an element of class Cons, but it
   -- conforms to the return type List, because Cons is a subclass of
   -- List.

   cons(i : Int) : List {
      (new Cons).init(i, self)
   };

};


(*
 *  Cons inherits all operations from List. We can reuse only the cons
 *  method though, because adding an element to the front of an emtpy
 *  list is the same as adding it to the front of a non empty
 *  list. All other methods have to be redefined, since the behaviour
 *  for them is different from the empty list.
 *
 *  Cons needs two attributes to hold the integer of this list
 *  cell and to hold the rest of the list.
 *
 *  The init() method is used by the cons() method to initialize the
 *  cell.
 *)

class Cons inherits List {

   car : Int;	-- The element in this list cell

   cdr : List;	-- The rest of the list

   isNil() : Bool { false };

   head()  : Int { car };

   tail()  : List { cdr };

   init(i : Int, rest : List) : List {
      {
	 car <- i;
	 cdr <- rest;
	 self;
      }
   };

};



(*
 *  The Main class shows how to use the List class. It creates a small
 *  list and then repeatedly prints out its elements and takes off the
 *  first element of the list.
 *)

class Main inherits IO {

   mylist : List;

   -- Print all elements of the list. Calls itself recursively with
   -- the tail of the list, until the end of the list is reached.

   print_list(l : List) : Object {
      if l.isNil() then out_string("\n")
                   else {
			   out_int(l.head());
			   out_string(" ");
			   print_list(l.tail());
		        }
      fi
   };

   -- Note how the dynamic dispatch mechanism is responsible to end
   -- the while loop. As long as mylist is bound to an object of 
   -- dynamic type Cons, the dispatch to isNil calls the isNil method of
   -- the Cons class, which returns false. However when we reach the
   -- end of the list, mylist gets bound to the object that was
   -- created by the (new List) expression. This object is of dynamic type
   -- List, and thus the method isNil in the List class is called and
   -- returns true.

   main() : Object {
      {
	 mylist <- new List.cons(1).cons(2).cons(3).cons(4).cons(5);
	 while (not mylist.isNil()) loop
	    {
	       print_list(mylist);
	       mylist <- mylist.tail();
	    }
	 pool;
      }
   };

};
"""
pipeline(text, 5)
