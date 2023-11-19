`timescale 1ns / 1ps
`include "instruction_head.v"

module new_ProgramCounter(
    input wire [`NPC_OP_LENGTH-1 : 0]   npc_op,     // NPCOp control signal

    input wire [31:0]                   pc,         // Program counter
    input wire [15:0]                   imm16,      // 16 bit immediate
    input wire [25:0]                   imm26,      // 26 bit immediate

    output reg [31:0]                   npc         // Next program counter
    );

    wire [31:0]                         pc_4;
    assign pc_4 = pc + 32'h4;

    always @ (*) begin
        case (npc_op)
            `NPC_OP_NEXT:                           // Basic next instruction: pc+4
                npc <= pc_4;
            `NPC_OP_JUMP:                           // Jump to offset: J
                npc <= {pc[31:28], imm26, 2'b00};
            `NPC_OP_OFFSET:                         // PC+4+offset: BEQ
                npc <= {pc_4 + {{14{imm16[15]}}, {imm16, 2'b00}}};
            `NPC_OP_HALT:
                npc <= pc;                          // Halt
            default:
                npc <= pc_4;                        // Default
        endcase
    end
endmodule