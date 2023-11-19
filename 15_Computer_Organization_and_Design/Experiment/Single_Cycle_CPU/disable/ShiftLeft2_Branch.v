`timescale 1ns / 1ps

module ShiftLeft2_Branch(
    input [31:0] in, // come from sign expand unit
    output reg [31:0] out
    );

    always @(*) begin
        out <= in << 2;
    end
endmodule
