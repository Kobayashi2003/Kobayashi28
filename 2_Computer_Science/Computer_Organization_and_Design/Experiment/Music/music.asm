ASSUME CS:CODE, SS:STACK, DS:DATA

DATA SEGMENT

    ; message
    MSG  DB "KOBAYASHI!!!!", 0
    CRLF DB 0DH, 0AH, '$'

    ; music frequency and duration
    FREQ_L 	DW	330, 1, 294, 1, 262, 1, 294, 1, 330, 1, 330, 1
      	    DW	330, 2, 294, 1, 294, 1, 294, 2, 330, 1, 392, 1
      	    DW	392, 2, 330, 1, 294, 1, 262, 1, 294, 1, 330, 1
      	    DW	330, 1, 330, 1, 330, 1, 294, 1, 294, 1, 330, 1
      	    DW	294, 1, 262, 4, 0 

DATA ENDS

STACK SEGMENT
    DW 128 DUP(?)
STACK ENDS

CODE SEGMENT

MAIN:

    MOV AX, DATA
    MOV DS, AX
    MOV AX, STACK
    MOV SS, AX
    MOV SP, 128
    MOV AX, 0
    MOV ES, AX

    MOV WORD PTR ES:[50*4],   OFFSET INT_50   ; set interrupt vector
    MOV WORD PTR ES:[50*4+2], CS
    MOV WORD PTR ES:[50*4+4], OFFSET INT_51   ; set interrupt vector
    MOV WORD PTR ES:[50*4+6], CS
    
    INT 50

    MOV AH, 9                                 ; print message 
    MOV DX, OFFSET MSG
    INT 21H

    INT 51
    

    MOV AX, 4C00H
    INT 21H

; --------------- interrupt service routine ------------------

INT_50:                                       ; clear screen
    PUSH AX                                   ; save registers
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH ES
    PUSHF

    MOV AX, 0B800H                           ; video memory
    MOV ES, AX
    MOV BX, 0
    MOV CX, 80*24                            ; screen size
clear_loop:                                  ; clear screen loop
    MOV WORD PTR ES:[BX], 0
    ADD BX, 2
    LOOP clear_loop 
END_50:
    POPF                                     ; restore registers
    POP ES
    POP DX
    POP CX
    POP BX
    POP AX
    IRET

INT_51:                                      ; play music
    PUSH AX                                  ; save registers
    PUSH BX
    PUSH CX
    PUSH DX
    PUSH DI
    PUSHF

    MOV AL, 0B6H                             ; control word
    OUT 43H, AL                              ; send control to 43h, let 8253 know we want to set timer 2

    LEA DI, FREQ_L                           ; load music frequency and duration
music_loop:
    MOV DX, 0012H                            ; the input frequency of timer 8253: 1.193182 MHz (1234DE H)
    MOV AX, 34DEH

    MOV BX, [DI]                             ; load frequency, if 0, end music
    CMP BX, 0
    JZ  END_51

    DIV BX                                   ; (0012 34DE H)  / (frequency), get the number of clock cycles
    OUT 42H, AL                              ; THEN SEND THE NUMBER OF CLOCK CYCLES TO 8253
    MOV AL, AH
    OUT 42H, AL

    IN  AL, 61H                              ; get the current status of speaker
    MOV AH, AL                               ; save the status to ah
    OR  AL, 3                                ; set the last two bits to 1, enable speaker
    OUT 61H, AL                              ; send the new status to 61h

    INC DI                                   ; load duration to bx
    INC DI
    MOV BX, [DI]
    CALL FUNC_DELAY_DURATION                 ; delay for the duration

    INC DI                                   ; point to the next frequency
    INC DI
    MOV AL, AH                               ; restore the status of speaker
    OUT 61H, AL

    CALL FUNC_DELAY                         ; delay between two notes

    JMP music_loop
END_51:
    POPF                                     ; restore registers
    POP DI
    POP DX
    POP CX
    POP BX
    POP AX
    IRET


; --------------- subroutines ------------------

FUNC_DELAY_DURATION PROC                     ; delay for the duration, the duration is stored in bx
    PUSH AX                                  ; save registers
    PUSH BX
    PUSH CX
    PUSH DX
    PUSHF
delay1_loop1:
    MOV CX, 0FFFFH                           ; control the delay time
delay1_loop2:
    IN  AL, 61H
    AND AL, 10H
    CMP AL, AH
    JE  delay1_loop2
    MOV AH, AL
    LOOP delay1_loop2
    DEC BL
    JNZ delay1_loop1

    POPF                                     ; restore registers
    POP DX
    POP CX
    POP BX
    POP AX
    RET
FUNC_DELAY_DURATION ENDP

FUNC_DELAY PROC                              ; delay between two notes
    PUSH AX                                  ; save registers
    PUSH BX
    PUSH CX
    PUSH DX
    PUSHF

    MOV CX, 1H                               ; control the delay time
delay2_loop1:
    MOV DX, 0FFFFH
delay2_loop2:
    DEC DX
    JNZ delay2_loop2
    LOOP delay2_loop1   

    POPF                                     ; restore registers
    POP DX
    POP CX
    POP BX
    POP AX
    RET
FUNC_DELAY ENDP

code ends
end main