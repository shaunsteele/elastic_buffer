# tb_control_transfer.py
# test cases:
# - valid and ready
# - multiple valid and ready
# - valid then ready
# - buffer test
# - buffer full test


import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, FallingEdge


async def reset_check(dut):
  await FallingEdge(dut.clk)
  assert dut.o_valid.value == 0
  assert dut.o_ready.value == 0
  cocotb.log.info("Reset Test Passed")


async def valid_and_ready(dut):
  await FallingEdge(dut.clk)
  assert dut.o_ready.value
  dut.i_valid.value = 1
  dut.i_data.value = 0x01
  dut.i_ready.value = 1

  await RisingEdge(dut.clk)
  await FallingEdge(dut.clk)
  assert dut.o_valid.value
  assert dut.o_data.value == 0x01
  cocotb.log.info("Valid and Ready Passed")
  dut.i_valid.value = 0
  await RisingEdge(dut.clk)


async def valid_and_ready_mul(dut):
  await FallingEdge(dut.clk)
  for i in range(0x10):
    assert dut.o_ready.value
    dut.i_valid.value = 1
    dut.i_data.value = i
    dut.i_ready.value = 1

    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    assert dut.o_valid.value
    assert dut.o_data.value == i
  cocotb.log.info("Multiple Valid and Ready Passed")
  dut.i_valid.value = 0
  await RisingEdge(dut.clk)


async def valid_then_ready(dut):
  await FallingEdge(dut.clk)
  assert dut.o_ready.value
  dut.i_valid.value = 1
  dut.i_data.value = 0x10
  dut.i_ready.value = 0

  await RisingEdge(dut.clk)
  await FallingEdge(dut.clk)
  assert dut.o_valid.value
  assert dut.o_data.value == 0x10
  dut.i_valid.value = 0
  dut.i_ready.value = 1

  await RisingEdge(dut.clk)
  await FallingEdge(dut.clk)
  assert dut.o_valid.value == 0
  cocotb.log.info("Valid then Ready Passed")
  dut.i_ready.value = 0
  await RisingEdge(dut.clk)


async def buffer_test(dut):
  await FallingEdge(dut.clk)
  assert dut.o_ready.value
  dut.i_valid.value = 1
  dut.i_data.value = 0x55
  dut.i_ready.value = 0

  await RisingEdge(dut.clk)
  await FallingEdge(dut.clk)
  assert dut.o_valid.value
  assert dut.o_data.value == 0x55
  dut.i_data.value = 0xAA

  await RisingEdge(dut.clk)
  await FallingEdge(dut.clk)
  assert dut.o_valid.value
  assert dut.o_data.value == 0x55
  assert dut.o_ready.value == 0
  dut.i_valid.value = 0
  dut.i_ready.value = 1

  await RisingEdge(dut.clk)
  await FallingEdge(dut.clk)
  assert dut.o_valid.value
  assert dut.o_data.value == 0xAA
  assert dut.o_ready.value

  await RisingEdge(dut.clk)
  await FallingEdge(dut.clk)
  assert dut.o_valid.value == 0
  cocotb.log.info("Buffer Test Passed")
  dut.i_ready.value = 0

  await RisingEdge(dut.clk)


async def buffer_full_test(dut):
  await FallingEdge(dut.clk)
  assert dut.o_ready.value
  dut.i_valid.value = 1
  dut.i_data.value = 0x01
  dut.i_ready.value = 0

  await RisingEdge(dut.clk)
  await FallingEdge(dut.clk)
  dut.i_data.value = 0x02

  # write 2
  await RisingEdge(dut.clk)
  await FallingEdge(dut.clk)
  assert dut.o_ready.value == 0
  dut.i_data.value = 0x03

  # write 3
  await RisingEdge(dut.clk)
  await FallingEdge(dut.clk)
  dut.i_ready.value = 1

  await RisingEdge(dut.clk)
  await FallingEdge(dut.clk)
  assert dut.o_ready.value

  await RisingEdge(dut.clk)
  await FallingEdge(dut.clk)
  dut.i_ready.value = 0
  dut.i_valid.value = 0
  cocotb.log.info("Buffer Full Test Passed")

  await RisingEdge(dut.clk)


@cocotb.test()
async def tb_elastic_buffer(dut):
  # initialize inputs
  dut.rstn.value = 0
  dut.i_valid.value = 0
  dut.i_data.value = 0
  dut.i_ready.value = 0

  # start clock
  cocotb.start_soon(Clock(dut.clk, 10, "ns").start())

  # reset raise
  await ClockCycles(dut.clk, 10)
  dut.rstn.value = 1

  # test cases
  await reset_check(dut)
  await valid_and_ready(dut)
  await valid_and_ready_mul(dut)
  await valid_then_ready(dut)
  await buffer_test(dut)
  await buffer_full_test(dut)

  await ClockCycles(dut.clk, 10)
  cocotb.log.info("Testing Completed")
