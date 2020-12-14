f1 = open('palindrome_test.cil', 'r')
lines_1 = f1.readlines()

f2 = open('palindrome.cil', 'r')
lines_2 = f2.readlines()
print(len(lines_1))
print(len(lines_2))
c = 0
for i in range(0, len(lines_1)):
    if lines_1[i] != lines_2[i]:
        print('line: ',i)
        print('f1: ', lines_1[i])
        print('f2: ', lines_2[i])
        c += 1
        # if c == 15:
        #     break
