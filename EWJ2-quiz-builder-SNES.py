import os
import struct
from itertools import cycle
from tkinter import filedialog
from math import floor

txt_file = ""
txt_file=filedialog.askopenfilename(initialdir=os.getcwd(), title="Choose TXT File" ,filetype=(('TXT file', '*.txt'),("ALL file",'*.*')))

if len(txt_file) != 0:
    txt_open = open(txt_file, "r")
    quiz_data= txt_open.readlines()
    txt_open.close()

    i=len(txt_file)- 1
    short_name_file = ""
    while i!= 0 and txt_file[i] != '.':
        i -= 1
    i -= 1
    while i!= 0 and txt_file[i] != '/':
        short_name_file = txt_file[i] + short_name_file
        i -= 1

    ROM_file = ""
    ROM_file=filedialog.askopenfilename(initialdir=os.getcwd(), title="Choose ROM File" ,filetype=(('SNES file', '*.sfc'), ('BIN file', '*.bin'),("ALL file",'*.*')))

    if len(ROM_file) != 0:
        ROM_open = open(ROM_file, "rb")
        ROM_data = ROM_open.read()
        ROM_open.close()

        new_line= bytearray()
        data_bin = bytearray()
        footer_pointer = [242490]
        footer_bin = bytearray()

        button_bit = [b'\x18', b'\x19', b'\x1A']

        for n in range (0, len(quiz_data)-1):
            quiz_data[n] = quiz_data[n][:-1]

        for n in range(0, len(quiz_data), 5):
          
            per_count = 0

            for y in range (0,5):
                per_count += quiz_data[n + y].count("%")

            new_line = bytearray()
            new_line += struct.pack("B", 20 + int(quiz_data[n+1]))

            if per_count < 6 :
                new_line += b'\x07'
            
            new_line += b'\x01'

            len_list = []
            
            ln = 0
            for x in range(1, len(quiz_data[n])):
                if quiz_data[n][x] == "%":
                    len_list.append(ln)
                    ln = 0
                else:
                    ln += 1
                    
            len_list.append(ln)

            new_line += struct.pack("B", 1 + floor((28 - len_list[0]) / 2))

            xl = 1
            
            for x in range(1,len(quiz_data[n])):
                if quiz_data[n][x] == "%":
                    new_line += b'\x07\x01'
                    new_line += struct.pack("B", 1 + floor((28 - len_list[xl]) / 2))
                    xl += 1
                else:
                    new_line += bytes(quiz_data[n][x].upper().encode("utf-8"))

            if per_count < 3:
                new_line += b'\x07\x07'
            else:
                if per_count < 6:
                    new_line += b'\x07'

            button_num = 1

            prop_len = 0
            for y in range (3,5):
                for z in range(len(quiz_data[n + y])):
                    prop_len += 1

            space_opt = 1
            if prop_len > 3:
                space_opt = 1
            else:
                space_opt = 5

            while button_num < 4:
                new_line += b'\x07\x07\x01' + struct.pack("B", 11 + space_opt) + button_bit[button_num - 1]
                for x in range(0,len(quiz_data[n+button_num+1])):
                    if quiz_data[n+button_num+1][x] == "%":
                        new_line += b'\x07\x01\x0D'
                        
                    else:
                        new_line += bytes(quiz_data[n+button_num+1][x].upper().encode("utf-8"))

                button_num += 1

            new_line += b'\x00'
            footer_pointer.append(len(new_line)+footer_pointer[-1])

            data_bin += new_line

        footer_pointer = footer_pointer[:-1]

        for n in range(len(footer_pointer)):
            footer_bin +=  struct.pack("<L", footer_pointer[n])[:2] + b'\xC3\x00'

        if len(footer_bin)/4 > 73:
            print("There are over 73 questions")
        
        if len(data_bin) < 8176:
            data_bin += bytes(8176 - len(data_bin))

        out_file = open(short_name_file + " Bin Data.bin", "wb+")
        out_file.write(data_bin + footer_bin)
        out_file.close()

        print("Bin Data Done")

        if len(data_bin) + len(footer_bin) < 8469 :
            
            new_ROM_data = ROM_data[:242490] + data_bin + footer_bin + ROM_data[250958:]

            out_file = open("Earthworm Jim 2 MOD + " + short_name_file + ".sfc", "wb+")
            out_file.write(new_ROM_data)
            out_file.close()

            print("New ROM File Done")
        
        else:
            print("Thus you can't add it in the ROM but have a bin file!")

    else:
        print("No ROM file selected")

else:
    print("No file choosen")
