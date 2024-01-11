
// Insturction Memory Capacity
`define IM_LENGTH           255
// Data Memory Capacity
`define DM_LENGTH           255 
// 32 digits of 0
`define INITIAL_VAL         32'h00000000

// R-Type instructions
`define INST_R_TYPE         6'b000000 // R-Type opcode, decode via function code
`define FUNC_ADD            6'b100000 // ADD func code 0/20H
`define FUNC_SUBU           6'b100011 // SUBU func code 0/23H
`define FUNC_AND            6'b100100 // AND func code 0/24H
`define FUNC_OR             6'b100101 // OR func code 0/25H
`define FUNC_NOR            6'b100111 // NOR func code 0/27H
`define FUNC_SLT            6'b101010 // SLT func code 0/2AH
`define FUNC_SLL            6'b000000 // SLL func code 0/00H

// I-Type instructions
`define INST_LUI            6'b001111 // LUI 0FH
`define INST_ADDIU          6'b001001 // ADDIU 9H
`define INST_LW             6'b100011 // LW 23H
`define INST_SW             6'b101011 // SW 2BH
`define INST_BEQ            6'b000100 // BEQ 4H

// J-Type instructions
`define INST_J              6'b000010 // J 2H

// Halt instruction
`define INST_HALT           6'b111111 // HALT 3FH

// System call
`define INST_SYSCALL        6'b001100 // SYSCALL 0CH
`define SYS_OP_LENGTH       2         // Bits of signal SysOp
`define SYSCALL_OUTPUT_INT  2'b01     // Print integer
`define SYSCALL_INPUT_INT   2'b10     // Input integer

// No operation
`define INST_NOP            6'b000000 // NOP 0H

// ALU Control Signals
`define ALU_CTRL_LENGTH     4 // Bits of signal ALUOp
`define ALU_CTRL_DEFAULT    4'b0010 // ALUOp default value
`define ALU_CTRL_AND        4'b0000 // ALUOp AND
`define ALU_CTRL_OR         4'b0001 // ALUOp OR
`define ALU_CTRL_ADD        4'b0010 // ALUOp ADD
`define ALU_CTRL_SUB        4'b0110 // ALUOp SUB
`define ALU_CTRL_SLT        4'b0111 // ALUOp SLT
`define ALU_CTRL_NOR        4'b1100 // ALUOp NOR
`define ALU_CTRL_SHIFT_L     4'b1000 // ALUOp Shift Left

// RegDst Control Signals
`define REG_DST_RT          1'b0 // Register write destination: rt
`define REG_DST_RD          1'b1 // Register write destination: rd

// ALUSrc Control Signals
`define ALU_SRC_REG         1'b0 // ALU source: register file
`define ALU_SRC_IMM         1'b1 // ALU Source: immediate
`define ALU_SRC_SHIFT       1'b1 // ALU Source: shift command
    
// RegSrc Control Signals
`define REG_SRC_LENGTH      2 // Bits of signal RegSrc
`define REG_SRC_DEFAULT     2'b00 // Register default value
`define REG_SRC_ALU         2'b01 // Register write source: ALU
`define REG_SRC_MEM         2'b10 // Register write source: Data Memory
`define REG_SRC_IMM         2'b11 // Register write source: Extended immediate

// ExtOp Control Signals
`define EXT_OP_LENGTH       2 // Bits of Signal ExtOp
`define EXT_OP_DEFAULT      2'b00 // ExtOp default value
`define EXT_OP_SFT16        2'b01 // LUI: Shift Left 16
`define EXT_OP_SIGNED       2'b10 // `imm16` signed extended to 32 bit
`define EXT_OP_UNSIGNED     2'b11 // `imm16` unsigned extended to 32 bit

// NPCOp Control Signals
`define NPC_OP_LENGTH       3 // Bits of NPCOp
`define NPC_OP_DEFAULT      3'b000 // NPCOp default value
`define NPC_OP_NEXT         3'b001 // Next instruction: normal
`define NPC_OP_JUMP         3'b010 // Next instruction: J
`define NPC_OP_OFFSET       3'b011 // Next instruction: BEQ
`define NPC_OP_HALT         3'b100 // Next instruction: HALT