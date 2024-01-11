# (C code)
# void bubble_sort(int arr[], int n) {
#     int i, j;
# 
#     // loop1
#     for (i = 0; i < n; ++i) {
#         // loop2
#         for (j = 0; j < n - 1 - i; ++j ) {
#             if (arr[j] > arr[j + 1]) {
#                 arr[j] = arr[j] + arr[j + 1];
#                 arr[j + 1] = arr[j] - arr[j + 1];
#                 arr[j] = arr[j] - arr[j + 1];  
#             }
#         }
#     }
# 
#     for (i = 0; i < n; ++i) {
#         ShowInt(arr[i]);
#     }
# }

# mips bubble sort
.data

arr : .word 5, 4, 3, 2, 1
n   : .word 5

.text

main:

    la $s0, arr # $s0 = &arr[0]
    lw $s1, n   # $s1 = n

    addi $t0, $zero, -1 # i = -1

loop1:

    addi $t0, $t0, 1 # i = i + 1
    beq $t0, $s1, exit # if i == n, exit
    addi $t1, $zero, -1 # j = -1

loop2:

    addi $t1, $t1, 1 # j = j + 1

    # $t3 = n - 1 - i
    addi $t2, $s1, -1 # $t2 = n - 1
    sub $t3, $t2, $t0 # $t3 = n - 1 - i
    ble $t3, $t1, loop1 # if n - 1 - i <= j, loop1

    # $t4 = &arr[j]
    sll $t4, $t1, 2 # $t4 = j * 4
    add $t4, $t4, $s0 # $t4 = &arr[j]
    # $t5 = &arr[j + 1]
    addi $t3, $t1, 1 # $t3 = j + 1
    sll $t3, $t3, 2 # $t3 = (j + 1) * 4
    add $t5, $t3, $s0 # $t5 = &arr[j + 1]

    lw $t6, 0($t4) # $t6 = arr[j]
    lw $t7, 0($t5) # $t7 = arr[j + 1]

    bgt $t6, $t7, swap # if arr[j] > arr[j + 1], swap

    j loop2

swap:
    sw $t6, 0($t5) # arr[j + 1] = arr[j]
    sw $t7, 0($t4) # arr[j] = arr[j + 1]

    j loop2

exit:
    li $v0, 10
    syscall