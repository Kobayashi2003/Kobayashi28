`timescale 1ns / 1ps
`include "definitions.v"

module extend(
    input wire[15:0]                  imm16,
    input wire[`EXT_OP_LENGTH  - 1:0] ext_op,

    output wire[31:0]                 extended_imm
    );

    assign extended_imm =
        (ext_op == `EXT_OP_SFT16)    ? {imm16, 16'b0} :            // LUI: shift left 16
        (ext_op == `EXT_OP_SIGNED)   ? {{16{imm16[15]}}, imm16} : // ADDIU: signed sign extend of imm16
        (ext_op == `EXT_OP_UNSIGNED) ? {16'b0, imm16} :           // LW, SW: unsigned sign extend of imm16
        32'b0;                                                    // fallback mode: 0
endmodule
