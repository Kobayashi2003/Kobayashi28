`timescale 1ns / 1ps

module display(
    input wire clk,
    input wire[15:0] num,
    output reg[3:0]  seg_C,
    output reg[6:0]  a_to_g
    );

    integer  seg_num = 0;
    reg[3:0] x = 0;

    always @ (posedge clk) begin
        case (seg_num)
            0: begin x = num[15:12]     ;    seg_C = 4'b0111; end
            1: begin x = num[11:8]      ;    seg_C = 4'b1011; end
            2: begin x = num[7:4]       ;    seg_C = 4'b1101; end
            3: begin x = num[3:0]       ;    seg_C = 4'b1110; end
            default: begin x = 0        ;    seg_C = 4'b1111; end
        endcase
        seg_num <= (seg_num + 1) % 4;
    end

    always @ (x) begin
        case (x)
            0: a_to_g = `VAL_0;
            1: a_to_g = `VAL_1;
            2: a_to_g = `VAL_2;
            3: a_to_g = `VAL_3;
            4: a_to_g = `VAL_4;
            5: a_to_g = `VAL_5;
            6: a_to_g = `VAL_6;
            7: a_to_g = `VAL_7;
            8: a_to_g = `VAL_8;
            9: a_to_g = `VAL_9;
            10: a_to_g = `VAL_A;
            11: a_to_g = `VAL_B;
            12: a_to_g = `VAL_C;
            13: a_to_g = `VAL_D;
            14: a_to_g = `VAL_E;
            15: a_to_g = `VAL_F;
            default: a_to_g = `VAL_DEF;
        endcase
    end

endmodule
