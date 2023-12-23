`timescale 1ns / 1ps
`include "definitions.v"


module reg_dst_mux(
    input wire[`REG_DST_LENGTH - 1:0] reg_dst,
    input wire[4:0] rt,
    input wire[4:0] rd,

    output wire[4:0] mux_out
    );

    wire[4:0] reg_31; // $ra
    assign reg_31 = `REG_31_ADDR;

    assign mux_out =
        (reg_dst == `REG_DST_RT    ) ? rt :
        (reg_dst == `REG_DST_RD    ) ? rd :
        (reg_dst == `REG_DST_REG_31) ? reg_31 :
        rt;
endmodule


module alu_src_mux(
    input wire[`ALU_SRC_LENGTH - 1:0] alu_src,
    input wire[31:0] rt_data,
    input wire[31:0] extend_imm,
    input wire[31:0] cp0_data,

    output wire[31:0] mux_out
    );

    assign mux_out = (alu_src == `ALU_SRC_REG) ? rt_data :
                     (alu_src == `ALU_SRC_IMM) ? extend_imm :
                     (alu_src == `ALU_SRC_CP0) ? cp0_data :
                     rt_data;
endmodule


module reg_src_mux(
    input wire[`REG_SRC_LENGTH - 1:0] reg_src,
    input wire[31:0] alu_result,
    input wire[31:0] read_mem_data,
    input wire[31:0] extend_imm,
    input wire[31:0] re_addr,

    output wire[31:0] mux_out
    );

    assign mux_out = 
        (reg_src == `REG_SRC_ALU    ) ? alu_result :
        (reg_src == `REG_SRC_MEM    ) ? read_mem_data :
        (reg_src == `REG_SRC_IMM    ) ? extend_imm :
        (reg_src == `REG_SRC_RETURN) ? re_addr :
        alu_result;
endmodule


module forward_mux(
    input wire[1:0]  forward_C,
    input wire[31:0] rs_rt_data,
    input wire[31:0] write_data,
    input wire[31:0] alu_result,

    output wire[31:0] mux_out
    );

    assign mux_out =
        (forward_C == 2'b10) ? alu_result :
        (forward_C == 2'b01) ? write_data :
        rs_rt_data;
endmodule 