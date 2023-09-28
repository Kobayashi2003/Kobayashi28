assume cs:codesg
stacksg segment
    db 8 dup (0)
    db 8 dup (0)
stacksg ends

codesg segment
start:
    mov ax, stack
    mov ss, ax
    mov sp, 16
    mov ax, 1000
    call s
    mov ax, 4c00h
    int 21h

s:
    add ax, ax
    ret

codesg ends
end start