org 0x7c00 ; origin, the start of the boot sector
[bits 16]

msg db '21312450', 0 ; the string to be output

xor ax, ax ; clear ax
; initialize segments
mov ds, ax
mov ss, ax
mov es, ax
mov fs, ax
mov gs, ax

; set stack pointer
mov sp, 0x7c00
mov ax, 0xb800
mov gs, ax

; init cursor position
mov bh, 0x00 ; page number
mov dh, 0x0c ; row
mov dl, 0x0c ; column

; set cursor position
mov ah, 0x02
int 0x10

; set output attributes
mov bl, 0x14 ; blue color
mov cx, 0x01 ; print one character at a time

mov si, msg ; load the address of the string into si

print_string:
    mov al, [si] ; load the character into al
    or al, al ; check if al is 0
    jz end_print_string ; if al is 0, jump to halt

    mov ah, 0x09 ; print character
    int 0x10 ; call video interrupt

    mov ah, 0x02 ; move cursor to next position
    inc dl ; increment column
    int 0x10 ; call video interrupt

    inc si ; move to next character

    jmp print_string ; repeat the process
end_print_string:

jmp $ ; jump to current address (infinite loop)

; times, an assembly pseudo-instruction, used to repeat the specified number of operations
; $ is the current address, $$ is the start of the current section
; fill the rest of the sector with 0s
times 510-($-$$) db 0  
db 0x55, 0xaa ; boot signature, meaning this is a bootable mbr
