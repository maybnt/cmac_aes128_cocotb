SIM ?= questa

PWD=$(shell pwd)

export PYTHONPATH := $(PWD)/../model:$(PYTHONPATH)

HDL_PATH =$(PWD)/../hdl

# 遍历hdl文件夹下的所有文件，最大深度3
DIRS = $(shell find $(HDL_PATH) -maxdepth 3 -type d)
DIRS_EXC_DIRS = $(shell find $(DIRS_EXC_PATH) -maxdepth 3 -type d)
DIRS := $(filter-out $(DIRS_EXC_DIRS), $(DIRS))

# 包含verilog文件
VERILOG_SOURCES += $(foreach dir, $(DIRS), $(wildcard $(dir)/*.v))
VERILOG_SOURCES += $(foreach dir, $(DIRS), $(wildcard $(dir)/*.sv))

TOPLEVEL := CMAC_Top_v2

TOPLEVEL_LANG ?= verilog

MODULE := test_cmac_aes128

# 保存波形
ifeq ($(SIM),verilator)
EXTRA_ARGS += --trace --trace-structs
# EXTRA_ARGS += --threads {4}
# EXTRA_ARGS += --trace-fst
# EXTRA_ARGS += --coverage
else ifeq ($(SIM),questa)
WAVES = 1
endif

include $(shell cocotb-config --makefiles)/Makefile.sim