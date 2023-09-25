assume cs:code
code segment
    dw 0123H, 0456H, 0789H, 0ABCH, 0DEFH, 0F12H, 0F45H, 0F78H
start:
    mov bx, 0
    mov ax, 0
    mov cx, 8
s:  add ax, cs:[bx]
    add bx, 2
    loop s
    mov ax, 4c00H
    int 21H
code ends
end start