
REPO_DIR := /home/shaun/repos/elastic_buffer

RTL_DIR := $(REPO_DIR)/rtl

SIM ?= verilator

EXTRA_ARGS += --trace --trace-structs

TOPLEVELLANG ?= verilog

VERILOG_SOURCES += $(RTL_DIR)/elastic_buffer.sv

TOPLEVEL = elastic_buffer

MODULE = tb_elastic_buffer

include $(shell cocotb-config --makefiles)/Makefile.sim

WAVEFILE = dump.vcd

.PHONY: waves
waves:
	gtkwave $(WAVEFILE)
