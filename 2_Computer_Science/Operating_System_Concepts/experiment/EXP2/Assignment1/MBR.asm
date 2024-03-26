org 0x7c00
[bits 16]
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

mov ah, 0x01 ; blue
mov al, 'H'
mov [gs:2*0], ax

mov al, 'e'
mov [gs:2*1], ax

mov al, 'l'
mov [gs:2*2], ax

mov al, 'l'
mov [gs:2*3], ax

mov al, 'o'
mov [gs:2*4], ax

mov al, ' '
mov [gs:2*5], ax

mov al, 'W'
mov [gs:2*6], ax

mov al, 'o'
mov [gs:2*7], ax

mov al, 'r'
mov [gs:2*8], ax

mov al, 'l'
mov [gs:2*9], ax

mov al, 'd'
mov [gs:2*10], ax

jmp $ ; jump to current address (infinite loop)

; times, an assembly pseudo-instruction, used to repeat the specified number of operations
; $ is the current address, $$ is the start of the current section
; fill the rest of the sector with 0s
times 510-($-$$) db 0  
db 0x55, 0xaa ; boot signature, meaning this is a bootable mbr
