`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/10/11 21:04:44
// Design Name: 
// Module Name: CLK_div
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


module CLK_div #(parameter N = 99999) (
    input CLK_in,
    output CLK_out
    );

    reg [31:0] cnt = 0;
    reg out = 0;

    always @(posedge CLK_in) begin
        if (cnt == N) begin
            cnt <= 0;
            out <= ~out;
        end
        else begin
            cnt <= cnt + 1;
        end 
    end

    assign CLK_out = out;
endmodule
