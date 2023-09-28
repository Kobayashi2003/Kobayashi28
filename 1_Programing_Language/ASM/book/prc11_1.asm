add128:
    push ax
    push cx
    push si
    push di
    sub ax, ax ; clear CF
    mov cx, 8
s:
    mov ax, [si]
    abc ax, [di]
    mov [si], ax
    inc si
    inc si
    inc di
    inc di
    loop s
    pop di
    pop si
    pop cx
    pop ax
    ret