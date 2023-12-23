lui  $t0, 0x4000    # buffer addr

lw   $t1, 0x10($t0) # array len
addi $t1, $t1, 1
addi $t0, $t0, 0x18 # array address

add  $t2, $zero, $zero # i = 0
add  $t3, $zero, $zero # j = 0

loop1:

beq  $t1, $t2, exit
add  $t3, $t2, $zero

loop2:

beq  $t1, $t3, loop1

sll  $t4, $t2, 2
sll  $t5, $t3, 2
add  $t4, $t0, $t4
add  $t5, $t0, $t5
lw   $t7, 0($t4)  # arr[i]
lw   $t8, 0($t5)  # arr[j]

slt  $t6, $t7, $t8
bne  $t6, $zero, tmp1

sw   $t7, 0($t5)
sw   $t8, 0($t4)

tmp1:

addi $t3, $t3, 1
bne  $t1, $t3, tmp2
addi $t2, $t2, 1
tmp2:

beq  $zero, $zero, loop2

exit: