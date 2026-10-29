# Deo · Dec 2026 – Jun 2027 training plan

Two targets, one portfolio:

1. **RTL / ASIC design** — Verilog and SystemVerilog, FPGA bring-up, static timing,
   verification, and one pass through a real open-source ASIC flow (Sky130 via OpenLane,
   Tiny Tapeout).
2. **Embedded C** — bare-metal Cortex-M (no Arduino, no HAL), linker scripts and startup
   code, interrupt-driven and DMA drivers, RTOS internals, bootloaders, test-driven
   firmware. You already ship ESP32 firmware; this track takes you from "it works" to
   "I know exactly why it works".

The two tracks converge in March–May on **your own RISC-V SoC on an FPGA running your own
C firmware**, which is the one project that proves both skills to either kind of hiring
manager.

| File | What it is |
|---|---|
| [PLAN.md](PLAN.md) | The full curriculum: month by month, weekly detail, milestones with "done when" checks, book and tool list, interview prep |
| [tasks.json](tasks.json) | Same plan as Gantt rows (edit this, not the HTML) |
| [Training_Gantt.html](Training_Gantt.html) | Interactive 31-week Gantt (open in a browser; hover a week) |
| `build_gantt.py` / `Update_Gantt.bat` | Regenerate the Gantt from `tasks.json` (same tool as `planning/`) |
| [log/TEMPLATE.md](log/TEMPLATE.md) | Weekly log template. One file per week, `log/2026-W50.md` etc. |

## Calendar

| Phase | Weeks | Dates | Theme |
|---|---|---|---|
| 0 | W1–W2 | Nov 30 – Dec 13 | Finish capstone (demo Dec 10). Order boards. Install toolchains. |
| 1 | W3–W5 | Dec 14 – Jan 3 | Foundations: digital logic + Verilog syntax, C memory model, first bare-metal blink |
| 2 | W6–W9 | Jan 4 – Jan 31 | FSMs, UART, FIFOs on real FPGA. Bare-metal STM32 peripherals and interrupts |
| 3 | W10–W13 | Feb 1 – Feb 28 | CDC and async FIFO, SPI/I2C, SystemVerilog, cocotb. RTOS internals, write a scheduler |
| 4 | W14–W18 | Mar 1 – Apr 4 | RV32I core (single-cycle → pipelined), STA. Linker scripts, bootloader, flash KV store, CI |
| 5 | W19–W22 | Apr 5 – May 2 | ASIC flow: OpenLane + Sky130 to GDS, Tiny Tapeout prep. Robust driver design, protocols |
| 6 | W23–W26 | May 3 – May 30 | Verification depth (constrained random, SVA, formal). SoC integration, C firmware on your core |
| 7 | W27–W31 | May 31 – Jul 4 | Portfolio polish, interview drills, applications. Buffer for slippage |

## Weekly rhythm (assumes ~30–35 focused hours)

- **Mon + Wed:** RTL day (reading in the morning, lab in the afternoon)
- **Tue + Thu:** C day (same shape)
- **Fri:** convergence project only (the thing that uses both tracks this month)
- **Sat (2–3 h):** HDLBits or C drills, write the weekly log, plan next week
- **Sun:** off. Seven months is a marathon.

If you have fewer hours, keep the order and stretch the phases; do not drop the Friday
project or the Saturday log. The log is what turns seven months into a story you can tell
in an interview.

## Shopping list (order in W1, total roughly $250–350)

| Item | Why | Approx |
|---|---|---|
| **iCEBreaker** (Lattice iCE40UP5K) or **Tang Nano 9K** (Gowin) | Fully open-source flow (Yosys + nextpnr), seconds to bitstream, great for the first 2 months | $20–80 |
| **Digilent Arty A7** or **Basys 3** (Xilinx Artix-7) | Vivado is what employers use. Timing reports, ILA, block RAM, enough LUTs for the RISC-V SoC | $150–250 |
| **STM32 Nucleo-F446RE** (or F411RE / G474RE) | Cortex-M4F with onboard ST-Link. The bare-metal track lives here | $15–25 |
| Cheap 8-channel USB logic analyzer (Sigrok/PulseView) | See your UART/SPI/I2C bits on the wire. Non-negotiable for driver work | $10–15 |
| Jumper wires, breadboard, a few I2C/SPI sensors (BME280, MPU-6050, an SPI flash chip) | Driver targets | $20–30 |
| Optional: Raspberry Pi Pico (RP2040) | PIO is a nice bridge between "firmware" and "RTL thinking" | $5 |

Books are listed in PLAN.md. Most of the course material is free; buy the three books
marked **buy**.

## Toolchain install (W1–W2, do it before Dec 14)

```bash
# RTL
sudo apt install iverilog gtkwave verilator yosys nextpnr-ice40 fpga-icestorm   # or build from source for current versions
pip install cocotb cocotb-test pytest
# Vivado ML Standard (free) from AMD for the Arty/Basys; ~40 GB, start the download early
# OpenLane 2 (needs Docker or Nix): https://openlane2.readthedocs.io
# SymbiYosys + Yosys for formal: https://symbiyosys.readthedocs.io

# Embedded C
sudo apt install gcc-arm-none-eabi gdb-multiarch openocd cmake ninja-build cppcheck clang-tidy clang-format
pip install pyocd    # alternative to OpenOCD for ST-Link
gem install ceedling # Unity + CMock test runner
# Renode (https://renode.io) to run STM32 firmware in CI without hardware
# RISC-V GNU toolchain (riscv64-unknown-elf-gcc) for month 4+
```
