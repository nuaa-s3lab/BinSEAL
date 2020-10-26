def ChangeAsmToList(asm_str, bss_size):
    asm_list = []
    for i in range(bss_size):
        asm_list.append(0)
    for asm_code in asm_str:
        asm_list.append(int(asm_code))
    return asm_list