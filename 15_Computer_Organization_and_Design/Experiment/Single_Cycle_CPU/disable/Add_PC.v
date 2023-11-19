`timescale 1ns / 1ps

module Add_PC(
    input [31:0] pc_in, // PC
    output reg [31:0] pc_out
    );

    always @(*) begin
        pc_out <= pc_in + 4;
    end
endmodule
