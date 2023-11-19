`timescale 1ns / 1ps

module ShiftLeft2_Jump(
    input [25:0] in, // come from instruction [25:0]
    input [31:0] pc, // come from PC + 4
    output reg [31:0] out
    );

    always @(*) begin
        out <= {pc[31:28], in, 2'b00};
    end
endmodule
