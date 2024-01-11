`timescale 1ns / 1ps
`include "hardware_head.v"

module ShowNum(
    input wire          clk,
    input wire [6:0]    rst,
    input wire [`NUM_SIZE - 1:0]    num,
    output reg [`SEG_SIZE - 1:0]    seg,
    output reg [6:0]    a_to_g
    );

    initial begin
        seg    = `SEG_DEF;
        a_to_g = `SEG_VAL_DEF;
    end

    reg [1:0]           seg_num = 0;
    reg [3:0]           x = 0;

    always @ (posedge clk) begin
        case (seg_num)
            0: begin x = num[15:12]     ;    seg = `SEG_1st; end
            1: begin x = num[11:8]      ;    seg = `SEG_2nd; end
            2: begin x = num[7:4]       ;    seg = `SEG_3rd; end
            3: begin x = num[3:0]       ;    seg = `SEG_4th; end
        endcase
        seg_num <= (seg_num + 1) % `SEG_SIZE;
    end

    always @ (x or rst) begin
        case (x)
            0:  a_to_g = `SEG_VAL_0;
            1:  a_to_g = `SEG_VAL_1;
            2:  a_to_g = `SEG_VAL_2;
            3:  a_to_g = `SEG_VAL_3;
            4:  a_to_g = `SEG_VAL_4;
            5:  a_to_g = `SEG_VAL_5;
            6:  a_to_g = `SEG_VAL_6;
            7:  a_to_g = `SEG_VAL_7;
            8:  a_to_g = `SEG_VAL_8;
            9:  a_to_g = `SEG_VAL_9;
            10: a_to_g = `SEG_VAL_A;
            11: a_to_g = `SEG_VAL_B;
            12: a_to_g = `SEG_VAL_C;
            13: a_to_g = `SEG_VAL_D;
            14: a_to_g = `SEG_VAL_E;
            15: a_to_g = `SEG_VAL_F;
            default: a_to_g = `SEG_VAL_DEF;
        endcase
        if (rst) a_to_g = rst;
        if (num == 16'hffff) a_to_g = 16'hfffe;
    end
endmodule
