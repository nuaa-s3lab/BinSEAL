from pwn import *

def EditTextSection(e, call_list, func_list, output_filename):
    for call_unit in call_list:
        addr = call_unit['address']
        asm_text = ''
        flag = False
        for func_unit in func_list:
            if call_unit['target'] == func_unit['address']:
                flag = True
                asm_text = "call {}".format(func_unit['new_addr'])
                break
        if flag is False:
            continue
        # print("[+] Origin asm: "+e.disasm(int(addr, 16), 5))
        # print("[+] New asm:    "+asm_text)
        e.asm(int(addr, 16), asm_text)
    e.save("temp/"+output_filename)
    print("[+] saved at "+"temp/"+output_filename)