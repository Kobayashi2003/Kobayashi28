DATA SEGMENT
SOURCE DB 2,3,4,5,17,38,49,10,40,94
COUNT EQU $-SOURCE
DEST  DB  COUNT DUP (0)
DATA ENDS
CODE SEGMENT
    ASSUME CS:CODE,DS:DATA
BEGIN:
    MOV AX,DATA
    MOV DS,AX
    MOV CX,COUNT
    LEA SI,SOURCE
    LEA DI,DEST
AG:
    MOV AL,[SI]
    MOV [DI],AL
    INC SI
    INC DI
    LOOP AG
    MOV AH,4CH
    INT 21H
CODE ENDS
    END BEGIN