`timescale 1ns / 1ps

module JumpMux(
    input [31:0] addr1, // come from BranchMux
    input [31:0] addr2, // come from ShiftLeft2_Jump
    input jump, // come from control unit
    output reg [31:0] out
    );

    always @(*) begin
        if (jump == 1)
            out <= addr2;
        else
            out <= addr1;
    end
endmodule
