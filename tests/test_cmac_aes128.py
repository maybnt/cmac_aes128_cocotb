import cocotb
import random
from cocotb.triggers import RisingEdge
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb_bus.bus import Bus
from cocotb_bus.drivers import BusDriver
# from cocotb.regression import TestFactory 
from cmac_aes128 import cmac_aes128

class PulseDriver(BusDriver):
    _signals = [
				'CLK',
				'cm_ld_Key',
				'cm_ld_Block',
				'Done',
				'cm_Last_Block',
				'cm_KEY',
				'cm_TextIn',
				'TextOut',
				'cm_Last_Block_Len'
            ]

    def __init__(self,dut):
        super().__init__(dut,'',dut.CLK)

    async def _driver_send(self,transaction,sync: bool = True) -> None:
        if sync:
            await RisingEdge(self.clock)
        self.bus <= transaction 

@cocotb.test()
async def test_cmac_aes128(dut):
    clock = Clock(dut.CLK,10,units='ns')
    cocotb.start_soon(clock.start(start_high=False))
    input_bus = Bus(dut,"cm",[
                              'ld_Key',
                              'ld_Block',
                              'Last_Block',
                              'KEY',
                              'TextIn',
                              'Last_Block_Len',
                                
    ],bus_separator = "_")
    pulse_driver = PulseDriver(dut)
    for i in range(10):
        input_bus.ld_Key.value = 1
        input_bus.ld_Block.value = 0
        input_bus.Last_Block.value = 0
        input_bus.KEY.value = random.randint(0,65535)
        input_bus.TextIn.value = random.randint(0,65535)
        input_bus.Last_Block_Len.value = 0
        transaction = [
                       input_bus.ld_Key,
                       input_bus.ld_Block,
                       input_bus.Last_Block,
                       input_bus.KEY,
                       input_bus.TextIn,
                       input_bus.Last_Block_Len,
                    ]
        await pulse_driver.send(transaction)
        

