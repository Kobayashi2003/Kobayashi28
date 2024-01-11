`timescale 1ns / 1ps
`include "definitions.v"

module reg_mem_wb(
    input wire clk,
    input wire rst,

    /* -- basic data -- */

    input wire[31:0] read_mem_data_in,
    input wire[31:0] alu_result_in,
    input wire[31:0] ext_imm_in,
    input wire[4:0]  dst_reg_in,
    input wire[31:0] re_addr_in,

    output reg[31:0] read_mem_data_out,
    output reg[31:0] alu_result_out,   
    output reg[31:0] ext_imm_out,
    output reg[4:0]  dst_reg_out,
    output reg[31:0] re_addr_out,


    /* -- control signals -- */

    // write back stage control signals 
    input wire                        cp0_write_in,
    input wire                        reg_write_in,
    input wire[`REG_SRC_LENGTH - 1:0] reg_src_in,

    output reg                        cp0_write_out,
    output reg                        reg_write_out,
    output reg[`REG_SRC_LENGTH - 1:0] reg_src_out
    );


    always @ (posedge clk or negedge rst) begin
        if (!rst) begin
            read_mem_data_out <= `INIT_32;
            alu_result_out    <= `INIT_32;
            ext_imm_out       <= `INIT_32;
            dst_reg_out       <= `INIT_32;
            re_addr_out       <= `INIT_32;

            cp0_write_out     <= `CP0_WRITE_DIS;
            reg_write_out     <= `REG_WRITE_DIS;
            reg_src_out       <= `REG_SRC_DEFAULT;
        end
        else begin
            read_mem_data_out <= read_mem_data_in;
            alu_result_out    <= alu_result_in;
            ext_imm_out       <= ext_imm_in;
            dst_reg_out       <= dst_reg_in;
            re_addr_out       <= re_addr_in;

            cp0_write_out     <= cp0_write_in;
            reg_write_out     <= reg_write_in;
            reg_src_out       <= reg_src_in;
        end
    end
        
endmodule
