`timescale 1ns / 1ps
`include "instruction_head.v"

module Top_CPU(
    input wire                          clk,
    input wire                          rst,     // reset signal

    output wire                         halt,    // halt signal
    output wire                         syscall, // syscall signal
    output wire [`SYS_OP_LENGTH - 1:0]  sys_op,  // syscall operation

    input wire [31:0]                   sys_inf_in,  // system input interface
    output wire [31:0]                  sys_inf_out, // system output interface

    // debug information
    output wire [7:0]                   debug_reg_single,
    output wire [5:0]                   debug_opcode,
    output wire [5:0]                   debug_func,
    output wire [7:0]                   debug_dm_single,
    output wire [9:0]                   debug_pc,
    output wire [7:0]                   debug_alu
    );


    // Instruction fetch moudle i/o
    wire [31:0]                         pc;
    wire [31:0]                         npc;
    wire [31:0]                         instruction;

    // Decode instruction type and function
    wire [5:0]                          opcode;
    wire [5:0]                          func;

    // Decode registers
    wire [4:0]                          rs;
    wire [4:0]                          rt;
    wire [4:0]                          rd;

    // Decode 16 bit and 26 bit immediates
    wire [15:0]                         imm16;
    wire [25:0]                         imm26;

    // Assign decoded instruction to variables
    assign opcode =                     instruction[31:26];
    assign func   =                     instruction[5:0];
    assign rs     =                     instruction[25:21];
    assign rt     =                     instruction[20:16];
    assign rd     =                     instruction[15:11];
    assign imm16  =                     instruction[15:0];
    assign imm26  =                     instruction[25:0];

    // MUX
    wire [4:0]                          reg_dst_out;
    wire [31:0]                         reg_src_out;
    wire [31:0]                         alu_src_out1;
    wire [31:0]                         alu_src_out2;

    // Data memory
    wire [31:0]                         read_mem_data;

    // Extend module
    wire [31:0]                         ext_out;

    // Register file
    wire [31:0]                         reg1_data;
    wire [31:0]                         reg2_data;

    // ALU
    wire [31:0]                         alu_result;

    // Control signals

    wire [`ALU_CTRL_LENGTH - 1:0]       alu_ctrl;
    wire reg_dst;
    wire reg_write;
    wire alu_src1;
    wire alu_src2;
    wire mem_write;
    wire [`REG_SRC_LENGTH - 1:0]        reg_src;
    wire [`EXT_OP_LENGTH - 1:0]         ext_op;
    wire [`NPC_OP_LENGTH - 1:0]         npc_op;
    wire zero;

    assign debug_opcode   = opcode;
    assign debug_func     = func;
    assign debug_dm_single = read_mem_data[7:0];
    assign debug_pc        = pc[9:0];
    assign debug_alu       = alu_result[7:0];

    // Instruction fetch module: PC, NPC, instruction
    ProgramCounter INST_PC(
        .clk(clk),
        .rst(rst),
        .npc(npc),
        .pc(pc));

    new_ProgramCounter INST_NPC(
        .npc_op(npc_op),
        .pc(pc),
        .imm16(imm16),
        .imm26(imm26),
        .npc(npc));


    // // simulate instruction memory
    // InstructionMemory INST_INSTR_MEM(
    //     .pc_addr(pc),
    //     .instruction(instruction));


    // IP catalog instruction memory
    instruction_mem INST_INSTR_MEM(
        .a(pc[11:2]),
        .spo(instruction));


    // Module: Control Unit
    Control INST_CU(
        .syscall(syscall),
        .sys_op(sys_op),
        .opcode(opcode),
        .func(func),
        .zero(zero),
        .alu_ctrl(alu_ctrl),
        .reg_write(reg_write),
        .reg_dst(reg_dst),
        .alu_src1(alu_src1),
        .alu_src2(alu_src2),
        .mem_write(mem_write),
        .reg_src(reg_src),  
        .ext_op(ext_op),
        .npc_op(npc_op),
        .halt(halt));


    // // Module: Data Memory
    // DataMemory INST_DATA_MEM(
    //     .clk(clk),
    //     .mem_write(mem_write),
    //     .mem_addr(alu_result),
    //     .write_mem_data(reg2_data),
    //     .read_mem_data(read_mem_data));

    // IP catalog data memory
    data_mem INST_DATA_MEM(
        .clk(clk),
        .a(alu_result[11:2]),
        .d(reg2_data),
        .we(mem_write),
        .spo(read_mem_data));


    // Module: Multiplexers
    mux_reg_dst INST_MUX_REG_DST(
        .syscall(syscall),
        .sys_op(sys_op),

        .reg_dst(reg_dst),
        .mux_in_0(rt),
        .mux_in_1(rd),
        .mux_out(reg_dst_out));

    mux_reg_src INST_MUX_REG_SRC(
        .syscall(syscall),
        .sys_op(sys_op),
        .sys_in(sys_inf_in),

        .reg_src(reg_src),
        .mux_in_0(alu_result),
        .mux_in_1(read_mem_data),
        .mux_in_2(ext_out),
        .mux_out(reg_src_out));

   mux_alu_src1 INST_MUX_ALU_SRC1(
        .alu_src1(alu_src1),
        .mux_in_0(reg1_data),
        .mux_in_1(reg2_data),
        .mux_out(alu_src_out1)); 

    mux_alu_src2 INST_MUX_ALU_SRC2(
        .alu_src2(alu_src2),
        .mux_in_0(reg2_data),
        .mux_in_1(ext_out),
        .mux_out(alu_src_out2));

    // Module: Register File
    RegisterFile INST_REG_FILE(
        .syscall(syscall),
        .sys_out(sys_inf_out),

        .clk(clk),
        .reg_write(reg_write),
        .read_reg1_addr(rs),
        .read_reg2_addr(rt),
        .write_reg_addr(reg_dst_out),
        .write_data(reg_src_out),
        .reg1_data(reg1_data),
        .reg2_data(reg2_data),
        .sys_op(sys_op),
        .debug_reg_single(debug_reg_single));

    // Module: ALU
    ALU INST_ALU(
        .alu_ctrl(alu_ctrl),
        .alu_input1(alu_src_out1),
        .alu_input2(alu_src_out2),
        .alu_result(alu_result),
        .zero(zero));
    
    // Module: Extend
    Extend INST_EXT(
        .ext_op(ext_op),
        .imm16(imm16),
        .ext_out(ext_out));
endmodule
