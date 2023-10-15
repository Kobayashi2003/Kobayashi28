`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company:
// Engineer:
//
// Create Date: 2023/10/11 21:04:00
// Design Name:
// Module Name: Top
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


module Top(
    input CLK,
    input [3:0] Num1,
    input [3:0] Num2,
    input [7:0] Control,

    input button1, // button1 and button2 control the value of isResult
    input button2,

    input button3, // button3 and button4 control the value of M
    input button4,

    output SF,
    output ZF,
    output CF,
    output OF,

    output [3:0] seg,
    output [6:0] a_to_g
    );

    wire CLK_wire;
    wire [3:0] Result;
    wire [3:0] ALUcontrol;
    wire [7:0] mux2_result;

    reg isResult = 0;
    reg isSigned = 0;
    reg M = 0;

    always @(*) begin
        if (button1 == 1)
            isResult <= 1;
        else if (button2 == 1)
            isResult <= 0;

        if (button3 == 1)
            M <= 1;
        else if (button4 == 1)
            M <= 0;

        isSigned <= Control[7];
    end

    CLK_div _CLK_div (
        .CLK_in(CLK),
        .CLK_out(CLK_wire)
    );

    ShowNum _showNum (
        .CLK(CLK_wire),
        ._show_num(mux2_result),
        .isResult(isResult),
        .isSigned(isSigned),
        .SF(SF),
        .seg(seg),
        .a_to_g(a_to_g)
    );

    toALUcontrol _toALUcontrol (
        .Control(Control),
        .ALUcontrol(ALUcontrol)
    );

    ALU _ALU (
        .Num1(Num1),
        .Num2(Num2),
        .Control(ALUcontrol),
        .M(M),
        .SF(SF),
        .ZF(ZF),
        .CF(CF),
        .OF(OF),
        .Result(Result)
    );

    Mux2 _mux2 (
        .Data1({Num1, Num2}),
        .Data2({4'b0000, Result}),
        .Sel(isResult),
        .Result(mux2_result)
    );

endmodule
