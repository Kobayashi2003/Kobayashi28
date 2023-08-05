data segment
xlist db 46,3,69,156,2,99,6,32,5,251
ylist db 9,1,5,65,2,34,6,4,0,9
operations db 1,0,0,1,1,1,0,1,0,0 ; 0:add, 1:sub
line db 0dh,0ah,'$'
data ends

code segment
assume cs:code,ds:data

begin:
    ; set data segment
    mov ax,data
    mov ds,ax

    mov cx,10   ; number of elements in xlist and ylist
    xor si,si   ; clear si
calculate:

    ; mov x to al
    xor ax,ax   ; clear ax
    lea bx,xlist
    mov al,[bx+si]
    call print_decimal  ; print x

    ; mov y to dl
    xor dx,dx   ; clear dx
    lea bx,ylist
    mov dl,[bx+si]
    push dx         ; save y

    ; get operation
    lea bx,operations
    mov dh,[bx+si]    ; dh = operation
    int 3
    mov dl,'+'
    cmp dh,0

    jnz plus
    pop dx  ; restore y
    mov dh,1
    neg dl  ; when operation is sub, negate y
    push dx ; save y
    mov dl,'-'
    int 3
plus:
    ; print '+' or '-'
    push ax
    mov ah,2
    int 21h
    pop ax

    ; print y
    pop dx  ; restore y, dx = y
    push ax ; save x
    mov ax,dx   ; ax = y
    cmp ah,0
    jz @n
    neg al
@n:
    call print_decimal
    pop ax  ; restore x

    ; print '='
    push dx
    push ax
    mov dl,'='
    mov ah,2
    int 21h
    pop ax
    pop dx

    ; calculate z
    add al,dl
    call print_decimal  ; print z

    ; line feed
    lea dx,line
    mov ah,9
    int 21h

    ; next element
    inc si  
    loop calculate

    ; exit
    mov ah,4ch
    int 21h

; Name: print_decimal
; Input: al - the value to print
; Output: the value in al printed in decimal
print_decimal:
    push ax     ; save ax
    push bx     ; save bx
    push cx     ; save cx
    push dx     ; save dx
    xor cx,cx   ; clear cx
    xor dl,dl   ; clear dl
    mov bl,10   ; set base to 10

    @d:
        inc cx      ; increment cx
        and ah,0    ; clear ah
        div bl      ; divide by 10
        push ax     ; push the remainder and quotient
        cmp al,0    ; check if quotient is 0
        jne @d      ; if not, go to @d

    print:
        pop dx      ; pop the remainder and quotient
        ; move the remainder to dl
        push cx     ; push the number of digits
        mov cx,8
        shr dx,cl
        pop cx      ; pop the number of digits
        or dl,30h   ; convert to ascii
        ; call print_char
        mov ah,2    
        int 21h
        loop print

    pop dx      ; restore dx
    pop cx      ; restore cx
    pop bx      ; restore bx
    pop ax      ; restore ax
    ret         ; return


code ends
   end begin