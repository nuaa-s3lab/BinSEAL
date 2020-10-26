import re
import os
import sys
import getopt
from pwn import *
from getAsm import getAsm
from editTextSection import EditTextSection
from changeAsmToList import ChangeAsmToList
from editDataSection import editDataSection

context.arch = 'amd64'

if __name__ == '__main__':
    input_filename = ''
    output_filename = ''
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hi:", ["input="])
    except getopt.GetoptError:
        print("[*] Usage: python %s -i <input-file>" %
              sys.argv[0])
        sys.exit(-1)

    for opt, arg in opts:
        if opt == '-h':
            print("[*] Usage: python %s -i <input-file> -o <output-file>" %
                  sys.argv[0])
            sys.exit()
        elif opt in ("-i", "--input"):
            input_filename = arg

        output_filename = input_filename+"_obfed"

    if input_filename == "" or output_filename == "":
        print("[!] Missing parameters!")
        exit(-1)

    # function_table = getFunction(input_filename, output_filename)
    # print(function_table)
    # exit(0)
    # asm_table = getAsm(input_filename, output_filename)
    call_list, func_list = getAsm(input_filename, output_filename)
    e = ELF(input_filename)
    data_section = e.get_section_by_name('.data').header
    bss_addr = data_section.sh_addr + data_section.sh_size
    bss_section = e.get_section_by_name('.bss').header
    bss_size = bss_section.sh_size
    print("[+] .bss addr: "+hex(bss_addr))
    print("[+] .bss size: "+hex(bss_size))

    exit(0)

    asm_to_add, func_list = editDataSection(
        bss_addr+bss_size, func_list)
    asm_list = ChangeAsmToList(asm_to_add, bss_size)
    # print(asm_list)

    # print(len(asm_list), "\nchar parasite[] = {" + str(asm_list)[1:-1] + "};")

    with open("data-infector/parasite.h", 'w') as out_f:
        out_f.write("char parasite[] = {" + str(asm_list)[1:-1] + "};")
# gcc -o ../temp/data_infector infect.c
    EditTextSection(e, call_list, func_list, output_filename)

    print("[+] gcc -o temp/data_infector data-infector/infect.c")

    if os.system("gcc -o temp/data_infector data-infector/infect.c") != 0:
        print("[-] Err")
        exit(0)
    print(output_filename)
    # exit(0)

    print("temp/data_infector {} {}".format("temp/" + output_filename, "temp/"+input_filename+"_latest"))
    if os.system("temp/data_infector {} {}".format("temp/"+output_filename, "temp/"+input_filename+"_latest")) != 0:
        print("[-] Err")
        exit(0)
