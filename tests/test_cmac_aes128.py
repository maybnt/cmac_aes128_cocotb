import cocotb
import random
from cocotb.triggers import RisingEdge,FallingEdge,ReadOnly
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb_bus.bus import Bus
from cocotb_bus.drivers import BusDriver
from cocotb_bus.monitors import BusMonitor
from cocotb_bus.scoreboard import Scoreboard
import warnings
# from cocotb.log import SimLog
# from cocotb.regression import TestFactory 
from cmac_aes128 import cmac_aes

class PulseDriver(BusDriver):
    _signals = []

    def __init__(self,dut): #创建初始化函数
        super().__init__(dut,'',dut.CLK) #super()可以用于调用父类的，等同于BusDriver.__init__(dut,'',dut.CLK)

    async def _driver_send(self,transaction,sync: bool = True) -> None: #定义异步函数，这个函数可以挂起，等某个操作完成之后再执行
        if sync:
            await RisingEdge(self.clock) #clock是从BusDriver中继承而来，在初始化函数中把它赋值为dut.CLK
        self.bus <= transaction # bus也是继承自BusDriver

class OutputMonitor(BusMonitor):
    """
        监控verilog的仿真数据结果
    """
    _signals = [
        'TextOut',
        'Done',
    ]
    def __init__(self, dut, callback=None, event=None):
        super().__init__(dut, '', dut.CLK, callback=callback, event=event)

    async def _monitor_recv(self):
        while True:
            await RisingEdge(self.clock)
            await ReadOnly()

            if self.bus.Done.value:
                cal_data = self.bus.TextOut.value
                self._recv(hex(cal_data)) 

@cocotb.test()
async def test_cmac_aes128(dut):
    clock = Clock(dut.CLK,10,units='ns')
    cocotb.start_soon(clock.start(start_high=False))
    pulse_driver = PulseDriver(dut)
    dut.Rst_n.value = 0
    simulate_output = []
    except_output=[]
    textin=0x30c81c46a35ce411e5fbc1191a0a52efae2d8a571e03ac9c9eb76fac45af8e516bc1bee22e409f96e93d7e117393172a
    key=0x2b7e151628aed2a6abf7158809cf4f3c
    last_block_len=128
    except_output=cmac_aes(textin,key,last_block_len)
    print('++++++++++++++++++++++++expect output0++++++++++++++++++++++++')
    print(except_output)
    key=0x2b7e151628aed2a6abf7158809cf4f3c
    textin=0
    last_block_len=0
    dut.ld_Block.value = 0
    dut.ld_Key.value = 0
    dut.Last_Block.value = 0
    dut.Last_Block_Len.value = 0    
    dut.KEY.value = 0x2b7e151628aed2a6abf7158809cf4f3c
    dut.TextIn.value = 0
    for _ in range(4):
        await RisingEdge(dut.CLK)
    dut.Rst_n.value = 1
    for _ in range(2):
        await RisingEdge(dut.CLK)
    dut.ld_Key.value = 1
    await RisingEdge(dut.CLK)
    dut.ld_Key.value = 0
    output_monitor_inst = OutputMonitor(dut=dut,callback=simulate_output.append)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    scoreboard = Scoreboard(dut,fail_immediately=False)
    scoreboard.add_interface(output_monitor_inst,except_output,reorder_depth=1,strict_type=False)
    print('++++++++++++++++++++++++expect output1++++++++++++++++++++++++')
    print(except_output)

    textin=0x6bc1bee22e409f96e93d7e117393172a
    last_block_len=128
    await FallingEdge(dut.Done)
    await Timer(500,units='ns')
    dut.ld_Block=1
    dut.Last_Block=0
    dut.TextIn=textin
    dut.Last_Block_Len=last_block_len
    await RisingEdge(dut.CLK)
    await Timer(1,units='ns')    
    dut.ld_Block=0
    dut.Last_Block=0
    dut.TextIn=0
    dut.Last_Block_Len=0
    # scoreboard.add_interface(output_monitor_inst,except_output,reorder_depth=1,strict_type=False)
    print('++++++++++++++++++++++++expect output2++++++++++++++++++++++++')
    print(except_output)

    textin=0xae2d8a571e03ac9c9eb76fac45af8e51
    last_block_len=128
    await FallingEdge(dut.Done)
    await Timer(500,units='ns')
    dut.ld_Block=1
    dut.Last_Block=0
    dut.TextIn=textin
    dut.Last_Block_Len=last_block_len
    await RisingEdge(dut.CLK)
    await Timer(1,units='ns')    
    dut.ld_Block=0
    dut.Last_Block=0
    dut.TextIn=0
    dut.Last_Block_Len=0
    # scoreboard.add_interface(output_monitor_inst,except_output,reorder_depth=1,strict_type=False)
    print('++++++++++++++++++++++++expect output3++++++++++++++++++++++++')
    print(except_output)

    textin=0x30c81c46a35ce411e5fbc1191a0a52ef
    last_block_len=128
    await FallingEdge(dut.Done)
    await Timer(500,units='ns')
    dut.ld_Block=1
    dut.Last_Block=1
    dut.TextIn=textin
    dut.Last_Block_Len=last_block_len
    await RisingEdge(dut.CLK)
    await Timer(1,units='ns')    
    dut.ld_Block=0
    dut.Last_Block=0
    dut.TextIn=0
    dut.Last_Block_Len=0
    for _ in range(20):
        await RisingEdge(dut.CLK)
    # scoreboard.add_interface(output_monitor_inst,except_output,reorder_depth=1,strict_type=False)
    print('++++++++++++++++++++++++expect output4++++++++++++++++++++++++')
    print(except_output)

    # except_output = ['0','0','0','0','0','0','0','0','0','0']
    # for i in range(100):
        # input_bus.ld_Key.value = 1
        # input_bus.ld_Block.value = 1
        # input_bus.Last_Block.value = 0
        # input_bus.KEY.value = random.randint(0,65535)
        # input_bus.TextIn.value = random.randint(0,65535)
        # input_bus.Last_Block_Len.value = 0
        # transaction = [
                    #    input_bus.ld_Key,
                    #    input_bus.ld_Block,
                    #    input_bus.Last_Block,
                    #    input_bus.KEY,
                    #    input_bus.TextIn,
                    #    input_bus.Last_Block_Len,
                    # ]
        # await pulse_driver.send(transaction)
        # output_monitor_inst = OutputMonitor(dut=dut,callback=simulate_output.append)
        # with warnings.catch_warnings():
            # warnings.simplefilter("ignore")
        # scoreboard = Scoreboard(dut,fail_immediately=True)
        # scoreboard.add_interface(output_monitor_inst,except_output,reorder_depth=10,strict_type=False)
    
    # for a in simulate_output:
        # print(a)

    # with warnings.catch_warnings():
        # warnings.simplefilter("ignore")
        # scoreboard = Scoreboard(dut,fail_immediately=True)
    # scoreboard.add_interface(output_monitor_inst,except_output,reorder_depth=10,strict_type=False)
    # print('**************test result**************')
    # assert scoreboard.result 
    # print(dut.TextOut.value)
