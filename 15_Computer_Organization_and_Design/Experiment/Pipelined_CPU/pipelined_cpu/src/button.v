`timescale 1ns / 1ps

module button #(parameter N = 32'd1_000_000) (
    input  wire clk,
    input  wire rst,
    input  wire btn_in,
    output reg  btn_out
    );

    reg[31:0] cnt = N;
    
    always @ (posedge clk or negedge rst) begin
        if (!rst) begin
            btn_out <= 0;
            cnt     <= N;
        end else begin
            if (btn_in) begin
                if (cnt == N) begin
                    btn_out <= 1;
                    cnt     <= 0;
                end else begin
                    btn_out <= 0;
                    cnt     <= cnt + 1;
                end
            end else begin
                btn_out <= 0;
                cnt     <= N;
            end
        end
    end
endmodule