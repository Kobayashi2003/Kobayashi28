`timescale 1ns / 1ps

module CLK_Div #(parameter N = 16'hffff) (
    input   wire    clk_in,
    output  wire    clk_out
    );

    reg [15:0]      cnt = 0;
    reg             out = 0;

    assign clk_out = out;

    always @(posedge clk_in) begin
        if (cnt == N) begin
            cnt <= 0;
            out <= ~out;
        end
        else begin
            cnt <= cnt + 1;
        end 
    end
endmodule