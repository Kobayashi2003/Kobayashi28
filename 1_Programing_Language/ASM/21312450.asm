DATA SEGMENT
STRING1 DB 123,22,321,22,25
STRING2 DB 82,432,90,38,22
LOGICAL DB 1,1,1,0,0; 0表示相加，1表示相减
LINE DB 0DH,0AH,'$'
DATA ENDS

CODE SEGMENT
ASSUME CS:CODE,DS:DATA

BEGIN:
    MOV AX,DATA
    MOV DS,AX

    MOV CX,5    ; STRING1与STRAG2含有的元素数
    XOR SI,SI   ; 清除SI

CALCULATE:

    XOR AX,AX
    LEA BX,STRING1
    MVO AL,[BX+SI]
    CALL print_decimal


    XOR DX,DX
    LEA BX,STRING2
    MOV DL,[BX+SI]
    PUSH DX

    LEA BX,LOGICAL
    MOV DH,[BX+SI]
    INT 3
    MOV DL,'+'
    CMP DH,0

    JNZ PLUS
    POP DX
    MOV DH,1
    NEG DL
    PUSH DX
    MOV DL
    INT 3
PLUS:
    PUSH AX
    MOV AH,2
    INT 21H
    POP AX

    POP DX
    PUSH AX
    MOV AX,DX
    CMP AH,0
    JZ @N
    NEG AL
@N:
    CALL print_decimal
    POP AX

    PUSH DX
    PUSH AX
    MOV DL,'='
    MOV AH,2
    INT 21H
    POP AX
    POP DX

    ADD AL,DL
    CALL print_decimal

    LEA DX,LINE
    MOV AH,9
    INT 21H

    INC SI
    LOOP CALCULATE

    MOV AH,4CH
    INT 21H

print_decimal:
    PUSH AX
    PUSH BX
    PUSH CX
    PUSH DX
    XOR CX,CX
    XOR DL,DL
    MOV BL,10

    @D:
        INC CX
        AND AH,0
        DIV BL
        PUSH AX
        CMP AL,0
        JNE @D

    PRINT:
        POP DX
        PUSH CX
        MOV CX,8
        SHR DX,CL
        POP CX
        OR AL,30h
        MOV AH,2
        INT 21H
        LOOP PRINT

    POP DX
    POP CX
    POP BX
    POP AX
    RET

CODE ENDS
    END BEGIN