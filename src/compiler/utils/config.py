TYPE_ERROR = "TypeError"
NAME_ERROR = "NameError"
ATTRIBUTE_ERROR = "AttributeError"
SEMANTIC_ERROR = "SemanticError"

SELF_TYPE = "SELF_TYPE"
INT = "Int"
BOOL = "Bool"
STRING = "String"
OBJECT = "Object"
IO = "IO"

ABORT = "abort"
COPY = "copy"
TYPE_NAME = "type_name"

OUT_STRING = "out_string"
OUT_INT = "out_int"
IN_STRING = "in_string"
IN_INT = "in_int"

LENGTH = "length"
CONCAT = "concat"
SUBSTR = "substr"


ABORT_SIGNAL = "abort_signal"#CIL
CASE_MISSMATCH = "case_missmatch"#CIL
CASE_VOID = "case_on_void"#MIPS
DISPATCH_VOID = "dispatch_on_void"#MIPS
ZERO_DIVISION = "division_by_zero"#MIPS
SUBSTR_OUT_RANGE = "substr_out_of_range"#MIPS
HEAP_OVERFLOW = "heap_overflow"

#code_gen
WORD = ".word"
ASCIIZ = ".asciiz"
SPACE = ".space"

t0 = "$t0"
t1 = "$t1"
t2 = "$t2"
t3 = "$t3"
t6 = "$t6" # convenios
t7 = "$t7" # convenios
a0 = "$a0"
a1 = "$a1"
fp = "$fp"
sp = "$sp"
ra = "$ra"
lo = "lo"
hi = "hi"
v0 = "$v0"
s0 = "$s0"
s1 = "$s1"
s2 = "$s2"
s3 = "$s3"
zero = "$zero"

BUFFER_SIZE = 1024
INSTANCE_EXTRA_FIELDS = 1 # just type_info
VTABLE_EXTRA_FIELDS = 3 # type_name, parent, size
FP_ARGS_DISTANCE = 3 # how far finishes $fp from arguments in method call
FP_LOCALS_DISTANCE = 0 # how far finishes $fp from localvars in method call
VOID = "void"
STR_CMP = "string_comparer"
EMPTY_STRING = "empty_string"
INPUT_STR_BUFFER = "input_str_buffer"
EXIT = "exit"

TYPEINFO_ATTR_OFFSET = 0

#type_info offsets
TYPENAME_OFFSET = 0
PARENT_OFFSET = 4
SIZE_OFFSET = 8

#str attributes offsets
LENGTH_ATTR_OFFSET = 4
CHARS_ATTR_OFFSET = 8

SYSCALL_PRINT_INT = 1
SYSCALL_PRINT_STR = 4
SYSCALL_READ_INT = 5
SYSCALL_READ_STR = 8
SYSCALL_SBRK = 9
SYSCALL_EXIT = 10

RA_OFFSET = 4
OLD_FP_OFFSET = 8
SELF_OFFSET = 12

BOX_SIZE = 8
BOXED_VALUE_OFFSET = 4
STRING_SIZE = 12