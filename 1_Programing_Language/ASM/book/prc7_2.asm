assume cs:codesg, ds:datasg
datasg segment
    string1 db 'BaSic', 0dh, 0ah, '$'
    string2 db 'iNfOrMatiOn', 0dh, 0ah, '$'
datasg ends

codesg segment
start:
    mov ax, datasg
    mov ds, ax
    mov bx, 0
    mov cx, 5
s:  mov al, [bx]
    and al, 11011111b
    mov [bx], al
    inc bx
    loop s 

    mov bx, 7
    mov cx, 11
s0: mov al, [bx]
    or al, 00100000b
    mov [bx], al
    inc bx
    loop s0

    lea dx, string1
    mov ah, 09h
    int 21h

    lea dx, string2
    mov ah, 09h
    int 21h

    mov ah, 4ch
    int 21h
codesg ends
end start