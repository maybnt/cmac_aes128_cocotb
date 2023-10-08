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
				'ld_Key',
				'ld_Block',
				'Done',
				'Last_Block',
				'KEY',
				'TextIn',
				'TextOut',
				'Last_Block_Len'
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
    pulse_driver = PulseDriver(dut)
    for i in range(10):
        dut.ld_Key.value = 1
        dut.ld_Block.value = 1
        dut.Rst_n.value = 1
        dut.Last_Block.value = 0
        dut.KEY.value = random.randint(0,65535)
        dut.TextIn.value = random.randint(0,65535)
        dut.Last_Block_Len.value = 0
        transaction = [
                       dut.ld_Key,
                       dut.ld_Block,
                       dut.Last_Block,
                       dut.KEY,
                       dut.TextIn,
                       dut.Last_Block_Len,
                    ]
        await pulse_driver.send(transaction)
        

