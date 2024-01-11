`timescale 1ns / 1ps
`include "instruction_head.v"
`include "hardware_head.v"

module Top(
    input wire clk_main, // main clock

    // button input, high level active
    input wire start,   // start to sort the array (use as reset)
    input wire go_lst,  // go to the last number 
    input wire go_nxt,  // go to the next number 
    input wire switch,  // switch between the current number and the debug information
    input wire confirm, // confirm to input the current number to the array
    // dip switch input, high level active
    input wire [`NUM_SIZE - 1:0]  cur_num, 

    output wire [`ARRAY_SIZE-1:0] cue_lgt, // cue light show the current index
    output wire [`SEG_SIZE - 1:0] seg,     
    output wire [6:0]  a_to_g
    );

    // reg clk_main;
    // reg debug = 0;
    // reg rst = 1;

    wire clk_div; // divided clock, convinient for debugging
    wire clk;     // clk chosen by clk_mux (clk_main or clk_div)

    // cpu debug information
    wire        debug;
    assign      debug = (cur_num[0]) ? 1'b1 : 1'b0;

    wire [7:0]  debug_reg_single; // debug information: single register value from gpr
    wire [7:0]  debug_dm_single;  // debug information: single data memory value from dm
    wire [5:0]  debug_opcode;     // debug information: opcode from instruction[31:26]
    wire [5:0]  debug_func;       // debug information: func from instruction[5:0]
    wire [9:0]  debug_pc;         // debug information: pc from pc[9:0]
    wire [7:0]  debug_alu;        // debug information: alu result from alu_result[7:0]
    // cpu debug signals
    wire cpu_wake; // debug signal: wake signal from cpu
    wire cpu_slep; // debug signal: sleep signal from cpu
    // debug pin
    reg [6:0] pin;

    // cpu status
    wire cpu_stat;                      // cpu state (0: sleep, 1: wake)
    wire halt;                          // halt signal from cpu 
    wire sysc_mp;                       // syscall mono pulse
    wire [`SYS_OP_LENGTH - 1:0] sys_op; // syscall operation from cpu 

    // array : a buffer between CPU and hardware 
    reg [15:0] array [0:`ARRAY_SIZE-1]; // array stores the 16 numbers
    reg [3:0]  index;                   // for sequential array traversal
    reg [3:0]  cur_index;               // current index of the array

    // ShowNum input interface
    wire [`NUM_SIZE:0] show_num; // show_num will be given to the ShowNum module  
                                 // and be shown on the seven-segment display 

    // system interface 
    reg [31:0] sys_inf_in;  // system input interface
    wire[31:0] sys_inf_out; // system output interface

    wire start_efct;   // effective start signal
    wire go_lst_efct;  // effective go_lst signal
    wire go_nxt_efct;  // effective go_nxt signal
    wire switch_efct;  // effective switch signal
    wire confirm_efct; // effective confirm signal

    wire   rst; 
    assign rst = ~start;

    wire   array_acc;    // array access signal
    assign array_acc = sysc_mp || confirm_efct;

    integer i;
    initial begin
        index = 0;
        cur_index  = 0;
        sys_inf_in = 0;

        pin = 0;

        for (i = 0; i < 16; i = i + 1) array[i] = 16 - i;

        // clk_main = 0;
        // forever 
        //     #1 clk_main = ~clk_main;
    end

    assign cpu_slep = (cur_num[1] && debug) ? 1'b1 : 1'b0;
    assign cpu_wake = (cur_num[2] && debug) ? 1'b1 : 1'b0;

    // To simplify the problem, I chose to use 
    // sequential array traversal to interact with the CPU.
    // When the start button is pressed, the index is reset to 0.
    // And every communication with the CPU will increase the index by 1.
    always @ (posedge array_acc) begin
        if (confirm_efct) begin
            array[cur_index] <= cur_num;
        end else if (sysc_mp && (sys_op == `SYSCALL_INPUT_INT)) begin
            // $display("sys_op = `SYSCALL_INPUT_INT, sys_inf_in  = %d", array[index]);
            sys_inf_in   <= array[index];
            index <= (index+1) % `ARRAY_SIZE;
        end else if (sysc_mp && (sys_op == `SYSCALL_OUTPUT_INT)) begin
            // $display("sys_op = `SYSCALL_OUTPUT_INT, sys_inf_out = %d", sys_inf_out);
            array[index] <= sys_inf_out[15:0];
            index <= (index+1) % `ARRAY_SIZE;
        end
    end

    // if go_lst (go_nxt) is pressed, cur_index - 1 (cur_index + 1)
    reg [31:0] cnt = `GO_BTN_DELAY;
    always @ (posedge clk_main) begin
        if (!go_lst_efct && !go_nxt_efct) begin
            cnt <= `GO_BTN_DELAY;
        end else begin 
            cnt <= cnt + 1;
            if (cnt == `GO_BTN_DELAY) begin
                cur_index <= cur_index + go_nxt_efct - go_lst_efct;
                if (cur_index == `ARRAY_SIZE) cur_index <= 0;
                else if (cur_index == -1)     cur_index <= `ARRAY_SIZE - 1;
                cnt <= 0;
            end
        end
    end

    // assign show_num = (switch) ? array[cur_index] : cur_num;
    assign show_num = ( switch ? 
                      // debug information
                      ( debug ? (
                       (cur_num[15]) ? {8'h00, debug_reg_single} :
                       (cur_num[14]) ? {2'h0, debug_opcode, 2'h0, debug_func} :
                       (cur_num[13]) ? {8'h00, debug_dm_single} :
                       (cur_num[12]) ? {8'h00, debug_pc} :
                       (cur_num[11]) ? {8'h00, debug_alu} :
                       (cur_num[10]) ? {3'h0, cpu_stat, 3'h0, halt, 3'h0, sysc_mp, index} :
                       (cur_num[9])  ? sys_op :
                       (cur_num[8])  ? sys_inf_in[15:0] :
                       (cur_num[7])  ? sys_inf_out[15:0] : 
                       array[cur_index]) : array[cur_index]) :
                       // normal information
                       cur_num);



    CLK_Div #(.N(`CLK_MAIN_DELAY)) INST_CLK_DIV(
        .clk_in(clk_main),
        .clk_out(clk_div));

    clk_mux INST_CLK_MUX (
        .clk_in1(clk_div),
        .clk_in2(clk_main),
        .chose(debug),
        .clk_out(clk));

    IO INST_IO (
        .clk(clk_main),
        .debug(pin),

        .start(start),
        .confirm(confirm),
        .go_lst(go_lst),
        .go_nxt(go_nxt),

        .show_num(show_num),
        .cur_index(cur_index),

        .start_efct(start_efct),
        .switch_efct(switch_efct),
        .confirm_efct(confirm_efct),
        .go_lst_efct(go_lst_efct),
        .go_nxt_efct(go_nxt_efct),

        .cue_lgt(cue_lgt),
        .seg(seg),
        .a_to_g(a_to_g));

    CPU_Ctrl INST_CPU_Ctrl(
        .clk(clk),
        .rst(rst),
        .start(start_efct),
        .cpu_slep(cpu_slep),
        .cpu_wake(cpu_wake),
        .sys_inf_in(sys_inf_in),

        .cpu_stat(cpu_stat),
        .halt(halt),
        .sysc_mp(sysc_mp),
        .sys_op(sys_op),
        .sys_inf_out(sys_inf_out),

        .debug_reg_single(debug_reg_single),
        .debug_opcode(debug_opcode),
        .debug_func(debug_func),
        .debug_dm_single(debug_dm_single),
        .debug_pc(debug_pc),
        .debug_alu(debug_alu));

endmodule
