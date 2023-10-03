assume cs:code, ds:data
data segment
    string db 256 dup(0)
data ends

code segment

start:
    mov ax, data
    mov ds, ax

    call getstr

    mov ah, 4ch
    int 21h

getstr:
    push ax
getstrs:
    mov ah, 0
    int 16h

    cmp al, 20h
    jb nochar   ; ASCII less than 0, no character
    mov ah, 0
    call charstack  ; push the character
    mov ah, 2
    call charstack  ; show the character
    jmp getstrs
nochar:
    cmp ah, 0eh ; backspace
    je backspace
    cmp ah, 1ch ; enter
    je enter
    jmp getstrs
backspace:
    mov ah, 1
    call charstack  ; pop the character
    mov ah, 2
    call charstack  ; show the character
    jmp getstrs
enter:
    mov al, 0
    mov ah, 0
    call charstack  ; push the 0 in the end of string
    mov ah, 2
    call charstack  ; show the character
    pop ax
    ret


; ah: function code (0=push, 1=pop, 2=show)
; ds:si points to the character stack
; fc 0: (al) = the character pushed
; fc 1: (al) = the character popped
; fc 2: (dh), (dl) = the line and column of the position to show
charstack:
    jmp short charstart

    table   dw charpush, charpop, charshow
    top     dw 0    ; top of stack

charstart:
    push bx
    push dx
    push di
    push es

    cmp ah, 2
    ja sret
    mov bl, ah
    mov bh, 0
    add bx, bx
    jmp word ptr [table+bx]
charpush:
    mov bx, top
    mov [si][bx], al
    inc top
    jmp sret
charpop:
    cmp top, 0
    je sret
    dec top
    mov bx, top
    mov al, [si][bx]
    jmp sret
charshow:
    mov bx, 0b800h
    mov es, bx
    mov al, 160
    mov ah, 0
    mul dh
    mov di, ax
    add dl, dl
    mov ah, 0
    add di, dx

    mov bx, 0
charshows:
    cmp bx, top
    jne noempty
    mov byte ptr es:[di], ' '
    jmp sret
noempty:
    mov al, [si][bx]
    mov es:[di], al
    mov byte ptr es:[di+2], ' '
    inc bx
    add di, 2
    jmp charshows
sret:
    pop es
    pop di
    pop dx
    pop bx
    ret

code ends
end start