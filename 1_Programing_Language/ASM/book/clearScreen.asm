assume cs:code
code segment
start:
    call clearScreen

    mov ax, 4c00h
    int 21h

clearScreen:
    push ax
    push bx
    push cx
    pushf

    mov ax, 0b800h
    mov es, ax
    mov bx, 0
    mov cx, 80*25
s:  mov word ptr es:[bx], 0
    add bx, 2
    loop s

    popf
    pop cx
    pop bx
    pop ax
    ret

code ends
end start