from pwn import *

# input_filename = 'bin/test'
input_filename = '/usr/bin/sort'

e = ELF(input_filename)

bss_sh_addr_addr = e.get_section_by_name('.bss').header['sh_addr']

for section in e.sections:
    if section.header['sh_addr'] >= bss_sh_addr_addr:
        print(section.header)