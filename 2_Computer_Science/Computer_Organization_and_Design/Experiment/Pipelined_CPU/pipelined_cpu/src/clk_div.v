`timescale 1ns / 1ps

module clk_div #(parameter N = 16'hffff) (
    input wire rst,
    input wire clk_in,
    output reg clk_out
    );

    reg [15:0]      cnt = 0;

    always @ (posedge clk_in or negedge rst) begin
        if (!rst) begin
            cnt     <= 0;
            clk_out <= 0;
        end  else begin
            cnt     <= (cnt == N) ? 0 : cnt + 1;
            clk_out <= (cnt == N) ? ~clk_out : clk_out;
        end
    end

endmodule