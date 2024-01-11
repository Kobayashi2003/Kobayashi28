`timescale 1ns / 1ps
`include "definitions.v"

module reg_id_ex(
    input wire clk,
    input wire rst,

    input wire[3:0] stall_C,
    input wire[3:0] flush_C,

    /* -- basic data -- */

    input wire[31:0] alu_input1_in,
    input wire[31:0] alu_input2_in,
    input wire[31:0] reg2_data_in,
    input wire[4:0]  rs_in,
    input wire[4:0]  rt_in,
    input wire[4:0]  rd_in,
    input wire[4:0]  sa_in,
    input wire[31:0] ext_imm_in,
    input wire[31:0] re_addr_in,
    input wire[4:0]  dst_reg_in,
    input wire[31:0] pc_in,

    output reg[31:0] alu_input1_out,
    output reg[31:0] alu_input2_out,
    output reg[31:0] reg2_data_out,
    output reg[4:0]  rt_out,
    output reg[4:0]  rd_out,
    output reg[4:0]  rs_out,
    output reg[4:0]  sa_out,
    output reg[31:0] ext_imm_out,  
    output reg[31:0] re_addr_out,
    output reg[4:0]  dst_reg_out,
    output reg[31:0] pc_out,


    /* -- control signals -- */

    // execute stage control signals
    input wire[`ALU_SRC_LENGTH - 1:0] alu_src_in,
    input wire[`ALU_OP_LENGTH  - 1:0] alu_op_in,
    input wire[`REG_DST_LENGTH - 1:0] reg_dst_in,

    // memory stage control signals
    input wire                        mem_read_in,
    input wire                        mem_write_in,
    input wire                        cp0_write_in,

    // write back stage control signals 
    input wire                        reg_write_in,
    input wire[`REG_SRC_LENGTH - 1:0] reg_src_in,

    input wire[`EXC_TYPE_LENGTH -1:0] exc_type_in,

    input wire                         bubble_in,

    output reg[`ALU_SRC_LENGTH - 1:0] alu_src_out,
    output reg[`ALU_OP_LENGTH  - 1:0] alu_op_out,
    output reg[`REG_DST_LENGTH - 1:0] reg_dst_out,
    output reg                        mem_read_out,
    output reg                        mem_write_out,
    output reg                        cp0_write_out,
    output reg                        reg_write_out,
    output reg[`REG_SRC_LENGTH - 1:0] reg_src_out,

    output reg[`EXC_TYPE_LENGTH -1:0] exc_type_out,

    output reg                        bubble_out
    );

    always @ (posedge clk or negedge rst) begin
        if (!rst) begin
            alu_input1_out <= `INIT_32;
            reg2_data_out <= `INIT_32;
            rt_out        <= `INIT_5;
            rd_out        <= `INIT_5;
            rs_out        <= `INIT_5;
            sa_out        <= `INIT_5;
            ext_imm_out   <= `INIT_32;
            re_addr_out   <= `INIT_32;
            dst_reg_out   <= `INIT_5;
            pc_out        <= `INIT_32;

            alu_src_out   <= `ALU_SRC_DEFAULT;
            alu_op_out    <= `ALU_OP_DEFAULT;
            reg_dst_out   <= `REG_DST_DEFAULT;
            mem_read_out  <= `MEM_READ_DIS;
            mem_write_out <= `MEM_WRITE_DIS;
            cp0_write_out <= `CP0_WRITE_DIS;
            reg_write_out <= `REG_WRITE_DIS;
            reg_src_out   <= `REG_SRC_DEFAULT;

            exc_type_out  <= `EXC_TYPE_DEFAULT;

            bubble_out    <= 1;
        end
        else if (flush_C[2] == 1) begin
            alu_input1_out <= `INIT_32;
            alu_input2_out <= `INIT_32;
            reg2_data_out <= `INIT_32;
            rt_out        <= `INIT_5;
            rd_out        <= `INIT_5;
            rs_out        <= `INIT_5;
            sa_out        <= `INIT_5;
            ext_imm_out   <= `INIT_32;
            re_addr_out   <= `INIT_32;
            dst_reg_out   <= `INIT_5;

            alu_src_out   <= `ALU_SRC_DEFAULT;
            alu_op_out    <= `ALU_OP_DEFAULT;
            reg_dst_out   <= `REG_DST_DEFAULT;
            mem_read_out  <= `MEM_READ_DIS;
            mem_write_out <= `MEM_WRITE_DIS;
            cp0_write_out <= `CP0_WRITE_DIS;
            reg_write_out <= `REG_WRITE_DIS;
            reg_src_out   <= `REG_SRC_DEFAULT;

            exc_type_out  <= `EXC_TYPE_DEFAULT;

            bubble_out    <= 1;
        end
        else if (stall_C[2] == 0) begin 
            alu_input1_out <= alu_input1_in;
            alu_input2_out <= alu_input2_in;
            reg2_data_out <= reg2_data_in;
            rt_out        <= rt_in;
            rd_out        <= rd_in;
            rs_out        <= rs_in;
            sa_out        <= sa_in;
            ext_imm_out   <= ext_imm_in;
            re_addr_out   <= re_addr_in;
            dst_reg_out   <= dst_reg_in;
            pc_out        <= pc_in;

            alu_src_out   <= alu_src_in;
            alu_op_out    <= alu_op_in;
            reg_dst_out   <= reg_dst_in;
            mem_read_out  <= mem_read_in;
            mem_write_out <= mem_write_in;
            cp0_write_out <= cp0_write_in;
            reg_write_out <= reg_write_in;
            reg_src_out   <= reg_src_in;

            exc_type_out  <= exc_type_in;

            bubble_out    <= bubble_in;
        end
        else if (stall_C[2] == 1 && stall_C[3] == 0) begin
            alu_input1_out <= `INIT_32;
            alu_input2_out <= `INIT_32;
            reg2_data_out <= `INIT_32;
            rt_out        <= `INIT_5;
            rd_out        <= `INIT_5;
            rs_out        <= `INIT_5;
            sa_out        <= `INIT_5;
            ext_imm_out   <= `INIT_32;
            re_addr_out   <= `INIT_32;
            dst_reg_out   <= `INIT_5;
            pc_out        <= `INIT_32;

            alu_src_out   <= `ALU_SRC_DEFAULT;
            alu_op_out    <= `ALU_OP_DEFAULT;
            reg_dst_out   <= `REG_DST_DEFAULT;
            mem_read_out  <= `MEM_READ_DIS;
            mem_write_out <= `MEM_WRITE_DIS;
            cp0_write_out <= `CP0_WRITE_DIS;
            reg_write_out <= `REG_WRITE_DIS;
            reg_src_out   <= `REG_SRC_DEFAULT;

            exc_type_out  <= `EXC_TYPE_DEFAULT;

            bubble_out    <= 1;
        end
        else begin
            // stall_C[2] == 1 && stall_C[3] == 1
            // do nothing
        end
    end

endmodule
