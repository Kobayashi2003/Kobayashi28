assume ds:datasg, cs:codesg
datasg segment
    string1 db 'HelloWorld',0dh,0ah,'$'
    string2 db 'HelloWorld',0dh,0ah,'$'
datasg ends
codesg segment
start:
    mov ax, datasg
    mov ds, ax
    mov bx, 0
    mov cx, 10
s:  mov al, [bx]
    and al, 11011111b
    mov [bx], al

    mov al, [bx+12]
    or al, 00100000b
    mov [bx+12], al

    inc bx
    loop s

    mov ah, 09h
    lea dx, string1
    int 21h

    mov ah, 09h
    lea dx, string2
    int 21h

    mov ah, 4ch
    int 21h
codesg ends 
end start