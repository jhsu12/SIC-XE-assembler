

fname="2-5.txt"
# means have not start yet
location_counter = -1

instruct_list = []
symbol_table = {} # 'sym': addr
register_number = {'A': 0, 'X': 1, 'L': 2, 'B': 3, 'S': 4, 'T': 5, 'F': 6}

mnemonic_info = {
    "STL": {"format":3, "opcode":0x80 },
    "STA": {"format":3, "opcode":0x0C },
    "LDB": {"format":3, "opcode":0x68 },
    "LDT": {"format":3, "opcode":0x74 },
    "JSUB": {"format":3, "opcode":0x48 },
    "LDA": {"format":3, "opcode":0x00 },
    "COMP": {"format":3, "opcode":0x28 },
    "JEQ": {"format":3, "opcode":0x30 },
    "J": {"format":3, "opcode":0x3C },
    "CLEAR": {"format":2, "opcode":0xB4 },
    "TD": {"format":3, "opcode":0xE0 },
    "RD": {"format":3, "opcode":0xD8 },
    "COMPR": {"format":2, "opcode":0xA0 },
    "STCH": {"format":3, "opcode":0x54 },
    "TIXR": {"format":2, "opcode":0xB8 },
    "JLT": {"format":3, "opcode":0x38 },
    "STX": {"format":3, "opcode":0x10 },
    "RSUB": {"format":3, "opcode":0x4c },
    "LDCH": {"format":3, "opcode":0x50 },
    "WD": {"format":3, "opcode":0xDC },

} # "LDA" : {"format":, "opcode"} if the format is 3/4, then it will store 3 as default since if it is format 4, it will have a + sign.
def construct_instruct(instruct):
    # nstruct_info = {"loc":, "sym":, "mne":, "oper":}
    # remember "END" is index 0
    if len(instruct) == 3:
        instruct_info = {
            'loc':-1,
            'sym': instruct[0],
            'mne': instruct[1],
            'oper': instruct[2],
        }
    elif len(instruct) == 2:
        instruct_info = {
            'loc':-1,
            'mne': instruct[0],
            'oper': instruct[1],
        }
    elif len(instruct) == 1:
        instruct_info = {
            'loc':-1,
            'mne': instruct[0],
        }
    instruct_list.append(instruct_info)
    return


def make_symbol_table():
    # decide the program name and also length
    p_name = ""
    p_length = -1
    start_location = -1
    global location_counter, symbol_table, mnemonic_info

    for instruct in instruct_list:

        # Update instruction info
        #print(hex(location_counter))
        instruct['loc'] = hex(location_counter)

        # Assemble directives
        if instruct['mne'] == "START":
            p_name = instruct['sym']
            location_counter = int(instruct['oper'])
            start_location = location_counter
            instruct['loc'] = hex(location_counter)
        elif instruct['mne'] == "BASE":
            continue
        elif instruct['mne'] == "BYTE":
            symbol_table[instruct['sym']] = hex(location_counter)

            operand = instruct['oper']
            if operand[0] == 'X':
                location_counter += int(len(operand[2:-1])/2)
            elif operand[0] == 'C':
                location_counter += len(operand[2:-1])

        elif instruct['mne'] == "RESW":
            symbol_table[instruct['sym']] = hex(location_counter)
            location_counter += int(instruct['oper']) * 3
        elif instruct['mne'] == "RESB":
            symbol_table[instruct['sym']] = hex(location_counter)
            location_counter += int(instruct['oper'])
        elif instruct['mne'] == "END":
            # Calculate length
            p_length = hex(location_counter-start_location)
        else:
        # Opcode
            # check synbol
            if 'sym' in instruct:
                symbol_table[instruct['sym']] = hex(location_counter)
                
            # Check whether it needs to add in to symbol table
            if 'oper' in instruct:
                # Construct symbol table

                # filter operand with # and @
                operand = instruct['oper'].replace('#', "").replace('@', "")

                # A,S or BUFFER,X ....
                if ',' in operand:
                    operand = operand.split(',')
                    if (operand[0] not in register_number) and (operand[0] not in symbol_table):
                        symbol_table[operand[0]] = -1
                # consist only alphabet and not register
                elif operand.isalpha() and operand not in register_number:
                    if operand not in symbol_table:
                        symbol_table[operand] = -1

            # Update location counter
            # format 4
            if '+' in instruct['mne']:
                location_counter += 4
            else:
                location_counter += mnemonic_info[instruct['mne']]['format']
    program_info = {"program_name": p_name, "program_length": p_length, "start_loc": hex(start_location)}
    return program_info


def print_symbol_table():
    global symbol_table
    sorted_symbol_table = dict(sorted(symbol_table.items(), key=lambda item: int(item[1], 16)))

    for symbol, address in sorted_symbol_table.items():
        
        print(f'Symbol: {symbol}, Address: {int(address, 16):04X}')
      

def read_file(fname):        
    with open(fname, 'r') as file:
        for l in file:
            if(len(l) == 0 or '.' in l):
                continue
            instruct = l.replace('\n', '').replace('\t', ' ').split()
            # construct instruction
            construct_instruct(instruct)
    return

def pass_one():
    ## construct symbol table and fill in the info of instruct_list
    program_info = make_symbol_table()
    return program_info

def pass_two():
    # T_record = [{}, {}] for each dict = {"start_loc": , "length":, "record": []}
    # M_record = [{}, {}] for each dict = {"start_loc":, "length":}
    global instruct_list, symbol_table

    for instruct in instruct_list:
        pass
    pass
# Not 
#print_symbol_table()

read_file(fname)
program_info = pass_one()
pass_two()
print(instruct_list)
print_symbol_table()