import cocotb
import random
from cocotb.triggers import RisingEdge,ReadOnly
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb_bus.bus import Bus
from cocotb_bus.drivers import BusDriver
from cocotb_bus.monitors import BusMonitor
from cocotb_bus.scoreboard import Scoreboard
import warnings
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
                cal_data = int(self.bus.TextOut.value)>>8
                self._recv(cal_data) 


@cocotb.test()
async def test_cmac_aes128(dut):
    clock = Clock(dut.CLK,10,units='ns')
    cocotb.start_soon(clock.start(start_high=False))

    dut.Rst_n.value = 0
    await Timer(100,units = 'ns')
    dut.Rst_n.value = 1

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
        input_bus.ld_Block.value = 1
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

    simulate_output = []
    output_monitor_inst = OutputMonitor(dut=dut,callback=simulate_output.append)
        
    except_output = []

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        scoreboard = Scoreboard(dut,fail_immediately=False)
    scoreboard.add_interface(output_monitor_inst,except_output)
    print(simulate_output)
    print(except_output)
    # print(dut.TextOut.value)
