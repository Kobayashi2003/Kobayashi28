`timescale 1ns / 1ps
`include "hardware_head.v"

module IO(
    input wire       clk,

    input wire       start,
    input wire       switch,
    input wire       confirm,
    input wire       go_lst,
    input wire       go_nxt,

    input wire[`ARRAY_SIZE-1:0] cur_index,
    input wire[`NUM_SIZE-1:0]   show_num,

    input wire[6:0]  debug,

    output wire      start_efct,
    output wire      switch_efct,
    output wire      confirm_efct,
    output wire      go_lst_efct,
    output wire      go_nxt_efct,

    output reg [`ARRAY_SIZE-1:0] cue_lgt,
    output wire[`SEG_SIZE - 1:0] seg,
    output wire[6:0] a_to_g
    );

    initial begin
        cue_lgt   = 16'b0;
    end

    // cue_lgt shows the current index
    always @ (cur_index) begin
        cue_lgt            <= 16'b0;
        cue_lgt[cur_index] <= 1'b1;
    end

    EfctButton #(.N(32'd100_000)) INST_START_EFCT (
        .clk(clk),
        .btn(start),
        .efct_btn(start_efct));

    EfctButton #(.N(32'd100_000)) INST_SWITCH_EFCT (
        .clk(clk),
        .btn(switch),
        .efct_btn(switch_efct));

    EfctButton #(.N(32'd100_000)) INST_CONFIRM_EFCT (
        .clk(clk),
        .btn(confirm),
        .efct_btn(confirm_efct));

    EfctButton #(.N(32'd100_000)) INST_GO_LST_EFCT (
        .clk(clk),
        .btn(go_lst),
        .efct_btn(go_lst_efct));

    EfctButton #(.N(32'd100_000)) INST_GO_NXT_EFCT (
        .clk(clk),
        .btn(go_nxt),
        .efct_btn(go_nxt_efct));

    Top_ShowModule INST_TOP_SHOW_M(
        .clk(clk),
        .debug(debug),
        .num(show_num),
        .seg(seg),
        .a_to_g(a_to_g));

endmodule
