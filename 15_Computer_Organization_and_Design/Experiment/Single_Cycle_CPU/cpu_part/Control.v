`timescale 1ns / 1ps
`include "instruction_head.v"

module Control(

    output wire                         syscall,
    input wire[`SYS_OP_LENGTH - 1:0]    sys_op, // System operation signal

    input wire[5:0] opcode,     // Instruction opcode
    input wire[5:0] func,       // R-Type instruction function
    input wire      zero,       // For instruction BEQ, determine the result of rs - rt

    // Control signals 
    output wire[`ALU_CTRL_LENGTH - 1:0] alu_ctrl,
    output wire                         reg_dst,
    output wire                         reg_write,
    output wire                         alu_src1,
    output wire                         alu_src2,
    output wire                         mem_write,
    output wire[`REG_SRC_LENGTH - 1:0]  reg_src,
    output wire[`EXT_OP_LENGTH  - 1:0]  ext_op, 
    output wire[`NPC_OP_LENGTH  - 1:0]  npc_op,

    output wire                         halt
    );

    // R-type 
    wire type_r, inst_add, inst_subu, inst_and, inst_or, inst_nor, inst_slt, inst_sll;
    // I-type
    wire inst_lui, inst_addiu, inst_lw, inst_sw, inst_beq;
    // J-type
    wire inst_j;

    // Whether instruction is R-Type 
    assign type_r   = (opcode == `INST_R_TYPE && func != `INST_SYSCALL) ? 1 : 0;
    // R-type instructions
    assign inst_add      = (type_r && func == `FUNC_ADD) ? 1 : 0;
    assign inst_subu     = (type_r && func == `FUNC_SUBU) ? 1 : 0;
    assign inst_and      = (type_r && func == `FUNC_AND) ? 1 : 0;
    assign inst_or       = (type_r && func == `FUNC_OR) ? 1 : 0;
    assign inst_nor      = (type_r && func == `FUNC_NOR) ? 1 : 0;
    assign inst_slt      = (type_r && func == `FUNC_SLT) ? 1 : 0;
    assign inst_sll      = (type_r && func == `FUNC_SLL) ? 1 : 0;

    // I-type instructions
    assign inst_lui      = (opcode == `INST_LUI) ? 1 : 0;
    assign inst_addiu    = (opcode == `INST_ADDIU) ? 1 : 0;
    assign inst_lw       = (opcode == `INST_LW) ? 1 : 0;
    assign inst_sw       = (opcode == `INST_SW) ? 1 : 0;
    assign inst_beq      = (opcode == `INST_BEQ) ? 1 : 0;

    // J-type instructions
    assign inst_j        = (opcode == `INST_J) ? 1 : 0;

    // Halt instruction
    assign halt     = (opcode == `INST_HALT) ? 1 : 0;

    // System call
    assign syscall  = (func == `INST_SYSCALL) ? 1 : 0;

    // Determine control signals
    assign alu_ctrl =   (inst_add || inst_addiu || inst_lw || inst_sw)  ? `ALU_CTRL_ADD :    // Addition in ALU
                        (inst_subu || inst_beq)         ? `ALU_CTRL_SUB :    // Subtraction in ALU
                        (inst_and)                      ? `ALU_CTRL_AND :    // Bitwise AND in ALU
                        (inst_or)                       ? `ALU_CTRL_OR :     // Bitwise OR in ALU
                        (inst_nor)                      ? `ALU_CTRL_NOR :    // Bitwise NOR in ALU
                        (inst_slt)                      ? `ALU_CTRL_SLT :    // Set less than in ALU
                        (inst_sll)                      ? `ALU_CTRL_SHIFT_L: // Shift left in ALU 
                                                          `ALU_CTRL_DEFAULT; // Default ALU operand (output the second ALU input)

    // RegDst signal
    assign reg_dst  =   (inst_add || inst_subu || inst_and || inst_or || inst_nor || inst_slt || inst_sll) ? 1 : 0;
    // ALUSrc1 signal
    assign alu_src1 =   (inst_sll) ? 1 : 0;
    // ALUSrc2 signal
    assign alu_src2 =   (inst_addiu || inst_lw || inst_sw || inst_sll) ? 1 : 0;

    // Write signals
    assign reg_write =  ( inst_lui || type_r || inst_add  || inst_subu || 
                         inst_and ||   inst_or  || inst_nor ||  inst_slt || 
                        inst_addiu ||   inst_lw   ||
                        (syscall && (sys_op == `SYSCALL_INPUT_INT))) ? 1 : 0;

    assign mem_write =  (inst_sw) ? 1 : 0;

    assign reg_src   =  (inst_lui)                                       ? `REG_SRC_IMM :    // Source: Extended immediate
                        (inst_addiu || inst_add || inst_subu || inst_and 
                        || inst_or || inst_nor || inst_slt || inst_sll)  ? `REG_SRC_ALU :    // Source: ALU result
                        (inst_lw)                                        ? `REG_SRC_MEM :
                                                                           `REG_SRC_DEFAULT; // Source: Data memory

    assign ext_op    =  (inst_lui)            ? `EXT_OP_SFT16 :       // Extend module operation: shift left 16
                        (inst_addiu)          ? `EXT_OP_SIGNED :      // Extend module operation: signed extend
                        (inst_lw || inst_sw)  ? `EXT_OP_UNSIGNED :    // Extend module operation: unsigned extend
                                                `EXT_OP_DEFAULT;      // Extend module operation: default operation (unsigned extend)

    assign npc_op    =  (inst_j)             ? `NPC_OP_JUMP :    // Jump
                        (inst_beq && zero)   ? `NPC_OP_OFFSET :  // Branch equal
                        (inst_beq && ~zero)  ? `NPC_OP_DEFAULT : // Branch not equal
                        (halt)               ? `NPC_OP_HALT :    // Halt
                                               `NPC_OP_NEXT;     // Next instruction: normal
endmodule
