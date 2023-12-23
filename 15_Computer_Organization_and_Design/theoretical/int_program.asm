assume cs:code, ss:stack, ds:data

data segment
    ID_STR db '21312450 LinJunZhe', 0
    CRLF db 0dh, 0ah, '$'
data ends

stack segment
    dw 128 dup(?)
stack ends

code segment
main:

    mov ax, data
    mov ds, ax

    mov ax, stack
    mov ss, ax
    mov sp, 128

    mov ax, 0
    mov es, ax

    mov word ptr es:[50*4], offset INT_50
    mov word ptr es:[50*4+2], cs
    
    int 50

    mov ah, 9
    mov dx, offset ID_STR
    int 21h

    jmp EXIT

INT_50:
    ; clear screen
    push ax
    push bx
    push cx
    push dx
    push es
    pushf

    mov ax, 0b800h
    mov es, ax
    mov bx, 0
    mov cx, 80*24

s: mov word ptr es:[bx], 0
    add bx, 2
    loop s

INT_50_END:
    popf
    pop es
    pop dx
    pop cx
    pop bx
    pop ax
    iret

EXIT:
    mov ax, 4c00h
    int 21h

code ends
end main