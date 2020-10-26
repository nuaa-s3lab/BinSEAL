from pwn import *
from generateAsm import generateAsm


def editDataSection(bss_addr, function_table):
    # Asm add to data section:
    #   call .bss_function (in text section)
    #   jmp origin function(in .bss section)
    # or we can use:
    #   push origin function
    #   ret ?
    asm_str = ""
    asm_asm = ""
    for function_data in function_table:
        function_data['new_addr'] = hex(bss_addr+len(asm_asm))
        asm_str += generateAsm(function_table, function_data)
        asm_asm = asm(asm_str, vma=bss_addr)
        # print(asm_asm)
    # print(asm_str)
    # print(function_table)
    return asm_asm, function_table
# getAsm('sh', 'test2222222')
