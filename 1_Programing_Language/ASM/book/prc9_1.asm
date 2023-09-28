assume cs:codesg
codesg segment
start:
    mov ax, 0
    jmp short start
    add short s
s:
    inc ax
codesg ends
end start