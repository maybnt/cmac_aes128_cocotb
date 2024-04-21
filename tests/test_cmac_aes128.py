import cocotb
import random
from cocotb.triggers import RisingEdge,FallingEdge,ReadOnly
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb_bus.bus import Bus
from cocotb_bus.drivers import BusDriver
from cocotb_bus.monitors import BusMonitor
from cocotb_bus.scoreboard import Scoreboard
from cocotb.regression import TestFactory
import warnings
import math
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

class test_cmac_aes128:

    def __init__(self,dut,) -> None:
        self.dut=dut
        self.simulate_output=[]
        self.except_output=[]
        self.output_monitor = OutputMonitor(dut=dut,callback=self.simulate_output.append)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
        self.scoreboard = Scoreboard(dut,fail_immediately=False)
        # self.scoreboard.add_interface(self.output_monitor,self.except_output,strict_type=False)        

    async def wait_clk_edge(self,edge='raise',cycle_num=0):
        if edge == 'raise':
            for _ in range(cycle_num):
                await RisingEdge(self.dut.CLK)
        elif edge == 'fall':
            for _ in range(cycle_num):
                await FallingEdge(self.dut.CLK)

    async def reset_module(self) -> None:
        self.dut.Rst_n.value = 0
        self.dut.ld_Block.value = 0
        self.dut.ld_Key.value = 0
        self.dut.Last_Block.value = 0
        self.dut.Last_Block_Len.value = 0    
        self.dut.KEY.value = 0
        self.dut.TextIn.value = 0
        await self.wait_clk_edge('raise',4)
        self.dut.Rst_n.value = 1
        
    async def assign_key(self,key=0) -> None:
        await self.wait_clk_edge('raise',2)
        self.dut.ld_Key.value = 1
        self.dut.KEY.value = key
        await RisingEdge(self.dut.CLK)
        self.dut.ld_Key.value = 0

    async def assign_text(self,text_in=0,last_block_len=0,last_block=0) -> None:
        await FallingEdge(self.dut.Done)
        await Timer(500,units='ns')
        self.dut.ld_Block=1
        self.dut.Last_Block=last_block
        self.dut.TextIn=text_in
        self.dut.Last_Block_Len=last_block_len
        await RisingEdge(self.dut.CLK)
        await Timer(1,units='ns')    
        self.dut.ld_Block=0
        self.dut.Last_Block=0
        self.dut.TextIn=0
        self.dut.Last_Block_Len=0

async def run_test(dut,cfg) -> None:
    # print(hex(cfg[0]),hex(cfg[1]),hex(cfg[2]))
    clock = Clock(dut.CLK,10,units='ns')
    cocotb.start_soon(clock.start(start_high=False))
    dut=test_cmac_aes128(dut)
    dut.except_output=cmac_aes(cfg[0],cfg[1],cfg[2])
    dut.scoreboard.add_interface(dut.output_monitor,dut.except_output,strict_type=False)        
    await dut.reset_module()
    await dut.assign_key(cfg[1])
    for i in range(math.ceil(cfg[0].bit_length()/128)):
        if i==math.ceil(cfg[0].bit_length()/128)-1:
            await dut.assign_text(cfg[0]>>128*i&0xffffffffffffffffffffffffffffffff,cfg[2],1)
        else:
            await dut.assign_text(cfg[0]>>128*i&0xffffffffffffffffffffffffffffffff,cfg[2],0)
    await dut.wait_clk_edge('raise',20)
    raise dut.scoreboard.result

cfg0=[
0x30c81c46a35ce411e5fbc1191a0a52efae2d8a571e03ac9c9eb76fac45af8e516bc1bee22e409f96e93d7e117393172a,
0x2b7e151628aed2a6abf7158809cf4f3c,
0,
]

factory=TestFactory(run_test)
factory.add_option('cfg',[cfg0])
factory.generate_tests()
