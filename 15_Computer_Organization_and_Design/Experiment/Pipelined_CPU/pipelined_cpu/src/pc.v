`timescale 1ns / 1ps
`include "definitions.v"

module pc(
    input wire       clk,
    input wire       rst,
    input wire[31:0] npc,

    input wire[3:0]  stall_C,
    input wire[3:0]  flush_C,

    output reg[31:0] pc
    );

    initial begin
        pc <= `INIT_32;
    end

    always @ (posedge clk or negedge rst) begin  
        if (!rst) begin
            pc <= `INIT_32;
        end
        else if (flush_C[0] == 1) begin
            pc <= `INIT_32;
        end
        else if (stall_C[0] == 0) begin
            pc <= npc;
        end
        else begin
            // do nothing
        end
    end
endmodule
