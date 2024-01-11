`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/10/11 21:05:17
// Design Name: 
// Module Name: toALUcontrol
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


module toALUcontrol(
    input [7:0] Control,
    output reg [3:0] ALUcontrol
    );

always @(Control) begin
    case (Control)
        8'b10000000: ALUcontrol = 4'b0000; // signed
        8'b01000000: ALUcontrol = 4'b0001; // unsigned 
        default: ALUcontrol = 4'b0000;
    endcase
end
endmodule
