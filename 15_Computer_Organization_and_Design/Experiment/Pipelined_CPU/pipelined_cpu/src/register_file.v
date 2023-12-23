`timescale 1ns / 1ps
`include "definitions.v"

module register_file(
    input wire clk,
    input wire[4:0]  rs,
    input wire[4:0]  rt,
    input wire[4:0]  write_reg_addr, 
    input wire[31:0] write_data,

    input wire reg_write,

    output wire[31:0] reg1_data,
    output wire[31:0] reg2_data
    );

    // Register file general purpose register
    reg[31:0] gpr[31:0];

    // Get register data from GPR
    // assign reg1_data = (rs == `REG_0_ADDR) ? `INIT_32 : gpr[rs];
    // assign reg2_data = (rt == `REG_0_ADDR) ? `INIT_32 : gpr[rt];

    assign reg1_data =  (rs == `REG_0_ADDR) ? `INIT_32 :
                        (reg_write && (write_reg_addr == rs)) ? write_data : gpr[rs];
                
    assign reg2_data =  (rt == `REG_0_ADDR) ? `INIT_32 :
                        (reg_write && (write_reg_addr == rt)) ? write_data : gpr[rt];

    always @ (posedge clk) begin
        if (reg_write && (write_reg_addr != `INIT_5)) begin
            gpr[write_reg_addr] <= write_data;
        end
    end
endmodule
