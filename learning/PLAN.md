# Seven-month plan: RTL/ASIC design + embedded C

**Dec 1, 2026 → Jun 30, 2027. 31 weeks. Week 1 starts Mon Nov 30.**

Two job families, both reachable from where you are now:

| Family | Titles you will see | What they test |
|---|---|---|
| Digital design | RTL Design Engineer, FPGA Engineer, Design Verification (DV) Engineer, ASIC Design Engineer | Verilog/SV fluency, FSMs, FIFOs, CDC, timing, synthesis-aware coding, testbenches, for DV: constrained random, coverage, UVM concepts |
| Embedded | Embedded Software/Firmware Engineer, Embedded Systems Engineer, Bare-metal / BSP Engineer | C at the register level, pointers and memory layout, interrupts, DMA, linker scripts, RTOS, debugging with a probe, driver design, protocols |

Note: DV roles outnumber RTL-design roles for early-career candidates by a wide margin.
Month 6 gives DV real weight for that reason. "RTL firmware" is not a title; the SoC
project (months 4–6) is what lets you apply to both families with one portfolio.

Where you start: you have shipped production-ish ESP32 firmware (NimBLE central, nanopb,
FreeRTOS mutex, flash forensics). You have not written Verilog. The C track is therefore
"intermediate → senior fundamentals", the RTL track is "zero → interview-ready".

---

## Month-by-month

### Phase 0 · W1–W2 · Nov 30 – Dec 13 · Close out and set up

- Capstone demo Dec 10, final report. Nothing else is scheduled these two weeks.
- Order the hardware in README.md on Dec 1. Start the Vivado download now.
- Create a `training` repo (or keep this folder) with one directory per project:
  `rtl-basics/`, `fpga-uart/`, `fifo-cdc/`, `rv32-core/`, `rv32-soc/`, `stm32-bare/`,
  `stm32-bootloader/`, `tt-tapeout/`. Each gets a README on day one, even if it says "empty".
- Install the toolchains (README.md). Verify: `iverilog` sim of a 2-line module shows a
  waveform in GTKWave; `arm-none-eabi-gcc` builds and `openocd` flashes a blink onto the
  Nucleo. If either fails, that is the first week's bug hunt.

### Phase 1 · W3–W5 · Dec 14 – Jan 3 · Foundations

Holiday weeks. Plan for 20 h/week, not 35.

**RTL**
- Harris & Harris, *Digital Design and Computer Architecture (RISC-V ed.)* ch. 1–5:
  combinational logic, sequential logic, Verilog, digital building blocks. Do the exercises
  on paper first; the book's value is the mental model, not the syntax.
- HDLBits, start to finish. Target 60 % by Jan 3, 100 % by Jan 31. Every problem in Icarus
  locally before you paste it into the site. Keep the solutions in `rtl-basics/hdlbits/`.
- Learn to read waveforms before you learn to write testbenches. One hour in GTKWave with a
  counter and a known bug.
- Read Cummings, *Nonblocking Assignments in Verilog Synthesis, Coding Styles That Kill!*
  (Sunburst Design, free). Then re-do HDLBits problems you got right for the wrong reason.

**C**
- *Modern C* (Gustedt, free PDF) levels 0–2, fast. *Effective C* (Seacord, 2nd ed, **buy**)
  ch. 1–8 slower. You know C; what you are fixing is undefined behavior, integer promotion,
  strict aliasing, `volatile`, `restrict`, alignment, and what the standard actually guarantees.
- CS:APP (Bryant & O'Hallaron) ch. 1–3. Compile your own `nav.c` with `-O2 -S` for Cortex-M
  and read the assembly until it is boring.
- Host-side kata, test-driven with Unity/Ceedling: ring buffer, fixed-point haversine,
  CRC-16/32 (table and bitwise), a `printf`-free integer formatter, a tiny allocator.
  Each one: tests first, 100 % branch coverage, `cppcheck` and `clang-tidy` clean.
- Memfault Interrupt, *From Zero to main()* series (free). Then do it: Nucleo blink with
  **your own** linker script, startup file, vector table, and `SystemInit`. No HAL, no CMSIS
  beyond the header. Step through reset in GDB.

**Done when**
- HDLBits ≥ 60 %, all solved locally first.
- Nucleo blinks from a 3-file project (linker script, startup.c, main.c) you wrote.
- Five C katas with tests and coverage in `stm32-bare/host-tests/`.

### Phase 2 · W6–W9 · Jan 4 – Jan 31 · First real hardware on both tracks

**RTL**
- FSM coding (Cummings, *FSM Design Using SystemVerilog*): Moore vs Mealy, one-hot vs
  binary, the "output registered" pattern. Debounce, edge detect, PWM, seven-seg mux.
- UART TX and RX from scratch with oversampling and a baud generator. Synchronous FIFO
  (Cummings part 1 of the FIFO papers). Then a line-based command parser on the FPGA:
  type `set pwm 128` into a terminal, an LED dims.
- First bitstream on the iCEBreaker/Tang Nano with Yosys + nextpnr. Read the resource
  report. Change the design and watch the LUT count move.
- Same design on the Arty/Basys in Vivado. Write the XDC constraints by hand. Read the
  timing summary: what is WNS, what is a clock constraint, why an unconstrained design
  "passes". Pong Chu, *FPGA Prototyping by SystemVerilog Examples* is the companion here.
- Finish HDLBits.

**C**
- Peripheral drivers on the Nucleo, register level, from the reference manual (RM0390 for
  F446): GPIO, SysTick, NVIC priorities, EXTI, TIM (PWM and input capture), USART
  (polling → interrupt → DMA circular buffer), SPI, I2C. Each driver has a host-side unit
  test with the registers mocked as a struct.
- ISR discipline: what is allowed in an ISR, `volatile` vs memory barriers, atomic sections
  with `PRIMASK`/`BASEPRI`, lock-free single-producer/single-consumer ring buffer.
- Yiu, *The Definitive Guide to ARM Cortex-M3/M4* (**buy**) ch. on exceptions, stack frames,
  and faults. Deliberately cause a HardFault, decode `CFSR`, recover the faulting PC from
  the stacked frame. Write the fault handler you will reuse forever.
- Miro Samek, *Modern Embedded Systems Programming* video course, lessons 1–20. He builds
  exactly this from nothing.

**Convergence (Fridays)**: logic analyzer on both boards. Capture your FPGA UART, decode
it in PulseView, then capture the STM32 UART, compare. Write up a one-page "what I saw".

**Done when**
- UART command parser on FPGA, timing met in Vivado at 100 MHz with hand-written XDC.
- STM32 drivers: GPIO, SysTick, USART (DMA), TIM, SPI, I2C, with host tests.
- HardFault handler prints faulting PC, LR, and CFSR bits over UART.
- HDLBits 100 %.

### Phase 3 · W10–W13 · Feb 1 – Feb 28 · The hard interview topics

**RTL**
- Clock domain crossing. Cummings, *Clock Domain Crossing Design & Verification Techniques
  Using SystemVerilog* and *Simulation and Synthesis Techniques for Asynchronous FIFO
  Design*. Metastability, 2-flop synchronizers, Gray-code pointers, MTBF, why you never
  synchronize a bus. Build the async FIFO, parameterized, and stress it with cocotb random
  traffic across two unrelated clocks.
- SPI slave with a register map; I2C slave. Block RAM inference, read-before-write vs
  write-first, the inference rules of your two tools. Small pipelined datapath (multiply
  accumulate) to learn where registers go and why.
- SystemVerilog for design: `logic`, `always_ff`/`always_comb`, packages, interfaces,
  `enum` FSMs. Sutherland, *RTL Modeling with SystemVerilog* (**buy**) ch. 1–9.
- Verification, first pass: self-checking testbenches, cocotb + Verilator, immediate and
  concurrent assertions (SVA basics), what functional coverage is for. ZipCPU blog posts on
  FIFOs and formal are the best free material here.

**C**
- RTOS from the inside. Samek lessons 21–30: write a preemptive scheduler with context
  switch in assembly (PendSV), then compare with the FreeRTOS source. *Mastering the
  FreeRTOS Real Time Kernel* (free PDF) cover to cover.
- Priority inversion, inheritance, deadlock, stack sizing with watermarks, static allocation
  only, the MPU. Move the STM32 driver suite onto FreeRTOS with queues feeding a logger task.
- Low power: sleep modes, wake-on-interrupt, measuring current with a meter, tickless idle.

**Convergence (Fridays)**: `spi-regs`. STM32 is the SPI master, FPGA is the slave with a
register map (ID, scratch, PWM duty, a 32-bit counter you can read). Both sides have tests.
Logic-analyzer capture in the README.

**Done when**
- Async FIFO passes 1 M random transfers in cocotb at clock ratios 1:1, 3:7, 7:3, no data
  loss or duplication; one-page CDC notes you could teach from.
- Your own scheduler switches three tasks on the Nucleo; you can explain PendSV in one minute.
- `spi-regs` works end to end.

### Phase 4 · W14–W18 · Mar 1 – Apr 4 · A CPU, and the toolchain beneath C

**RTL**
- RV32I single-cycle core (Harris & Harris ch. 7, Patterson & Hennessy RISC-V ed. ch. 4).
  Then 5-stage pipeline with forwarding and hazard detection. Assemble tests with the
  RISC-V GNU toolchain; run the `riscv-tests` rv32ui suite in Verilator with a pass/fail
  signature.
- Synthesize on the Arty. Timing closure for real: setup/hold, slack, critical path, where
  to add a pipeline stage, false and multicycle paths, `set_clock_groups`. Bhasker & Chadha,
  *Static Timing Analysis for Nanometer Designs* ch. 1–4 as reference.
- Lint everything with `verilator --lint-only -Wall`. Fix every warning, learn why each exists.

**C**
- Linking in depth: CS:APP ch. 7. Sections, `.data` copy and `.bss` zero in your startup
  code, `KEEP`, `__attribute__((section))`, placing a function in RAM, map-file reading.
- Bootloader + application on the Nucleo: two linker scripts, vector table relocation
  (`VTOR`), UART firmware update with CRC and a rollback slot, jump to app with a clean
  stack. Memfault's bootloader posts are the guide.
- Flash key-value store with wear leveling and power-loss safety on the on-chip flash.
  You already did the forensics on NVS; now write the thing you were debugging.
- Build and quality: CMake + Ninja, `clang-format`, `cppcheck`, `clang-tidy`, Barr Group
  *Embedded C Coding Standard* (free), awareness of MISRA C:2023 categories. GitHub Actions
  CI: host tests on every push, firmware built with `arm-none-eabi-gcc`, and the firmware
  run in **Renode** so the UART output is checked without hardware.

**Convergence (Fridays)**: `rv32-core` README with a pipeline diagram, test signature
output, and Vivado timing/utilization table.

**Done when**
- Pipelined RV32I passes all rv32ui tests, meets timing at ≥ 50 MHz on Artix-7.
- Bootloader updates the app over UART, rejects a corrupted image, survives power loss
  mid-write (pull the USB cable during a test; it must boot the old image).
- CI badge green with Renode-run firmware tests.

### Phase 5 · W19–W22 · Apr 5 – May 2 · The ASIC flow

**ASIC**
- OpenLane 2 + Sky130 PDK: take the UART-with-register-map (not the CPU, keep it small)
  from RTL to GDS. Synthesis with Yosys, floorplan, placement, CTS, routing, DRC, LVS,
  antenna checks. Read the area, power, and timing reports at each stage.
- Concepts to be able to explain: standard cells and `.lib` files, SDC constraints,
  clock tree, hold fixing, IR drop, DFT and scan chains (concept level), clock gating
  and low-power basics, what an ECO is. Weste & Harris, *CMOS VLSI Design* ch. 1, 4, 8, 15
  selectively.
- Tiny Tapeout: read the current shuttle schedule, pick a design that fits a tile, run
  their template flow, submit if a deadline falls in May–June. A Tiny Tapeout entry is the
  cheapest real tape-out line on a résumé there is.
- Equivalence and lint: gate-level sim of the post-synthesis netlist against the RTL
  testbench.

**C**
- Robust driver design: timeouts on every bus transaction, bus recovery for a stuck I2C
  slave, watchdog with a kick-from-every-task policy, brown-out handling, error codes vs
  asserts, a structured logging/tracing path (SEGGER RTT or ITM).
- Protocol work on the Nucleo: nanopb on bare metal with a framed UART transport (COBS +
  CRC), the thing you did on the ESP32 but without the Arduino safety net. Optional: USB CDC
  from the register level.
- White, *Making Embedded Systems* 2nd ed (**buy**) in full; it is the book behind most
  embedded interviews.

**Convergence (Fridays)**: `tt-tapeout` repo with the GDS render, reports, and a
testbench; README written for someone who has never heard of OpenLane.

**Done when**
- DRC- and LVS-clean GDS of your own design, with a one-page flow summary.
- Tiny Tapeout submission made, or prepared and dated for the next shuttle.
- Nucleo firmware runs 72 h on the bench with watchdog and I2C recovery, no reset.

### Phase 6 · W23–W26 · May 3 – May 30 · Verification depth and the SoC

**DV**
- SystemVerilog classes, randomization with constraints, functional coverage groups,
  virtual interfaces. Spear, *SystemVerilog for Verification* ch. 1–9. UVM at the level of
  "I can read a UVM testbench and explain agent, driver, monitor, scoreboard"; build the
  same structure in cocotb so you can run it on Verilator.
- Write a verification plan for the RV32I core: features, coverage points, directed and
  random tests, pass criteria. Hit the coverage holes.
- Formal with SymbiYosys: prove the sync FIFO never overflows and the async FIFO pointers
  never skip a Gray code. ZipCPU's formal tutorials.
- Bus protocols: AXI4-Lite slave (formal-checked with ZipCPU's properties), Wishbone.

**SoC + C**
- `rv32-soc`: your core + UART + GPIO + timer + SPI + a small boot ROM on the Arty, memory
  mapped over AXI-Lite. Then the C side: `crt0.S`, linker script, drivers for **your own**
  peripherals, `printf` over your own UART, interrupt controller and a timer ISR.
- Port the capstone nav math (haversine, bearing, dead reckoning from `firmware-display/src/nav/`)
  to run on the SoC. Optional but memorable: a hardware fixed-point multiply-accumulate
  or CRC peripheral the firmware uses, with before/after cycle counts.
- Performance: cycle-counting with `mcycle`, where time goes, fixed-point vs float on a
  core without an FPU.

**Done when**
- SoC boots, prints a banner over UART, blinks via timer interrupt, runs the nav math and
  prints bearing/distance for a scripted pair of fixes.
- Verification plan with coverage ≥ 90 % on the core; two formal proofs passing.

### Phase 7 · W27–W31 · May 31 – Jul 4 · Portfolio, interviews, buffer

- Three polished repos: `rv32-soc` (RTL + firmware + DV), `stm32-bare` (drivers +
  bootloader + KV store + CI), `tt-tapeout` (GDS + reports). Each: diagram, how to run in
  under five minutes, screenshots of waveforms and timing reports, CI badge.
- One short technical write-up per repo (a blog post or the README itself). Hiring managers
  read the write-up; they rarely clone.
- Interview drills, daily, alternating:
  - **RTL/DV:** blocking vs nonblocking, FIFO depth calculation from burst/rate, CDC
    synchronizer design, Gray code, setup/hold and slack, latch inference, synthesizable
    vs not, FSM in 10 minutes on a whiteboard, "find the bug in this always block", UVM
    component roles, what coverage closure means.
  - **Embedded C:** `volatile`, bit manipulation puzzles, pointer-to-function tables,
    struct packing and alignment, endianness, memory layout of a running program, what
    happens from reset to `main`, interrupt latency, priority inversion, DMA vs
    interrupt vs polling trade-offs, debugging a HardFault from a stack dump, "write a
    circular buffer on the whiteboard".
- Apply from June 1. Target 3–5 applications a week to RTL, DV, FPGA, and embedded roles.
  Two mock interviews a week with anyone technical you can find.
- The final two weeks are buffer. Something in phases 4–6 will slip; this is where it lands.

---

## Resources

**Free, use heavily**
- HDLBits — hdlbits.01xz.net
- Sunburst Design papers (Cliff Cummings) — sunburst-design.com/papers
- ZipCPU blog (Dan Gisselquist) — zipcpu.com. FIFOs, AXI, formal, debugging on FPGA
- Memfault Interrupt blog — interrupt.memfault.com. Zero to main(), bootloaders, faults
- Miro Samek, *Modern Embedded Systems Programming* (YouTube)
- *Mastering the FreeRTOS Real Time Kernel* (FreeRTOS.org PDF)
- Jens Gustedt, *Modern C* (free PDF)
- OpenLane 2 docs, Tiny Tapeout docs, SymbiYosys docs, cocotb docs, Renode docs
- Barr Group *Embedded C Coding Standard* (free PDF)
- STM32F446 reference manual RM0390 and the Cortex-M4 Generic User Guide. Read the actual documents, not forum posts.

**Buy (three books)**
- Seacord, *Effective C*, 2nd ed.
- Yiu, *The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors*, 3rd ed.
- White, *Making Embedded Systems*, 2nd ed.

**Buy or borrow**
- Harris & Harris, *Digital Design and Computer Architecture*, RISC-V ed.
- Sutherland, *RTL Modeling with SystemVerilog for Simulation and Synthesis*
- Spear, *SystemVerilog for Verification*, 3rd ed.
- Chu, *FPGA Prototyping by SystemVerilog Examples*, 2nd ed.
- Bryant & O'Hallaron, *Computer Systems: A Programmer's Perspective*, 3rd ed. (ch. 1–3, 6, 7, 9)
- Patterson & Hennessy, *Computer Organization and Design*, RISC-V ed. (ch. 4 only)
- Grenning, *Test-Driven Development for Embedded C*
- Weste & Harris, *CMOS VLSI Design*, 4th ed. (reference, selective)
- Bhasker & Chadha, *Static Timing Analysis for Nanometer Designs* (reference)

## Rules that keep this on track

1. **Hardware every week from W6.** Simulation-only Verilog and host-only C both lie.
2. **Tests before features**, on both tracks. A module without a testbench is not done. A
   driver without a host test is not done.
3. **Write the weekly log on Saturday** (`log/TEMPLATE.md`). Thirty lines. What you
   built, what broke, what you now understand that you did not on Monday.
4. **One convergence project per month, always on Fridays.** It is the portfolio.
5. **Read the primary source.** Reference manual, standard, paper. Forum answers are for
   finding which page of the manual to read.
6. **Ask for review.** Post the async FIFO, the bootloader, and the core on r/FPGA,
   r/embedded, or to anyone senior you know. Being corrected in public in February is
   cheaper than in an interview in June.
