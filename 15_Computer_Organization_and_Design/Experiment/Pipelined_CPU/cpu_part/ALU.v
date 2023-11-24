`timescale 1ns / 1ps
`include "instruction_head.v"

module ALU(

    input [`ALU_CTRL_LENGTH - 1:0] alu_ctrl,   // ALU control signal

    input [31:0]                   alu_input1, // ALU first input
    input [31:0]                   alu_input2, // ALU second input

    output wire [31:0]             alu_result, // ALU result
    output wire                    zero        // Whether result == 0, to determine BEQ
    );

    reg [32:0]                     alu_reg;

    assign alu_result = alu_reg[31:0];

    // Whether ALU result is zero
    assign zero       = (alu_reg == 0) ? 1'b1 : 1'b0;

    always @(*) begin 
        case (alu_ctrl)
            `ALU_CTRL_ADD:
                alu_reg <= {alu_input1[31], alu_input1} + {alu_input2[31], alu_input2};
            `ALU_CTRL_SUB:
                alu_reg <= {alu_input1[31], alu_input1} - {alu_input2[31], alu_input2};
            `ALU_CTRL_AND:
                alu_reg <= alu_input1 & alu_input2;
            `ALU_CTRL_OR:
                alu_reg <= alu_input1 | alu_input2;
            `ALU_CTRL_NOR:
                alu_reg <= ~(alu_input1 | alu_input2);
            `ALU_CTRL_SLT:
                alu_reg <= (alu_input1 < alu_input2) ? 1 : 0;
            `ALU_CTRL_SHIFT_L:
                alu_reg <= (alu_input1 << alu_input2[10:6]);
            default:
                alu_reg <= {alu_input2[31], alu_input2};
        endcase
    end
endmodule