assume cs:code
code segment
start:
    mov ax, 0b800h
    mov es, ax
    mov byte ptr es:[12*160+40*2], '!'

    mov ax, 4c00h
    int 21h
code ends
end start
