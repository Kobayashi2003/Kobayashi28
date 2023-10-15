`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/10/11 21:05:01
// Design Name: 
// Module Name: ShowNum
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


module ShowNum(
    input CLK,
    input [7:0] _show_num,
    input isResult,
    input isSigned,
    input SF,
    output reg [3:0] seg,
    output reg [6:0] a_to_g
    );

    reg [7:0] show_num = 0;

    reg [3:0] seg_num = 0;
    reg [3:0] x = 0;

    reg sign1, sign2;
    reg [3:0] num1;
    reg [3:0] num2;

    always @(posedge CLK) begin
        if (isResult)  begin
            if (isSigned && SF)
                show_num = ((~_show_num) + 1) & 8'h0f; // convert to 2's complement and only keep last 4 bits 
            else 
                show_num = _show_num & 8'h0f;

            case (seg_num)
                0: begin x = show_num / 1000; seg = 4'b0111; end
                1: begin x = show_num / 100 % 10; seg = 4'b1011; end
                2: begin x = show_num / 10 % 10; seg = 4'b1101; end
                3: begin x = show_num % 10; seg = 4'b1110; end
            endcase
        end


        else begin
            if (isSigned) begin
                sign1 = _show_num[7]; // sign bit of num1
                sign2 = _show_num[3]; // sign bit of num2

                if (sign1) 
                    num1 = (~_show_num[7:4] + 1);
                else 
                    num1 = _show_num[7:4];
                
                if (sign2) 
                    num2 = (~_show_num[3:0] + 1);
                else 
                    num2 = _show_num[3:0];

                show_num = {num1, num2};
            end
            else begin
                show_num = _show_num;
            end

            case (seg_num)
                0: begin x = show_num[7:4] / 10; seg = 4'b0111; end
                1: begin x = show_num[7:4] % 10; seg = 4'b1011; end
                2: begin x = show_num[3:0] / 10; seg = 4'b1101; end
                3: begin x = show_num[3:0] % 10; seg = 4'b1110; end
            endcase
        end

        seg_num = (seg_num + 1) % 4;
    end

    always @(*) begin
        case (x)
            0: a_to_g = 7'b0000001;
            1: a_to_g = 7'b1001111;
            2: a_to_g = 7'b0010010;
            3: a_to_g = 7'b0000110;
            4: a_to_g = 7'b1001100;
            5: a_to_g = 7'b0100100;
            6: a_to_g = 7'b0100000;
            7: a_to_g = 7'b0001111;
            8: a_to_g = 7'b0000000;
            9: a_to_g = 7'b0000100;
            default: a_to_g = 7'b1111111;
        endcase
    end

endmodule
