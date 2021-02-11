li $v0, 1 # system call code for print_int
li $a0, 5 # integer to print
syscall   # print it

#exit()
li $v0, 10
syscall