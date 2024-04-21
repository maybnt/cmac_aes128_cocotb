import numpy as np
import math
aes_box = [
0x63,
0x7c,
0x77,
0x7b,
0xf2,
0x6b,
0x6f,
0xc5,
0x30,
0x01,
0x67,
0x2b,
0xfe,
0xd7,
0xab,
0x76,
0xca,
0x82,
0xc9,
0x7d,
0xfa,
0x59,
0x47,
0xf0,
0xad,
0xd4,
0xa2,
0xaf,
0x9c,
0xa4,
0x72,
0xc0,
0xb7,
0xfd,
0x93,
0x26,
0x36,
0x3f,
0xf7,
0xcc,
0x34,
0xa5,
0xe5,
0xf1,
0x71,
0xd8,
0x31,
0x15,
0x04,
0xc7,
0x23,
0xc3,
0x18,
0x96,
0x05,
0x9a,
0x07,
0x12,
0x80,
0xe2,
0xeb,
0x27,
0xb2,
0x75,
0x09,
0x83,
0x2c,
0x1a,
0x1b,
0x6e,
0x5a,
0xa0,
0x52,
0x3b,
0xd6,
0xb3,
0x29,
0xe3,
0x2f,
0x84,
0x53,
0xd1,
0x00,
0xed,
0x20,
0xfc,
0xb1,
0x5b,
0x6a,
0xcb,
0xbe,
0x39,
0x4a,
0x4c,
0x58,
0xcf,
0xd0,
0xef,
0xaa,
0xfb,
0x43,
0x4d,
0x33,
0x85,
0x45,
0xf9,
0x02,
0x7f,
0x50,
0x3c,
0x9f,
0xa8,
0x51,
0xa3,
0x40,
0x8f,
0x92,
0x9d,
0x38,
0xf5,
0xbc,
0xb6,
0xda,
0x21,
0x10,
0xff,
0xf3,
0xd2,
0xcd,
0x0c,
0x13,
0xec,
0x5f,
0x97,
0x44,
0x17,
0xc4,
0xa7,
0x7e,
0x3d,
0x64,
0x5d,
0x19,
0x73,
0x60,
0x81,
0x4f,
0xdc,
0x22,
0x2a,
0x90,
0x88,
0x46,
0xee,
0xb8,
0x14,
0xde,
0x5e,
0x0b,
0xdb,
0xe0,
0x32,
0x3a,
0x0a,
0x49,
0x06,
0x24,
0x5c,
0xc2,
0xd3,
0xac,
0x62,
0x91,
0x95,
0xe4,
0x79,
0xe7,
0xc8,
0x37,
0x6d,
0x8d,
0xd5,
0x4e,
0xa9,
0x6c,
0x56,
0xf4,
0xea,
0x65,
0x7a,
0xae,
0x08,
0xba,
0x78,
0x25,
0x2e,
0x1c,
0xa6,
0xb4,
0xc6,
0xe8,
0xdd,
0x74,
0x1f,
0x4b,
0xbd,
0x8b,
0x8a,
0x70,
0x3e,
0xb5,
0x66,
0x48,
0x03,
0xf6,
0x0e,
0x61,
0x35,
0x57,
0xb9,
0x86,
0xc1,
0x1d,
0x9e,
0xe1,
0xf8,
0x98,
0x11,
0x69,
0xd9,
0x8e,
0x94,
0x9b,
0x1e,
0x87,
0xe9,
0xce,
0x55,
0x28,
0xdf,
0x8c,
0xa1,
0x89,
0x0d,
0xbf,
0xe6,
0x42,
0x68,
0x41,
0x99,
0x2d,
0x0f,
0xb0,
0x54,
0xbb,
0x16
]

rcon = [
0x01000000,
0x02000000,
0x04000000,
0x08000000,
0x10000000,
0x20000000,
0x40000000,
0x80000000,
0x1b000000,
0x36000000
]

set_1_num_list = [
0x00000000000000000000000000000000,    
0x00000000000000000000000000000001,
0x00000000000000000000000000000002,
0x00000000000000000000000000000004,
0x00000000000000000000000000000008,
0x00000000000000000000000000000010,
0x00000000000000000000000000000020,
0x00000000000000000000000000000040,
0x00000000000000000000000000000080,
0x00000000000000000000000000000100,
0x00000000000000000000000000000200,
0x00000000000000000000000000000400,
0x00000000000000000000000000000800,
0x00000000000000000000000000001000,
0x00000000000000000000000000002000,
0x00000000000000000000000000004000,
0x00000000000000000000000000008000,
0x00000000000000000000000000010000,
0x00000000000000000000000000020000,
0x00000000000000000000000000040000,
0x00000000000000000000000000080000,
0x00000000000000000000000000100000,
0x00000000000000000000000000200000,
0x00000000000000000000000000400000,
0x00000000000000000000000000800000,
0x00000000000000000000000001000000,
0x00000000000000000000000002000000,
0x00000000000000000000000004000000,
0x00000000000000000000000008000000,
0x00000000000000000000000010000000,
0x00000000000000000000000020000000,
0x00000000000000000000000040000000,
0x00000000000000000000000080000000,
0x00000000000000000000000100000000,
0x00000000000000000000000200000000,
0x00000000000000000000000400000000,
0x00000000000000000000000800000000,
0x00000000000000000000001000000000,
0x00000000000000000000002000000000,
0x00000000000000000000004000000000,
0x00000000000000000000008000000000,
0x00000000000000000000010000000000,
0x00000000000000000000020000000000,
0x00000000000000000000040000000000,
0x00000000000000000000080000000000,
0x00000000000000000000100000000000,
0x00000000000000000000200000000000,
0x00000000000000000000400000000000,
0x00000000000000000000800000000000,
0x00000000000000000001000000000000,
0x00000000000000000002000000000000,
0x00000000000000000004000000000000,
0x00000000000000000008000000000000,
0x00000000000000000010000000000000,
0x00000000000000000020000000000000,
0x00000000000000000040000000000000,
0x00000000000000000080000000000000,
0x00000000000000000100000000000000,
0x00000000000000000200000000000000,
0x00000000000000000400000000000000,
0x00000000000000000800000000000000,
0x00000000000000001000000000000000,
0x00000000000000002000000000000000,
0x00000000000000004000000000000000,
0x00000000000000008000000000000000,
0x00000000000000010000000000000000,
0x00000000000000020000000000000000,
0x00000000000000040000000000000000,
0x00000000000000080000000000000000,
0x00000000000000100000000000000000,
0x00000000000000200000000000000000,
0x00000000000000400000000000000000,
0x00000000000000800000000000000000,
0x00000000000001000000000000000000,
0x00000000000002000000000000000000,
0x00000000000004000000000000000000,
0x00000000000008000000000000000000,
0x00000000000010000000000000000000,
0x00000000000020000000000000000000,
0x00000000000040000000000000000000,
0x00000000000080000000000000000000,
0x00000000000100000000000000000000,
0x00000000000200000000000000000000,
0x00000000000400000000000000000000,
0x00000000000800000000000000000000,
0x00000000001000000000000000000000,
0x00000000002000000000000000000000,
0x00000000004000000000000000000000,
0x00000000008000000000000000000000,
0x00000000010000000000000000000000,
0x00000000020000000000000000000000,
0x00000000040000000000000000000000,
0x00000000080000000000000000000000,
0x00000000100000000000000000000000,
0x00000000200000000000000000000000,
0x00000000400000000000000000000000,
0x00000000800000000000000000000000,
0x00000001000000000000000000000000,
0x00000002000000000000000000000000,
0x00000004000000000000000000000000,
0x00000008000000000000000000000000,
0x00000010000000000000000000000000,
0x00000020000000000000000000000000,
0x00000040000000000000000000000000,
0x00000080000000000000000000000000,
0x00000100000000000000000000000000,
0x00000200000000000000000000000000,
0x00000400000000000000000000000000,
0x00000800000000000000000000000000,
0x00001000000000000000000000000000,
0x00002000000000000000000000000000,
0x00004000000000000000000000000000,
0x00008000000000000000000000000000,
0x00010000000000000000000000000000,
0x00020000000000000000000000000000,
0x00040000000000000000000000000000,
0x00080000000000000000000000000000,
0x00100000000000000000000000000000,
0x00200000000000000000000000000000,
0x00400000000000000000000000000000,
0x00800000000000000000000000000000,
0x01000000000000000000000000000000,
0x02000000000000000000000000000000,
0x04000000000000000000000000000000,
0x08000000000000000000000000000000,
0x10000000000000000000000000000000,
0x20000000000000000000000000000000,
0x40000000000000000000000000000000,
0x00000000000000000000000000000000
]

clear_0_num_list = [
0xffffffffffffffffffffffffffffffff,    
0xfffffffffffffffffffffffffffffff1,
0xfffffffffffffffffffffffffffffff2,
0xfffffffffffffffffffffffffffffff4,
0xfffffffffffffffffffffffffffffff8,
0xffffffffffffffffffffffffffffff10,
0xffffffffffffffffffffffffffffff20,
0xffffffffffffffffffffffffffffff40,
0xffffffffffffffffffffffffffffff80,
0xfffffffffffffffffffffffffffff100,
0xfffffffffffffffffffffffffffff200,
0xfffffffffffffffffffffffffffff400,
0xfffffffffffffffffffffffffffff800,
0xffffffffffffffffffffffffffff1000,
0xffffffffffffffffffffffffffff2000,
0xffffffffffffffffffffffffffff4000,
0xffffffffffffffffffffffffffff8000,
0xfffffffffffffffffffffffffff10000,
0xfffffffffffffffffffffffffff20000,
0xfffffffffffffffffffffffffff40000,
0xfffffffffffffffffffffffffff80000,
0xffffffffffffffffffffffffff100000,
0xffffffffffffffffffffffffff200000,
0xffffffffffffffffffffffffff400000,
0xffffffffffffffffffffffffff800000,
0xfffffffffffffffffffffffff1000000,
0xfffffffffffffffffffffffff2000000,
0xfffffffffffffffffffffffff4000000,
0xfffffffffffffffffffffffff8000000,
0xffffffffffffffffffffffff10000000,
0xffffffffffffffffffffffff20000000,
0xffffffffffffffffffffffff40000000,
0xffffffffffffffffffffffff80000000,
0xfffffffffffffffffffffff100000000,
0xfffffffffffffffffffffff200000000,
0xfffffffffffffffffffffff400000000,
0xfffffffffffffffffffffff800000000,
0xffffffffffffffffffffff1000000000,
0xffffffffffffffffffffff2000000000,
0xffffffffffffffffffffff4000000000,
0xffffffffffffffffffffff8000000000,
0xfffffffffffffffffffff10000000000,
0xfffffffffffffffffffff20000000000,
0xfffffffffffffffffffff40000000000,
0xfffffffffffffffffffff80000000000,
0xffffffffffffffffffff100000000000,
0xffffffffffffffffffff200000000000,
0xffffffffffffffffffff400000000000,
0xffffffffffffffffffff800000000000,
0xfffffffffffffffffff1000000000000,
0xfffffffffffffffffff2000000000000,
0xfffffffffffffffffff4000000000000,
0xfffffffffffffffffff8000000000000,
0xffffffffffffffffff10000000000000,
0xffffffffffffffffff20000000000000,
0xffffffffffffffffff40000000000000,
0xffffffffffffffffff80000000000000,
0xfffffffffffffffff100000000000000,
0xfffffffffffffffff200000000000000,
0xfffffffffffffffff400000000000000,
0xfffffffffffffffff800000000000000,
0xffffffffffffffff1000000000000000,
0xffffffffffffffff2000000000000000,
0xffffffffffffffff4000000000000000,
0xffffffffffffffff8000000000000000,
0xfffffffffffffff10000000000000000,
0xfffffffffffffff20000000000000000,
0xfffffffffffffff40000000000000000,
0xfffffffffffffff80000000000000000,
0xffffffffffffff100000000000000000,
0xffffffffffffff200000000000000000,
0xffffffffffffff400000000000000000,
0xffffffffffffff800000000000000000,
0xfffffffffffff1000000000000000000,
0xfffffffffffff2000000000000000000,
0xfffffffffffff4000000000000000000,
0xfffffffffffff8000000000000000000,
0xffffffffffff10000000000000000000,
0xffffffffffff20000000000000000000,
0xffffffffffff40000000000000000000,
0xffffffffffff80000000000000000000,
0xfffffffffff100000000000000000000,
0xfffffffffff200000000000000000000,
0xfffffffffff400000000000000000000,
0xfffffffffff800000000000000000000,
0xffffffffff1000000000000000000000,
0xffffffffff2000000000000000000000,
0xffffffffff4000000000000000000000,
0xffffffffff8000000000000000000000,
0xfffffffff10000000000000000000000,
0xfffffffff20000000000000000000000,
0xfffffffff40000000000000000000000,
0xfffffffff80000000000000000000000,
0xffffffff100000000000000000000000,
0xffffffff200000000000000000000000,
0xffffffff400000000000000000000000,
0xffffffff800000000000000000000000,
0xfffffff1000000000000000000000000,
0xfffffff2000000000000000000000000,
0xfffffff4000000000000000000000000,
0xfffffff8000000000000000000000000,
0xffffff10000000000000000000000000,
0xffffff20000000000000000000000000,
0xffffff40000000000000000000000000,
0xffffff80000000000000000000000000,
0xfffff100000000000000000000000000,
0xfffff200000000000000000000000000,
0xfffff400000000000000000000000000,
0xfffff800000000000000000000000000,
0xffff1000000000000000000000000000,
0xffff2000000000000000000000000000,
0xffff4000000000000000000000000000,
0xffff8000000000000000000000000000,
0xfff10000000000000000000000000000,
0xfff20000000000000000000000000000,
0xfff40000000000000000000000000000,
0xfff80000000000000000000000000000,
0xff100000000000000000000000000000,
0xff200000000000000000000000000000,
0xff400000000000000000000000000000,
0xff800000000000000000000000000000,
0xf1000000000000000000000000000000,
0xf2000000000000000000000000000000,
0xf4000000000000000000000000000000,
0xf8000000000000000000000000000000,
0x10000000000000000000000000000000,
0x20000000000000000000000000000000,
0x40000000000000000000000000000000,
0xffffffffffffffffffffffffffffffff
]

def mixcolumns(b):
    if((b>>7)&0b1):
        xtime = (b<<1)&0xff^0x1b
    else:
        xtime = (b<<1)&0xff^0x00
    return xtime

def aes_cipher(textin,key):
    a=np.zeros((4,4),dtype=int)
    a_sb=np.zeros((4,4),dtype=int)
    a_sr=np.zeros((4,4),dtype=int)
    a_mc=np.zeros((4,4),dtype=int)
    a_next=np.zeros((4,4),dtype=int)
    for i in range(10):
        if(i == 0):
            wk3_sb = (aes_box[(key>>16)&0xff] << 24) + (aes_box[(key>>8)&0xff] << 16) + (aes_box[key&0xff] << 8) + aes_box[(key>>24)&0xff]
            wk0_next = wk3_sb ^ ((key>>96)&0xffffffff) ^ rcon[i]
            wk1_next = wk3_sb ^ ((key>>96)&0xffffffff) ^ rcon[i] ^ ((key>>64)&0xffffffff)
            wk2_next = wk3_sb ^ ((key>>96)&0xffffffff) ^ rcon[i] ^ ((key>>64)&0xffffffff) ^ ((key>>32)&0xffffffff)
            wk3_next = wk3_sb ^ ((key>>96)&0xffffffff) ^ rcon[i] ^ ((key>>64)&0xffffffff) ^ ((key>>32)&0xffffffff) ^ (key&0xffffffff)
            wk0r = wk0_next
            wk1r = wk1_next
            wk2r = wk2_next
            wk3r = wk3_next
            for j in range(4):
                for k in range(4):
                    a[j,k] = ((textin>>(128-(j+1)*8-k*32))&0xff)^((key>>(128-(j+1)*8-k*32))&0xff)
        else:
            wk3_sb = (aes_box[(wk3_next>>16)&0xff] << 24) + (aes_box[(wk3_next>>8)&0xff] << 16) + (aes_box[wk3_next&0xff] << 8) + aes_box[(wk3_next>>24)&0xff]
            wk0_next = wk3_sb ^ wk0r ^ rcon[i]
            wk1_next = wk3_sb ^ wk0r ^ rcon[i] ^ wk1r
            wk2_next = wk3_sb ^ wk0r ^ rcon[i] ^ wk1r ^ wk2r
            wk3_next = wk3_sb ^ wk0r ^ rcon[i] ^ wk1r ^ wk2r ^ wk3r 
            wk0r = wk0_next
            wk1r = wk1_next
            wk2r = wk2_next
            wk3r = wk3_next
            a=a_next
        # for i in range(4):
            # a_index = 0
            # if i == 0:
                # print("**********")
            # for j in range(4):
                # a_index+=a[i,j]<<(8*j)
                # if j == 3:
                    # print(hex(a_index))
        for j in range(4):
            for k in range(4):
                a_sb[j,k] = aes_box[a[j,k]]
        for j in range(4):
            for k in range(4):
                if k+j<4:
                    a_sr[j,k] = a_sb[j,(k+j)]
                else:
                    a_sr[j,k] = a_sb[j,(k+j-4)]
        # for i in range(4):
            # a_index = 0
            # b_index = 0
            # if i == 0:
                # print("**********")
            # for j in range(4):
                # a_index+=a_sb[i,j]<<(8*j)
                # b_index+=a_sr[i,j]<<(8*j)
                # if j == 3:
                    # print(hex(a_index))
                    # print(hex(b_index))
        for j in range(4):
            a_mc[0,j] = mixcolumns(a_sr[0,j])^mixcolumns(a_sr[1,j])^a_sr[1,j]^a_sr[2,j]^a_sr[3,j]
            a_mc[1,j] = a_sr[0,j]^mixcolumns(a_sr[1,j])^mixcolumns(a_sr[2,j])^a_sr[2,j]^a_sr[3,j]
            a_mc[2,j] = a_sr[0,j]^a_sr[1,j]^mixcolumns(a_sr[2,j])^mixcolumns(a_sr[3,j])^a_sr[3,j]
            a_mc[3,j] = mixcolumns(a_sr[0,j])^a_sr[0,j]^a_sr[1,j]^a_sr[2,j]^mixcolumns(a_sr[3,j])
        for j in range(4):
            a_next[j,0] = a_mc[j,0]^((wk0r>>(8*(3-j)))&0xff)
            a_next[j,1] = a_mc[j,1]^((wk1r>>(8*(3-j)))&0xff)
            a_next[j,2] = a_mc[j,2]^((wk2r>>(8*(3-j)))&0xff)
            a_next[j,3] = a_mc[j,3]^((wk3r>>(8*(3-j)))&0xff)
        # print(hex(wk0r),hex(wk1r),hex(wk2r),hex(wk3r))
        # for i in range(4):
            # a_index = 0
            # b_index = 0
            # if i == 0:
                # print("**********")
            # for j in range(4):
                # a_index+=a_mc[i,j]<<(8*j)
                # b_index+=a_next[i,j]<<(8*j)
                # if j == 3:
                    # print(hex(a_index))
                    # print(hex(b_index))
        # print(hex(a[0,0]))
        # for i in range(4):
            # a_index = 0
            # if i == 0:
                # print("**********")
            # for j in range(4):
                # a_index+=a_sr[i,j]<<(8*j)
                # if j == 3:
                    # print(hex(a_index))
        textout0 = 0
        textout1 = 0
        textout2 = 0
        textout3 = 0
        for j in range(4):
            textout0+=((a_sr[j,0]^(wk0r>>8*(3-j)&0xff))<<8*(3-j))
            textout1+=((a_sr[j,1]^(wk1r>>8*(3-j)&0xff))<<8*(3-j))
            textout2+=((a_sr[j,2]^(wk2r>>8*(3-j)&0xff))<<8*(3-j))
            textout3+=((a_sr[j,3]^(wk3r>>8*(3-j)&0xff))<<8*(3-j))
        textout=hex(textout0)[2:].zfill(8)+hex(textout1)[2:].zfill(8)+hex(textout2)[2:].zfill(8)+hex(textout3)[2:].zfill(8)
    return textout
def cmac_aes(textin,key,last_block_len):
    text_out_list=[]
    mask_128bit=0xffffffffffffffffffffffffffffffff
    text_len = textin.bit_length()
    cal_round = math.ceil(text_len/128)
    k1_k2_reg=int(aes_cipher(0,key),16)
    text_out_list.append(hex(k1_k2_reg))
    k1_k2_reg_shift1=k1_k2_reg<<1&mask_128bit
    if k1_k2_reg>>127&0b1:
        k1_temp=k1_k2_reg_shift1^0x87
    else:
        k1_temp=k1_k2_reg_shift1
    k1_temp_shift1=k1_temp<<1&mask_128bit
    if k1_temp>>127&0b1:
        k2_temp=k1_temp_shift1^0x87
    else:
        k2_temp=k1_temp_shift1
    # print(hex(k1_temp),'\n',hex(k2_temp),'\n',hex(k1_k2_select))
    iv_reg=0x0
    text_out=0x0
    for i in range(cal_round):
        text_cal=textin>>i*128&mask_128bit
        textin_cbc=iv_reg^text_cal
        # print(i,cal_round-1)
        if (i!=cal_round-1 and math.ceil(text_cal.bit_length()/4)*4==128) | (i==cal_round-1 and last_block_len==128):
            k1_k2_select = k1_temp
            # print('k1_temp')
        else:
            k1_k2_select = k2_temp
            # print('k2_temp')
        if i != cal_round-1:
            clear_0_num=0x0
            set_1_num=0x0
        else:
            clear_0_num=clear_0_num_list[last_block_len]
            set_1_num=set_1_num_list[last_block_len]
        textin_filled=(text_cal&clear_0_num)|set_1_num
        textin_last=iv_reg^textin_filled^k1_k2_select
        if i == cal_round-1:
            textin_temp=textin_last
        else:
            textin_temp=textin_cbc
        # print(text_len,last_block_len)
        # print(hex(clear_0_num),hex(set_1_num))
        # print('\n',hex(iv_reg),'\n',hex(k1_k2_select),'\n',hex(k1_temp),'\n',hex(k2_temp),'\n',hex(textin_temp),hex(key))
        text_out=int(aes_cipher(textin_temp,key),16)
        # print(hex(text_out))
        # print(i,text_out)
        iv_reg=text_out
        text_out_list.append(hex(text_out))
    return text_out_list
# textin=0x6bc1bee22e409f96e93d7e117393172a
# textin=0xae2d8a571e03ac9c9eb76fac45af8e51
# textin=0x30c81c46a35ce411e5fbc1191a0a52ef
# textin=0x30c81c46a35ce411e5fbc1191a0a52efae2d8a571e03ac9c9eb76fac45af8e516bc1bee22e409f96e93d7e117393172a
# key=0x2b7e151628aed2a6abf7158809cf4f3c
# last_block_len=128
# print(cmac_aes(textin,key,last_block_len))
# print(aes_cipher(textin,key))
# for a in aes_key_expand(key):
    # print(a)