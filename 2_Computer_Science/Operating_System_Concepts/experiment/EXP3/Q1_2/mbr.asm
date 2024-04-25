; read 5 sectors from disk to memory by CHS
; and jump to the bootloaded code
org 0x7c00
[bits 16]
xor ax, ax ; eax = 0
; initialize stack, set all stack values to 0
mov ds, ax
mov ss, ax
mov es, ax
mov fs, ax
mov gs, ax

; set stack pointer to 0x7c00
mov sp, 0x7c00

; read the status of the disk



times 510 - ($ - $$) db 0
db 0x55, 0xaa
