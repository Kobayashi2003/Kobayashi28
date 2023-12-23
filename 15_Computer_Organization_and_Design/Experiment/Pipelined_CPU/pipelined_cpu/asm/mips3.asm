lui  $t0, 0x4000
lw   $t1, 0x14($t0)
xori $t1, $t1, 1
sw   $t1, 0x14($t0)
