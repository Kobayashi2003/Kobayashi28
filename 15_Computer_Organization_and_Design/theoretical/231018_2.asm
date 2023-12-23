code segment
assume cs:code
begin:
    mov al, -1
    cmp al, 2   
    ja NEXT
    mov dl, '0'
    jmp EXIT
NEXT:
    mov dl, '1'
EXIT:
    mov ah, 2
    int 21h
    mov ah, 4ch
    int 21h
code ends
end begin