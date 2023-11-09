

fname="2-5.txt"
# means have not start yet
location_counter = -1

instruct_list = []
symbol_table = {} # 'sym': addr
register_number = {'A': 0x0, 'X': 0x1, 'L': 0x2, 'B': 0x3, 'S': 0x4, 'T': 0x5, 'F': 0x6}

mnemonic_info = {
    "STL": {"format":3, "opcode":0x14 },
    "STA": {"format":3, "opcode":0x0C },
    "LDB": {"format":3, "opcode":0x68 },
    "LDT": {"format":3, "opcode":0x74 },
    "LDL": {"format":3, "opcode":0x08 },
    "LDX": {"format":3, "opcode":0x04 },
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
    "TIX": {"format":3, "opcode":0x2C },
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

def hex_to_twos_complement(hex_string, num_bits):
    # Convert hexadecimal to binary
    binary_string = bin(int(hex_string, 16))[3:]
    #print(binary_string)
    # Pad with leading zeros if necessary
    binary_string = binary_string.zfill(num_bits)
    #print(binary_string)
    # Invert the bits
    inverted_string = ''.join('1' if bit == '0' else '0' for bit in binary_string)
    #print(inverted_string)
    # Add 1 to get the two's complement
    twos_complement = bin(int(inverted_string, 2) + 1)[2:]
    #print(twos_complement.zfill(num_bits))
    return twos_complement.zfill(num_bits)

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
            location_counter = int(instruct['oper'], 16)
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
        elif instruct['mne'] == "WORD":
            symbol_table[instruct['sym']] = hex(location_counter)
            location_counter += 3
        elif instruct['mne'] == "RESW":
            symbol_table[instruct['sym']] = hex(location_counter)
            location_counter += int(instruct['oper']) * 3
        elif instruct['mne'] == "RESB":
            symbol_table[instruct['sym']] = hex(location_counter)
            location_counter += int(instruct['oper'])
        elif instruct['mne'] == "END":
            # Calculate length
            p_length = f'{int(hex(location_counter-start_location), 16):06X}'
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
    if len(p_name) != 6:
        space = 6-len(p_name)
        p_name += " " * space
    program_info = {"program_name": p_name, "program_length": p_length, "start_loc": f'{int(hex(start_location), 16):06X}'}
    return program_info


def print_symbol_table():
    global symbol_table
    sorted_symbol_table = dict(sorted(symbol_table.items(), key=lambda item: int(item[1], 16)))

    for symbol, address in sorted_symbol_table.items():
        
        print(f'Symbol: {symbol}, Address: {int(address, 16):04X}')
      
def print_instruct_list():
    global instruct_list
    for instruct in instruct_list:
        print(instruct)
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

def generate_object_code(opcode, base, pc, instruction):
    ## construct object code for format 3, 4 instruction
    global symbol_table
    #print(instruction)
    mne = instruction['mne']
    oper = instruction['oper']
    objCode = -1
    nixbpe = 0b0
    
    # decide n i
    if '@' in oper:
        # (n, i) = (1, 0)
        nixbpe = nixbpe | (0b10 << 4)
    elif '#' in oper:
        # (n, i) = (0, 1)
        nixbpe = nixbpe | (0b01 << 4)
    else:
        # (n, i) = (1, 1)
        nixbpe = nixbpe | (0b11 << 4)

    # format = 4
    if '+' in mne:
        m_record = {}
        # +STCH BUFFER,X
        if ',' in oper:
            symbol = oper.split(",")[0]
            nixbpe = nixbpe | (0b1001)
            symbol_loc = symbol_table[symbol]
            objCode = (opcode << 24) | (nixbpe << 20) | int(symbol_loc, 16)
        elif '#' in oper:
            symbol = oper[1:]
            nixbpe = nixbpe | (0b0001)
            if symbol.isalpha():
                symbol_loc = symbol_table[symbol]
                objCode = (opcode << 24) | (nixbpe << 20) | int(symbol_loc, 16)
            else:
                # Number
                number = hex(int(symbol))
                #print(type(number))
                
                objCode = (opcode << 24) | (nixbpe << 20) | int(number, 16)
            #print(mne, oper, hex(objCode))
        else:
            # x, b, p, e = 0001
            nixbpe = nixbpe | (0b0001)
            symbol_loc = symbol_table[oper]
            objCode = (opcode << 24) | (nixbpe << 20) | int(symbol_loc, 16)
            #print(mne, oper, hex(objCode))

            # M record? 
            m_record = {"start_loc": f"{(int(instruction['loc'], 16) + 0x1):06X}", "length": "05"}
            #print(instruction)
            #print(m_record)
        objCode_format = f'{int(hex(objCode), 16):08X}'
        #print(objCode_format, "  here")
        # print(instruction)
        # print(objCode_format)
        return objCode_format, m_record
    # format = 3
    else:
        if '#' in oper:
            if oper[1:].isalpha():
                # get rid of # if operand is #label
                oper = oper[1:]

                # check pc relative or base relative
                # pc -2048 - 2047
                # base 0 - 4095
                target_address = int(symbol_table[oper], 16)
                relative = target_address - pc
                if relative >= -2048 and relative < 2047:
                    # (x, b, p, e) = (0, 0, 1, 0)
                    nixbpe = nixbpe | (0b0010)
                else:
                    # base relative
                    # (x, b, p, e) = (0, 1, 0, 0)
                    nixbpe = nixbpe | (0b0100)
                objCode = (opcode << 16) | (nixbpe << 12) | int(hex(relative), 16)
            else:
                # number
                
                number = hex(int(oper[1:]))
                objCode = (opcode << 16) | (nixbpe << 12) | int(number, 16)
                #print(mne, oper, hex(objCode))
        else:
            # setting x bit ?
            x_index = False
            if ',' in oper:
                oper = oper.split(",")[0]
                x_index = True
            symbol = oper
            if '@' in oper:
                symbol = symbol[1:]
            
            # check pc relative or base relative
            # pc -2048 - 2047
            # base 0 - 4095
            target_address = int(symbol_table[symbol], 16)
            relative = target_address - pc
            if relative >= -2048 and relative < 2047:
                # (x, b, p, e) = (0, 0, 1, 0)
                nixbpe = nixbpe | (0b0010)
                if relative < 0:
                    # convert to two's compliment
                    #print(relative)
                    relative = int(hex_to_twos_complement(hex(relative), 12), 2)
                    

            else:
                # base relative
                # default (x, b, p, e) = (0, 1, 0, 0)
                nixbpe = nixbpe | (0b0100)
                
                # using X index, setting x bit to 1
                if x_index:
                    nixbpe = nixbpe | (0b1000)
                relative = target_address - int(base, 16)

            objCode = (opcode << 16) | (nixbpe << 12) | int(hex(relative), 16)

        objCode_format = f'{int(hex(objCode), 16):06X}'
    # print(instruction)
    # print(objCode_format)
    return objCode_format

    
def pass_two():
    # T_record = [{}, {}] for each dict = {"start_loc": , "length":, "record": []}
    # M_record = [{}, {}] for each dict = {"start_loc":, "length":}
    global instruct_list, symbol_table, mnemonic_info
    T_record, M_record = list(), list()
    t_record = dict()
    objCode = -1
    base = 0
    pc = 0
    for index, instruct in enumerate(instruct_list):
        # Check 
        #     assemble directive ?
        #     instruction ?
        #         format 1, 2 => obj code
        #         format 3, 4:
        #             LDB needs to set BASE register
        #             - + format 4 e =1
        #             - else format 3
        #                 - @ indirect (n, i) = (1, 0)
        #                 - # direct (n, i) = (0, 1)
        #                     #num (x, b, p) = (0, 0, 0)
        #                     #label pc or base relative
        #                 - operand no @, # (n, i) = (1, 1)
        #             operand consist of X ?
        #             pc, base relative ?


        # Set program counter
        if (index + 1) != len(instruct_list):
            pc = int(instruct_list[index+1]['loc'], 16)
        # Assemble directives
        if instruct['mne'] == "START":
            continue
        elif instruct['mne'] == "BASE":
            base = symbol_table[instruct['oper']]
            continue
        elif instruct['mne'] == "BYTE":
            operand = instruct['oper']
            val = operand[2:-1]
            if operand[0] == 'X':
               objCode = f'{val}'
            elif operand[0] == 'C':
                #print(val)
                objCode = ''.join([f'{ord(char):x}' for char in val])
            #print(objCode)
        elif instruct['mne'] == "WORD":
           continue
        elif instruct['mne'] == "RESW" or instruct['mne'] == "RESB" or instruct['mne'] == "END":
            # if t_record isn't empty then append
            if len(t_record) != 0:
                # append old t_record to T_record
                t_record['length'] = f"{int(hex(int(t_record['length'])), 16):02X}"
                new_t = t_record.copy()
                T_record.append(new_t)
                # print("\n\n T_RECORD")
                # print(T_record)
                # print("\n\n")
                # clear old t_record
                t_record.clear()
            continue
           
        elif instruct['mne'] == 'RSUB':
            objCode = "4F0000"
        else:
            # instruction
            mne = instruct['mne']
                
            if '+' in mne:
                format = 4
                opcode = mnemonic_info[mne[1:]]['opcode']
            else:
                format = mnemonic_info[mne]['format']
                opcode = mnemonic_info[mne]['opcode']

            if format == 1:
                pass
                continue
            elif format == 2:
                oper = instruct['oper']
                if len(oper) == 1:
                    # CLEAR X
                    reg_num = register_number[oper]
                    objCode = (opcode << 8) | (reg_num << 4)
                    #print(hex(objCode))
                else:
                    # COMPR A,X
                    reg1, reg2 = oper.split(',')
                    reg_num1 = register_number[reg1]
                    reg_num2 = register_number[reg2]
                    objCode = (opcode << 8) | (reg_num1 << 4) | reg_num2
                objCode = f'{int(hex(objCode), 16):04X}'
                #print(mne, oper, hex(objCode))


            elif format == 3:
                objCode = generate_object_code(opcode, base, pc, instruct_list[index])
            elif format == 4:
                objCode, m_record = generate_object_code(opcode, base, pc, instruct_list[index])
                if len(m_record) !=0:
                    # append m_record
                    M_record.append(m_record)

        # initialize t_record
        if 'start_loc' not in t_record:
            t_record['start_loc'] = f"{int(instruct['loc'], 16):06X}"
            t_record['length'] = 0
            t_record['result'] = []
        
        objCode_length = len(objCode)/2

        # check length
        if t_record['length'] + objCode_length > 0xFF:
            # append old t_record to T_record
            new_t = t_record.copy()
            T_record.append(new_t)

            # create new t_record
            t_record.clear()
            t_record['start_loc'] = f"{int(instruct['loc'], 16):06X}"
            t_record['length'] = 0
            t_record['result'] = []
            
        t_record['length'] += objCode_length
        t_record['result'].append(objCode)
        #print(instruct, t_record)
        # if len(T_record) != 0:
        #     print(len(T_record))
        #print(instruct, T_record)
    return T_record, M_record

def print_object_program(program_info, T_record, M_record):
    print("\nObject Program: \n\n")

    print("H", program_info['program_name'], program_info['start_loc'], program_info['program_length'])

    for t_rec in T_record:
        print("T",t_rec['start_loc'], t_rec['length'], end=" ")
        for obj in t_rec['result']:
            print(obj, end=" ")
        print("")
    for m_rec in M_record:
        print("M", m_rec['start_loc'], m_rec['length'], end=" ")
        print("")
    print("E", program_info['start_loc'])
read_file(fname)

# Pass One
program_info = pass_one()
print("Symbol Table:\n\n")
print_symbol_table()

# Pass Two
T_record, M_record = pass_two()
print_object_program(program_info, T_record, M_record)
#print(program_info)

#print(M_record)
#print_instruct_list()
