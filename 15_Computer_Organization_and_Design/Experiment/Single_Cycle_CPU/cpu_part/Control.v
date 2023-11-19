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
    wire type_r, add, subu, _and, _or, _nor, slt, sll;
    // I-type
    wire lui, addiu, lw, sw, beq;
    // J-type
    wire j;

    // Whether instruction is R-Type 
    assign type_r   = (opcode == `INST_R_TYPE && func != `INST_SYSCALL) ? 1 : 0;
    // R-type instructions
    assign add      = (type_r && func == `FUNC_ADD) ? 1 : 0;
    assign subu     = (type_r && func == `FUNC_SUBU) ? 1 : 0;
    assign _and     = (type_r && func == `FUNC_AND) ? 1 : 0;
    assign _or      = (type_r && func == `FUNC_OR) ? 1 : 0;
    assign _nor     = (type_r && func == `FUNC_NOR) ? 1 : 0;
    assign slt      = (type_r && func == `FUNC_SLT) ? 1 : 0;
    assign sll      = (type_r && func == `FUNC_SLL) ? 1 : 0;

    // I-type instructions
    assign lui      = (opcode == `INST_LUI) ? 1 : 0;
    assign addiu    = (opcode == `INST_ADDIU) ? 1 : 0;
    assign lw       = (opcode == `INST_LW) ? 1 : 0;
    assign sw       = (opcode == `INST_SW) ? 1 : 0;
    assign beq      = (opcode == `INST_BEQ) ? 1 : 0;

    // J-type instructions
    assign j        = (opcode == `INST_J) ? 1 : 0;

    // Halt instruction
    assign halt     = (opcode == `INST_HALT) ? 1 : 0;

    // System call
    assign syscall  = (func == `INST_SYSCALL) ? 1 : 0;

    // Determine control signals
    assign alu_ctrl =   (add || addiu || lw || sw)  ? `ALU_CTRL_ADD :    // Addition in ALU
                        (subu || beq)               ? `ALU_CTRL_SUB :    // Subtraction in ALU
                        (_and)                      ? `ALU_CTRL_AND :    // Bitwise AND in ALU
                        (_or)                       ? `ALU_CTRL_OR :     // Bitwise OR in ALU
                        (_nor)                      ? `ALU_CTRL_NOR :    // Bitwise NOR in ALU
                        (slt)                       ? `ALU_CTRL_SLT :    // Set less than in ALU
                        (sll)                       ? `ALU_CTRL_SHIFT_L: // Shift left in ALU 
                                                      `ALU_CTRL_DEFAULT; // Default ALU operand (output the second ALU input)

    // RegDst signal
    assign reg_dst  =   (add || subu || _and || _or || _nor || slt || sll) ? 1 : 0;
    // ALUSrc1 signal
    assign alu_src1 =   (sll) ? 1 : 0;
    // ALUSrc2 signal
    assign alu_src2 =   (addiu || lw || sw || sll) ? 1 : 0;

    // Write signals
    assign reg_write =  ( lui || type_r || add  || subu || 
                         _and ||   _or  || _nor ||  slt || 
                        addiu ||   lw   ||
                        (syscall && (sys_op == `SYSCALL_INPUT_INT))) ? 1 : 0;

    assign mem_write =  (sw) ? 1 : 0;

    assign reg_src   =  (lui)                          ? `REG_SRC_IMM :    // Source: Extended immediate
                        (addiu || add || subu || _and 
                        || _or || _nor || slt || sll)  ? `REG_SRC_ALU :    // Source: ALU result
                        (lw)                           ? `REG_SRC_MEM :
                                                         `REG_SRC_DEFAULT; // Source: Data memory

    assign ext_op    =  (lui)       ? `EXT_OP_SFT16 :       // Extend module operation: shift left 16
                        (addiu)     ? `EXT_OP_SIGNED :      // Extend module operation: signed extend
                        (lw || sw)  ? `EXT_OP_UNSIGNED :    // Extend module operation: unsigned extend
                                      `EXT_OP_DEFAULT;      // Extend module operation: default operation (unsigned extend)

    assign npc_op    =  (j)             ? `NPC_OP_JUMP :    // Jump
                        (beq && zero)   ? `NPC_OP_OFFSET :  // Branch equal
                        (beq && ~zero)  ? `NPC_OP_DEFAULT : // Branch not equal
                        (halt)          ? `NPC_OP_HALT :    // Halt
                                          `NPC_OP_NEXT;     // Next instruction: normal
endmodule
