[bits 32]

global asm_hello_world

section .data
    message db '21312450 KOBAYASHI', 0  ; Define the message and a null terminator

section .text

asm_hello_world:
    pusha                       ; Push all general-purpose registers

    xor eax, eax                ; Clear EAX register
    mov ah, 0x03                ; Set attribute to cyan (foreground color)

    mov esi, message            ; Point ESI to the start of the message
    xor ecx, ecx                ; Zero ECX, will be used as index

print_char:
    lodsb                       ; Load byte at address ESI into AL, increment ESI
    test al, al                 ; Test if AL is zero (end of string)
    jz done                     ; If zero, jump to done

    shl ecx, 1                  ; Multiply index by 2 (word size offset for GS segment)
    mov [gs:ecx], ax            ; Move character and attribute to [GS:ECX]
    shr ecx, 1                  ; Divide index by 2 to restore it for next iteration
    inc ecx                     ; Increment index

    jmp print_char              ; Loop back to print next character

done:
    popa                        ; Pop all general-purpose registers
    ret                         ; Return from the function
