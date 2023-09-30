import cocotb
from cocotb.triggers import RisingEdge
from cocotb.triggers import Timer
from cocotb.clock import Clock
# from cocotb.regression import TestFactory 
from cmac_aes128 import cmac_aes128

print('*************************************begin**********************************')




@cocotb.test()
async def test_cmac_aes128(dut):
    dut.CLK.value = 0
    dut.Rst_n.value = 0
    dut.ld_Block.value = 0
    dut.ld_Key.value = 1
    dut.Last_Block.value = 0
    dut.Last_Block_Len.value = 0
    dut.TextIn.value = 0
    dut.KEY.value = 0x2b7e151628aed2a6abf7158809cf4f3c
    print('***************************init done**********************************')
    clock = Clock(dut.CLK,10,units="ns")
    cocotb.start_soon(clock.start(start_high = False))
    print('***************************clock running**********************************')
    await Timer(100,units = 'ns')
    dut.Rst_n.value = 1
    await Timer(200,units = 'ns')
    dut.ld_Key.value = 0
    print('***************************reset done**********************************')
    await Timer(500,units = 'ns')
    dut.ld_Block.value = 1
    dut.Last_Block.value = 1
    dut.Last_Block_Len.value = 0
    dut.TextIn.value = 0x6bc1bee22e409f96e93d7e117393172a
    print('***************************value init**********************************')
    await RisingEdge(dut.CLK)
    dut.ld_Block.value = 0
    dut.Last_Block.value = 0
    dut.Last_Block_Len.value = 0
    dut.TextIn.value = 0
    print('***************************value init done**********************************')
    await RisingEdge(dut.Done)
    print(hex(dut.TextOut.value))
    print('***************************&&&&&&&&&&&&&&&**********************************')
# 定义一个十六进制数
    hex_number = '6bc1bee22e409f96e93d7e117393172a'

# 使用hex()函数将十六进制数转换为字符串
    # string_number = hex(hex_number)
    # string_number = str(string_number)
    # string_number = string_number[2:]
# hex()函数生成的字符串前缀为'0x'，所以需要将其去除
    # print(string_number)
    print(cmac_aes128(hex_number))

