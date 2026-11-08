.model small
.stack 100h

.data
    a dw 3
    b dw 10
    c dw 4
    result dw ?
    Ten dw 10       

.code
start:
    mov ax, @data
    mov ds, ax

    mov ax, b
    sub ax, c
    add ax, a
    mov result, ax

    mov bx, result
    call PrintNumber

    mov ah, 4Ch
    int 21h

; ----------------------
; Підпрограма виведення числа
; ----------------------
PrintNumber proc
    mov cx, 0
    mov dx, 0

NextDigit:
    xor dx, dx
    div word ptr Ten
    push dx
    inc cx
    test ax, ax
    jnz NextDigit

PrintLoop:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop PrintLoop

    ret
PrintNumber endp

end start
