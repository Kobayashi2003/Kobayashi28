`timescale 1ns / 1ps
`include "definitions.v"

module control(
    input wire rst,
    input wire[5:0] opcode, // Instruction opcode
    input wire[4:0] rs,     // mt 
    input wire[4:0] rt  ,   // trap code
    input wire[4:0] rd,
    input wire[4:0] sa,
    input wire[5:0] func,   // R-Type instruction function code
    input wire      zero,   // Zero flag

    input wire      int_signal,
    input wire      eret_signal,

    output wire[`EXT_OP_LENGTH  - 1:0] ext_op,

    output wire[`ALU_SRC_LENGTH - 1:0] alu_src,
    output wire[`ALU_OP_LENGTH  - 1:0] alu_op,

    output wire                        mem_read,
    output wire                        mem_write,

    output wire                        cp0_read,
    output wire                        cp0_write,

    output wire                        reg_write,  
    output wire[`REG_SRC_LENGTH - 1:0] reg_src,
    output wire[`REG_DST_LENGTH - 1:0] reg_dst,

    output wire[`NPC_OP_LENGTH  - 1:0] npc_op,

    output wire[3:0]                   flush_C,
    output wire                        slot_flush,

    output wire[`EXC_TYPE_LENGTH -1:0] exc_type,

    output wire                        inst_ukn
    );


    /* --- Init instruction signals --- */

    // R-Type instructions
    wire type_r;
    wire inst_add, inst_addu, inst_sub, inst_subu;
    wire inst_slt, inst_sltu, inst_and, inst_or, inst_nor, inst_xor;
    wire inst_sll, inst_srl, inst_sra, inst_sllv, inst_srlv, inst_srav;
    wire inst_jr, inst_jalr;

    wire inst_syscall;
        // rt   instructions
    wire inst_teq, inst_tne, inst_tge, inst_tgeu, inst_tlt, inst_tltu;


    // I-Type instructions
    wire inst_addi, inst_addiu, inst_beq, inst_bne;
    wire inst_sltiu, inst_andi, inst_ori, inst_xori;
    wire inst_lui, inst_lw, inst_sw;

        // rt   instructions
    wire inst_teqi, inst_tnei, inst_tgei, inst_tgeiu, inst_tlti, inst_tltiu;


    // J-Type instructions
    wire inst_j, inst_jal;


    // Coprocessor instructions
    wire inst_mtc0, inst_mfc0;
    wire inst_eret;


    // NOP
    wire inst_nop;


    /* --- Decode instructions --- */

    // Whether instruction is R-Type
    assign type_r         = (opcode==`SPECIAL             ) ? 1 : 0;
    // R-Type instructions
    assign inst_add       = (type_r && func == `FUNC_ADD  ) ? 1 : 0;
    assign inst_addu      = (type_r && func == `FUNC_ADDU ) ? 1 : 0;
    assign inst_sub       = (type_r && func == `FUNC_SUB  ) ? 1 : 0;
    assign inst_subu      = (type_r && func == `FUNC_SUBU ) ? 1 : 0;
    assign inst_slt       = (type_r && func == `FUNC_SLT  ) ? 1 : 0;
    assign inst_sltu      = (type_r && func == `FUNC_SLTU ) ? 1 : 0;
    assign inst_and       = (type_r && func == `FUNC_AND  ) ? 1 : 0;
    assign inst_or        = (type_r && func == `FUNC_OR   ) ? 1 : 0;
    assign inst_nor       = (type_r && func == `FUNC_NOR  ) ? 1 : 0;
    assign inst_xor       = (type_r && func == `FUNC_XOR  ) ? 1 : 0;
    assign inst_sll       = (type_r && func == `FUNC_SLL  ) ? 1 : 0;
    assign inst_srl       = (type_r && func == `FUNC_SRL  ) ? 1 : 0;
    assign inst_sra       = (type_r && func == `FUNC_SRA  ) ? 1 : 0;
    assign inst_sllv      = (type_r && func == `FUNC_SLLV ) ? 1 : 0;
    assign inst_srlv      = (type_r && func == `FUNC_SRLV ) ? 1 : 0;
    assign inst_srav      = (type_r && func == `FUNC_SRAV ) ? 1 : 0;
    assign inst_jr        = (type_r && func == `FUNC_JR   ) ? 1 : 0;
    assign inst_jalr      = (type_r && func == `FUNC_JALR ) ? 1 : 0;

    assign inst_syscall   = (type_r && func == `FUNC_SYSCALL) ? 1 : 0;
    assign inst_teq       = (type_r && func == `FUNC_TEQ  ) ? 1 : 0;
    assign inst_tne       = (type_r && func == `FUNC_TNE  ) ? 1 : 0;
    assign inst_tge       = (type_r && func == `FUNC_TGE  ) ? 1 : 0;
    assign inst_tgeu      = (type_r && func == `FUNC_TGEU ) ? 1 : 0;
    assign inst_tlt       = (type_r && func == `FUNC_TLT  ) ? 1 : 0;
    assign inst_tltu      = (type_r && func == `FUNC_TLTU ) ? 1 : 0;

    // I-Type Instructions
    assign inst_addi      = (opcode == `INST_ADDI  ) ? 1 : 0;
    assign inst_addiu     = (opcode == `INST_ADDIU ) ? 1 : 0;
    assign inst_sltiu     = (opcode == `INST_SLTIU ) ? 1 : 0;
    assign inst_andi      = (opcode == `INST_ANDI  ) ? 1 : 0;
    assign inst_ori       = (opcode == `INST_ORI   ) ? 1 : 0;
    assign inst_xori      = (opcode == `INST_XORI  ) ? 1 : 0;
    assign inst_lui       = (opcode == `INST_LUI   ) ? 1 : 0;
    assign inst_lw        = (opcode == `INST_LW    ) ? 1 : 0;
    assign inst_sw        = (opcode == `INST_SW    ) ? 1 : 0;
    assign inst_beq       = (opcode == `INST_BEQ   ) ? 1 : 0;
    assign inst_bne       = (opcode == `INST_BNE   ) ? 1 : 0;

    assign inst_teqi      = (opcode == `REGIMM && rt == `INST_TEQI ) ? 1 : 0;
    assign inst_tnei      = (opcode == `REGIMM && rt == `INST_TNEI ) ? 1 : 0;
    assign inst_tgei      = (opcode == `REGIMM && rt == `INST_TGEI ) ? 1 : 0;
    assign inst_tgeiu     = (opcode == `REGIMM && rt == `INST_TGEIU) ? 1 : 0;
    assign inst_tlti      = (opcode == `REGIMM && rt == `INST_TLTI ) ? 1 : 0;
    assign inst_tltiu     = (opcode == `REGIMM && rt == `INST_TLTIU) ? 1 : 0;
        

    // J-Type Instructions
    assign inst_j         = (opcode == `INST_J     ) ? 1 : 0;
    assign inst_jal       = (opcode == `INST_JAL   ) ? 1 : 0;



    // Coprocessor Instructions
    assign inst_mtc0      = (opcode == `COP0 && rs == `COP0_MTC0) ? 1 : 0;
    assign inst_mfc0      = (opcode == `COP0 && rs == `COP0_MFC0) ? 1 : 0;
    assign inst_eret      = {opcode, rs, rt, rd, sa, func} == `INST_ERET ? 1 : 0;


    // NOP (actually, nop is the same as sll $0, $0, 0)
    assign inst_nop       = {opcode, rs, rt, rd, sa, func} == `INIT_32 ? 1 : 0;



    /* --- Determine control signals --- */
    
    // ExtOp
    assign ext_op =
            // shift left 16
            (inst_lui                               ) ? `EXT_OP_SFT16 :
            // signed extend 
            (inst_addi || inst_addiu || inst_sltiu  ) ? `EXT_OP_SIGNED :
            // unsigned extend
            (inst_andi || inst_ori   || inst_xori  ||
             inst_lw   || inst_sw                   ) ? `EXT_OP_UNSIGNED : `EXT_OP_DEFAULT;

    // ALUSrc
    assign alu_src =
            (inst_addi || inst_addiu || inst_sltiu || inst_andi  ||
             inst_ori  || inst_xori  || inst_lw    || inst_sw    ||
             inst_teqi || inst_tnei  || inst_tgei  || inst_tgeiu ||
             inst_tlti || inst_tltiu || inst_lui                  ) ? `ALU_SRC_IMM : 
            (inst_mfc0                                            ) ? `ALU_SRC_CP0 : `ALU_SRC_REG;

    // ALUOp
    assign alu_op =
            (inst_addi || inst_add   || inst_lw   ||
             inst_sw                               ) ? `ALU_OP_ADD :     // Addition in ALU
            (inst_addu || inst_addiu               ) ? `ALU_OP_ADDU:     // Addition unsigned in ALU
            (inst_sub  || inst_beq   || inst_bne   ) ? `ALU_OP_SUB :     // Subtraction in ALU
            (inst_subu                             ) ? `ALU_OP_SUBU:     // Subtraction unsigned in ALU
            (inst_slt  || inst_sltu  || inst_sltiu ) ? `ALU_OP_SLT :     // Set less than in ALU
            (inst_and  || inst_andi                ) ? `ALU_OP_AND :     // Bitwise AND in ALU
            (inst_or   || inst_ori                 ) ? `ALU_OP_OR  :     // Bitwise OR in ALU
            (inst_xor  || inst_xori                ) ? `ALU_OP_XOR :     // Bitwise XOR in ALU
            (inst_nor                              ) ? `ALU_OP_NOR :     // Bitwise NOR in ALU
            (inst_sll                              ) ? `ALU_OP_SLL :     // Shift left in ALU
            (inst_srl                              ) ? `ALU_OP_SRL :     // Shift right in ALU
            (inst_sra                              ) ? `ALU_OP_SRA :     // Shift right arithmetic in ALU
            (inst_sllv                             ) ? `ALU_OP_SLLV:     // Shift left variable in ALU
            (inst_srlv                             ) ? `ALU_OP_SRLV:     // Shift right variable in ALU
            (inst_srav                             ) ? `ALU_OP_SRAV:     // Shift right arithmetic variable in ALU
            (inst_teq  || inst_teqi                ) ? `ALU_OP_TEQ :     // TEQ in ALU
            (inst_tne  || inst_tnei                ) ? `ALU_OP_TNE :     // TNE in ALU
            (inst_tge  || inst_tgei                ) ? `ALU_OP_TGE :     // TGE in ALU
            (inst_tgeu || inst_tgeiu               ) ? `ALU_OP_TGEU:     // TGEU in ALU
            (inst_tlt  || inst_tlti                ) ? `ALU_OP_TLT :     // TLT in ALU
            (inst_tltu || inst_tltiu               ) ? `ALU_OP_TLTU:     // TLTU in ALU
            (inst_mfc0 || inst_mtc0 || inst_lui    ) ? `ALU_OP_2ND :     // Default ALU operand (output the second ALU input)
            `ALU_OP_DEFAULT; // Default ALU operand (output the second ALU input)

    // MemRead
    assign mem_read =
            (inst_lw) ? 1 : 0;

    // MemWrite
    assign mem_write =
            (inst_sw) ? 1 : 0;

    // CP0 Read
    assign cp0_read =
            (inst_mfc0) ? 1 : 0;

    // CP0 Write
    assign cp0_write =
            (inst_mtc0) ? 1 : 0;


    // RegWrite
    assign reg_write =
            (inst_add  || inst_addu  || inst_sub   ||
             inst_subu || inst_slt   || inst_sltu  ||
             inst_and  || inst_or    || inst_nor   ||
             inst_xor  || inst_sll   || inst_srl   ||
             inst_sra  || inst_sllv  || inst_srlv  ||
             inst_srav || inst_jalr  || inst_jal   ||
             inst_lui  || inst_lw    || inst_mfc0  ||
             inst_addi || inst_addiu || inst_sltiu ||
             inst_andi || inst_ori   || inst_xori   ) ? 1 : 0;


    // RegDst
    assign reg_dst = 
            (inst_add  || inst_addu  || inst_sub   ||
             inst_subu || inst_slt   || inst_sltu  ||
             inst_and  || inst_or    || inst_nor   ||
             inst_xor  || inst_sll   || inst_srl   ||
             inst_sra  || inst_sllv  || inst_srlv  ||
             inst_srav || inst_jalr  || inst_mtc0   ) ? `REG_DST_RD :
            (inst_lui  || inst_lw    || inst_mfc0  ||
             inst_addi || inst_addiu || inst_sltiu ||
             inst_andi || inst_ori   || inst_xori   ) ? `REG_DST_RT :
            (inst_jal                               ) ? `REG_DST_REG_31 : `REG_DST_DEFAULT;


    // RegSrc
    assign reg_src =
            // Extended immediate
            (inst_lui                               ) ? `REG_SRC_IMM :

            // ALU result
            (inst_add  || inst_addu  || inst_sub   ||
             inst_subu || inst_slt   || inst_sltu  ||
             inst_and  || inst_or    || inst_nor   ||
             inst_xor  || inst_sll   || inst_srl   ||
             inst_sra  || inst_sllv  || inst_srlv  ||
             inst_srav || inst_addi  || inst_addiu ||
             inst_sltiu|| inst_andi  || inst_ori   ||
             inst_xori || inst_mfc0  || inst_mtc0   ) ? `REG_SRC_ALU :

            // Data memory
            (inst_lw                                ) ? `REG_SRC_MEM :

            // PC + 8
            (inst_jalr || inst_jal                  ) ? `REG_SRC_RETURN : `REG_SRC_DEFAULT;

    assign npc_op = 
                // normal: next instruction
                (inst_add  || inst_addu  || inst_sub   ||
                 inst_subu || inst_slt   || inst_sltu  ||
                 inst_and  || inst_or    || inst_nor   ||
                 inst_xor  || inst_sll   || inst_srl   ||
                 inst_sra  || inst_sllv  || inst_srlv  ||
                 inst_srav || inst_mfc0  || inst_mtc0  ||
                 inst_addi || inst_addiu || inst_sltiu ||
                 inst_andi || inst_ori   || inst_xori  ||
                 inst_lui  || inst_lw    || inst_sw     ) ? `NPC_OP_NEXT :

                // BEQ
                // normal: next instruction
                (inst_beq && ! zero                     ) ? `NPC_OP_NEXT :
                // jump to target
                (inst_beq && zero                       ) ? `NPC_OP_OFFSET :

                // BNE 
                // normal: next instruction
                (inst_bne && zero                       ) ? `NPC_OP_NEXT : 
                // jump to target
                (inst_bne && ! zero                     ) ? `NPC_OP_OFFSET : 

                // jump to instruction address  
                (inst_j || inst_jal                     ) ? `NPC_OP_JUMP :
                // jump to rs data
                (inst_jr || inst_jalr                   ) ? `NPC_OP_RS : `NPC_OP_DEFAULT;


    assign flush_C = (int_signal || eret_signal) ? 4'b1110 : 4'b0000;

    assign slot_flush = 
                // BEQ BNE
                ((inst_beq && zero)  || (inst_bne && !zero)) ? 1 :
                // J JAL JALR JR
                (inst_j || inst_jal || inst_jalr || inst_jr) ? 1 : 0;


    assign exc_type = inst_syscall ? `EXC_TYPE_SYS     : 
                      inst_eret    ? `EXC_TYPE_ERET    : 
                      inst_ukn     ? `EXC_TYPE_RI      : `EXC_TYPE_DEFAULT;


    /* --- Exception --- */
    assign inst_ukn = (
            // R-Type
            inst_add  || inst_addu  || inst_sub   || inst_subu  ||
            inst_slt  || inst_sltu  || inst_and   || inst_or    ||
            inst_nor  || inst_xor   || inst_sll   || inst_srl   ||
            inst_sra  || inst_sllv  || inst_srlv  || inst_srav  ||
            inst_jr   || inst_jalr  || inst_syscall             ||
            inst_teq  || inst_tne   || inst_tge   || inst_tgeu  ||
            inst_tlt  || inst_tltu                              ||
            // I-Type
            inst_addi || inst_addiu || inst_sltiu || inst_andi  ||
            inst_ori  || inst_xori  || inst_lui   || inst_lw    ||
            inst_sw   || inst_beq   || inst_bne   || inst_teqi  ||
            inst_tnei || inst_tgei  || inst_tgeiu || inst_tlti  ||
            inst_tltiu                                          ||
            // J-Type
            inst_j    || inst_jal                               ||
            // Coprocessor
            inst_mtc0 || inst_mfc0  || inst_eret                ||
            // NOP
            inst_nop                                             ) ? 0 : 1;
                
endmodule
