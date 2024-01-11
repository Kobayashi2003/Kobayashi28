`timescale 1ns / 1ps
`include "instruction_head.v"

module RegisterFile(

    input wire          syscall,
    output wire[31:0]   sys_out,

    input wire          clk,
    input wire          reg_write,          // "Register Write" signal

    input wire[4:0]     read_reg1_addr,     // Register rs address
    input wire[4:0]     read_reg2_addr,     // Register rt address
    input wire[4:0]     write_reg_addr,     // "Write" target register address
    input wire[31:0]    write_data,         // "Write" target register data

    output wire [31:0]  reg1_data,          // Register rs data
    output wire [31:0]  reg2_data,          // Register rt data

    output wire [`SYS_OP_LENGTH - 1:0] sys_op, // System operation signal

    output wire[7:0]    debug_reg_single    // Debug signal
    );

    // General purpose register
    reg [31:0]          gpr[31:0];

    integer i;
    initial begin
        for (i = 0; i < 32; i = i + 1) gpr[i] = 0;
    end

    // System operation signal
    assign sys_op  = gpr[2][`SYS_OP_LENGTH - 1:0]; // $v0
    assign sys_out = (syscall && (sys_op == `SYSCALL_OUTPUT_INT)) ? gpr[4] : 32'h0; // $a0

    // Debug signal output 
    assign debug_reg_single = gpr[4][7:0];

    assign reg1_data        = (read_reg1_addr == 0) ? `INITIAL_VAL : gpr[read_reg1_addr];
    assign reg2_data        = (read_reg2_addr == 0) ? `INITIAL_VAL : gpr[read_reg2_addr];

    always @ (posedge clk) begin
        if (reg_write && (write_reg_addr != 0)) begin
            // write data to register
            gpr[write_reg_addr] <= write_data;
        end
    end
endmodule
