.text
    li $t0, -1
    li $t1, 2
    slt $t2, $t0, $t1
    beq $t2, $zero, NEXT
    li $t3, 1
    j EXIT
NEXT:
    li $t3, 0
EXIT:
    li $v0, 1
    move $a0, $t3
    syscall
    li $v0, 10
    syscall