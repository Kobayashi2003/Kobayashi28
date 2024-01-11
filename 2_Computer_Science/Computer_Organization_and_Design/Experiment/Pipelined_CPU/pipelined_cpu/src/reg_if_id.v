`timescale 1ns / 1ps
`include "definitions.v"

module reg_if_id(
    input wire clk,
    input wire rst,

    input wire[3:0] stall_C,
    input wire[3:0] flush_C,
    input wire      slot_flush,

    input wire[31:0] pc_in,
    input wire[31:0] instructions_in,

    output reg[31:0] pc_out,
    output reg[31:0] instructions_out,

    output reg       bubble_out
    );
    
    always @ (posedge clk or negedge rst) begin 
        if (!rst) begin
            pc_out           <= `INIT_32;
            instructions_out <= `INIT_32;
            bubble_out       <= 1;
        end
        else if (flush_C[1] == 1) begin
            pc_out           <= `INIT_32;
            instructions_out <= `INIT_32;
            bubble_out       <= 1;
        end
        else if (stall_C[1] == 1) begin
            // do nothing
        end
        else if (slot_flush == 1) begin
            pc_out           <= `INIT_32;
            instructions_out <= `INIT_32;
            bubble_out       <= 1;
        end
        else begin
            pc_out           <= pc_in;
            instructions_out <= instructions_in;
            bubble_out       <= 0;
        end
    end

endmodule
