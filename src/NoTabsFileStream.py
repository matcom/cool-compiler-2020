
from antlr4.FileStream import FileStream


class NoTabsFileStream(FileStream):

    def __init__(self, fileName:str, tabSpaces: int = 1):
        self.tabSpaces = tabSpaces
        super().__init__(fileName, "utf-8")

    def readDataFrom(self, fileName:str, encoding:str, errors:str='strict'):
        s = super().readDataFrom(fileName, encoding, errors)
        r = ""
        for t in s:
            if t == '\t':
                i = self.tabSpaces
                while i > 0:
                    r += ' '
                    i -= 1
            else:
                r += t
        return r


