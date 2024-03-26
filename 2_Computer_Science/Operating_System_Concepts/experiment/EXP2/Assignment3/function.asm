mov eax, 0 ; i = 0
mov ebx, [your_string]

print_loop:
    movzx ecx, byte [ebx + eax]
    test ecx, ecx
    jz end_print_loop 

    push eax
    push ebx
    push ecx ; the argument to print_a_char
    call print_a_char
    pop ecx
    pop ebx
    pop eax

    inc eax
    jmp print_loop
end_print_loop: