f1 = open('hello_world_test.mips', 'r')
lines_1 = f1.readlines()

f2 = open('hello_world.mips', 'r')
lines_2 = f2.readlines()

for i in range(0, len(lines_1)):
    if lines_1[i] != lines_2[i]:
        print('line: ',i)
        print('f1: ', lines_1[i])
        print('f2: ', lines_2[i])