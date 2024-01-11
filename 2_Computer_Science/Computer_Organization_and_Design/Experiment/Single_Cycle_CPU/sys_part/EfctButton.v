`timescale 1ns / 1ps
`include "hardware_head.v"

module EfctButton #(N = `BTN_EFCT_DELAY) ( // effective button
    input wire clk,
    input wire btn,
    output reg efct_btn // 1: pressed, 0: not pressed
    );

    initial begin
        efct_btn = 0;
    end

    reg [31:0] cnt;
    always @(posedge clk) begin
        if (btn) begin
            cnt <= cnt + 1;
            if (cnt == N) begin
                cnt <= 0;
                efct_btn <= 1;
            end
        end else begin
            cnt <= 0;
            efct_btn <= 0;
        end
    end
endmodule