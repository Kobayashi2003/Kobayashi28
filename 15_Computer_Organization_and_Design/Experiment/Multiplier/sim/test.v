`timescale 1ns / 1ps

module test();

    reg clk;
    reg rst;
    reg [15:0] num1;
    reg [15:0] num2;

    wire[31:0] result;

    initial begin
        clk = 0;
        rst = 0;
        num1 = 0;
        num2 = 0;

        num1 = 16'h1234;
        num2 = 16'h0003;
        #30 rst = 1;
    end

    always #5 clk = ~clk;

    multiplier multiplier_inst(
        .clk(clk),
        .rst(rst),
        .num1(num1),
        .num2(num2),
        .result(result)
        );

endmodule
