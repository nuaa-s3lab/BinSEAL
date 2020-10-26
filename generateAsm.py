import random


def generateAsm(function_table, function_data):
    address = int(function_data['address'], 16)
    opaque_1 = (address >> 16) & 0xFFFF
    opaque_2 = (address >> 8) & 0xFF
    opaque_3 = address & 0xFF

    # basic asm
    asm_str = '''
    lea rsp, [rsp-8]
    push rax
    xor rax, rax
'''
    # opaque 1, $x^2>=0$
    asm_str += '''
    mov eax, edi
    imul eax, edi
    not rax
    shr rax, 0x3f
    movzx rax, al
    cmp rax, 1
    jnz $+16
    mov rax, {}
    mov [rsp+0x8], rax
    jmp $+14
    mov rax, {}
    mov [rsp+0x8], rax
'''.format(opaque_1, random.randint(0, 0xFFFF))
# 3+73-61+117-77+154-124 = 15+40+30
    # opaque 2, $(x^2+x+7)%81!=0$
    asm_str += '''
    push rcx
    push rdx
    mov eax, edi
    and rax, 0x7FFFFFFF
    add rax, 1
    imul rax, rax
    add rax, 7
    mov rcx, rax
    mov rdx, 0x6522C3F35BA78195
    mov rax, rcx
    imul rdx
    sar rdx, 5
    mov rax, rcx
    sar rax, 0x3F
    sub rdx, rax
    mov rax, rdx
    shl rax, 3
    add rax, rdx
    lea rdx, [rax*0x8]
    add rax, rdx
    sub rcx, rax
    mov rax, rcx
    pop rdx
    pop rcx
    cmp rax, 0

    jz $+25
    mov rax, [rsp+0x8]
    push rbx
    shl rax, 8
    mov rbx, {}
    add rax, rbx
    pop rbx
    jmp $+23
    mov rax, [rsp+0x8]
    push rbx
    shl rax, 8
    mov rbx, {}
    add rax, rbx
    pop rbx

    mov [rsp+0x8], rax
'''.format(opaque_2, random.randint(0, 0xFFFF))

    # opaque 3,
    asm_str += '''
    ;
    push rbx
    push rcx
    mov eax, edi
    imul eax, 0xdeadbeef
    sub eax, 0x1142153
    mov ebx, eax
    shl eax, 0x11
    xor ebx, eax
    mov eax, [rsp+0x28]
    imul eax, 0xdeadbeef
    sub eax, 0x1142153
    mov ecx, eax
    shl eax, 11
    xor ecx, eax
    cmp ecx, ebx
    je $+23
    mov rax, [rsp+0x18]
    shl rax, 8
    mov rbx, {}
    add rax, rbx
    jmp $+21
    mov rax, [rsp+0x18]
    shl rax, 8
    mov rbx, {}
    add rax, rbx

    mov [rsp+0x18], rax
    pop rcx
    pop rbx
    pop rax
    ret
'''.format(opaque_3, random.randint(0, 0xFFFF))
    return asm_str
