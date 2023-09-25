assume cs:codesg, ds:datasg
datasg segment
    db 'ibm             '
    db 'dec             '
    db 'dos             '
    db 'vax             '
    dw 0
datasg ends
codesg segment
  start:
    mov ax, datasg
    mov ds, ax
    mov bx, 0
    mov cx, 4
  s0:
    mov ds:[40H], cx
    mov si, 0
    mov cx, 3
  s: 
    mov al, [bx+si]
    and al, 11011111b
    mov [bx+si], al
    inc si

    loop s

    add bx, 16
    mov cx, ds:[40H]
    loop s0

    int 3

    mov ax, 4c00h
    int 21h

codesg ends
  end start