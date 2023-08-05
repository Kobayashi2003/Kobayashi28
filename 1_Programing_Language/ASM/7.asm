ASSUME CS:CODE,DS:DATA,SS:STACK

DATA SEGMENT
    NAME0 DB 10,?,10 DUP(?),'$'
	TABLE DB '0123456789ABCDEF'

	PASSBUF DB 10,?
	PASS0 DB 10 DUP(?)	   ;密码原串存储区
	PASS1 DB 4 DUP(0)	   ;填0区
	PASS2 DB 2 DUP(?)	   ;存储长度区

	TABLES DB 1, 8, 6, 4, 7, 2, 3, 5, 7, 6, 1, 4, 7, 4, 5,3	;S表
	TABLET DB 2, 3, 1, 4,8,7,5,6,9,10,13,11,16,15,14,12					;T表

	HA DB 01H			   ;初始标准幻数
	HB DB 23H
	HC DB 45H
	HD DB 67H

	FA DB 01H			   ;四个函数的参数
	FB DB 23H
	FC DB 45H
	FD DB 67H
	FX DB ?
	FT DB ?
	FUS DB ?

	RESULT DB 00DH,0E0H,07FH,0C1H

	MSG0 DB 0AH,'Input your name:$'
    MSG1 DB 0AH,'Input your password:$'
    MSG2 DB 0AH,'You password is error,Try Again?(Y/N):$'
	MSG3 DB 0AH,'OK!$'
	MSG4 DB 0AH,'You have no chance!$'
DATA ENDS

STACK SEGMENT STACK
    DW 10 DUP(?)
STACK ENDS

CODE SEGMENT 'CODE'
START:
    MOV AX,DATA
    MOV DS,AX
	MOV AX,STACK
	MOV SS,AX

    MOV DX,OFFSET MSG0     ;提示用户输入姓名
    MOV AH,09H
    INT 21H

    MOV DX,OFFSET NAME0	   ;接收用户输入的姓名
    MOV AH,0AH
    INT 21H

    MOV AL,NAME0+1		   ;在用户输入的姓名后追加'$'符号
    ADD AX,2
    MOV AH,0
    MOV SI,AX
    MOV NAME0[SI],'$'

	MOV CX,4
INPUT0:
	MOV HA,01H
	MOV HB,23H
	MOV HC,45H
	MOV HD,67H
	MOV FA,01H
	MOV FB,23H
	MOV FC,45H
	MOV FD,67H
	PUSH CX
	MOV CX,0
LOOP0:
	CMP CX,10
	JZ OUTLOOP0
	MOV SI,CX
	MOV PASS0[SI],0
	INC CX
	JMP LOOP0
OUTLOOP0:
	POP CX

	DEC CX
	CMP CX,0
	JZ OUT1
    MOV DX,OFFSET MSG1	   ;提示用户输入密码
    MOV AH,09H
    INT 21H

    MOV DX,OFFSET PASSBUF  ;接收用户输入的密码
    MOV AH,0AH
    INT 21H

	PUSH CX
MD5:
	MOV AL,PASSBUF+1	   ;在用户输入的密码后加上1
    MOV AH,0
    MOV SI,AX
    MOV PASS0[SI],80H

	MOV AH,PASSBUF+1	   ;将长度存入AX
	MOV CL,3
	SHL AH,CL			   ;左移3位结果就是长度(按位)

	MOV PASS2[1],AH	       ;长度存入长度区,因为最多为10个字符也就是80位只需占用最后一个字节

	MOV CX,15			   ;循环变量
LOOP1:
	MOV SI,CX
	MOV AH,PASS0[SI]
	MOV FX,AH	   		   ;函数传值
	MOV AH,TABLET[SI]
	MOV FT,AH
	MOV AH,TABLES[SI]
	MOV FUS,AH

	JCXZ LOOP1OUT		   ;CX为0则跳转
	DEC CX
	PUSH CX
	CALL FF
	POP CX
	JMP LOOP1
LOOP1OUT:
	MOV CX,15
LOOP2:
	MOV SI,CX
	MOV AH,PASS0[SI]
	MOV FX,AH	   		   ;函数传值
	MOV AH,TABLET[SI]
	MOV FT,AH
	MOV AH,TABLES[SI]
	MOV FUS,AH

	JCXZ LOOP2OUT		   ;CX为0则跳转
	DEC CX
	PUSH CX
	CALL GG
	POP CX
	JMP LOOP2
LOOP2OUT:
	MOV CX,15
LOOP3:
	MOV SI,CX
	MOV AH,PASS0[SI]
	MOV FX,AH	   		   ;函数传值
	MOV AH,TABLET[SI]
	MOV FT,AH
	MOV AH,TABLES[SI]
	MOV FUS,AH

	JCXZ LOOP3OUT		   ;CX为0则跳转
	DEC CX
	PUSH CX
	CALL HH
	POP CX
	JMP LOOP3
LOOP3OUT:
	MOV CX,15
LOOP4:
	MOV SI,CX
	MOV AH,PASS0[SI]
	MOV FX,AH	   		   ;函数传值
	MOV AH,TABLET[SI]
	MOV FT,AH
	MOV AH,TABLES[SI]
	MOV FUS,AH

	JCXZ LOOP4OUT		   ;CX为0则跳转
	DEC CX
	PUSH CX
	CALL II
	POP CX
	JMP LOOP4
LOOP4OUT:
	POP CX
	MOV AH,FA
	ADD HA,AH
	MOV AH,FB
	ADD HB,AH
	MOV AH,FC
	ADD HC,AH
	MOV AH,FD
	ADD HD,AH

	MOV AH,HA
	MOV AL,HB
	MOV BH,HC
	MOV BL,HD

	XOR AH,RESULT		   ;比较
	XOR AL,RESULT+1
	XOR BH,RESULT+2
	XOR BL,RESULT+3

	CMP AX,0			   ;结果出现不相等的则返回重试
	JNZ INPUT1
	CMP BX,0
	JNZ INPUT1

	JMP OUT0			   ;没有不相等的去到程序末尾


FF:
	MOV AH,FB			   ;A += ((B & C) | (~B & D))
	AND AH,FC
	MOV AL,FB
	NOT AL
	AND AL,FD
	OR AH,AL
	ADD FA,AH
	JMP COMON
GG:
	MOV AH,FB			   ;A += ((B & D) | (C & ~D))
	AND AH,FD
	MOV AL,FD
	NOT AL
	AND AL,FC
	OR AH,AL
	ADD FA,AH
	JMP COMON
HH:
	MOV AH,FB			   ; A += (B ^ C ^ D)
	XOR AH,FC
	XOR AH,FD
	ADD FA,AH
	JMP COMON
II:
	MOV AH,FC
	MOV AL,FD
	NOT AL
	OR AL,FB
	XOR AH,AL
	ADD FA,AH

COMON:
	MOV AH,FT			   ;A += X + T
	ADD AH,FX
	ADD FA,AH

	MOV CL,FUS			   ;A = ((A << S) | (A >> (8-S)))
	MOV AH,FA
	MOV AL,AH
	SHL AH,CL
	MOV CL,8
	SUB CL,FUS
	SHR AL,CL
	OR AH,AL
	MOV FA,AH

	MOV AH,FB			   ;A += B
	ADD FA,AH

	MOV AH,FA			   ;ABCD参数的轮换 A->AH
	MOV AL,FB
	MOV BH,FC
	MOV BL,FD

	MOV FB,AH
	MOV FC,AL
	MOV FD,BH
	MOV FA,BL

	RET
INPUT1:
	MOV DX,OFFSET MSG2;
	MOV AH,09H
	INT 21H

	MOV AH,01H;
	INT 21H

	CMP AL,'y'
	JZ INPUT0
	CMP AL,'Y'
	JZ INPUT0
	JMP OUT1
OUT0:
    MOV DL,0AH			   ;输出一个换行符
    MOV AH,02H
    INT 21H

    MOV DX,OFFSET NAME0+2  ;输出用户输入的姓名
    MOV AH,09H
    INT 21H

	MOV DX,OFFSET MSG3     ;输出OK
    MOV AH,09H
    INT 21H

    MOV AH,4CH
    INT 21H
OUT1:
	MOV DX,OFFSET MSG4	   ;输出结束信息
	MOV AH,09H
	INT 21H

	MOV AH,4CH
    INT 21H
CODE ENDS
    END START