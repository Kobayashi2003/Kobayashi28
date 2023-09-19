data segment
    string db "linjunzhe, 21312450!",0AH,0DH,"$"
data ends

code segment
    assume cs:code, ds:data
start:
    mov ax, data
    mov ds, ax
    lea dx, string
    mov ah, 9
    int 21h
    mov ah, 4ch
    int 21h
code ends
    end
