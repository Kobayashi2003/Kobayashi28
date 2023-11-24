`timescale 1ns / 1ps
`include "instruction_head.v"

module mux_reg_dst(
    input wire syscall,
    input wire[`SYS_OP_LENGTH - 1:0] sys_op,

    input wire      reg_dst,  // mux control signal: RegDst
    input wire[4:0] mux_in_0, // mux input source: rt
    input wire[4:0] mux_in_1, // mux input source: rd

    output reg[4:0] mux_out   // mux output
    );


    always @ (*) begin
        case (reg_dst)
            `REG_DST_RT:
                mux_out <= mux_in_0;
            `REG_DST_RD:
                mux_out <= mux_in_1;
        endcase
        if (syscall && (sys_op == `SYSCALL_INPUT_INT)) begin
            mux_out <= 5'b00100; // $a0
        end
    end
endmodule


module mux_reg_src(
    input wire syscall,        // syscall signal
    input wire[`SYS_OP_LENGTH - 1:0] sys_op, // system operation signal
    input wire[31:0] sys_in,   // system input data

    input wire[`REG_SRC_LENGTH - 1:0] reg_src, // mux control signal: RegSrc
    input wire[31:0] mux_in_0, // mux input source: ALU result
    input wire[31:0] mux_in_1, // mux input source: Data Memory
    input wire[31:0] mux_in_2, // mux input source: Extend module output

    output reg[31:0] mux_out   // mux output
    );

    always @ (*) begin
        case (reg_src)
            `REG_SRC_ALU:
                mux_out <= mux_in_0;
            `REG_SRC_MEM:
                mux_out <= mux_in_1;
            `REG_SRC_IMM:
                mux_out <= mux_in_2;
            default:
                mux_out <= mux_in_0;
        endcase

        if (syscall && (sys_op == `SYSCALL_INPUT_INT)) begin
            mux_out <= sys_in; // system input data
        end
    end
endmodule

module mux_alu_src1(
    input wire alu_src1,       // mux control signal: ALUSrc1
    input wire[31:0] mux_in_0, // mux input source: reg1 (rs) data
    input wire[31:0] mux_in_1, // mux input source: reg2 (rt) data

    output reg[31:0] mux_out   // mux output
    );

    always @(*) begin
        case (alu_src1)
            `ALU_SRC_SHIFT:
                mux_out <= mux_in_1;
            default:
                mux_out <= mux_in_0;
        endcase
    end
endmodule

module mux_alu_src2(
    input wire       alu_src2, // mux control signal: ALUSrc2
    input wire[31:0] mux_in_0, // mux input source: register file
    input wire[31:0] mux_in_1, // mux input source: immediate

    output reg[31:0] mux_out   // mux output
    );

    always @ (*) begin
        case (alu_src2)
            `ALU_SRC_REG:
                mux_out <= mux_in_0;
            `ALU_SRC_IMM:
                mux_out <= mux_in_1;
            default:
                mux_out <= mux_in_0;
        endcase
    end
endmodule