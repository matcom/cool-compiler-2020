import os
from semantic_analyzer import SemanticAnalyzer
import sys
from parser import Parser

class Tester:
    def __init__(self):
        self.success = []
        self.failed = []
        
    def run_correct_test(self, path):
        test_list = os.listdir(path)
        for test in test_list:
            try:
                errors = self.execute_test(path +"/"+ test)
            except:
                self.failed.append(test)
            else:
                if len(errors) > 1:
                    self.failed.append(test)
                else:
                    self.success.append(test)
        print("Total of Correct Test:", len(test_list))
        print("Success:", len(self.success))
        print("Failed:", len(self.failed))
        print(self.failed)
        return self.failed
    
    def run_bad_test(self, path):
        test_list = os.listdir(path)
        for test in test_list:
            try:
                errors = self.execute_test(path +"/"+ test)
            except:
                self.failed.append(test)
            else:
                if len(errors) == 0:
                    self.failed.append(test)
                else:
                    self.success.append(test)
        print("Total of Bad Test:", len(test_list))
        print("Success:", len(self.success))
        print("Failed:", len(self.failed))
        print(self.failed)
        return self.failed


    def execute_test(self, test_name):
        parser = Parser()
       
        with open(test_name, encoding="utf-8") as file:
            cool_program_code = file.read()

        parse_result = parser.parse(cool_program_code)

        if parser.errors:
            print(parser.errors[0])
            exit(1)

        analyzer = SemanticAnalyzer(parse_result)
        analyzer.analyze()

        return analyzer.errors

if __name__ == '__main__':
    tester = Tester()
    # tester.run_correct_test("../tests/semantic/Correct")
    tester.run_bad_test("../tests/semantic/Bad")