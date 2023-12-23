`timescale 1ns / 1ps
`include "definitions.v"

module npc(
    input  wire [31:0]                 pc_if,
    input  wire [31:0]                 pc_id,    // pc from if_id
    input  wire [31:0]                 cp0_epc,  // cp0 epc
    input  wire [15:0]                 imm16,    // 16 bit immediate
    input  wire [25:0]                 imm26,    // 26 bit immediate
    input  wire [31:0]                 rs_data,  // rs data
    
    input  wire [`NPC_OP_LENGTH   - 1:0] npc_op,   // NPC control signal
    input  wire [`NPC_INT_OP_LENGTH-1:0] npc_int_op, // NPC interrupt control signal

    output wire [31:0]                 npc,      // next program counter
    output wire [31:0]                 re_addr   // JAL, JAJR return address
    );

    wire[31:0] pc_4;
    assign pc_4 = pc_if + 32'h4;

    assign re_addr = pc_if + 32'h8;

    assign npc = 
        // interrupt operation
        (npc_int_op == `NPC_OP_HARD0 ) ? `NPC_ADDR_HARD0  :                          // pc = hard0
        (npc_int_op == `NPC_OP_HARD1 ) ? `NPC_ADDR_HARD1  :                          // pc = hard1
        (npc_int_op == `NPC_OP_HARD2 ) ? `NPC_ADDR_HARD2  :                          // pc = hard2
        (npc_int_op == `NPC_OP_HARD3 ) ? `NPC_ADDR_HARD3  :                          // pc = hard3
        (npc_int_op == `NPC_OP_HARD4 ) ? `NPC_ADDR_HARD4  :                          // pc = hard4
        (npc_int_op == `NPC_OP_HARD5 ) ? `NPC_ADDR_HARD5  :                          // pc = hard5
        (npc_int_op == `NPC_OP_SOFT0 ) ? `NPC_ADDR_SOFT0  :                          // pc = soft0
        (npc_int_op == `NPC_OP_SOFT1 ) ? `NPC_ADDR_SOFT1  :                          // pc = soft1
        (npc_int_op == `NPC_OP_SYS   ) ? `NPC_ADDR_SYS    :                          // pc = sys
        (npc_int_op == `NPC_OP_ERET  ) ? cp0_epc :                                   // pc = epc
        (npc_int_op == `NPC_OP_RI    ) ? `NPC_ADDR_RI     :                          // pc = ri
        (npc_int_op == `NPC_OP_OV    ) ? `NPC_ADDR_OV     :                          // pc = ov
        (npc_int_op == `NPC_OP_TR    ) ? `NPC_ADDR_TR     :                          // pc = tr
        // normal operation 
        (npc_op == `NPC_OP_NEXT  ) ? pc_4 :                                            // pc + 4
        (npc_op == `NPC_OP_JUMP  ) ? {pc_id[31:28], imm26, 2'b00} :                    // pc = target
        (npc_op == `NPC_OP_OFFSET) ? {pc_id + 4 + {{14{imm16[15]}}, {imm16, 2'b00}}} : // pc + 4 + offset
        (npc_op == `NPC_OP_RS    ) ? rs_data :                                         // pc = rs data
        pc_4;                                                                          // fallback mode: pc + 4
endmodule
