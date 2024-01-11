nop

add $s0, $zero, $zero # arr address  
add $s1, $zero, $zero # arr length 

addiu $s2, $zero, 0x00ff # not num flg

addiu $t0, $zero, 0x0010 # N = 16, i = 16

load_array:

addiu $t0, $t0, -1      # N--

addiu $v0, $zero, 2     # syscall input integer to $a0
syscall 

beq   $a0, $s2, not_num 

# if is efct num
sll   $t1, $s1, 2       # arr_len * 4
add   $t1, $t1, $s0     # arr_base + arr_len * 4
sw    $a0, 0($t1)       # store integer in array
addiu $s1, $s1, 1       # arr_len++

not_num:

beq   $t0, $zero, sort_arr
j     load_array

sort_arr:

addiu $t0, $zero, -1    # i = -1

loop1: 

addiu $t0, $t0, 1        # i++
beq   $t0, $s1, exit     #if i == n, exit
addiu $t1, $zero, -1     # j = -1

loop2:

addiu $t1, $t1, 1        # j++

# $t3 = n - 1 - i
addiu $t2, $s1, -1       # t2 = n - 1
subu  $t3, $t2, $t0      # t3 = n - 1 - i
beq   $t1, $t3, loop1    # if j == n - 1 - i, loop1

# $t4 = &arr[j]
sll   $t4, $t1, 2        # t4 = j * 4
add   $t4, $t4, $s0      # t4 = arr_base + j * 4
# $t5 = &arr[j + 1]
addiu $t5, $t4, 4        # t5 = t4 + 4

# $t6 = arr[j] 
lw    $t6, 0($t4)        # t6 = *t4
# $t7 = arr[j + 1]
lw    $t7, 0($t5)        # t7 = *t5

slt   $t8, $t7, $t6      # t8 = t7 < t6
beq   $t8, $zero, loop2  # if t7 >= t6, loop2

# swap
sw    $t6, 0($t5)        # arr[j + 1] = arr[j]
sw    $t7, 0($t4)        # arr[j] = arr[j + 1]

j     loop2

exit:

add $t0, $zero, $zero  # i = 0

output_array:

beq   $t0, $s1, end      # if i == n, end

sll  $t1, $t0, 2        # t1 = i * 4
add  $t1, $t1, $s0      # t1 = arr_base + i * 4
lw   $a0, 0($t1)        # a0 = arr[i]

addiu $v0, $zero, 1      # syscall output integer
syscall

addiu $t0, $t0, 1        # i++

j    output_array

end:

halt