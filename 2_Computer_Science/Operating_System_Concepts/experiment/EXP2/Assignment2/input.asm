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

; get the current cursor position 
mov ah, 0x03
int 0x10

; read the keyboard, and output the character to the screen
read_key:
    ; read the key from the keyboard, and store it in al 
    mov ah, 0
    int 0x16

    cmp al, 0x0d ; check if the character is enter
    jz end_read_key 

    ; show the character in al on the screen
    mov ah, 0x0e
    mov al, al
    mov bh, 0
    mov bl, 0x07
    int 0x10
    jmp read_key
end_read_key:

jmp $ ; jump to current address (infinite loop)

times 510-($-$$) db 0  
db 0x55, 0xaa ; boot signature, meaning this is a bootable mbr
