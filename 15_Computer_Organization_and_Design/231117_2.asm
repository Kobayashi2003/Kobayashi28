.data
string: .asciiz "ADRAdfghtGHgff"
dest: .space 16

.text
main:
    la $a0, string
    la $a1, dest

    li $t1, 0x10
loop:
    lb $t0, 0($a0)
    andi $t0, $t0, 0xDF
    sb $t0, 0($a1)
    addi $a0, $a0, 1
    addi $a1, $a1, 1
    addi $t1, $t1, -1
    bne $t1, $zero, loop

    la $v0, 4
    la $a0, dest
    syscall

    li $v0, 10
    syscall