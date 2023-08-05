DATA SEGMENT

inputStrMsg DB "PLEASE INPUT A STRING: ",'$'    ; 提示输入一个字符串
inputNumMsg DB "PLEASE INPUT A NUMBER: ",'$'    ; 提示输入一个数字
showMsg  DB "YOUR INPUT: ",'$'  ; 提示输入的字符串
ErrorInput DB "INPUT ERROR!",'$'   ; 提示输入错误
encodeMsg DB "ENCODE: ",'$'     ; 提示加密后
deCodeMsg DB "DECODE: ",'$'     ; 提示解密后



NUM DB '0'  ; 用以保存偏移量

NumBuffer DB 20 ; 预定义20字节的空间用于存储用户输入的凯撒偏移量
DB ?    ; 用户输入完成后，自动获得输入的字符个数
DB 20 DUP(0)    ; 将该空间初始化

StrBuffer DB 20 ; 预定义20字节的空间用于存储用户输入的字符串
DB ?
DB 20 DUP(0)

CRLF DB 0AH,0DH,'$' ; 存储换行命令

codeStr DB 20 DUP('$') ; 预定义20字节的空间用于存储加密或解密后的字符串

DATA ENDS

CODE SEGMENT
    ASSUME CS:CODE,DS:DATA  ; 建立段寄存器与段名之间的联系
BEGIN:
    MOV AX,DATA
    MOV DS,AX ; 数据初始化

    CALL inputStr   ; 调用字符串输入模块进行输入
    CALL inputNum   ; 调用数字输入模块进行输入

    LEA DX,CRLF ; 换行
    MOV AH,09H
    INT 21H

; 判断输入的数字是否为两位
    LEA SI,NumBuffer+1 ; 取NumBuffer的偏移地址，加1后转移到SI
    MOV AL,[SI]

    CMP AL,0
    JBE MID_ERROR ; 所输入的数字位数不大于0时结束程序

    CMP AL,2
    JA MID_ERROR ; 所输入的数字位数大于2时结束程序

; 判断输入的数字的正负性
    LEA SI,NumBuffer+2
    MOV AL,[SI]

    CMP AL,'-'
    JE Negative ; 相等时说明所输入的为负数，跳转到负数处理模块

    CMP AL,'-'
    JNE MID_Positive ; 不相等则说明输入的为正数，跳转到正数处理模块

    JMP EXIT


; 字符串输入模块
inputStr:
; 打印提示输入字符串信息
    LEA DX,inputStrMsg
    MOV AH,09H
    INT 21H

; 输入字符串
    LEA DX,StrBuffer
    MOV AH,0AH ; 调用dos系统中的中断函数进行输入
    INT 21H

; 处理字符串
    MOV AL,StrBuffer+1
    ADD AL,2
    MOV AH,0
    MOV SI,AX
    MOV StrBuffer[SI],'$' ; 在字符串的末尾增添'$'作为结束符号

    LEA DX,CRLF ; 换行
    MOV AH,09H
    INT 21H

    RET


; 数字输入模块
inputNum:
; 打印提示信息
    LEA DX,inputNumMsg
    MOV AH,09H
    INT 21H

; 输入数字
    LEA DX,NumBuffer
    MOV AH,0AH
    INT 21H

; 对输入的“数字”字符串进行处理，同上字符串处理
    MOV AL,NumBuffer+1
    ADD AL,2
    MOV AH,0
    MOV SI,AX
    MOV NumBuffer[SI],'$'

    RET

MID_ERROR: ; 中继，用以跳转到ERROR模块
    JMP ERROR

MID_Positive: ; 中继，用以跳转到Positive（正数处理）模块
    JMP Positive

; 负数处理模块
Negative:
    LEA DX,CRLF ; 换行
    MOV AH,09H
    INT 21H

; 打印提示信息
    LEA DX,deCodeMsg
    MOV AH,09H
    INT 21H

    LEA DX,CRLF ; 换行
    MOV AH,09H
    INT 21H

    INC SI ; 当输入的数为负数时，需要读取第四个数，并将其作为凯撒偏移量
    MOV AL,[SI] ; 读取输入的负数的无符号部分（即正数部分）

    MOV NUM,AL  ; 将读取到的正整数的偏移量保存到NUM中
    SUB NUM,48  ; 将获取到的ASCII码转为实际数字（减去48）

    CMP NUM,0
    JB ERROR ; 若NUM小于0，终止程序

    CMP NUM,8
    JG ERROR ; 若NUM大于8，终止程序

    JMP DECODE ; 若处理后数据无误，跳转到DECODE模块

    JMP EXIT

; 正数处理模块
Positive:
    LEA DX,CRLF ; 换行
    MOV AH,09H
    INT 21H

    MOV AL,[SI] ; 读取输入的正整数，该数位于第三位
    MOV NUM,AL
    SUB NUM,48

    CMP NUM,0
    JE ShowInput ; 若所输入的凯撒偏移量为0，直接跳转到ShowInput模块显示用户所输入的字符串

    LEA DX,CRLF ; 换行
    MOV AH,09H
    INT 21H

    CMP NUM,0
    JB ERROR ; 若NUM处理后的值小于0，终止程序

    CMP NUM,8
    JG ERROR ; 若NUM处理后的值大于8，终止程序

    LEA DX,encodeMsg ; 打印提示信息
    MOV AH,09H
    INT 21H

    JMP ENCODE

ERROR:
    LEA DX,ErrorInput ; 打印提示错误信息
    MOV AH,09H
    INT 21H

    JMP EXIT

ShowInput:
    LEA DX,showMsg
    MOV AH,09H
    INT 21H

    LEA DX,StrBuffer+2
    MOV AH,09H
    INT 21H

    JMP EXIT

; ENCODE模块
ENCODE:
    LEA SI,StrBuffer+2 ; 键入字符串的起始地址
    LEA DI,codeStr ; 键入codeStr的起始地址
    MOV CL,StrBuffer+2 ; 初始化开始循环的起始地址
    MOV CH,0 ; 初始化计数寄存器

ENCODE_AGAIN:
; 取字符，若此时的字符为终止符'$'，则结束加密，跳转到SHOW模块
    MOV AL,[SI]
    CMP AL,'$'
    JE SHOW

    CMP AL,'A' ; 小于'A'的字符不需要处理，处理下一个字符
    JL ENCODE_NEXT

    CMP AL,'z' ; 大于'z'的字符不需要处理，处理下一个字符
    JG ENCODE_NEXT

    CMP AL,'a' ; 小于'a'的字符有可能为大写的英文字母，转移到对应模块进行判断处理
    JL ENCODE_UP

    CMP AL,'a'
    JAE ENCODE_LOW

ENCODE_UP:
    CMP AL,'Z' ; 大于'Z'不用处理，处理下一个字符
    JG ENCODE_NEXT

    ADD AL,NUM ; 让当前的字符加上凯撒偏移量，实现字符的加密

    CMP AL,'Z'
    JA OVER
    JMP ENCODE_NEXT

ENCODE_LOW:
    ADD AL,NUM

    CMP AL,'z'
    JA OVER
    JMP ENCODE_NEXT

OVER: ; 若字符在加上了凯撒偏移量后其结果大于26，则应该减去26
    SUB AL,26
    JMP ENCODE_NEXT

ENCODE_NEXT:
    MOV [DI],AL
    INC SI
    INC DI
    LOOP ENCODE_AGAIN



; DECODE模块，处理过程与ENCODE大致相同
DECODE:
    LEA SI,StrBuffer+2
    LEA DI,codeStr
    MOV CL,StrBuffer+2
    MOV CH,0

DECODE_AGAIN:
    MOV AL,[SI]
    CMP AL,'$'
    JE SHOW

    CMP AL,'A'
    JB DECODE_NEXT

    CMP AL,'z'
    JA DECODE_NEXT

    CMP AL,'a'
    JB DECODE_UP

    CMP AL,'a'
    JAE DECODE_LOW

DECODE_UP:
    CMP AL,'Z'
    JA DECODE_NEXT

    SUB AL,NUM
    CMP AL,'A'
    JB UNDER
    JMP DECODE_NEXT

DECODE_LOW:
    SUB AL,NUM
    CMP AL,'a'
    JB UNDER
    JMP DECODE_NEXT

DECODE_NEXT:
    MOV [DI],AL
    INC SI
    INC DI
    LOOP DECODE_AGAIN

UNDER:
    ADD AL,26
    JMP DECODE_NEXT

SHOW: ; 输出字符
    LEA DX,codeStr
    MOV AH,09H
    INT 21H

    JMP EXIT

EXIT: ; 终止程序
    MOV AH,4CH
    INT 21H

CODE ENDS
    END BEGIN