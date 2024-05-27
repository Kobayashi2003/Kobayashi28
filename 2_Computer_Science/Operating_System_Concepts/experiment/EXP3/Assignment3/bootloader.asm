%include "boot.inc"
; org 0x7e00
[bits 16]

; Initialize Global Descriptor Table (GDT) entries
mov dword [GDT_START_ADDRESS+0x00], 0x00000000  ; Null descriptor
mov dword [GDT_START_ADDRESS+0x04], 0x00000000

mov dword [GDT_START_ADDRESS+0x08], 0x0000FFFF  ; Base=0, Limit=0xFFFFF (code segment)
mov dword [GDT_START_ADDRESS+0x0C], 0x00CF9200  ; Granularity=4KB, Code segment descriptor

mov dword [GDT_START_ADDRESS+0x10], 0x00000000  ; Base=0, Limit=0 (stack segment)
mov dword [GDT_START_ADDRESS+0x14], 0x00409600  ; Granularity=1 byte

mov dword [GDT_START_ADDRESS+0x18], 0x80007FFF  ; Base=0x000B8000, Limit=0x07FFF (video memory)
mov dword [GDT_START_ADDRESS+0x1C], 0x0040920B  ; Granularity=byte

mov dword [GDT_START_ADDRESS+0x20], 0x0000FFFF  ; Base=0, Limit=0xFFFFF (flat mode code segment)
mov dword [GDT_START_ADDRESS+0x24], 0x00CF9800  ; Granularity=4KB, Code segment descriptor

; Initialize GDTR
mov word [pgdt], 39
lgdt [pgdt]

; Enable A20 line
in al, 0x92
or al, 0x02
out 0x92, al

; Disable interrupts and set PE bit
cli
mov eax, cr0
or eax, 1
mov cr0, eax

; Jump to protected mode
jmp dword CODE_SELECTOR:protect_mode_begin

[bits 32]
protect_mode_begin:

; Define constants
_DR equ 1
_UR equ 2
_UL equ 3
_DL equ 4
delay equ 200
ddelay equ 100

; Start of code segment
START:
mov eax, DATA_SELECTOR
mov ds, eax
mov gs, eax
mov eax, STACK_SELECTOR
mov ss, eax
mov eax, VIDEO_SELECTOR
mov es, eax
mov esi, 0
mov edi, 0

; Print loop
PRINT:
    mov ebx, msg
    mov al, [ebx+esi]
    cmp al, 0
    jz LOOP
    mov ebx, 52
    mov byte [es:ebx+edi], al
    mov byte [es:ebx+edi+1], 1
    inc esi
    add edi, 2
    jmp PRINT

; Delay loop
LOOP:
    dec dword [count]
    jnz LOOP

    mov dword [count], delay
    dec dword [dcount]
    jnz LOOP

    mov dword [count], delay
    mov dword [dcount], ddelay

    mov al, 1
    cmp al, byte [rdul]
    jz DnRt

    mov al, 2
    cmp al, byte [rdul]
    jz UpRt

    mov al, 3
    cmp al, byte [rdul]
    jz UpLt

    mov al, 4
    cmp al, byte [rdul]
    jz DnLt

    jmp $

; Movement and collision detection logic for DnRt, UpRt, UpLt, DnLt

; Move Down-Right (DnRt)
DnRt:
    inc dword [x]
    inc dword [y]
    mov ebx, dword [x]
    mov eax, 25
    sub eax, ebx
    jz dr2ur  ; If at right boundary, change direction to Up-Right

    mov ebx, dword [y]
    mov eax, 80
    sub eax, ebx
    jz dr2dl  ; If at bottom boundary, change direction to Down-Left

    jmp show

dr2ur:
    mov dword [x], 23
    mov byte [rdul], _UR
    jmp show

dr2dl:
    mov dword [y], 78
    mov byte [rdul], _DL
    jmp show

; Move Up-Right (UpRt)
UpRt:
    dec dword [x]
    inc dword [y]
    mov ebx, dword [y]
    mov eax, 80
    sub eax, ebx
    jz ur2ul  ; If at top boundary, change direction to Up-Left

    mov ebx, dword [x]
    mov eax, 0
    sub eax, ebx
    jz ur2dr  ; If at right boundary, change direction to Down-Right

    jmp show

ur2ul:
    mov dword [y], 78
    mov byte [rdul], _UL
    jmp show

ur2dr:
    mov dword [x], 1
    mov byte [rdul], _DR
    jmp show

; Move Up-Left (UpLt)
UpLt:
    dec dword [x]
    dec dword [y]
    mov ebx, dword [x]
    mov eax, 0
    sub eax, ebx
    jz ul2dl  ; If at left boundary, change direction to Down-Left

    mov ebx, dword [y]
    mov eax, 0
    sub eax, ebx
    jz ul2ur  ; If at top boundary, change direction to Up-Right

    jmp show

ul2dl:
    mov dword [x], 1
    mov byte [rdul], _DL
    jmp show

ul2ur:
    mov dword [y], 1
    mov byte [rdul], _UR
    jmp show

; Move Down-Left (DnLt)
DnLt:
    inc dword [x]
    dec dword [y]
    mov ebx, dword [y]
    mov eax, 0
    sub eax, ebx
    jz dl2dr  ; If at bottom boundary, change direction to Down-Right

    mov ebx, dword [x]
    mov eax, 25
    sub eax, ebx
    jz dl2ul  ; If at left boundary, change direction to Up-Left

    jmp show

dl2dr:
    mov dword [y], 1
    mov byte [rdul], _DR
    jmp show

dl2ul:
    mov dword [x], 23
    mov byte [rdul], _UL
    jmp show

; Show character on screen
show:
    xor eax, eax
    mov eax, dword [x]
    mov ebx, 80
    mul ebx
    add eax, dword [y]
    mov ebx, 2
    mul ebx
    mov ebx, eax
    mov ah, byte [color]
    mov al, byte [char]
    mov [es:ebx], eax

    inc byte [char]
    cmp byte [char], 'z' + 1
    jnz keep
    mov byte [char], '0'

keep:
    inc byte [color]
    cmp byte [color], 0x10
    jnz LOOP
    mov byte [color], 0x40
    jmp LOOP

end:
    jmp $

; Data definitions
count dd delay
dcount dd ddelay
rdul db _DR
color db 0x02
x dd 0
y dd 0
char db 'A'
msg db 'KOBAYASHI', 0

pgdt dw 0
dd GDT_START_ADDRESS
