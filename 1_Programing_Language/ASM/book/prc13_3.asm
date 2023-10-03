assume cs:code
data segment
    string db 'conversation', 0
    endsign db 0dh, 0ah, '$'
data ends

code segment
start:

    mov ax, cs
    mov ds, ax
    mov si, offset capital
    mov ax, 0
    mov es, ax
    mov di, 200h
    mov cx, offset capitalend-offset capital
    cld
    rep movsb

    mov ax, 0
    mov es, ax
    mov word ptr es:[7ch*4], 200h
    mov word ptr es:[7ch*4+2], 0


main:
    mov ax, data
    mov ds, ax
    mov si, 0
    int 7ch

    mov ah, 9
    mov dx, offset string
    int 21h

    mov ax, 4c00h
    int 21h


capital:
    push cx
    push si
change:
    mov cl, [si]
    mov ch, 0
    jcxz ok
    and byte ptr [si], 11011111b
    inc si
    jmp short change
ok:
    pop si
    pop cx
    iret
capitalend:
    nop

code ends
end start