`timescale 1ns / 1ps
`include "hardware_head.v"

module Top_ShowModule(
    input wire          clk,
    input wire [6:0]    debug,
    input wire [`NUM_SIZE-1:0]   num,
    output wire[`SEG_SIZE-1:0]   seg,
    output wire [6:0]   a_to_g
    );

    wire                clk_div;

    CLK_Div #(.N(`SEG_DELAY)) INST_CLK_DIV (
        .clk_in(clk),
        .clk_out(clk_div));

    ShowNum INST_SHOW_NUM (
        .clk(clk_div),
        .rst(debug),
        .num(num),
        .seg(seg),
        .a_to_g(a_to_g));
endmodule
