`timescale 1ns / 1ps

module Add_Branch(
    input [31:0] pc_in, // PC + 4
    input [31:0] offset, // come from shift left 2 unit (branch)
    output reg [31:0] pc_out
    );

    always @(*) begin
        pc_out <= pc_in + offset;
    end
endmodule
