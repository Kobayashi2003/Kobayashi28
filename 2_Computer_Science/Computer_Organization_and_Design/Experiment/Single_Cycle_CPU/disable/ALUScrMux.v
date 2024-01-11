`timescale 1ns / 1ps

module ALUScrMux(
    input num1[31:0], // come from register file [rt]
    input num2[31:0], // come from sign expand unit
    input ALUSrc,     // come from control unit
    output reg [31:0] out
    );

    always @(*) begin
        if (ALUSrc == 1)
            out <= num2;
        else
            out <= num1;
    end
endmodule
