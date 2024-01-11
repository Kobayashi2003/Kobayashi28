`timescale 1ns / 1ps

module clk_mux(
    input wire clk_in1,
    input wire clk_in2,
    input wire chose,
    output wire clk_out
    );

    assign clk_out = chose ? clk_in1 : clk_in2;
endmodule