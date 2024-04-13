org 0x7c00
[bits 16]
xor ax, ax ; eax = 0
; initialize stack, set all stack values to 0
mov ds, ax
mov ss, ax
mov es, ax
mov fs, ax
mov gs, ax

; initialize stack pointer
mov sp, 0x7c00
mov ax, 1 ; logical sector number 0~15 bits
mov cx, 0 ; logical sector number 16~31 bits
mov bx, 0x7e00 ; storage address of bootloader
load_bootloader:
    call asm_read_hard_disk ; read hard disk
    inc ax
    cmp ax, 5
    jle load_bootloader
jmp 0x0000:0x7e00 ; jump to the bootloader

jmp $ ; infinite loop

asm_read_hard_disk:
; read a sector from hard disk

; arguments:
; ax = logical sector number 0~15 bits
; cx = logical sector number 16~31 bits
; ds:bx = storage address

; return:
; bx = bx + 512

    mov dx, 0x1f3
    out dx, al ; LBA 7~0 bits

    inc dx ; 0x1f4
    mov al, ah
    out dx, al ; LBA 15~8 bits

    mov ax, cx

    inc dx ; 0x1f5
    out dx, al ; LBA 23~16 bits

    inc dx ; 0x1f6
    mov al, ah
    and al, 0x0f
    or al, 0xe0 ; LBA 27~24 bits
    out dx, al

    mov dx, 0x1f2
    mov al, 1 ; read 1 sector
    out dx, al

    mov dx, 0x1f7
    mov al, 0x20 ; read command
    out dx, al

.waits:
    ; wait for the hard disk to be ready
    in al, dx ; dx = 0x1f7
    and al, 0x88
    cmp al, 0x88
    jnz .waits

    ; read 512 bytes from the hard disk to ds:bx
    ; read 2 bytes each time, read 256 times
    mov cx, 256
    mov dx, 0x1f0 ; data port
.readw:
    in ax, dx
    mov [bx], ax
    add bx, 2
    loop .readw

    ret

times 510 - ($ - $$) db 0
db 0x55, 0xaa


