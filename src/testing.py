from cil.baseCilVisitor import BaseCoolToCilVisitor
from abstract.semantics import Context

if __name__ == '__main__':
    context = Context()
    object_type = context.create_type('Object')
    int_type = context.create_type('Integer')
    string_type = context.create_type('String')
    a_type = context.create_type('A')
    b_typpe = context.create_type('B')
    c_type = context.create_type('C')
    d_type = context.create_type('D')
    int_type.set_parent(object_type)
    string_type.set_parent(object_type)
    a_type.set_parent(string_type)
    b_typpe.set_parent(string_type)
    c_type.set_parent(a_type)
    d_type.set_parent(object_type)

    v = BaseCoolToCilVisitor(context)
    print(v.tdt_table)
