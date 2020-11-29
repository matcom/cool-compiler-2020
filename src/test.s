.data
			Int_name:     .asciiz      "Int"
			Int_size:     .word     16
__virtual_table__Int:
			 .word function_abort_at_Object
			 .word function_type_name_at_Object
			 .word function_copy_at_Object
			String_name:     .asciiz      "String"
			String_size:     .word     16
__virtual_table__String:
			 .word function_abort_at_Object
			 .word function_type_name_at_Object
			 .word function_copy_at_Object
			 .word function_length_at_String
			 .word function_concat_at_String
			 .word function_substr_at_String
			Bool_name:     .asciiz      "Bool"
			Bool_size:     .word     16
__virtual_table__Bool:
			 .word function_abort_at_Object
			 .word function_type_name_at_Object
			 .word function_copy_at_Object
			Object_name:     .asciiz      "Object"
			Object_size:     .word     12
__virtual_table__Object:
			 .word function_abort_at_Object
			 .word function_type_name_at_Object
			 .word function_copy_at_Object
			IO_name:     .asciiz      "IO"
			IO_size:     .word     12
__virtual_table__IO:
			 .word function_abort_at_Object
			 .word function_type_name_at_Object
			 .word function_copy_at_Object
			 .word function_out_string_at_IO
			 .word function_out_int_at_IO
			 .word function_in_int_at_IO
			 .word function_in_string_at_IO
			Main_name:     .asciiz      "Main"
			Main_size:     .word     32
__virtual_table__Main:
			 .word function_abort_at_Object
			 .word function_type_name_at_Object
			 .word function_copy_at_Object
			 .word function_out_string_at_IO
			 .word function_out_int_at_IO
			 .word function_in_int_at_IO
			 .word function_in_string_at_IO
			 .word function_main_at_Main
			_empty:     .asciiz      ""
			data_1:     .asciiz      "2 is trivially prime.
"
			data_2:     .asciiz      " is prime.
"
			data_3:     .asciiz      "continue"
			data_4:     .asciiz      "halt"
            _error1:    .asciiz     "Halt program because abort"
            _buffer:    .space      2048
            _void:      .asciiz       ""
             

.text
main:

 #muevo el fp al sp, pongo en sp ra y avanzo la pila

			move $fp, $sp
			sw $ra, 0($sp)
			addiu $sp, $sp, -4

 #muevo la pila x las variables locales

			addiu $sp, $sp, -12

 #init allocate

			li $v0, 9
			lw $a0, Main_size
			syscall
			sw $v0, -4($fp)

 #end allocate


 #guardando los parametros

			sw $fp, 0($sp)
			addiu $sp, $sp, -4
			lw $a0, -4($fp)
			sw $a0, 0($sp)
			addiu $sp, $sp, -4

 # fin guardando los parametros


 #comienzo llamada al constructor

			jal function_Ctr_at_Main
			sw $a0, -8($fp)

 #fin llamada dinamica


 #guardando los parametros

			sw $fp, 0($sp)
			addiu $sp, $sp, -4
			lw $a0, -8($fp)
			sw $a0, 0($sp)
			addiu $sp, $sp, -4

 # fin guardando los parametros


 #comienzo llamada dinamica

			la $a0, __virtual_table__Main
			lw $a0, 28($a0)
			jalr $a0
			sw $a0, -12($fp)

 #fin llamada dinamica


 #retornando el valor

			li $a0, 0

 #return sp, fp, ra

			lw $ra, 0($fp)
			addiu $sp, $sp, 20
			lw $fp, 0($sp)
			jr $ra
function_main_at_Main:

 #muevo el fp al sp, pongo en sp ra y avanzo la pila

			move $fp, $sp
			sw $ra, 0($sp)
			addiu $sp, $sp, -4

 #muevo la pila x las variables locales

			addiu $sp, $sp, -0

 #retornando el valor

			li $a0, 0

 #return sp, fp, ra

			lw $ra, 0($fp)
			addiu $sp, $sp, 12
			lw $fp, 0($sp)
			jr $ra
function_Ctr_at_Main:

 #muevo el fp al sp, pongo en sp ra y avanzo la pila

			move $fp, $sp
			sw $ra, 0($sp)
			addiu $sp, $sp, -4

 #muevo la pila x las variables locales

			addiu $sp, $sp, -4

 #LOAD inicia

			la $t1, Main_name
			lw $t2, 4($fp)
			sw $t1, 0($t2)

 #LOAD inicia

			lw $t1, Main_size
			lw $t2, 4($fp)
			sw $t1, 4($t2)

 #LOAD inicia

			la $t1, __virtual_table__Main
			lw $t2, 4($fp)
			sw $t1, 8($t2)

 #guardando los parametros

			sw $fp, 0($sp)
			addiu $sp, $sp, -4
			lw $a0, 4($fp)
			sw $a0, 0($sp)
			addiu $sp, $sp, -4

 # fin guardando los parametros


 #comienzo llamada al constructor

			jal function_Init_at_Main
			sw $a0, -4($fp)

 #fin llamada dinamica


 #retornando el valor

			lw $a0, 4($fp)

 #return sp, fp, ra

			lw $ra, 0($fp)
			addiu $sp, $sp, 16
			lw $fp, 0($sp)
			jr $ra
function_Init_at_Main:

 #muevo el fp al sp, pongo en sp ra y avanzo la pila

			move $fp, $sp
			sw $ra, 0($sp)
			addiu $sp, $sp, -4

 #muevo la pila x las variables locales

			addiu $sp, $sp, -180

 #guardando los parametros

			sw $fp, 0($sp)
			addiu $sp, $sp, -4
			lw $a0, 4($fp)
			sw $a0, 0($sp)
			addiu $sp, $sp, -4

 # fin guardando los parametros


 #comienzo llamada al constructor

			jal function_Init_at_IO
			sw $a0, -4($fp)

 #fin llamada dinamica

			la $t1, data_1
			sw $t1, -12($fp)

 #guardando los parametros

			sw $fp, 0($sp)
			addiu $sp, $sp, -4
			lw $a0, -12($fp)
			sw $a0, 0($sp)
			addiu $sp, $sp, -4
			lw $a0, 4($fp)
			sw $a0, 0($sp)
			addiu $sp, $sp, -4

 # fin guardando los parametros

			lw $a0, 4($fp)
			lw $a0, 8($a0)
			lw $a0, 12($a0)
			jalr $a0
			sw $a0, -8($fp)

 #init set attribute

			lw $a0, 4($fp)
			li $t1, 2
			sw $t1, 12($a0)

 #end set attribute


 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 12($a0)
			sw $a0, -16($fp)

 #init set attribute

			lw $a0, 4($fp)
			lw $t1, -16($fp)
			sw $t1, 16($a0)

 #end set attribute


 #init set attribute

			lw $a0, 4($fp)
			li $t1, 0
			sw $t1, 20($a0)

 #end set attribute


 #init set attribute

			lw $a0, 4($fp)
			li $t1, 1000
			sw $t1, 24($a0)

 #end set attribute

label_Init_at_Main_0:
			li $a0, 1
			bne $a0, $zero, label_Init_at_Main_1
			j label_Init_at_Main_2
label_Init_at_Main_1:

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 16($a0)
			sw $a0, -24($fp)
			lw $t1, -24($fp)
			li $a0, 1
			add $a0, $a0, $t1
			sw $a0, -20($fp)

 #init set attribute

			lw $a0, 4($fp)
			lw $t1, -20($fp)
			sw $t1, 16($a0)

 #end set attribute


 #init set attribute

			lw $a0, 4($fp)
			li $t1, 2
			sw $t1, 20($a0)

 #end set attribute

label_Init_at_Main_3:

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 16($a0)
			sw $a0, -32($fp)

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 20($a0)
			sw $a0, -40($fp)

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 20($a0)
			sw $a0, -44($fp)
			lw $t1, -40($fp)
			lw $a0, -44($fp)
			mul $a0 $t1 $a0
			sw $a0, -36($fp)
			lw $t1, -32($fp)
			lw $a0, -36($fp)
			blt $t1, $a0, label_Init_at_Main_6
			li $a0, 0
			j label_Init_at_Main_7
label_Init_at_Main_6:
			li $a0, 1
label_Init_at_Main_7:
			sw $a0, -28($fp)
			lw $a0, -28($fp)
			bne $a0, $zero, label_Init_at_Main_8

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 16($a0)
			sw $a0, -60($fp)

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 20($a0)
			sw $a0, -68($fp)

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 16($a0)
			sw $a0, -76($fp)

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 20($a0)
			sw $a0, -80($fp)
			lw $t1, -76($fp)
			lw $a0, -80($fp)
			div $a0, $t1, $a0
			sw $a0, -72($fp)
			lw $t1, -68($fp)
			lw $a0, -72($fp)
			mul $a0 $t1 $a0
			sw $a0, -64($fp)
			lw $t1, -60($fp)
			lw $a0, -64($fp)
			sub $a0, $t1, $a0
			sw $a0, -56($fp)
			lw $t1, -56($fp)
			li $a0, 0
			sub $a0, $t1, $a0
			sw $a0, -84($fp)
			lw $a0, -84($fp)
			bne $a0, $zero, label_Init_at_Main_10
			li $t1, 1
			sw $t1, -52($fp)
			j label_Init_at_Main_11
label_Init_at_Main_10:
			li $t1, 0
			sw $t1, -52($fp)
label_Init_at_Main_11:
			lw $a0, -52($fp)
			bne $a0, $zero, label_Init_at_Main_12
			li $t1, 1
			sw $t1, -88($fp)
			j label_Init_at_Main_13
label_Init_at_Main_12:
			li $t1, 0
			sw $t1, -88($fp)
label_Init_at_Main_13:
			lw $t1, -88($fp)
			sw $t1, -48($fp)
			j label_Init_at_Main_9
label_Init_at_Main_8:
			li $t1, 0
			sw $t1, -48($fp)
label_Init_at_Main_9:
			lw $a0, -48($fp)
			bne $a0, $zero, label_Init_at_Main_4
			j label_Init_at_Main_5
label_Init_at_Main_4:

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 20($a0)
			sw $a0, -96($fp)
			lw $t1, -96($fp)
			li $a0, 1
			add $a0, $a0, $t1
			sw $a0, -92($fp)

 #init set attribute

			lw $a0, 4($fp)
			lw $t1, -92($fp)
			sw $t1, 20($a0)

 #end set attribute

			j label_Init_at_Main_3
label_Init_at_Main_5:
			la $t1, _void
			sw $t1, -100($fp)

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 16($a0)
			sw $a0, -108($fp)

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 20($a0)
			sw $a0, -116($fp)

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 20($a0)
			sw $a0, -120($fp)
			lw $t1, -116($fp)
			lw $a0, -120($fp)
			mul $a0 $t1 $a0
			sw $a0, -112($fp)
			lw $t1, -108($fp)
			lw $a0, -112($fp)
			blt $t1, $a0, label_Init_at_Main_14
			li $a0, 0
			j label_Init_at_Main_15
label_Init_at_Main_14:
			li $a0, 1
label_Init_at_Main_15:
			sw $a0, -104($fp)
			lw $a0, -104($fp)
			bne $a0, $zero, label_Init_at_Main_16
			li $t1, 0
			sw $t1, -124($fp)
			j label_Init_at_Main_17
label_Init_at_Main_16:

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 16($a0)
			sw $a0, -128($fp)

 #init set attribute

			lw $a0, 4($fp)
			lw $t1, -128($fp)
			sw $t1, 12($a0)

 #end set attribute


 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 12($a0)
			sw $a0, -136($fp)

 #guardando los parametros

			sw $fp, 0($sp)
			addiu $sp, $sp, -4
			lw $a0, -136($fp)
			sw $a0, 0($sp)
			addiu $sp, $sp, -4
			lw $a0, 4($fp)
			sw $a0, 0($sp)
			addiu $sp, $sp, -4

 # fin guardando los parametros

			lw $a0, 4($fp)
			lw $a0, 8($a0)
			lw $a0, 16($a0)
			jalr $a0
			sw $a0, -132($fp)
			la $t1, data_2
			sw $t1, -144($fp)

 #guardando los parametros

			sw $fp, 0($sp)
			addiu $sp, $sp, -4
			lw $a0, -144($fp)
			sw $a0, 0($sp)
			addiu $sp, $sp, -4
			lw $a0, 4($fp)
			sw $a0, 0($sp)
			addiu $sp, $sp, -4

 # fin guardando los parametros

			lw $a0, 4($fp)
			lw $a0, 8($a0)
			lw $a0, 12($a0)
			jalr $a0
			sw $a0, -140($fp)
			lw $t1, -140($fp)
			sw $t1, -124($fp)
label_Init_at_Main_17:

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 24($a0)
			sw $a0, -152($fp)

 #init get attribute

			lw $a0, 4($fp)
			lw $a0, 16($a0)
			sw $a0, -156($fp)
			lw $t1, -152($fp)
			lw $a0, -156($fp)
			ble $t1, $a0, label_Init_at_Main_18
			li $a0, 0
			j label_Init_at_Main_19
label_Init_at_Main_18:
			li $a0, 1
label_Init_at_Main_19:
			sw $a0, -148($fp)
			lw $a0, -148($fp)
			bne $a0, $zero, label_Init_at_Main_20
			la $t1, data_3
			sw $t1, -164($fp)
			lw $t1, -164($fp)
			sw $t1, -160($fp)
			j label_Init_at_Main_21
label_Init_at_Main_20:
			la $t1, data_4
			sw $t1, -172($fp)

 #init allocate

			li $v0, 9
			lw $a0, String_size
			syscall
			sw $v0, -176($fp)

 #end allocate


 #init set attribute

			lw $a0, -176($fp)
			lw $t1, -172($fp)
			sw $t1, 12($a0)

 #end set attribute


 #LOAD inicia

			la $t1, String_name
			lw $t2, -176($fp)
			sw $t1, 0($t2)

 #LOAD inicia

			lw $t1, String_size
			lw $t2, -176($fp)
			sw $t1, 4($t2)

 #LOAD inicia

			la $t1, __virtual_table__String
			lw $t2, -176($fp)
			sw $t1, 8($t2)

 #guardando los parametros

			sw $fp, 0($sp)
			addiu $sp, $sp, -4
			lw $a0, -176($fp)
			sw $a0, 0($sp)
			addiu $sp, $sp, -4

 # fin guardando los parametros


 #comienzo llamada dinamica

			lw $a0, -176($fp)
			lw $a0, 8($a0)
			lw $a0, 0($a0)
			jalr $a0
			sw $a0, -168($fp)

 #fin llamada dinamica

			lw $t1, -168($fp)
			sw $t1, -160($fp)
label_Init_at_Main_21:
			j label_Init_at_Main_0
label_Init_at_Main_2:
			la $t1, _void
			sw $t1, -180($fp)

 #init set attribute

			lw $a0, 4($fp)
			lw $t1, -180($fp)
			sw $t1, 28($a0)

 #end set attribute


 #retornando el valor

			lw $a0, 4($fp)

 #return sp, fp, ra

			lw $ra, 0($fp)
			addiu $sp, $sp, 192
			lw $fp, 0($sp)
			jr $ra


function_Ctr_at_Object:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4
            
            la $t1, Object_name
			lw $t2, 4($fp)
			sw $t1, 0($t2)

			lw $t1, Object_size
			lw $t2, 4($fp)
			sw $t1, 4($t2)

			la $t1, __virtual_table__Object
			lw $t2, 4($fp)
			sw $t1, 8($t2)


            lw $a0, 4($fp)

            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

function_Init_at_Object:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4
            
            lw $a0, 4($fp)

            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

function_Ctr_at_IO:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            la $t1, IO_name
			lw $t2, 4($fp)
			sw $t1, 0($t2)

			lw $t1, IO_size
			lw $t2, 4($fp)
			sw $t1, 4($t2)

			la $t1, __virtual_table__IO
			lw $t2, 4($fp)
			sw $t1, 8($t2)


            lw $a0, 4($fp)

            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

function_Init_at_IO:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $a0, 4($fp)

            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

function_type_name_at_Object:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4
            lw $a0, 4($fp)   
            lw  $a0 0($a0)      
            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra

function_abort_at_Object:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4
            la $a0, _error1
            li $v0, 4
            syscall
            li $v0, 10
            syscall

function_copy_at_Object:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $a0, 4($fp)
            lw $a0, 0($a0)
            la $t0, Int_name

            bne $a0, $t0, not_int
            lw $a0, 4($fp)
            lw $a0, 8($a0)
            j end

        not_int:
            lw $a0, 4($fp)
            lw $a0, 0($a0)
            la $t0, Bool_name

            bne $a0, $t0, not_bool
            lw $a0, 4($fp)
            lw $a0, 8($a0)
            j end

        not_bool:
            lw $a0, 4($fp)
            lw $a0, 0($a0)
            la $t0, String_name

            bne $a0, $t0, not_string
            lw $a0, 4($fp)
            lw $a0, 8($a0)
            j end
        
        not_string:
            lw $a0, 4($fp)
            move $t2, $a0 
            lw $a0, 4($a0)
            move $t1, $a0

            li $v0, 9
            syscall

            move $a0, $v0

        copy:
            lw $t0, 0($t2)
            sw $t0, 0($a0)
            addiu $a0, $a0, 4
            addiu $t2, $t2, 4
            addiu $t1, $t1, -4
            bne $t1, $zero, copy
            
            move $a0, $v0

        end:
            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

function_length_at_String:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $s0, 4($fp)
            li $a0, -1

        length:
            lb $t0, ($s0)
            addiu $a0, $a0, 1
            addiu $s0, $s0, 1
            bne $t0, $zero, length
            
            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

function_concat_at_String:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $s1, 4($fp)
            sw $fp, 0($sp)
            addiu $sp, $sp, -4
            sw $s1, 0($sp)
            addiu $sp, $sp, -4
            jal function_length_at_String
            
            sw $a0, 0($sp)
            addiu $sp, $sp, -4

            lw $s1, 8($fp)
            sw $fp, 0($sp)
            addiu $sp, $sp, -4
            sw $s1, 0($sp)
            addiu $sp, $sp, -4
            jal function_length_at_String

            lw $t7, 4($sp)
            addiu $sp, $sp, 4

            move $t6, $a0
            add $a0, $t7, $t6
            addiu $a0, $a0, 1

            li $v0, 9
            syscall

            move $t0, $v0

            lw $s1, 4($fp)
        copy_self:
            lb $t5, ($s1)
            beq $t5, $zero, end_copy_self
            sb $t5, ($t0)
            addiu $s1, $s1, 1
            addiu $t0, $t0, 1
            j copy_self

        end_copy_self:
            lw $s1, 8($fp)

        copy_given:
            lb $t5, ($s1)
            sb $t5, ($t0)
            addiu $s1, $s1, 1
            addiu $t0, $t0, 1
            bne $t5, $zero, copy_given


            move $a0, $v0

            lw $ra, 0($fp)
            addiu $sp, $sp, 16
            lw $fp, 0($sp)
            jr $ra 


function_substr_at_String:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $a0, 12($fp)
            addiu $a0, $a0, 1
            li $v0, 9
            syscall

            move $t0, $v0

            lw $s1, 4($fp)
            lw $t1, 8($fp)
            add $s1, $s1, $t1

            lw $t1, 12($fp)

        substr:
            lb $t5, ($s1)
            sb $t5, ($t0)
            addiu $s1, $s1, 1
            addiu $t0, $t0, 1
            addiu $t1, $t1, -1
            bne $t1, $zero, substr

            sb $zero, ($t0)
            move $a0, $v0

            lw $ra, 0($fp)
            addiu $sp, $sp, 20
            lw $fp, 0($sp)
            jr $ra 


function_comparer_string:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $s1, 4($fp)
            sw $fp, 0($sp)
            addiu $sp, $sp, -4
            sw $s1, 0($sp)
            addiu $sp, $sp, -4
            jal function_length_at_String
            
            sw $a0, 0($sp)
            addiu $sp, $sp, -4

            lw $s1, 8($fp)
            sw $fp, 0($sp)
            addiu $sp, $sp, -4
            sw $s1, 0($sp)
            addiu $sp, $sp, -4
            jal function_length_at_String

            lw $t7, 4($sp)
            addiu $sp, $sp, 4

            bne $t7, $a0, not_equals_strings

            lw $t7, 4($fp)
            lw $a0, 8($fp)

        equal_chart:
            lb $t1, ($t7)
            lb $t2, ($a0)
            addiu $t7, $t7, 1
            addiu $a0, $a0, 1
            bne $t1, $t2, not_equals_strings
            beq $t1, $zero, equals_strings
            j equal_chart

        not_equals_strings:
            li $a0, 0
            j end_equal_string

        equals_strings:
            li $a0, 1

        end_equal_string:
            lw $ra, 0($fp)
            addiu $sp, $sp, 16
            lw $fp, 0($sp)
            jr $ra 



function_out_string_at_IO:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $a0, 8($fp)
            li $v0, 4
            syscall

            lw $a0, 4($fp)

            lw $ra, 0($fp)
            addiu $sp, $sp, 16
            lw $fp, 0($sp)
            jr $ra 

function_out_int_at_IO:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $a0, 8($fp)
            li $v0, 1
            syscall

            lw $a0, 4($fp)

            lw $ra, 0($fp)
            addiu $sp, $sp, 16
            lw $fp, 0($sp)
            jr $ra 

function_in_int_at_IO:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            lw $a0, 4($fp)
            li $v0, 5
            syscall

            move $a0, $v0

            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

function_in_string_at_IO:
            move $fp, $sp
            sw $ra, 0($sp)
            addiu $sp, $sp, -4

            la $a0, _buffer
            li $a1, 1024

            li $v0, 8
            syscall

            sw $fp, 0($sp)
            addiu $sp, $sp, -4
            sw $a0, 0($sp)
            addiu $sp, $sp, -4
            jal function_length_at_String

            addiu $a0, $a0, 1
            li $v0, 9
            syscall

            move $t0, $v0
            la $a0, _buffer

        IO_copy:
            lb $t1, ($a0)
            sb $t1, ($t0)
            addiu $a0, $a0, 1
            addiu $t0, $t0, 1
            bne $t1, $zero, IO_copy

            addiu $t0, $t0, -2
            sb $zero, ($t0)

            move $a0, $v0

            lw $ra, 0($fp)
            addiu $sp, $sp, 12
            lw $fp, 0($sp)
            jr $ra 

            
