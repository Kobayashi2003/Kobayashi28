asm_read_hard_disk:
; read a logical block from the hard disk

; arguments:
; ax = logical block number 0~15 bit
; cx = logical block number 16~27 bit
; ds:bx = the address to save the data read from the hard disk

; return:
; bx = bx + 512

; 7~0 bit of LBA
mov dx, 0x1f3
out dx, al

; 15~8 bit of LBA
inc dx
mov al, ah
out dx, al

mov ax, cx

; 23~16 bit of LBA
inc dx
out dx, al

; 27~24 bit of LBA, 
; 0xe0 means the hard disk is master, and use LBA mode
inc dx
mov al, ah
and al, 0x0f
or  al, 0xe0
out dx, al

; the number of sectors to read should be written to 0x1f2
mov dx, 0x1f2
mov al, 1
out dx, al

; write 0x20 to 0x1f7 to tell the hard disk to read
mov dx, 0x1f7
mov al, 0x20
out dx, al

; we can get the disk status from 0x1f7
; 7 bit : 1 means the hard disk is busy
; 3 bit : 1 means the hard disk is ready
; 0 bit : 1 means there is an error when executing last command
.waits:
in al, dx
and al, 0x88
cmp al, 0x08
jnz .waits

; read the data from the hard disk, 0x1f0 is the data port
mov cx, 256
mov dx, 0x1f0
.readw:
in  ax, dx
mov [bx], ax
add bx, 2
loop .readw

ret
