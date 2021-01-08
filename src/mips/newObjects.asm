#class ListNode {
#    int data;
#    ListNode next;
#   
#	ListNode(int data) {
#		this.data = data;
#		next = null;
#	}
#	...
#	next = new ListNode(data);
#	...
#}

j target


newListNode:
#...not shown: save registers
li $a0, 3
move $s0, $a0  		#s0=data

addiu $a0, $zero, 8 #call sbrk(sizeof(ListNode))

#jal sbrk			#	i.e.,sbrk(8)
li $v0, 9 			#set syscall code for sbrk
syscall

addu $s1,$zero,$v0	#s1=this
sw $s0,0($s1)		#this.data = data
addu $t0,$zero,$zero#$t0 <-- null	(0)
sw $t0, 4($s1)		#this.next = null\\memory[$s1+4] <-- null
addu $v0, $zero, $s1 #return this
#...not shown: restore registers
jr $ra 		#return		#regreso a: --> jal function



target:
jal newListNode	#ejecuto la funcion y retorno a este punto

la $t1,($v0)	#copiar direccion
lw $a0, 0($t1) 	#interger to print || $v0 contiene la direccion del new object
li $v0, 1		# system call code for print_int
syscall 		# print it


#imprimir $v0
#imprimir memory[$v0+4]
#lw $a0, 0($v0) #interger to print || $v0 contiene la direccion del new object
#li $v0, 1	# system call code for print_int
#syscall # print it




#exit()
li $v0, 10	# Systemcall code exit
syscall

