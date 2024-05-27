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
; storage address of bootloader
mov bx, 0x7e00
load_bootloader: ; load sectors 1-5
    call asm_read_hard_disk_chs

jmp 0x0000:0x7e00
jmp $ ; infinite loop

; read the status of the disk (C/H/S)
asm_read_hard_disk_chs:
    mov al, 0x05 ; number of sectors to read 

    mov dl, 0x80 ; drive: 0x80 = 1st hard disk
    mov ch, 0x00 ; cylinder
    mov dh, 0x00 ; head
    mov cl, 0x02 ; sector

    mov ah, 0x02 ; function: read sectors
    int 0x13
ret

times 510 - ($ - $$) db 0
db 0x55, 0xaa
