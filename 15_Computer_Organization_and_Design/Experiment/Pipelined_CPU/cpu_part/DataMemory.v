`timescale 1ns / 1ps
`include "instruction_head.v"

module DataMemory(
    input wire          clk,
    input wire          mem_write, // Data memory write signal: MemWrite

    input wire[31:0]    mem_addr, // Data memory target address
    input wire[31:0]    write_mem_data, // Data: write to data memory

    output wire[31:0]   read_mem_data // Data: read from data memory
    );

    // Data Memory Storage
    reg[31:0]           dm[`DM_LENGTH:0];
    assign read_mem_data = dm[mem_addr];

    always @(posedge clk) begin
        if (mem_write) begin
            dm[mem_addr] <= write_mem_data;
        end    
    end
endmodule
