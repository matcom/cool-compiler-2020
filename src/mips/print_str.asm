.data
    hello: .asciiz "Hello, world!"

.text
    li $v0, 4		# system call code for print_str
    la $a0, hello 	# str to print
    syscall			# print it
    
    #exit()
    li $v0, 10
    syscall