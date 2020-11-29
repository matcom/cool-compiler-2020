from .ast import *


def optimization_locals(program: ProgramNode):
    # Each local have a start and end index
    # Index is the instruction index
    for function in program.code:
        intervals = {}
        unnecessary = []
        for local in function.locals:
            # Search initial index of local
            start = 0
            for index, instruction in enumerate(function.body):
                if local in instruction.locals:
                    start = index
                    break
            else:
                # If local is not in any statement then it is marked as unused
                unnecessary.append(local)
                continue
            # Search end index of local
            end = start
            for index, instruction in enumerate(function.body[start:]):
                if local in instruction.locals:
                    end = start + index
            intervals[local] = (start, end)

        # Build and sort new tuples (start,end,localID)
        a = []
        for x in intervals.keys():
            s, e = intervals[x]
            a.append((s, e, x))
        # Keep final locals
        final_locals = []
        if len(a) != 0:
            final_locals.append(a[0])
        for l in a[1:]:
            s, e, x = l
            for index in range(len(final_locals)):
                s2, e2, y = final_locals[index]
                if e2 < s:
                    unnecessary.append(x)
                    x.id = y.id
                    final_locals[index] = (s2, e, y)
                    break
                elif e < s2:
                    unnecessary.append(x)
                    x.id = y.id
                    final_locals[index] = (s, e2, y)
                    break
            else:
                final_locals.append(l)
        # Remove unnnecessary locals
        for u in unnecessary:
            function.locals.remove(u)

def remove_unused_locals(program: ProgramNode):
    for function in program.code:
        used_locals=[]
        for instruction in function.body:
            for local in instruction.locals:
                if local not in used_locals:
                    try:
                        if instruction.result.id!=local.id:
                            used_locals.append(local)
                    except:
                            used_locals.append(local)
        body=(function.body).copy()
        for instruction in function.body:
            for local in instruction.locals:
                try:
                    if instruction.result.id==local.id and local not in used_locals and not isinstance(instruction, VCAllNode):
                        body.remove(instruction)
                except:
                    pass

        function.body=body
        function.locals=used_locals
                           
                    
                    
                    
                    
                    