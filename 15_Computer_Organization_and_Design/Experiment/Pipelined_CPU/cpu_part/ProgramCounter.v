`timescale 1ns / 1ps
`include "instruction_head.v"

module ProgramCounter(
    input wire          clk,
    input wire          rst, // reset signal
    input wire [31:0]   npc,

    output reg [31:0]   pc
    );

    initial begin
        pc <= `INITIAL_VAL;
    end

    always @(posedge clk or negedge rst)
    begin 
        if (!rst)
            pc <= `INITIAL_VAL;
        else
            pc <= npc;
    end
endmodule