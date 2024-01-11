`timescale 1ns / 1ps
`include "definitions.v"    

module cpu_top(
    input wire clk,
    input wire rst, 
    input wire[31:0]  button_in,
    input wire[31:0]  switch_in,
    output wire[31:0] display_C,
    output wire[31:0] led_C,
    output wire       timer_int
    );

    /* 
     * Instanciate modules
     */


    /* --- Coprocessor 0 --- */

    wire[5:0]  hard_int;
    assign hard_int = {timer_int, button_in[4:0]};

    // cp0
    wire[31:0] cp0_read_data;
    wire[31:0] cp0_count;
    wire[31:0] cp0_compare;
    wire[31:0] cp0_status;
    wire[31:0] cp0_cause;
    wire[31:0] cp0_epc;
    wire[31:0] cp0_config;
    wire[31:0] cp0_prid;
    // wire       timer_int;
    wire       int_signal;
    wire       eret_signal;
    wire[`NPC_INT_OP_LENGTH-1:0] npc_int_op;

    wire [7:0] ip;       // interrupt pending
    wire [7:0] im;       // interrupt mask
    wire [4:0] exc_code; // exception code

    assign ip       = cp0_cause[15:8];
    assign im       = cp0_status[15:8];
    assign exc_code = cp0_cause[6:2];



    /* --- Stage 1: Instruction Fetch --- */

    wire[31:0] npc;
    wire[31:0] re_addr;
    wire[31:0] pc;
    wire[31:0] instruction;

    /* if/id register */
    wire[31:0] pc_id;
    wire[31:0] instruction_id;
    wire       bubble_id;



    /* --- Stage 2: Instruction Decode --- */

    // Decode instruction opcode and funct
    wire[5:0] opcode;
    wire[5:0] func;

    // Decode registers 
    wire[4:0] rs;
    wire[4:0] rt;
    wire[4:0] rd;
    wire[4:0] sa;

    // Decode 16 bit and 26 bit immediates
    wire[15:0] imm16;
    wire[25:0] imm26;

    // Assign decoded instruction to variables
    assign opcode = instruction_id[31:26];
    assign func   = instruction_id[5:0];
    assign rs     = instruction_id[25:21];
    assign rt     = instruction_id[20:16];
    assign rd     = instruction_id[15:11];
    assign sa     = instruction_id[10:6];
    assign imm16  = instruction_id[15:0];
    assign imm26  = instruction_id[25:0];

    // Control unit
    wire[`EXT_OP_LENGTH-1:0]  ext_op;
    wire[`ALU_SRC_LENGTH-1:0] alu_src;
    wire[`ALU_OP_LENGTH-1:0]  alu_op;
    wire                      mem_read;
    wire                      mem_write;
    wire                      reg_write;
    wire[`REG_SRC_LENGTH-1:0] reg_src;
    wire[`REG_DST_LENGTH-1:0] reg_dst;
    wire[`NPC_OP_LENGTH-1:0]  npc_op;
    wire                      cp0_read;
    wire                      cp0_write;
    wire[3:0]                 flush_C;
    wire                      slot_flush;
    wire[`EXC_TYPE_LENGTH-1:0]exc_type;
    wire                      inst_ukn;

    // stall unit
    wire[3:0]  stall_C;
    // register file
    wire[31:0] reg1_data;
    wire[31:0] reg2_data;
    // extention unit
    wire[31:0] ext_imm;
    // forwarding unit
    wire[1:0]  forward_A;
    wire[1:0]  forward_B;
    // forwarding mux
    wire[31:0] forward_mux_out_A;
    wire[31:0] forward_mux_out_B;
    // alu src mux
    wire[31:0] alu_src_mux_out;
    // branch judge
    wire       zero;
    // reg dst mux
    wire[4:0]  reg_dst_mux_out;

    /* id/ex register */
    wire[31:0] alu_input1_exe;
    wire[31:0] alu_input2_exe;
    wire[31:0] reg2_data_exe;
    wire[4:0]  rs_exe;
    wire[4:0]  rt_exe;
    wire[4:0]  rd_exe;
    wire[4:0]  sa_exe;
    wire[31:0] ext_imm_exe;
    wire[31:0] re_addr_exe;
    wire[4:0]  dst_reg_exe;
    wire[31:0] pc_exe;
    wire[`ALU_SRC_LENGTH-1:0] alu_src_exe;
    wire[`ALU_OP_LENGTH -1:0] alu_op_exe;
    wire[`REG_DST_LENGTH-1:0] reg_dst_exe;
    wire                      mem_read_exe;
    wire                      mem_write_exe;
    wire                      cp0_write_exe;
    wire                      reg_write_exe;
    wire[`REG_SRC_LENGTH-1:0] reg_src_exe;
    wire[`EXC_TYPE_LENGTH-1:0]exc_type_exe;
    wire                      bubble_exe;


    /* --- Stage 3: Execute --- */

    // ALU
    wire[31:0] alu_result;
    wire[`EXC_TYPE_LENGTH-1:0] exc_type_out;
    
    // ex/mem register
    wire[31:0] alu_result_mem;
    wire[31:0] reg2_data_mem; 
    wire[31:0] ext_imm_mem;
    wire[4:0]  dst_reg_mem;
    wire[31:0] re_addr_mem;
    wire[31:0] pc_mem;
    wire                      mem_read_mem;
    wire                      mem_write_mem;
    wire                      cp0_write_mem;
    wire                      reg_write_mem;
    wire[`REG_SRC_LENGTH-1:0] reg_src_mem;
    wire[`EXC_TYPE_LENGTH-1:0]exc_type_mem;
    wire                      bubble_mem;



    /* --- Stage 4: Memory Access --- */

    // Data memory
    wire[31:0] read_mem_data;

    // io memory
    wire datamem_w;
    wire iomem_w;

    wire[31:0] read_datamem;
    wire[31:0] read_iomem;

    assign datamem_w = mem_write_mem & (alu_result_mem[31:30] == 2'b00);
    assign iomem_w   = mem_write_mem & (alu_result_mem[31:30] == 2'b01);

    assign read_mem_data = (alu_result_mem[31:30] == 2'b00) ? read_datamem :
                           (alu_result_mem[31:30] == 2'b01) ? read_iomem   :
                           `INIT_32;

    // mem/wb register
    wire[31:0] read_mem_data_wb;
    wire[31:0] alu_result_wb;
    wire[31:0] ext_imm_wb;
    wire[4:0]  dst_reg_wb;
    wire[31:0] re_addr_wb;
    wire                      cp0_write_wb;
    wire                      reg_write_wb;
    wire[`REG_SRC_LENGTH-1:0] reg_src_wb;



    /* --- Stage 5: Write Back --- */

    // Register source mux
    wire[31:0] reg_src_mux_out;

    /* coprocessor 0 instruction */

    cp0 inst_cp0(
        .clk(clk),
        .rst(rst),

        .pc_if(pc),
        .pc_id(pc_id),
        .pc_exe(pc_exe),
        .pc_mem(pc_mem),
        .bubble_id(bubble_id),
        .bubble_exe(bubble_exe),
        .bubble_mem(bubble_mem),

        .hard_int(hard_int),
        .exc_type(exc_type_mem),

        .reg_read_addr(rd),
        .reg_write_addr(dst_reg_wb),
        .cp0_read(cp0_read),
        .cp0_write(cp0_write_wb),
        .cp0_write_data(reg_src_mux_out),

        .cp0_read_data(cp0_read_data),
        .cp0_count(cp0_count),
        .cp0_compare(cp0_compare),
        .cp0_status(cp0_status),
        .cp0_cause(cp0_cause),
        .cp0_epc(cp0_epc),
        .cp0_config(cp0_config),
        .cp0_prid(cp0_prid),
        .timer_int(timer_int),
        .int_signal(int_signal),
        .eret_signal(eret_signal),
        .npc_int_op(npc_int_op)
    );



    /* --- Stage 1: Instruction Fetch --- */

    npc inst_npc(
        .pc_if(pc),
        .pc_id(pc_id),
        .cp0_epc(cp0_epc),
        .imm16(imm16),
        .imm26(imm26),
        .rs_data(forward_mux_out_A),
        .npc_op(npc_op),
        .npc_int_op(npc_int_op),

        .npc(npc),
        .re_addr(re_addr)
    );

    pc inst_pc(
        .clk(clk),
        .rst(rst),
        .npc(npc),
        .stall_C(stall_C),
        .flush_C(flush_C),

        .pc(pc)
    );

    // instruction_memory inst_instruction_memory(
    //     .instruction_addr(pc[11:2]),

    //     .instruction(instruction)
    // );

    instruction_memory_ip inst_instruction_memory_ip(
        .a(pc[11:2]),

        .spo(instruction)
    );

    /* if/id register */

    reg_if_id inst_reg_if_id(
        .clk(clk),
        .rst(rst),
        .stall_C(stall_C),
        .flush_C(flush_C),
        .slot_flush(slot_flush),

        .pc_in(pc),
        .instructions_in(instruction),

        .pc_out(pc_id),
        .instructions_out(instruction_id),
        .bubble_out(bubble_id)
    );




    /* --- Stage 2: Instruction Decode --- */

    control inst_control(
        .rst(rst),
        .opcode(opcode),
        .rs(rs),
        .rt(rt),
        .rd(rd),
        .sa(sa),
        .func(func),
        .zero(zero),
        .int_signal(int_signal),
        .eret_signal(eret_signal),

        .ext_op(ext_op),
        .alu_src(alu_src),
        .alu_op(alu_op),
        .mem_read(mem_read),
        .mem_write(mem_write),
        .cp0_read(cp0_read),
        .cp0_write(cp0_write),
        .reg_write(reg_write),
        .reg_src(reg_src),
        .reg_dst(reg_dst),
        .npc_op(npc_op),
        .flush_C(flush_C),
        .slot_flush(slot_flush),
        .exc_type(exc_type),
        .inst_ukn(inst_ukn)
    );

    stall_unit inst_stall_unit(
        .cp0_write_exe(cp0_write_exe),
        .cp0_read_id(cp0_read),
        .reg_write_exe(reg_write_exe),
        .reg_write_mem(reg_write_mem),
        .mem_read_exe(mem_read_exe),
        .mem_read_mem(mem_read_mem),
        .dst_reg_exe(dst_reg_exe),
        .dst_reg_mem(dst_reg_mem),
        .if_id_rs(rs),
        .if_id_rt(rt),
        .if_id_rd(rd),

        .stall_C(stall_C)
    );

    register_file inst_register_file(
        .clk(clk),
        .rs(rs),
        .rt(rt),
        .write_reg_addr(dst_reg_wb),
        .write_data(reg_src_mux_out),
        .reg_write(reg_write_wb),

        .reg1_data(reg1_data),
        .reg2_data(reg2_data)
    );

    extend inst_extend(
        .imm16(imm16),
        .ext_op(ext_op),

        .extended_imm(ext_imm)
    );

    forwarding_unit_id inst_forwarding_unit(
        .if_id_cp0read(cp0_read),
        .ex_mem_cp0write(cp0_write_mem),
        .mem_wb_cp0write(cp0_write_wb),
        .ex_mem_regwrite(reg_write_mem),
        .ex_mem_regdst(dst_reg_mem),
        .mem_wb_regwrite(reg_write_wb),
        .mem_wb_regdst(dst_reg_wb),
        .if_id_rs(rs),
        .if_id_rt(rt),
        .if_id_rd(rd),

        .forward_A(forward_A),
        .forward_B(forward_B)
    );

    forward_mux inst_forward_mux_A(
        .forward_C(forward_A),
        .rs_rt_data(reg1_data),
        .write_data(reg_src_mux_out),
        .alu_result(alu_result_mem),

        .mux_out(forward_mux_out_A)
    );

    forward_mux inst_forward_mux_B(
        .forward_C(forward_B),
        .rs_rt_data(reg2_data),
        .write_data(reg_src_mux_out),
        .alu_result(alu_result_mem),

        .mux_out(forward_mux_out_B)
    );

    alu_src_mux inst_alu_src_mux(
        .alu_src(alu_src),
        .rt_data(forward_mux_out_B),
        .extend_imm(ext_imm),
        .cp0_data(cp0_read_data),

        .mux_out(alu_src_mux_out)
    );

    branch_judge inst_branch_judge(
        .reg1_data(forward_mux_out_A),
        .reg2_data(forward_mux_out_B),

        .zero(zero)
    );

    reg_dst_mux inst_reg_dst_mux(
        .reg_dst(reg_dst),
        .rt(rt),
        .rd(rd),

        .mux_out(reg_dst_mux_out)
    );

    /* id/ex register */

    reg_id_ex inst_reg_id_ex(
        .clk(clk),
        .rst(rst),
        .stall_C(stall_C),
        .flush_C(flush_C),
        .alu_input1_in(forward_mux_out_A),
        .alu_input2_in(alu_src_mux_out),   
        .reg2_data_in(forward_mux_out_B),
        .rs_in(rs),
        .rt_in(rt),
        .rd_in(rd),
        .sa_in(sa),
        .ext_imm_in(ext_imm),
        .re_addr_in(re_addr),
        .dst_reg_in(reg_dst_mux_out),
        .pc_in(pc_id),

        .alu_src_in(alu_src),
        .alu_op_in(alu_op),
        .reg_dst_in(reg_dst),
        .mem_read_in(mem_read),
        .mem_write_in(mem_write),
        .cp0_write_in(cp0_write),
        .reg_write_in(reg_write),
        .reg_src_in(reg_src),
        .exc_type_in(exc_type),
        .bubble_in(bubble_id),

        .alu_input1_out(alu_input1_exe),
        .alu_input2_out(alu_input2_exe),
        .reg2_data_out(reg2_data_exe),
        .rs_out(rs_exe),
        .rt_out(rt_exe),
        .rd_out(rd_exe),
        .sa_out(sa_exe),
        .ext_imm_out(ext_imm_exe),
        .re_addr_out(re_addr_exe),
        .dst_reg_out(dst_reg_exe),
        .pc_out(pc_exe),

        .alu_src_out(alu_src_exe),
        .alu_op_out(alu_op_exe),
        .reg_dst_out(reg_dst_exe),
        .mem_read_out(mem_read_exe),
        .mem_write_out(mem_write_exe),
        .cp0_write_out(cp0_write_exe),
        .reg_write_out(reg_write_exe),
        .reg_src_out(reg_src_exe),
        .exc_type_out(exc_type_exe),
        .bubble_out(bubble_exe)
    );



    /* --- Stage 3: Execute --- */

    alu inst_alu(
        .alu_input1(alu_input1_exe),
        .alu_input2(alu_input2_exe),
        .sa(sa_exe),
        .alu_op(alu_op_exe),
        .exc_type_in(exc_type_exe),

        .alu_result(alu_result),
        .exc_type_out(exc_type_out)
    );

    /* ex/mem register */

    reg_ex_mem inst_reg_ex_mem(
        .clk(clk),
        .rst(rst),
        .stall_C(stall_C),
        .flush_C(flush_C),
        .alu_result_in(alu_result),
        .reg2_data_in(reg2_data_exe),
        .ext_imm_in(ext_imm_exe),
        .dst_reg_in(dst_reg_exe),
        .re_addr_in(re_addr_exe),
        .pc_in(pc_exe),
        
        .mem_read_in(mem_read_exe),
        .mem_write_in(mem_write_exe),
        .cp0_write_in(cp0_write_exe),
        .reg_write_in(reg_write_exe),
        .reg_src_in(reg_src_exe),
        .exc_type_in(exc_type_exe),
        .bubble_in(bubble_exe),

        .alu_result_out(alu_result_mem),
        .reg2_data_out(reg2_data_mem),
        .ext_imm_out(ext_imm_mem),
        .dst_reg_out(dst_reg_mem),
        .re_addr_out(re_addr_mem),
        .pc_out(pc_mem),

        .mem_read_out(mem_read_mem),
        .mem_write_out(mem_write_mem),
        .cp0_write_out(cp0_write_mem),
        .reg_write_out(reg_write_mem),
        .reg_src_out(reg_src_mem),
        .exc_type_out(exc_type_mem),
        .bubble_out(bubble_mem)
    );



    /* --- Stage 4: Memory Access --- */

    data_memory inst_data_memory(
        .clk(clk),
        .mem_write(datamem_w),
        .mem_addr(alu_result_mem[11:2]),
        .write_mem_data(reg2_data_mem),

        .read_mem_data(read_datamem)
    );

    io_memory inst_io_memory(
        .clk(clk),
        .rst(rst),

        .display_C(display_C),
        .led_C(led_C),
        .switch_in(switch_in),
        .button_in(button_in),

        .mem_write(iomem_w),
        .mem_addr(alu_result_mem[11:2]),
        .write_mem_data(reg2_data_mem),

        .read_mem_data(read_iomem)
    );

    /* mem/wb register */

    reg_mem_wb inst_reg_mem_wb(
        .clk(clk),
        .rst(rst),
        .read_mem_data_in(read_mem_data),
        .alu_result_in(alu_result_mem),
        .ext_imm_in(ext_imm_mem),
        .dst_reg_in(dst_reg_mem),
        .re_addr_in(re_addr_mem),

        .cp0_write_in(cp0_write_mem),
        .reg_write_in(reg_write_mem),
        .reg_src_in(reg_src_mem),

        .read_mem_data_out(read_mem_data_wb),
        .alu_result_out(alu_result_wb),
        .ext_imm_out(ext_imm_wb),
        .dst_reg_out(dst_reg_wb),
        .re_addr_out(re_addr_wb),

        .cp0_write_out(cp0_write_wb),
        .reg_write_out(reg_write_wb),
        .reg_src_out(reg_src_wb)
    );



    /* --- Stage 5: Write Back --- */

    reg_src_mux inst_reg_src_mux(
        .reg_src(reg_src_wb),
        .alu_result(alu_result_wb),
        .read_mem_data(read_mem_data_wb),
        .extend_imm(ext_imm_wb),
        .re_addr(re_addr_wb),

        .mux_out(reg_src_mux_out)
    );

endmodule
