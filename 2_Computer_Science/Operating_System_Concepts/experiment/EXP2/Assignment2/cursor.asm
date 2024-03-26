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

; press h, j, k, l to move the cursor
; press q to quit
read_key:

; write down a 'X' 
mov ah, 0x09
mov al, 'X'
mov bh, 0
mov bl, 0x14
mov cx, 1
int 0x10

mov ah, 0
int 0x16
cmp al, 'h'
je move_left
cmp al, 'j'
je move_down
cmp al, 'k'
je move_up
cmp al, 'l'
je move_right
cmp al, 'q'
je quit
jmp read_key

move_left:
mov ah, 0x02
int 0x10
sub dl, 1
mov ah, 0x0c
int 0x10
jmp read_key

move_down:
mov ah, 0x02
int 0x10
add dh, 1
mov ah, 0x0c
int 0x10
jmp read_key

move_up:
mov ah, 0x02
int 0x10
sub dh, 1
mov ah, 0x0c
int 0x10
jmp read_key

move_right:
mov ah, 0x02
int 0x10
add dl, 1
mov ah, 0x0c
int 0x10
jmp read_key

quit:

jmp $ ; jump to current address (infinite loop)

; times, an assembly pseudo-instruction, used to repeat the specified number of operations
; $ is the current address, $$ is the start of the current section
; fill the rest of the sector with 0s
times 510-($-$$) db 0  
db 0x55, 0xaa ; boot signature, meaning this is a bootable mbr
