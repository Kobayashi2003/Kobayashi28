; load the value of a1 into eax
mov eax, [a1]

; if a1 < 12, then goto if1
mov ebx, 12
cmp eax, ebx
jl if1

; else if a1 < 24, then goto if2
mov ebx, 24
cmp eax, ebx
jl if2

; else, if_flag = a1 << 4
shl eax, 4
mov [if_flag], eax
jmp endif

; if1: if_flag = (a1 / 2) + 1
if1:
shr eax, 1
inc eax
mov [if_flag], eax
jmp endif

; if2: if_flag = (24 - a1) * a1
if2:
mov ecx, 24
sub ecx, eax
imul ecx, eax
mov [if_flag], ecx
jmp endif

endif:
