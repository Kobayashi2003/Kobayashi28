`timescale 1ns / 1ps
`include "definitions.v"

module cp0(
    input wire clk,
    input wire rst,

    input wire[31:0]  pc_if,
    input wire[31:0]  pc_id,
    input wire[31:0]  pc_exe,
    input wire[31:0]  pc_mem,
    input wire        bubble_id,
    input wire        bubble_exe,
    input wire        bubble_mem,

    input wire[4:0]   reg_read_addr,
    input wire[4:0]   reg_write_addr,
    input wire[31:0]  cp0_write_data,

    // interrupt siganls input
    input wire[5:0]                    hard_int,
    input wire[`EXC_TYPE_LENGTH - 1:0] exc_type,
    
    // cp0 read/write signals
    input wire                         cp0_read,
    input wire                         cp0_write,

    output wire[31:0] cp0_read_data,

    // cp0 registers
    output reg[31:0]  cp0_count,
    output reg[31:0]  cp0_compare,
    output reg[31:0]  cp0_status,
    output reg[31:0]  cp0_cause,
    output reg[31:0]  cp0_epc,
    output reg[31:0]  cp0_config,
    output reg[31:0]  cp0_prid,

    // interrupt signals output
    output reg                          timer_int,
    output wire                         int_signal,
    output wire                         eret_signal,
    output wire[`NPC_INT_OP_LENGTH-1:0] npc_int_op
    );

    wire[7:0] im;  // interrupt mask
    wire[7:0] ip;  // interrupt pending
    wire[4:0] exc_code; // exception code

    wire exl; // exception level
    wire ie;  // interrupt enable

    assign im = cp0_status[15:8];
    assign ip = cp0_cause[15:8];
    assign exc_code = cp0_cause[6:2];

    assign exl = cp0_status[1];
    assign ie  = cp0_status[0];

    wire int_avi;

    assign int_avi = ((exc_type == `EXC_TYPE_INT  && (im[7:2] & hard_int)      ) ||
                      (exc_type == `EXC_TYPE_SYS) || (exc_type == `EXC_TYPE_RI ) ||
                      (exc_type == `EXC_TYPE_OV ) || (exc_type == `EXC_TYPE_TR )  ) ? 1 : 0;   

    assign int_signal = (ie && !exl) ? int_avi : 0;
                       
    assign eret_signal = ((!ie || exl) && (exc_type == `EXC_TYPE_ERET)) ? 1 : 0;

    assign npc_int_op = (int_signal                ) ? 
                        (im[2] && hard_int[0]      ) ? `NPC_OP_HARD0 :
                        (im[3] && hard_int[1]      ) ? `NPC_OP_HARD1 :
                        (im[4] && hard_int[2]      ) ? `NPC_OP_HARD2 :
                        (im[5] && hard_int[3]      ) ? `NPC_OP_HARD3 :
                        (im[6] && hard_int[4]      ) ? `NPC_OP_HARD4 :
                        (im[7] && hard_int[5]      ) ? `NPC_OP_HARD5 :
                        (im[0] && ip[0]            ) ? `NPC_OP_SOFT0 :
                        (im[1] && ip[1]            ) ? `NPC_OP_SOFT1 :
                        (exc_type == `EXC_TYPE_SYS ) ? `NPC_OP_SYS :
                        (exc_type == `EXC_TYPE_RI  ) ? `NPC_OP_RI :
                        (exc_type == `EXC_TYPE_OV  ) ? `NPC_OP_OV :
                        (exc_type == `EXC_TYPE_TR  ) ? `NPC_OP_TR : `NPC_INI_OP_DEFAULT :
                        (eret_signal               ) ? `NPC_OP_ERET : `NPC_INI_OP_DEFAULT;

    assign cp0_read_data = (!cp0_read) ? `INIT_32 :
        (reg_read_addr == `CP0_REG_COUNT  ) ? (
            (cp0_write && reg_write_addr == `CP0_REG_COUNT) ? cp0_write_data : cp0_count
        ) :
        (reg_read_addr == `CP0_REG_COMPARE) ? (
            (cp0_write && reg_write_addr == `CP0_REG_COMPARE) ? cp0_write_data : cp0_compare
        ) :
        (reg_read_addr == `CP0_REG_STATUS ) ? (
            (cp0_write && reg_write_addr == `CP0_REG_STATUS) ? cp0_write_data : cp0_status
        ) :
        (reg_read_addr == `CP0_REG_CAUSE  ) ? (
            (cp0_write && reg_write_addr == `CP0_REG_CAUSE) ? 
                {cp0_cause[31:24], cp0_write_data[23:22], cp0_cause[21:10], cp0_write_data[9:8], cp0_cause[7:0]} :cp0_cause
        ) :
        (reg_read_addr == `CP0_REG_EPC    ) ? (
            (cp0_write && reg_write_addr == `CP0_REG_EPC) ? cp0_write_data : cp0_epc
        ) :
        (reg_read_addr == `CP0_REG_CONFIG ) ? cp0_config :
        (reg_read_addr == `CP0_REG_PRID   ) ? cp0_prid :
        `INIT_32;

    always @ (posedge clk or negedge rst) begin
        if (!rst) begin
            cp0_count     <= `INIT_32;
            cp0_compare   <= `CP0_COMPARE_DEFAULT;
            cp0_status    <= `CP0_STATUS_DEFAULT;
            cp0_cause     <= `INIT_32;
            cp0_epc       <= `INIT_32;
            cp0_config    <= `INIT_32;
            cp0_prid      <= `INIT_32;
            timer_int     <= `INTERRUPT_NOT_ASSERT;
        end
        else begin
            cp0_count        <= (cp0_write && reg_write_addr == `CP0_REG_COUNT  ) ? cp0_write_data : cp0_count + 1;
            cp0_compare      <= (cp0_write && reg_write_addr == `CP0_REG_COMPARE) ? cp0_write_data : cp0_compare;
            timer_int        <= (cp0_write && reg_write_addr == `CP0_REG_COMPARE) ? `INTERRUPT_NOT_ASSERT :
                                (timer_int == `INTERRUPT_ASSERT                 ) ? `INTERRUPT_ASSERT :
                                (cp0_compare != `INIT_32 && cp0_count == cp0_compare) ? `INTERRUPT_ASSERT : `INTERRUPT_NOT_ASSERT;

            cp0_cause[31]    <= 0;         // branch delay slot
            cp0_cause[23]    <= (cp0_write && reg_write_addr == `CP0_REG_CAUSE  ) ? cp0_write_data[23] : cp0_cause[23]; // interrupt vector
            cp0_cause[22]    <= (cp0_write && reg_write_addr == `CP0_REG_CAUSE  ) ? cp0_write_data[22] : cp0_cause[22]; // watch pending

            cp0_cause[15:10] <= (cp0_write && reg_write_addr == `CP0_REG_CAUSE  ) ? cp0_write_data[15:10] : 
                                (int_avi                                        ) ? hard_int :
                                (eret_signal                                    ) ? `INIT_6 : ip; // hardware interrupt pending

            cp0_cause[9:8]   <= (cp0_write && reg_write_addr == `CP0_REG_CAUSE  ) ? cp0_write_data[9:8] : cp0_cause[9:8]; // software interrupt pending

            cp0_cause[6:2]   <= (cp0_write && reg_write_addr == `CP0_REG_CAUSE  ) ? cp0_write_data[6:2] : 
                                (int_signal                                     ) ? exc_type :
                                (eret_signal                                    ) ? `INIT_5 : exc_code; // exception code

            cp0_status[31:2] <= (cp0_write && reg_write_addr == `CP0_REG_STATUS ) ? cp0_write_data[31:2] : cp0_status[31:2];
        
            cp0_status[1]    <= (cp0_write && reg_write_addr == `CP0_REG_STATUS ) ? cp0_write_data[1] : 
                                (int_signal                                     ) ? 1 :
                                (eret_signal                                    ) ? 0 : exl; // exception level

            cp0_status[0]    <= (cp0_write && reg_write_addr == `CP0_REG_STATUS ) ? cp0_write_data[0] :
                                (int_signal                                     ) ? 0 :
                                (eret_signal                                    ) ? 1 : ie; // interrupt enable
            cp0_epc          <= (cp0_write && reg_write_addr == `CP0_REG_EPC    ) ? cp0_write_data : 
                                (int_signal                                     ) ? (
                                    (!bubble_mem                                ) ? pc_mem :
                                    (!bubble_exe                                ) ? pc_exe :
                                    (!bubble_id                                 ) ? pc_id : pc_if) : 
                                (eret_signal                                    ) ? `INIT_32 : cp0_epc; // exception program counter
        end
    end
endmodule
