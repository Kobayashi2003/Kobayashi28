`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/10/11 21:04:29
// Design Name: 
// Module Name: Mux2
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


module Mux2(
    input [7:0] Data1,
    input [7:0] Data2,
    input Sel, 
    output reg [7:0] Result
    );

    always @(Data1 or Data2 or Sel) begin
        if (Sel == 0)
            Result = Data1;
        else 
            Result = Data2;
    end

endmodule
