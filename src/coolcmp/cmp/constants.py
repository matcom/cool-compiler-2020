WORD = 4

# static literals

LABEL_ABORT_STR = '_static_abort'
LABEL_SPACE = '_static_space'
LABEL_ENDL = '_static_endl'

static_literals = {
    LABEL_ABORT_STR: 'Abort called from class',
    LABEL_SPACE: ' ',
    LABEL_ENDL: r'\n'
}

LABEL_STR_LITERAL = '_str_literal_'
LABEL_INT_LITERAL = '_int_literal_'

LABEL_FUNC_PREF = '_st_'

LABEL_EXIT = '_exit'
LABEL_RESERVE_MEMORY = '_reserve_memory'
LABEL_RUNTIME_DISPATCH = '_runtime_dispatch'
LABEL_PRINT_ERROR_EXIT = '_print_error_exit'
LABEL_MAIN = 'main'

# represents a loop start and end, they print as {LABEL_...}{id}
LABEL_START_LOOP = '_loop_'
LABEL_END_LOOP = '_end_loop_'

# static errors literals

LABEL_DISPATCH_VOID = '_err_dispatch_void'
LABEL_CASE_VOID = '_err_case_void'
LABEL_CASE_NO_BRANCH = '_err_case_no_branch'
LABEL_DIV_BY_0 = '_err_div_by_0'
LABEL_SUBSTR_RANGE = '_err_substr_range'
LABEL_HEAP_OVERFLOW = '_err_heap_overflow'

rte_errors = {
    LABEL_DISPATCH_VOID: 'Dispatch on void',
    LABEL_CASE_VOID: 'Case on void',
    LABEL_CASE_NO_BRANCH: 'Case without a matching branch',
    LABEL_DIV_BY_0: 'Division by zero',
    LABEL_SUBSTR_RANGE: 'Substring out of range',
    LABEL_HEAP_OVERFLOW: 'Heap overflow'
}

LABEL_BOOL_TRUE = '_bool_true'
LABEL_BOOL_FALSE = '_bool_false'
LABEL_BOOL_END = '_bool_end'

# represents a branch, it prints as {LABEL_BRANCH}{id}
LABEL_BRANCH = '_branch_label_'

LABEL_EQ_FUNCTION = '_eq_function'

# branches for eq
LABEL_EQ_NOT_PRIMITIVE = '_branch_not_primitive_type'
LABEL_EQ_BRANCH_INT = '_branch_int_type'
LABEL_EQ_BRANCH_BOOL = '_branch_bool_type'
LABEL_EQ_BRANCH_STRING = '_branch_string_type'
LABEL_EQ_END = '_branch_end_eq'

# to add in static info for each object 
TYPE_NOT_PRIMITIVE = 0
TYPE_INT = 1
TYPE_BOOL = 2
TYPE_STRING = 3