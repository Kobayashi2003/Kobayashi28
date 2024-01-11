`timescale 1ns / 1ps
`include "instruction_head.v"

module InstructionMemory(
    // address for instruction
    input wire [31:0]   pc_addr,

    output wire [31:0]  instruction
    );

    reg [7:0]           im[`IM_LENGTH:0]; 

    assign instruction[31:24]   = im[pc_addr];
    assign instruction[23:16]   = im[pc_addr+1];
    assign instruction[15:8]    = im[pc_addr+2];
    assign instruction[7:0]     = im[pc_addr+3];
endmodule
