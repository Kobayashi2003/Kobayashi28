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

mov ah, 0x14 ; red on blue

mov al, '2'
mov [gs:0x0a*160+0x0c*2], ax
mov al, '1'
mov [gs:0x0a*160+0x0d*2], ax
mov al, '3'
mov [gs:0x0a*160+0x0e*2], ax
mov al, '1'
mov [gs:0x0a*160+0x0f*2], ax
mov al, '2'
mov [gs:0x0a*160+0x10*2], ax
mov al, '4'
mov [gs:0x0a*160+0x11*2], ax
mov al, '5'
mov [gs:0x0a*160+0x12*2], ax
mov al, '0'
mov [gs:0x0a*160+0x13*2], ax

jmp $ ; jump to current address (infinite loop)

; times, an assembly pseudo-instruction, used to repeat the specified number of operations
; $ is the current address, $$ is the start of the current section
; fill the rest of the sector with 0s
times 510-($-$$) db 0  
db 0x55, 0xaa ; boot signature, meaning this is a bootable mbr
