from automatons.nondeterministic import NFA

def automata_union(a1,a2):
    transitions={}
    start=0
    d1=1
    d2=a1.states+d1
    u=a2.states+d2

    for src, d in a1.transitions.items():
        for symbol, dest in d.items():
            transitions[src+d1,symbol]=[state+d1 for state in dest]

    for src, d in a2.transitions.items():
        for symbol, dest in d.items():
            transitions[src+d2,symbol]=[state+d2 for state in dest]

    transitions[start,'']=[a1.start+d1,a2.start+d2]
    
    for dx,S in zip([d1,d2],[a1.finals,a2.finals]):
        for z in S:
            try:
                eps_trans=transitions[z+dx,'']
            except KeyError:
                eps_trans=transitions[z+dx,'']=[]
            eps_trans.append(u)

    states=a1.states+a2.states+2
    finals={u}
    return NFA(states,finals,transitions,start)

def automata_concatenation(a1,a2):
    transitions={}
    start=0
    d1=0
    d2=a1.states+d1
    u=a2.states+d2

    for src, d in a1.transitions.items():
        for symbol, dest in d.items():
            transitions[src+d1,symbol]=[state+d1 for state in dest]

    for src, d in a2.transitions.items():
        for symbol, dest in d.items():
            transitions[src+d2,symbol]=[state + d2 for state in dest]
    
    for z in a1.finals:
        try:
            eps_trans=transitions[z+d1,'']
        except KeyError:
            eps_trans=transitions[z+d1,'']=[]
        eps_trans.append(a2.start+d2)
   
    for z in a2.finals:
        try:
            eps_trans=transitions[z+d2,'']
        except KeyError:
            eps_trans=transitions[z+d2,'']=[]
        eps_trans.append(u)
    
    states=a1.states+a2.states+2
    finals={u}
    return NFA(states,finals,transitions,start)

def automata_closure(a1):
    transitions={}
    start=0
    d1=1
    u=a1.states+d1

    for A, d in a1.transitions.items():
        for b, O in d.items():
            transitions[A+d1,b]=[F+d1 for F in O]
    transitions[start,'']=[a1.start+d1,u]
    
    for z in a1.finals:
        try:
            X=transitions[z+d1,'']
        except KeyError:
            X=transitions[z+d1,'']=[]
        X.append(u)
        X.append(a1.start+d1)
    
    states=a1.states+2
    finals={u}
    return NFA(states,finals,transitions,start)

