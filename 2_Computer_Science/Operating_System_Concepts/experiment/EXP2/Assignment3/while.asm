; load the value of a2 into ebx
mov ebx, [a2]

while_loop:
    ; if a2 < 12, end the loop
    cmp ebx, 12
    jl end_while_loop

    ; push and save ebx
    push ebx
    ; generate a random character and store it in al
    call my_random
    ; pop and restore ebx
    pop ebx

    ; read the value of char array pointer while_flag
    mov edx, [while_flag]
    ; calculate the address of the current character, 
    ; and store the random character in it
    mov [edx + ebx - 12], al

    dec ebx
    mov [a2], ebx
    
    jmp while_loop
end_while_loop:
