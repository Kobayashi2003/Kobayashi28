assume cs:code
data segment
    db 8, 11, 8, 1, 8, 5, 63, 38
data ends

code segment
start:
    mov ax, data
    mov ds, ax

    mov ax, 0
    mov bx, 0

    mov cx, 8
s:
    cmp byte ptr [bx], 8
    je ok
    jmp short next
ok:
    inc ax
next:
    inc bx
    loop s

    int 3

    mov ah, 4ch
    int 21h

code ends
end start