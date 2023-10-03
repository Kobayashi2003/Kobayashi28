assume cs:code
data segment
    db 'Welcome to masm!'
    db 16 dup(0)
    db 0dh, 0ah, '$'
data ends

code segment
start:
    mov ax, data
    mov ds, ax
    mov es, ax

    mov si, 0
    mov di, 16
    mov cx, 16
    cld
    rep movsb

    mov ah, 9
    mov dx, 0
    int 21h

    mov ah, 4ch
    int 21h

code ends
end start