`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/10/11 20:56:30
// Design Name: 
// Module Name: ALU
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module ALU(
    input [3:0] Num1,
    input [3:0] Num2,
    input [3:0] Control,
    input M, // 0 for add, 1 for sub

    output SF,
    output ZF,
    output CF,
    output OF,

    output reg [3:0] Result
    );

    reg [3:0] c_out; // carry out
    reg c_in; // carry in
    reg cg, cp; // carry generate, carry propagate
    reg [3:0] i;

    always @(*) begin
        // calculate carry 
        if (M == 0) begin
            c_in = 0;
            for (i = 0; i < 4; i = i + 1) begin
                cg = Num1[i] & Num2[i];
                cp = Num1[i] | Num2[i];
                c_out[i] = cg | (cp & c_in);
                c_in = c_out[i];
            end
        end
        else begin
            c_in = 1;
            for (i = 0; i < 4; i = i + 1) begin
                cg = Num1[i] & ~Num2[i];
                cp = Num1[i] | ~Num2[i];
                c_out[i] = cg | (cp & c_in);
                c_in = c_out[i];
            end
        end

        case (Control) 
            4'b0000, 4'b0001: begin // b0000 for unsigned, b0001 for signed
                if (M == 0) 
                    Result = Num1 + Num2;
                else
                    Result = Num1 + ~Num2 + 1;
            end

            default: Result = 4'b0000;
        endcase
    end

    assign CF = c_out[3] ^ M;
    assign OF = c_out[3] ^ c_out[2];
    assign SF = Result[3];
    assign ZF = (Result == 0);

endmodule
