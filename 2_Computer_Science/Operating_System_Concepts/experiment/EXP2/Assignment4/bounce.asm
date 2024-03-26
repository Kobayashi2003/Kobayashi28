org 0x7c00
[bits 16]
; initialize segments
xor ax, ax 
mov ds, ax
mov ss, ax
mov es, ax
mov fs, ax
mov gs, ax

; set stack pointer
mov sp, 0x7c00
mov ax, 0xb800
mov gs, ax

; set cursor position to (2,0)
mov ah, 0x02
mov bh, 0x00
mov dh, 0x02
mov dl, 0x00
int 0x10

; the screen size is 80*25

; I use bl to save the color and the direction at the same time
; 0x01: right up, blue
; 0x02: right down, green
; 0x04: left up, red
; 0x08: left down, yellow

mov bl, 0x02 ; the initial direction is right down

move_loop:
    ; judge the current direction 
    ; and choose the next move
    cmp bl, 0x01
    je move_right_up
    cmp bl, 0x02
    je move_right_down
    cmp bl, 0x04
    je move_left_up
    cmp bl, 0x08
    je move_left_down

move_right_up:
    ; judge if the cursor is at the end of top
    cmp dh, 0x00
    je change_right_down
    ; judge if the cursor is at the end of right
    cmp dl, 0x50
    je change_left_up
    ; move
    mov ah, 0x02
    inc dl
    dec dh
    int 0x10
    jmp move_next

move_right_down:
    ; judge if the cursor is at the end of bottom
    cmp dh, 0x18
    je change_right_up
    ; judge if the cursor is at the end of right 
    cmp dl, 0x50
    je change_left_down
    ; move
    mov ah, 0x02
    inc dl
    inc dh
    int 0x10
    jmp move_next

move_left_up:
    ; judge if the cursor is at the end of top  
    cmp dh, 0x00
    je change_left_down
    ;  judge if the cursor is at the end of left
    cmp dl, 0x00
    je change_right_up
    ; move 
    mov ah, 0x02
    dec dl
    dec dh
    int 0x10
    jmp move_next

move_left_down:
    ; judge if the cursor is at the end of bottom 
    cmp dh, 0x18
    je change_left_up
    ; judge if the cursor is at the end of left 
    cmp dl, 0x00
    je change_right_down
    ; move 
    mov ah, 0x02
    dec dl
    inc dh
    int 0x10
    jmp move_next

move_next:
    ; show the path 
    mov ah, 0x09
    mov al, 'X'
    mov cx, 0x01
    int 0x10

    ; delay 
    push cx
    push dx
    call delay
    pop dx
    pop cx

    jmp move_loop

jmp $ ; jump to current address (infinite loop)

; delay function
delay:
    mov cx, 0x0ff
delay_loop1:
    mov dx, 0x0ffff
delay_loop2:
    dec dx
    jnz delay_loop2
    dec cx
    jnz delay_loop1
    ret

; change direction
change_right_down:
    mov bl, 0x02
    jmp move_right_down
change_left_up:
    mov bl, 0x04
    jmp move_left_up
change_left_down:
    mov bl, 0x08
    jmp move_left_down
change_right_up:
    mov bl, 0x01
    jmp move_right_up

times 510-($-$$) db 0  
db 0x55, 0xaa ; boot signature, meaning this is a bootable mbr
