%include "boot.inc"
; org 0x7e00
[bits 16]


mov dword [GDT_START_ADDRESS+0x00],0x00
mov dword [GDT_START_ADDRESS+0x04],0x00  

mov dword [GDT_START_ADDRESS+0x08],0x0000ffff    ; 基地址为0，段界限为0xFFFFF
mov dword [GDT_START_ADDRESS+0x0c],0x00cf9200    ; 粒度为4KB，存储器段描述符 

;建立保护模式下的堆栈段描述符       
mov dword [GDT_START_ADDRESS+0x10],0x00000000    ; 基地址为0x00000000，界限0x0 
mov dword [GDT_START_ADDRESS+0x14],0x00409600    ; 粒度为1个字节

;建立保护模式下的显存描述符    
mov dword [GDT_START_ADDRESS+0x18],0x80007fff    ; 基地址为0x000B8000，界限0x07FFF 
mov dword [GDT_START_ADDRESS+0x1c],0x0040920b    ; 粒度为字节

;创建保护模式下平坦模式代码段描述符
mov dword [GDT_START_ADDRESS+0x20],0x0000ffff    ; 基地址为0，段界限为0xFFFFF
mov dword [GDT_START_ADDRESS+0x24],0x00cf9800    ; 粒度为4kb，代码段描述符 

;初始化描述符表寄存器GDTR
mov word [pgdt], 39       ;描述符表的界限    
lgdt [pgdt]
       
in al,0x92                           ;南桥芯片内的端口 
or al,0000_0010B
out 0x92,al                          ;打开A20

cli                                  ;中断机制尚未工作
mov eax,cr0
or eax,1
mov cr0,eax                          ;设置PE位
       
;以下进入保护模式
jmp dword CODE_SELECTOR:protect_mode_begin

;16位的描述符选择子：32位偏移
;清流水线并串行化处理器
[bits 32]            
protect_mode_begin:                                

;定义各个符号
    _DR equ 1
    _UR equ 2
    _UL equ 3
    _DL equ 4
    delay equ 200
    ddelay equ 100
    
;代码段
;初始化各个寄存器
START:

mov eax, DATA_SELECTOR
mov ds, eax
mov gs, eax
mov eax, STACK_SELECTOR
mov ss, eax
mov eax, VIDEO_SELECTOR
mov es, eax

; mov ecx,0
; mov eax,0
; _init_:
;     cmp ecx,0x00007FFF
;     je _loop
    ; mov dword[gs:ecx], eax
;     add ecx,1
;     jmp _init_
; _loop:
; mov ebx,2
; mov ecx,0
; mov esi,1        ;offset
; mov edi,1        ;offset
; ; dead loop
; ;initilizing the start_point
;     mov ax, cs
;     mov es, ax
;     mov ds, ax
;     mov ax, 0b800h
;     mov es, ax
    mov esi, 0
    mov edi, 0

; 输出学号姓名
PRINT:    mov ebx, name
    mov al, [ebx+esi]
    cmp al, 0
    jz LOOP1    
    mov ebx, 52
    mov byte[es:ebx+edi], al    
    mov byte[es:ebx+edi+1], 1
    inc esi
    add edi, 2
    jmp PRINT

;循环实现延迟
LOOP1:
    dec dword[count]
    jnz LOOP1
    
    mov dword[count], delay
    dec dword[dcount]
    jnz LOOP1
    
    mov dword[count], delay
    mov dword[dcount], ddelay
    
    mov al,1
        cmp al, byte[rdul]
    jz DnRt 
       
    mov al, 2
           cmp al, byte[rdul]
    jz UpRt

           mov al, 3
           cmp al, byte[rdul]
    jz UpLt
       
    mov al, 4
           cmp al, byte[rdul]
    jz  DnLt

    jmp $

;往右下移动，判断是否碰壁并显示字符
DnRt:
    inc dword[x]
    inc dword[y]
    mov ebx, dword[x]
    mov eax, 25
    sub eax, ebx
          jz  dr2ur
    
    mov ebx, dword[y]
    mov eax, ebx
           jz  dr2dl
    
    jmp show

dr2ur:
           mov dword[x], 23
           mov byte[rdul], _UR    
           jmp show
dr2dl:
           mov dword[y], 78
          mov byte[rdul], _DL    
           jmp show

;往右上移动，判断是否碰壁并显示字符
UpRt:
    dec dword[x]
    inc dword[y]
    mov ebx, dword[y]
    mov eax, 80
    sub eax, ebx
           jz  ur2ul
    
    mov ebx, dword[x]
    mov eax, 0
    sub eax, ebx
          jz  ur2dr
    
    jmp show

ur2ul:
           mov dword[y], 78
           mov byte[rdul], _UL    
           jmp show
ur2dr:
           mov dword[x], 1
           mov byte[rdul], _DR    
           jmp show
    
;往左上移动，判断是否碰壁并显示字符
UpLt:
    dec dword[x]
    dec dword[y]
    mov ebx, dword[x]
    mov eax, 0
    sub eax, ebx
           jz  ul2dl

    mov ebx,dword[y]
    mov eax, -1
    sub eax, ebx
          jz  ul2ur
    
    jmp show

ul2dl:
           mov dword[x], 1
           mov byte[rdul], _DL    
           jmp show
ul2ur:
           mov dword[y], 1
           mov byte[rdul], _UR    
           jmp show

;往左下移动，判断是否碰壁并显示字符
DnLt:
    inc dword[x]
    dec dword[y]
    mov ebx, dword[y]
    mov eax, -1
    sub eax, ebx
           jz  dl2dr
    
    mov ebx, dword[x]
    mov eax, 25
    sub eax, ebx
           jz  dl2ul
    
    jmp show

dl2dr:
           mov dword[y], 1
           mov byte[rdul], _DR    
           jmp show
dl2ul:
           mov dword[x], 23
          mov byte[rdul], _UL    
           jmp show

;在屏幕上显示字符
show:    
    xor eax, eax                  ; 计算显存地址
    mov eax, dword[x]
    mov ebx, 80
    mul ebx
    add eax, dword[y]
    mov ebx, 2
    mul ebx
    mov ebx, eax
    mov ah, byte[color]    ;  0000：黑底、1111：亮白字（默认值为0x07）
    mov al, byte[char]    ;  AL = 显示字符值（默认值为20h=空格符）
    mov [es:ebx], eax       ;  显示字符的ASCII码值
    
    inc byte[char]
    cmp byte[char], 'z'+1
    jnz keep
    mov byte[char], '0'

keep:    
    inc byte[color]
    cmp byte[color], 0x10
    jnz LOOP1
    mov byte[color], 0x40 ;    循环显示不同样式的字符
    jmp LOOP1

end:
    jmp $

;数据定义
    count dd delay        ;一层延迟
    dcount dd ddelay    ;二层延迟
    rdul db _DR             ;方向变量
    color db 0x02        ;样式（颜色）变量
    x dd 0                 ;横坐标
    y dd 0                 ;纵坐标
    char db 'A'             ;要显示的字符
    name db '19335025 CYH', 0    ;学号姓名

    ; times 510-($-$$) db 0
    ; dw 0aa55h


pgdt dw 0
     dd GDT_START_ADDRESS