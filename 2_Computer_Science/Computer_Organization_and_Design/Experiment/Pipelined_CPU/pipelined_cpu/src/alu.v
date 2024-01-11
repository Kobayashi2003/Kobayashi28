`timescale 1ns / 1ps
`include "definitions.v"

module alu(
    input wire[31:0]                  alu_input1,
    input wire[31:0]                  alu_input2, 
    input wire[4:0]                   sa,
    input wire[`ALU_OP_LENGTH - 1:0]  alu_op,
    input wire[`EXC_TYPE_LENGTH-1:0]  exc_type_in,

    output wire[31:0]                 alu_result,
    output wire                       overflow,
    output wire                       zero,
    output wire[`EXC_TYPE_LENGTH-1:0] exc_type_out
    );

    // use double signed to detect overflow
    reg[32:0] alu_temp_result;
    assign alu_result = alu_temp_result[31:0];

    // detect overflow
    assign overflow = (alu_temp_result[32] != alu_temp_result[31]) ? `OVERFLOW_TRUE : `OVERFLOW_FALSE;

    // detect zero
    assign zero = (alu_result == 0) ? `ZERO_TRUE : `ZERO_FALSE;

    // shift amount defined by sa or rs
    wire[4:0] shamt;
    assign shamt =
        (alu_op == `ALU_OP_SLL ||
         alu_op == `ALU_OP_SRL ||
         alu_op == `ALU_OP_SRA) ? sa : alu_input1[4:0];

    // exception code
    assign exc_type_out = (alu_op == `ALU_OP_TEQ  && alu_result ||
                           alu_op == `ALU_OP_TNE  && alu_result ||
                           alu_op == `ALU_OP_TGE  && alu_result ||
                           alu_op == `ALU_OP_TGEU && alu_result ||
                           alu_op == `ALU_OP_TLT  && alu_result ||
                           alu_op == `ALU_OP_TLTU && alu_result  ) ? `EXC_TYPE_TR :
                          (alu_op == `ALU_OP_ADD  && overflow   ||
                           alu_op == `ALU_OP_ADDI && overflow   ||
                           alu_op == `ALU_OP_SUB  && overflow    ) ? `EXC_TYPE_OV : exc_type_in;

    always @ (*) begin
        case (alu_op)
            // normal arithmetic operations
            `ALU_OP_ADD, `ALU_OP_ADDU:
                alu_temp_result <= {alu_input1[31], alu_input1} + {alu_input2[31], alu_input2};
            `ALU_OP_SUB, `ALU_OP_SUBU:
                alu_temp_result <= {alu_input1[31], alu_input1} - {alu_input2[31], alu_input2};

            `ALU_OP_SLT:
                alu_temp_result <= (alu_input1 < alu_input2) ? 32'h00000001 : 32'h00000000;

            // bit operations
            `ALU_OP_AND:
                alu_temp_result <= {alu_input1[31], alu_input1} & {alu_input2[31], alu_input2};
            `ALU_OP_OR :
                alu_temp_result <= {alu_input1[31], alu_input1} | {alu_input2[31], alu_input2};
            `ALU_OP_NOR:
                alu_temp_result <= (({alu_input1[31], alu_input1} & ~{alu_input2[31], alu_input2}) |
                                    (~{alu_input1[31], alu_input1} & {alu_input2[31], alu_input2}));
            `ALU_OP_XOR:
                alu_temp_result <= {alu_input1[31], alu_input1} ^ {alu_input2[31], alu_input2};

            // shift left logically 
            `ALU_OP_SLL:
                alu_temp_result <= {alu_input2[31], alu_input2} << shamt;
            `ALU_OP_SLLV:
                alu_temp_result <= {alu_input2[31], alu_input2} << shamt;

            // shift right logically
            `ALU_OP_SRL:
                alu_temp_result <= {alu_input2[31], alu_input2} >> shamt;
            `ALU_OP_SRLV:
                alu_temp_result <= {alu_input2[31], alu_input2} >> shamt;
            // shift right arithmetically
            `ALU_OP_SRA:
                alu_temp_result <= ({{31{alu_input2[31]}}, 1'b0} << (~shamt)) | (alu_input2 >> shamt);
            `ALU_OP_SRAV:
                alu_temp_result <= ({{31{alu_input2[31]}}, 1'b0} << (~shamt)) | (alu_input2 >> shamt);

            // trap instructions
            `ALU_OP_TEQ:
                alu_temp_result <= (alu_input1 == alu_input2) ? 32'h00000001 : 32'h00000000;
            `ALU_OP_TNE:
                alu_temp_result <= (alu_input1 != alu_input2) ? 32'h00000001 : 32'h00000000;
            `ALU_OP_TGE:
                if (alu_input1[31] == alu_input2[31])
                    alu_temp_result <= (alu_input1 >= alu_input2) ? 32'h00000001 : 32'h00000000;
                else
                    alu_temp_result <= (alu_input1[31] == 1) ? 32'h00000000 : 32'h00000001;
            `ALU_OP_TLT:
                if (alu_input1[31] == alu_input2[31])
                    alu_temp_result <= (alu_input1 < alu_input2) ? 32'h00000001 : 32'h00000000;
                else
                    alu_temp_result <= (alu_input1[31] == 1) ? 32'h00000001 : 32'h00000000;
            `ALU_OP_TGEU:
                alu_temp_result <= (alu_input1 >= alu_input2) ? 32'h00000001 : 32'h00000000;
            `ALU_OP_TLTU:
                alu_temp_result <= (alu_input1 < alu_input2) ? 32'h00000001 : 32'h00000000;
            
            // default operation : pass input2
            `ALU_OP_DEFAULT:
                alu_temp_result <= {alu_input2[31], alu_input2};
        endcase
    end
endmodule