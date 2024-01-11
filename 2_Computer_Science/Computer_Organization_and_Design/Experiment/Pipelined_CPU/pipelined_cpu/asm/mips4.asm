lui  $t0, 0x4000
lw   $t1, 0x14($t0)
beq  $t1, $zero, tmp1
lw   $t1, 0x10($t0)
sll  $t1, $t1, 2
add  $t1, $t1, $t0
lw   $t1, 0x18($t1)
beq  $zero, $zero, tmp2
tmp1:
lw   $t1, 0x8($t0)
tmp2:
sw   $t1, 0x0($t0)

addi $t0, $zero, 0x1000
mtc0 $t0, $11
mtc0 $zero, $9