import os, re
from functools import reduce

def getAsm(input_filename, output_filename):
    print("------ Find call assemblies ------")
    print("[+] objdump -d %s | grep callq > temp/call_func.txt\n" % input_filename)
    if os.system("objdump -d %s | grep callq > temp/call_func.txt" % input_filename) != 0:
        print("\033[1;31m[-] Objdump Error!\033[1;31m")
        exit(0)

    asm_table = []
    with open('temp/call_func.txt', 'r') as cf:
        clines = cf.readlines()
        # print(clines)
        call_function_list = []
        function_list = []
        for line in clines:
            call_function_set = {}
            function_set = {}
            func_address_group = re.search(r'(.*):', line, re.M|re.I)
            func_address = "0x"+func_address_group.group().lstrip()[:-1]
            # print(func_address.group().lstrip()[:-1])
            if "*" in line:
                continue
            call_address_group = re.search(r'call(.*)<', line, re.M|re.I)
            if call_address_group is not None:
                # print(call_address_group.group()[:-2])
                call_address = "0x"+call_address_group.group()[7:-2]
                call_function_set['address'] = func_address
                call_function_set['target'] = call_address
                function_set['address'] = call_address
                call_function_list.append(call_function_set)
                function_list.append(function_set)
                # print(call_address)
        # print(call_function_list, call_function_set)
        run_function = lambda x, y: x if y in x else x + [y]
        stripped_function_list = reduce(run_function, [[], ]+function_list)
        # print(stripped_function_list)
        return call_function_list, stripped_function_list