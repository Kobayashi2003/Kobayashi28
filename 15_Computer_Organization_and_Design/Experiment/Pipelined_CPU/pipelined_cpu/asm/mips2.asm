lui  $t0, 0x4000
lw   $t1, 0x10($t0)
lw   $t2, 0x08($t0)
sll  $t1, $t1, 2
add  $t1, $t1, $t0
sw   $t2, 0x18($t1)
