class ScopeMIPS:
    def __init__(self):
        self.classmethods={}
        self.methodname=""
        self.locals={}
        self.attributes=[]
        self.registerparameters={}
        self.parameters={}
        self.paramcount=0
        self.methodclass=""