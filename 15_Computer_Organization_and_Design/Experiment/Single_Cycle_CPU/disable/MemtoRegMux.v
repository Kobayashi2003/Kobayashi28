`timescale 1ns / 1ps

module MemtoRegMux(
    input [31:0] alu_out, // come from ALU
    input [31:0] mem_out, // come from data memory
    input MemtoReg,       // come from control unit
    output reg [31:0] out
    );

    always @(*) begin
        if (MemtoReg == 1)
            out <= mem_out;
        else
            out <= alu_out;
    end
endmodule
