`timescale 1ns / 1ps
`include "definitions.v"

module io_memory(
    input wire clk,
    input wire rst,

    input wire[31:0] switch_in,
    input wire[31:0] button_in,

    input wire mem_write,

    input wire[11:2] mem_addr,
    input wire[31:0] write_mem_data,

    output wire[31:0] read_mem_data,

    output reg[31:0]  display_C,
    output reg[31:0]  led_C
    );

    // buffer memory
    reg[31:0] buffer[`BUF_LENGTH:0];
    integer i;

    assign read_mem_data = 
        (mem_addr == `IO_ADDR_DISPLAY) ? display_C :
        (mem_addr == `IO_ADDR_LED    ) ? led_C :
        (mem_addr == `IO_ADDR_SWITCH ) ? switch_in :
        (mem_addr == `IO_ADDR_BUTTON ) ? button_in :
        (mem_addr >= `IO_ADDR_BUF && mem_addr < `IO_ADDR_BUF + `BUF_LENGTH) ?
            buffer[mem_addr - `IO_ADDR_BUF] : `INIT_32;

    always @ (posedge clk or negedge rst) begin
        if (!rst) begin
            display_C <= `DISPLAY_INIT;
            led_C     <= `LED_INIT;
            for (i = 0; i < 18; i = i + 1) begin
                buffer[i] <= `INIT_32;
            end
        end
        else begin
            if (mem_write) begin
                if (mem_addr == `IO_ADDR_DISPLAY) begin
                    display_C <= write_mem_data;
                end
                else if (mem_addr == `IO_ADDR_LED) begin
                    led_C <= write_mem_data;
                end
                else if (mem_addr >= `IO_ADDR_BUF && mem_addr < `IO_ADDR_BUF + `BUF_LENGTH) begin
                    buffer[mem_addr - `IO_ADDR_BUF] <= write_mem_data;
                end
                else begin
                    // do nothing
                end
            end else begin
                // do nothing
            end 
        end
    end

endmodule
