data segment
   string db "Hello, World!", 0Ah, 0Dh, "$"
data ends

code segment 
assume cs:code, ds:data
start:
   mov ax, data
   mov ds, ax
   lea dx, string
   mov ah, 09h
   mov cx, 3

print_string:
   int 21h
   loop print_string

   mov ah, 4ch
   int 21h
code ends
end start