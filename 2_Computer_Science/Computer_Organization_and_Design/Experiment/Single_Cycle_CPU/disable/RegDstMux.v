`timescale 1ns / 1ps

module RegDstMux(
    input [4:0] rd, // come from instruction [20:16]
    input [4:0] rt, // come from instruction [15:11]
    input RegDst,   // come from control unit
    output reg [4:0] out
    );

    always @(*) begin
        if (RegDst == 1)
            out <= rd;
        else
            out <= rt;
    end
endmodule
