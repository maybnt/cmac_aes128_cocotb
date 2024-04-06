import numpy as np
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
        print(textout)
    return textout
key = 0x2b7e151628aed2a6abf7158809cf4f3c
textin=0x9c1c12d244a2f95a1036bf0f97fe4611

print(aes_cipher(textin,key))
# for a in aes_key_expand(key):
    # print(a)