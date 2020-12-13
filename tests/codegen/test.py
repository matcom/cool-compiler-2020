f1 = open('io_test.mips', 'r')
lines_1 = f1.readlines()

f2 = open('io.mips', 'r')
lines_2 = f2.readlines()
print(len(lines_1))
print(len(lines_2))
for i in range(0, len(lines_1)):
    if lines_1[i] != lines_2[i]:
        print('line: ',i)
        print('f1: ', lines_1[i])
        print('f2: ', lines_2[i])
