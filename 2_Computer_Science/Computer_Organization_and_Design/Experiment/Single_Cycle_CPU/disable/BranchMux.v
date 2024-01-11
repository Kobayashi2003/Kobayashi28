`timescale 1ns / 1ps

module BranchMux(
    input addr1, // PC + 4
    input addr2, // come from add branch unit
    input branch, // come from control unit
    input zero, // come from ALU
    output reg [31:0] out
    );

    always @(*) begin
        if (branch == 1 && zero == 1)
            out <= addr2;
        else
            out <= addr1;
    end

endmodule
