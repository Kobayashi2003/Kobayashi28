assume cs:codesg
codesg segment
    dw 0123H, 0456H, 0789H, 0ABCH, 0DEFH, 0FEDH, 0CBAH, 0987H
    dw 0, 0, 0, 0, 0, 0, 0, 0

start:
    mov ax, cs
    mov ss, ax
    mov sp, 32
    mov bx, 0
    mov cx, 8
s:  push cs:[bx]
    add bx, 2
    loop s
    mov bx, 0
    mov cx, 8
s0: pop cs:[bx]
    add bx, 2
    loop s0
    mov ax, 4C00H
    int 21H
codesg ends
end start
