assume cs:code, ds:data, es:extra

DATA SEGMENT 
string db 'ADRAdfghtGHgff'
count equ $-string
DATA ENDS 

EXTRA SEGMENT 
dest db count dup (?)
EXTRA ENDS 

CODE SEGMENT
begin:

    mov ax, data
    mov ds, ax
    mov ax, extra
    mov es, ax

    mov cx, count
    lea si, string
    lea di, dest
    cld

again:
    lodsb
    and al, 0DFH
    stosb
    loop again

    mov ah, 4CH
    int 21H
CODE ENDS
end begin