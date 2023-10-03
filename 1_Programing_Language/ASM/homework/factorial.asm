assume cs:code, ds:data
data segment
    n dw 3
data ends
code segment
main:
    mov ax, data
    mov ds, ax

fact:
    mov ax, 1
    mov cx, [n]
fact_loop:
    mul cx
    loop fact_loop
    mov ah, 4ch
    int 21h

code ends
end main