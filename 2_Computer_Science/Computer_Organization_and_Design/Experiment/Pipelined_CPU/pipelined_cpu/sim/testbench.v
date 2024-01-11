`timescale 1ns / 1ps

module testbench();


reg clk;
reg rst;
reg[4:0]  button_in;
reg[15:0] switch_in;
wire[15:0] led_C;

wire[4:0] button_out;

wire[31:0] display_C_32;
wire[31:0] led_C_32;
wire timer_int;

assign led_C = led_C_32[15:0];

// genvar i;
// generate
//     for (i = 0; i < 16; i = i + 1) begin
//         button #(.N(32'd100)) inst_button(
//             .clk (clk ),
//             .rst (rst ),
//             .btn_in  (button_in[i] ),
//             .btn_out (button_out[i] )
//         );
//     end
// endgenerate

assign button_out = button_in;

cpu_top inst_cpu_top(
              .clk (clk ),
              .rst (rst ),
              .button_in ({27'b0, button_out} ),
              .switch_in ({16'b0, switch_in} ),
              .display_C (display_C_32 ),
              .led_C (led_C_32 ),
              .timer_int (timer_int )
          );

initial begin
    // Load instructions
    $readmemh("../../../../pipelined_cpu.tbcode/instructions.txt", inst_cpu_top.inst_instruction_memory.im);
    // Load register initial values
    $readmemh("../../../../pipelined_cpu.tbcode/register.txt", inst_cpu_top.inst_register_file.gpr);
    // Load memory data initial values
    $readmemh("../../../../pipelined_cpu.tbcode/data_memory.txt", inst_cpu_top.inst_data_memory.dm);

    rst = 0;
    clk = 0;
    button_in = 0;
    switch_in = 0;

    #30 rst = 1;

    // #400  button_in[3] = 1;
    // #8000 button_in = 0;
    // #400  button_in[4] = 1;
    // #8000 button_in = 0;
    // #400  button_in[1] = 1;
    // #2000  button_in = 0;
    #400  button_in[0] = 1;

    // #2000 $stop;
end

// always @ (*)
    // hard_int[0] = timer_int;

always begin
    #20 clk = ~clk;
    switch_in = switch_in + 1;
end
endmodule
