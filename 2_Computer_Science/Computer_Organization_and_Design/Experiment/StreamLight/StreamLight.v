`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/10/14 02:15:18
// Design Name: 
// Module Name: StreamLight
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


module StreamLight(
    input CLK_in,
    input Reset,
    input Reverse,
    input Stop,
    input Run,

    output reg [15:0] LED
    );

    reg [31:0] cnt = 0;

    always @(posedge CLK_in) begin
        if (!Run) begin
            cnt <= 0;
            LED <= 0;
        end
        else if (Reset) begin
            cnt <= 0;
            LED <= 1;
        end
        else if (Stop) begin
            cnt <= cnt;
            LED <= LED;
        end
        else begin
            if (cnt == 10000000) begin
                cnt <= 0;
                if (Reverse) begin 
                    LED <= (LED >> 1);
                    if (LED == 0)
                        LED <= 16'h8000;
                end
                else begin
                LED <= (LED << 1);
                if (LED == 0)
                    LED <= 1;
                end
            end
            else begin
                cnt <= cnt + 1;
                LED <= LED;
            end
        end
    end
endmodule
