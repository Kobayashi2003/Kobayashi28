`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/10/14 02:14:19
// Design Name: 
// Module Name: Top
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


module Top(
    input CLK,
    input Stop,
    input Reset,
    input Reverse,

    output [15:0] LED
    );

    StreamLight _StreamLight(
        .CLK_in(CLK),
        .Stop(Stop),
        .Reset(Reset),
        .Reverse(Reverse),
        .LED(LED)
        );
endmodule
