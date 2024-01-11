`timescale 1ns / 1ps

module top(

    input  wire clk,

    input  wire[4:0]  btn,
    input  wire[15:0] sw,

    output reg[1:0]   led,
    output wire[3:0]  seg,
    output wire[6:0]  a_to_g
    );

    // reg clk;
    // reg[4:0] btn;
    // reg[15:0] sw;

    // initial begin
    //     clk = 0;
    //     btn = 0;
    //     sw  = 0;
    // end

    // always 
    //     #5 clk = ~clk;

    reg      init = 0;
    reg[4:0] init_cycle = 5'b11111;
    always @ (posedge clk)
        if (init_cycle == 0)
            init <= 1;
        else
            init_cycle <= init_cycle - 1;

    reg [15:0] num1;
    reg [15:0] num2;
    wire[31:0] result;

    wire show_result;
    wire show_buffer;
    wire show_num1;
    wire show_num2;
    wire reset;  // reset the num1 or num2, also reset the multiplier

    assign show_result  = btn[0];
    assign show_buffer  = btn[1];
    assign show_num1    = btn[2];
    assign show_num2    = btn[3];
    assign reset        = btn[4];

    reg [15:0] show_num;

    always @ (posedge clk or negedge init) begin
        if (!init) begin
            num1 <= 0;
            num2 <= 0;
            show_num <= 0;
        end else begin
            if (show_result && show_num1) begin
                show_num <= result[31:16];
                led      <= 2'b10;
            end else if (show_result && show_num2) begin
                show_num <= result[15:0];
                led      <= 2'b01;
            end else if (show_buffer && show_num1) begin
                show_num <= num1;
                led      <= 2'b10;
            end else if (show_buffer && show_num2) begin
                show_num <= num2;
                led      <= 2'b01;
            end else begin
                show_num <= sw;
                led      <= 2'b00;
            end

            if (show_num1 && reset)
                num1 <= sw;
            else if (show_num2 && reset)
                num2 <= sw;
        end
    end

    wire rst;
    assign rst = init && !reset;

    multiplier multiplier_inst(
        .clk(clk),
        .rst(rst),
        .num1(num1),
        .num2(num2),
        .result(result)
        );

    wire clk_div;

    clk_div clk_div_inst(
        .rst(init),
        .clk_in(clk),
        .clk_out(clk_div)
        );

    display display(
        .clk(clk_div),
        .num(show_num),
        .seg_C(seg),
        .a_to_g(a_to_g)
        );

endmodule
