`timescale 1ns / 1ps
`include "instruction_head.v"

module CPU_Ctrl(
    // signal: system -> cpu
    input wire clk,
    input wire rst,
    input wire start,
    input wire cpu_wake,   // wake signal from cpu
    input wire cpu_slep,   // sleep signal from cpu

    // input interface: system -> cpu
    input wire [31:0] sys_inf_in, // system input interface

    // signal: cpu -> system
    output reg cpu_stat,
    output reg sysc_mp, 
    output wire [`SYS_OP_LENGTH - 1:0] sys_op, // syscall operation from cpu

    // output interface: cpu -> system
    output wire[31:0] sys_inf_out, // system output interface

    // debug information: cpu -> system
    output wire [7:0] debug_reg_single,
    output wire [5:0] debug_opcode,
    output wire [5:0] debug_func,
    output wire [7:0] debug_dm_single,
    output wire [9:0] debug_pc,
    output wire [7:0] debug_alu,

    output wire halt    // halt signal from cpu
    );

    wire syscall; // syscall signal to cpu

    wire clk_div;
    wire clk_cpu;  // cpu clock
    assign clk_cpu = (cpu_stat) ? clk_div : 0;

    initial begin
        cpu_stat = 0;
        sysc_mp = 0;
    end

    // change the syscall signal to a mono pulse signal
    reg syc_flg = 1;
    always @ (posedge clk) begin
        if (!syscall) begin 
            syc_flg <= 1;
            sysc_mp <= 0;
        end else begin
            if (syc_flg) begin
                sysc_mp <= 1;
                syc_flg <= 0;
            end else begin
                sysc_mp <= 0;
            end
        end
    end

    // control the cpu state
    always @ (posedge clk) begin
        if (cpu_wake || start)
            cpu_stat <= 1;
        else if (cpu_slep || halt) 
            cpu_stat <= 0;
    end

    CLK_Div #(.N(`CLK_CPU_DELAY)) INST_CLK_DIV(
        .clk_in(clk),
        .clk_out(clk_div));

    Top_CPU INST_TOP_CPU(
        .clk(clk_cpu),
        .rst(rst),

        .halt(halt),
        .syscall(syscall),
        .sys_op(sys_op),

        .sys_inf_in(sys_inf_in),
        .sys_inf_out(sys_inf_out),

        // debug information
        .debug_reg_single(debug_reg_single),
        .debug_opcode(debug_opcode),
        .debug_func(debug_func),
        .debug_dm_single(debug_dm_single),
        .debug_pc(debug_pc),
        .debug_alu(debug_alu));
endmodule