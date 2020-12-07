from json import dumps

class functionSerializable:
    def __init__(self, func,
                       funcName,
                       params ):
        self.func= func
        self.funcName= funcName
        self.params= params

    def __repr__(self):
        return self.toJSON()

    def toJSON(self):
        return dumps(self, default=lambda  o: o.__dict__,
            sort_keys=True, indent=4, separators=(',', ': '))


class funcs:
    abortFunc= functionSerializable (
               func= lambda: sys.exit('Error in program execution'), 
               funcName= "abortFunc",
               params= [])
    typeNameFunc= functionSerializable (
                  func= lambda className: className,
                  funcName= "typeNameFunc",
                  params= ['className'])
    copyFunc= functionSerializable (
              func= lambda className: self.types[className],
              funcName= "copyFunc",
              params= ["className"])    
    outStringFunc= functionSerializable (
              func= lambda argument: print(argument) or 'SELF_TYPE',
              funcName= "outStringFunc",
              params= [])
    outIntFunc= functionSerializable (
                func= lambda argument: print(argument) or 'SELF_TYPE',
                funcName= "outIntFunc",
                params= [])
    readFromInputFunc= functionSerializable(
                func= lambda: input(),
                funcName= "readFromInputFunc",
                params= [])
    concatFunc= functionSerializable(
                func= lambda selfVal, otherVal : selfVal + otherVal,
                funcName= "concatFunc",
                params= ["selfVal", "otherVal"])
    substrFunc= functionSerializable (
                func= lambda selfVal, i1, i2: selfVal[i1:i2],
                funcName= "substrFunc",
                params= ["selfVal", 'i1', "i2"])

    
