`timescale 1ns / 1ps

module top(
    input wire clk,
    input wire[4:0]   btn_in,
    input wire[15:0]  sw,
    output wire[15:0] led_C,
    output wire[3:0]  seg_C,
    output wire[6:0]  a_to_g
    );

    // clock
    wire       clk_cpu;
    wire       clk_dsp;

    // reset signal
    wire       rst;
    reg[31:0]  rst_c = 1024; // rst cycle

    wire[4:0]  btn_out;
    wire[31:0] display_C_32;
    wire[31:0] led_C_32;
    wire       timer_int;

    assign rst         = (rst_c == 0);
    assign led_C[15:0] = led_C_32[15:0];

    always @ (posedge clk)
        rst_c <= (rst_c == 0) ? 0 : rst_c - 1;


    /* --- clock --- */

    clk_div #(.N(16'h10)) inst_clk_cpu(
        .rst (rst ),
        .clk_in (clk ),
        .clk_out (clk_cpu )
    );

    clk_div #(.N(16'hffff)) inst_clk_dsp(
        .rst (rst ),
        .clk_in (clk ),
        .clk_out (clk_dsp )
    );


    /* --- cpu --- */

    cpu_top inst_cpu_top(
                  .clk (clk_cpu ),
                  .rst (rst ),
                  .switch_in ({16'b0, sw}  ),
                  .button_in ({27'b0, btn_out} ),
                  .display_C (display_C_32 ),
                  .led_C     (led_C_32 ),
                  .timer_int (timer_int )
              );


    /* --- io --- */

    display inst_display(
        .clk (clk_dsp ),
        .num (display_C_32[15:0] ),
        .seg_C (seg_C ),
        .a_to_g (a_to_g )
    );
    
    genvar i;
    generate
    for (i = 0; i < 5; i = i + 1) begin
        button inst_button(
            .clk (clk ),
            .rst (rst ),
            .btn_in  (btn_in[i] ),
            .btn_out (btn_out[i])
        );
    end
    endgenerate

endmodule
