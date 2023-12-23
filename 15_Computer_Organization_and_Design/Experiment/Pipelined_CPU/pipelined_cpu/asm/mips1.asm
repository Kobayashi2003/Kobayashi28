lui  $t0, 0x4000
lw   $t1, 0x10($t0)
addi $t2, $zero, 0x0
bne  $t1, $t2, tmp
addi $t1, $zero, 0xf
beq  $zero, $zero, tmp2
tmp:
addi $t1, $t1, -1
tmp2:
sw   $t1, 0x10($t0)

lw   $t1, 0x4($t0)
srl  $t1, $t1, 0x1
andi $t1, $t1, 0xffff
bne  $t1, $zero, tmp3
addi $t1, $zero, 0x8000
tmp3:
sw   $t1, 0x4($t0)

