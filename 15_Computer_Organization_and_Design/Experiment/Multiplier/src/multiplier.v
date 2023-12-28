`timescale 1ns / 1ps

module multiplier(

    input wire clk,
    input wire rst,

    input wire[15:0] num1,
    input wire[15:0] num2,

    output wire[31:0] result
    );

    reg [32:0] result_temp;
    assign result = result_temp[31:0];

    wire   lowest;
    assign lowest = result_temp[0];

    reg[5:0] count = 0;

    wire[16:0] temp;
    assign temp = result_temp[32:16] + num1;

    always @(posedge clk or negedge rst) begin
        if (!rst) begin
            result_temp[32:16] <= 0;
            result_temp[15:0]  <= num2;
            count              <= 0;
        end else if (count != 5'h10) begin
            if (lowest) begin
                result_temp <= {temp, result_temp[15:0]} >> 1;
            end else begin
                result_temp <= result_temp >> 1;
            end
            count <= count + 1;
        end else begin
            // do nothing
        end
    end

endmodule
