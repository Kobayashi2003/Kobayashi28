`timescale 1ns / 1ps
`include "definitions.v"

module stall_unit(
    input wire       cp0_write_exe,
    input wire       cp0_read_id,
    input wire       reg_write_exe,
    input wire       reg_write_mem,
    input wire       mem_read_exe,
    input wire       mem_read_mem,
    input wire[4:0]  dst_reg_exe,
    input wire[4:0]  dst_reg_mem,
    input wire[4:0]  if_id_rs,
    input wire[4:0]  if_id_rt,
    input wire[4:0]  if_id_rd,

    output wire[3:0] stall_C 
    );

    assign stall_C = 
        ((mem_read_mem && reg_write_mem) && (dst_reg_mem != `REG_0_ADDR && dst_reg_mem == if_id_rs)) ? `MEM_STALL :
        ((mem_read_mem && reg_write_mem) && (dst_reg_mem != `REG_0_ADDR && dst_reg_mem == if_id_rt)) ? `MEM_STALL :
        ((mem_read_exe && reg_write_exe) && (dst_reg_exe != `REG_0_ADDR && dst_reg_exe == if_id_rs)) ? `EXE_STALL :
        ((mem_read_exe && reg_write_exe) && (dst_reg_exe != `REG_0_ADDR && dst_reg_exe == if_id_rt)) ? `EXE_STALL :
        ((reg_write_exe                ) && (dst_reg_exe != `REG_0_ADDR && dst_reg_exe == if_id_rs)) ? `EXE_STALL :
        ((reg_write_exe                ) && (dst_reg_exe != `REG_0_ADDR && dst_reg_exe == if_id_rt)) ? `EXE_STALL :
        ((cp0_read_id  && cp0_write_exe) && (dst_reg_exe == if_id_rd                              )) ? `EXE_STALL :
        `NON_STALL;

    
endmodule
