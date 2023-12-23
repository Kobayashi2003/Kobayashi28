`timescale 1ns / 1ps
`include "definitions.v"

module reg_ex_mem(
    input wire clk,
    input wire rst,

    input wire[3:0] stall_C,
    input wire[3:0] flush_C,

    /* -- basic data -- */

    input wire[31:0] alu_result_in,
    input wire[31:0] reg2_data_in,
    input wire[31:0] ext_imm_in,
    input wire[4:0]  dst_reg_in,
    input wire[31:0] re_addr_in,
    input wire[31:0] pc_in,

    output reg[31:0] alu_result_out,
    output reg[31:0] reg2_data_out,
    output reg[31:0] ext_imm_out,
    output reg[4:0]  dst_reg_out,
    output reg[31:0] re_addr_out,
    output reg[31:0] pc_out,


    /* -- control signals -- */

    // memory stage control signals
    input wire                        mem_read_in,
    input wire                        mem_write_in,
    input wire                        cp0_write_in,

    // write back stage control signals 
    input wire                        reg_write_in,
    input wire[`REG_SRC_LENGTH - 1:0] reg_src_in,

    input wire[`EXC_TYPE_LENGTH -1:0] exc_type_in,

    input wire                        bubble_in,

    output reg                        mem_read_out,
    output reg                        mem_write_out,
    output reg                        cp0_write_out,

    output reg                        reg_write_out,
    output reg[`REG_SRC_LENGTH - 1:0] reg_src_out,

    output reg[`EXC_TYPE_LENGTH - 1:0] exc_type_out,

    output reg                         bubble_out
    );

    always @ (posedge clk or negedge rst) begin
        if (!rst) begin
            alu_result_out <= `INIT_32;
            reg2_data_out  <= `INIT_32;
            ext_imm_out    <= `INIT_32;
            dst_reg_out    <= `INIT_32;
            re_addr_out    <= `INIT_32;
            pc_out         <= `INIT_32;

            mem_read_out   <= `MEM_READ_DIS;
            mem_write_out  <= `MEM_WRITE_DIS;
            cp0_write_out  <= `CP0_WRITE_DIS;
            reg_write_out  <= `REG_WRITE_DIS;
            reg_src_out    <= `REG_SRC_DEFAULT;

            exc_type_out   <= `EXC_TYPE_DEFAULT;

            bubble_out     <= 1;
        end
        else if (flush_C[3] == 1) begin
            alu_result_out <= `INIT_32;
            reg2_data_out  <= `INIT_32;
            ext_imm_out    <= `INIT_32;
            dst_reg_out    <= `INIT_32;
            re_addr_out    <= `INIT_32;
            pc_out         <= `INIT_32;

            mem_read_out   <= `MEM_READ_DIS;
            mem_write_out  <= `MEM_WRITE_DIS;
            cp0_write_out  <= `CP0_WRITE_DIS;
            reg_write_out  <= `REG_WRITE_DIS;
            reg_src_out    <= `REG_SRC_DEFAULT;

            exc_type_out   <= `EXC_TYPE_DEFAULT;

            bubble_out     <= 1;
        end
        else if (stall_C[3] == 0) begin 
            alu_result_out <= alu_result_in;
            reg2_data_out  <= reg2_data_in;
            ext_imm_out    <= ext_imm_in;
            dst_reg_out    <= dst_reg_in;
            re_addr_out    <= re_addr_in;
            pc_out         <= pc_in;

            mem_read_out   <= mem_read_in;
            mem_write_out  <= mem_write_in;
            cp0_write_out  <= cp0_write_in;
            reg_write_out  <= reg_write_in;
            reg_src_out    <= reg_src_in;

            exc_type_out   <= exc_type_in;

            bubble_out     <= bubble_in;
        end
        else begin
            alu_result_out <= `INIT_32;
            reg2_data_out  <= `INIT_32;
            ext_imm_out    <= `INIT_32;
            dst_reg_out    <= `INIT_32;
            re_addr_out    <= `INIT_32;
            pc_out         <= `INIT_32;

            mem_read_out   <= `MEM_READ_DIS;
            mem_write_out  <= `MEM_WRITE_DIS;
            cp0_write_out  <= `CP0_WRITE_DIS;
            reg_write_out  <= `REG_WRITE_DIS;
            reg_src_out    <= `REG_SRC_DEFAULT;

            exc_type_out   <= `EXC_TYPE_DEFAULT;

            bubble_out     <= 1;
        end
    end

endmodule
