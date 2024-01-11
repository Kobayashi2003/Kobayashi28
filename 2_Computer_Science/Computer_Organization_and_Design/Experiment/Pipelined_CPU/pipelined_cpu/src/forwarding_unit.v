`timescale 1ns / 1ps
`include "definitions.v"

module forwarding_unit(
    input wire      ex_mem_regwrite,
    input wire[4:0] ex_mem_regdst,
    input wire      mem_wb_regwrite,
    input wire[4:0] mem_wb_regdst,

    input wire[4:0] id_ex_rs,
    input wire[4:0] id_ex_rt,

    output wire[1:0] forward_A,
    output wire[1:0] forward_B
    );

    assign forward_A = (ex_mem_regwrite && ex_mem_regdst != `REG_0_ADDR && ex_mem_regdst == id_ex_rs) ? 2'b10 : 
                       (mem_wb_regwrite && mem_wb_regdst != `REG_0_ADDR && mem_wb_regdst == id_ex_rs) ? 2'b01 : 2'b00;
    assign forward_B = (ex_mem_regwrite && ex_mem_regdst != `REG_0_ADDR && ex_mem_regdst == id_ex_rt) ? 2'b10 : 
                       (mem_wb_regwrite && mem_wb_regdst != `REG_0_ADDR && mem_wb_regdst == id_ex_rt) ? 2'b01 : 2'b00;
endmodule


module forwarding_unit_id(
    input wire      if_id_cp0read,
    input wire      ex_mem_cp0write,
    input wire      mem_wb_cp0write,    

    input wire      ex_mem_regwrite,
    input wire[4:0] ex_mem_regdst,
    input wire      mem_wb_regwrite,
    input wire[4:0] mem_wb_regdst,

    input wire[4:0] if_id_rs,
    input wire[4:0] if_id_rt,
    input wire[4:0] if_id_rd,

    output wire[1:0] forward_A,
    output wire[1:0] forward_B
    );

    assign forward_A = (ex_mem_regwrite && ex_mem_regdst != `REG_0_ADDR && ex_mem_regdst == if_id_rs) ? 2'b10 : 
                       (mem_wb_regwrite && mem_wb_regdst != `REG_0_ADDR && mem_wb_regdst == if_id_rs) ? 2'b01 : 2'b00;

    assign forward_B = (ex_mem_regwrite && ex_mem_regdst != `REG_0_ADDR && ex_mem_regdst == if_id_rt) ? 2'b10 : 
                       (mem_wb_regwrite && mem_wb_regdst != `REG_0_ADDR && mem_wb_regdst == if_id_rt) ? 2'b01 : 
                       (if_id_cp0read && ex_mem_cp0write && ex_mem_regdst == if_id_rd) ? 2'b10 :
                       (if_id_cp0read && mem_wb_cp0write && mem_wb_regdst == if_id_rd) ? 2'b01 : 2'b00;

endmodule