STACK SEGMENT PARA STACK'STACK'
        DB 32 DUP(?)
STACK ENDS
DATA SEGMENT
FREQ_L 	DW	330, 1, 294, 1, 262, 1, 294, 1, 330, 1, 330, 1
  	DW	330, 2, 294, 1, 294, 1, 294, 2, 330, 1, 392, 1
  	DW	392, 2, 330, 1, 294, 1, 262, 1, 294, 1, 330, 1
  	DW	330, 1, 330, 1, 330, 1, 294, 1, 294, 1, 330, 1
  	DW	294, 1, 262, 4,0
DATA ENDS
CODE SEGMENT
        ASSUME CS:CODE,DS:DATA,SS:STACK
BEGIN:
        MOV AX,DATA
        MOV DS,AX
        MOV AL,0B6H
        OUT 43H,AL
        LEA DI,FREQ_L
NEXT:
        MOV AX,34DEH
        MOV DX,0012H ; 将被除数存放在DX、AX中
        MOV BX,[DI] ; 将频率值作为除数
        CMP BX,0 ; 将除数与0作比较
        JZ DONE ; 若除数为0，结束，返回DOS
        DIV BX
        OUT 42H,AL ; 将商值作为计数值
        MOV AL,AH
        OUT 42H,AL
        IN AL,61H
        MOV AH,AL ; 保存扬声器的状态
        OR AL,3
        OUT 61H,AL ; 打开扬声器，使扬声器发声
        INC DI
        INC DI
        MOV BX,[DI] ; 控制音调时间
        CALL DELAY
        INC DI
        INC DI
        MOV AL,AH ; 将扬声器恢复为原来的状态
        OUT 61H,AL
        CALL DELAY2
        JMP NEXT
DONE:
        MOV AH,4CH ; 返回控制面板
        INT 21H
DELAY PROC
        PUSH AX
AGAIN1:
        MOV CX,0FFFFH ; 控制需要延迟的秒数
AGAIN:
        IN AL,61H ; 8255A的 PB4 每隔15.08μs翻转一次
        AND AL,10H
        CMP AL,AH
        JE AGAIN
        MOV AH,AL
        LOOP AGAIN
        DEC BL
        JNZ AGAIN1
        POP AX
        RET
DELAY ENDP
DELAY2 PROC
        MOV CX,1328
REPEAT:
        IN AL,61H
        AND AL,10H
        CMP AL,AH
        JE REPEAT
        MOV AH,AL
        LOOP REPEAT
        RET
DELAY2 ENDP
CODE ENDS
        END BEGIN