`timescale 1ns / 1ps


// Instruction Memory Length
`define IM_LENGTH 1023
`define DM_LENGTH 1023

`define REG_0_ADDR    5'b00000
`define REG_31_ADDR   5'b11111

// Init reg/wire with zeros
`define INIT_32 32'h00000000
`define INIT_16 16'h0000
`define INIT_6  6'b000000
`define INIT_5  5'b00000

/* --- Instruction Decode --- */

// R-Type instructions
`define SPECIAL 6'b000000 // R-Type opcode

// func code
`define FUNC_ADD        6'b100000  // ADD
`define FUNC_ADDU       6'b100001  // ADDU
`define FUNC_SUB        6'b100010  // SUB
`define FUNC_SUBU       6'b100011  // SUBU
`define FUNC_SLT        6'b101010  // SLT
`define FUNC_SLTU       6'b101011  // SLTU
`define FUNC_AND        6'b100100  // AND
`define FUNC_OR         6'b100101  // OR
`define FUNC_NOR        6'b100111  // NOR
`define FUNC_XOR        6'b100110  // XOR
`define FUNC_SLL        6'b000000  // SLL
`define FUNC_SRL        6'b000010  // SRL
`define FUNC_SRA        6'b000011  // SRA
`define FUNC_SLLV       6'b000100  // SLLV
`define FUNC_SRLV       6'b000110  // SRLV
`define FUNC_SRAV       6'b000111  // SRAV

`define FUNC_JR         6'b001000  // JR
`define FUNC_JALR       6'b001001  // JALR

`define FUNC_SYSCALL    6'b001100  // SYSCALL
`define FUNC_TEQ        6'b110100  // TEQ
`define FUNC_TNE        6'b110110  // TNE
`define FUNC_TGE        6'b110000  // TGE
`define FUNC_TGEU       6'b110001  // TGEU
`define FUNC_TLT        6'b110010  // TLT
`define FUNC_TLTU       6'b110011  // TLTU

// I-Type instructions
`define INST_ADDI       6'b001000  // ADDI
`define INST_ADDIU      6'b001001  // ADDIU
`define INST_SLTIU      6'b001011  // SLTIU
`define INST_ANDI       6'b001100  // ANDI
`define INST_ORI        6'b001101  // ORI
`define INST_XORI       6'b001110  // XORI
`define INST_LUI        6'b001111  // LUI
`define INST_LW         6'b100011  // LW
`define INST_SW         6'b101011  // SW
`define INST_BEQ        6'b000100  // BEQ
`define INST_BNE        6'b000101  // BNE

`define REGIMM          6'b000001
`define INST_TEQI       5'b01100   // TEQI
`define INST_TNEI       5'b01110   // TNEI
`define INST_TGEI       5'b01000   // TGEI
`define INST_TGEIU      5'b01001   // TGEIU
`define INST_TLTI       5'b01010   // TLTI
`define INST_TLTIU      5'b01011   // TLTIU


// J-Type instructions
`define INST_J          6'b000010  // J
`define INST_JAL        6'b000011  // JAL



/* --- Control Signals --- */

// ExtOp Control Signals
`define EXT_OP_LENGTH   2           // Bits of signal ExtOp
`define EXT_OP_DEFAULT  2'b00       // ExtOp default value
`define EXT_OP_SFT16    2'b01       // LUI: Shift Left 16
`define EXT_OP_SIGNED   2'b10       // `imm16` signed extended to 32 bit
`define EXT_OP_UNSIGNED 2'b11       // `imm16` unsigned extended to 32 bit

// ALUSrc Control Signals
`define ALU_SRC_LENGTH  2            // Bits of signal ALUSrc
`define ALU_SRC_DEFAULT 2'b00        // ALU source default value
`define ALU_SRC_REG     2'b00        // ALU source: register file
`define ALU_SRC_IMM     2'b01        // ALU Source: immediate
`define ALU_SRC_CP0     2'b10        // ALU Source: CP0

// ALU Control Signals 
`define ALU_OP_LENGTH  5            // Bits of signal ALUOp
`define ALU_OP_DEFAULT 5'b00000      // ALUOp default value     
`define ALU_OP_2ND     5'b00000      // ALUOp the second input
`define ALU_OP_ADD     5'b00001      // ALU add                 
`define ALU_OP_SUB     5'b00010      // ALU sub                 
`define ALU_OP_SLT     5'b00011      // ALU set less than       
`define ALU_OP_AND     5'b00100      // ALU and                 
`define ALU_OP_OR      5'b00101      // ALU or                  
`define ALU_OP_XOR     5'b00110      // ALU xor                 
`define ALU_OP_NOR     5'b00111      // ALU nor                 
    // respect to shamnt
`define ALU_OP_SLL     5'b01000      // ALU shift left logical  
`define ALU_OP_SRL     5'b01001      // ALU shift right logical 
`define ALU_OP_SRA     5'b01010      // ALU shift right arith   
    // respect to rs    
`define ALU_OP_SLLV    5'b01011      // ALU shift left logical  
`define ALU_OP_SRLV    5'b01100      // ALU shift right logical 
`define ALU_OP_SRAV    5'b01101      // ALU shift right arith   
`define ALU_OP_ADDU    5'b01110      // ALU add unsigned        
`define ALU_OP_SUBU    5'b01111      // ALU sub unsigned        
    // trap instructions
`define ALU_OP_TEQ     5'b11000      // ALU trap equal
`define ALU_OP_TNE     5'b11001      // ALU trap not equal
`define ALU_OP_TGE     5'b11010      // ALU trap greater equal
`define ALU_OP_TGEU    5'b11011      // ALU trap greater equal unsigned
`define ALU_OP_TLT     5'b11100      // ALU trap less than
`define ALU_OP_TLTU    5'b11101      // ALU trap less than unsigned

    // overflow detection
`define OVERFLOW_TRUE  1'b1
`define OVERFLOW_FALSE 1'b0
    // zero detection
`define ZERO_TRUE      1'b1
`define ZERO_FALSE     1'b0

// RegDst Control Signals
`define REG_DST_LENGTH  2          // Bits of signal RegDst
`define REG_DST_DEFAULT 2'b00      // Register default value                      0
`define REG_DST_RT      2'b01      // Register write destination: rt              1
`define REG_DST_RD      2'b10      // Register write destination: rd              2
`define REG_DST_REG_31  2'b11      // Register write destination: 31 bit gpr($ra) 3

// RegSrc Control Signals
`define REG_SRC_LENGTH  3          // Bits of signal RegSrc
`define REG_SRC_DEFAULT 3'b000     // Register default value                    0
`define REG_SRC_ALU     3'b001     // Register write source: ALU                1   
`define REG_SRC_MEM     3'b010     // Register write source: Data Memory        2
`define REG_SRC_IMM     3'b011     // Register write source: Extended immediate 3
`define REG_SRC_RETURN  3'b100     // Register write source: Jump destination   4
// `define REG_SRC_CP0     3'b101     // Register write source: CP0                5

// NPCOp Control Signals
`define NPC_OP_LENGTH   3          // Bits of signal NPCOp
`define NPC_OP_DEFAULT  3'b000     // NPCOp default value
`define NPC_OP_NEXT     3'b001     // NPCOp next instruction
`define NPC_OP_JUMP     3'b010     // NPCOp jump instruction
`define NPC_OP_OFFSET   3'b011     // NPCOp offset instruction
`define NPC_OP_RS       3'b100     // NPCOp rs instruction

    // Branching signals
`define BRANCH_TRUE     1'b1       // Branching signal: true
`define BRANCH_FALSE    1'b0       // Branching signal: false

// Memory Write EN
`define MEM_WRITE_EN    1'b1       // Enable memory write
`define MEM_WRITE_DIS   1'b0       // Disable memory write

// Memory Read EN
`define MEM_READ_EN     1'b1       // Enable memory read
`define MEM_READ_DIS    1'b0       // Disable memory read

// RegWrite
`define REG_WRITE_EN    1'b1       // Enable register write
`define REG_WRITE_DIS   1'b0       // Disable register write


/* --- Hazard Contorl --- */

// Forwarding Control Signals
`define FORWARD_ONE_CYCLE  2'b10
`define FORWARD_TWO_CYCLE  2'b01
`define FORWARD_ZERO_CYCLE 2'b00

// Stall Contorl Signals
`define EXE_STALL      4'b0111       // Stall signal: EXE
`define MEM_STALL      4'b1111       // Stall signal: MEM
`define NON_STALL      4'b0000       // Stall signal: NONE


/* --- coprocessor 0 --- */

// coprocessor 0 instruction
`define COP0             6'b010000
`define COP0_MFC0        5'b00000
`define COP0_MTC0        5'b00100
`define INST_ERET        32'h42000018

`define CP0_READ_DIS     1'b0
`define CP0_READ_EN      1'b1
`define CP0_WRITE_DIS    1'b0
`define CP0_WRITE_EN     1'b1

// coprocessor 0 register 
`define CP0_REG_COUNT    5'b01001
`define CP0_REG_COMPARE  5'b01011
`define CP0_REG_STATUS   5'b01100
`define CP0_REG_CAUSE    5'b01101
`define CP0_REG_EPC      5'b01110
`define CP0_REG_PRID     5'b01111
`define CP0_REG_CONFIG   5'b10000
    // default value
`define CP0_COMPARE_DEFAULT 32'h00001000
`define CP0_STATUS_DEFAULT  32'h1000fc11
    // interrupt enable
`define INTERRUPT_NOT_ASSERT 1'b0
`define INTERRUPT_ASSERT     1'b1

// Exception Code
`define EXC_TYPE_LENGTH  5
`define EXC_TYPE_DEFAULT 5'b00000
`define EXC_TYPE_INT     5'b00000
`define EXC_TYPE_SYS     5'b01000
`define EXC_TYPE_RI      5'b01010
`define EXC_TYPE_OV      5'b01100
`define EXC_TYPE_TR      5'b01101
`define EXC_TYPE_ERET    5'b01110

// new pc: interrupt operation
`define NPC_INT_OP_LENGTH  4
`define NPC_INI_OP_DEFAULT 4'b0000
`define NPC_OP_HARD0       4'b0001
`define NPC_OP_HARD1       4'b0010
`define NPC_OP_HARD2       4'b0011
`define NPC_OP_HARD3       4'b0100
`define NPC_OP_HARD4       4'b0101
`define NPC_OP_HARD5       4'b0110
`define NPC_OP_SOFT0       4'b0111
`define NPC_OP_SOFT1       4'b1000
`define NPC_OP_SYS         4'b1001
`define NPC_OP_ERET        4'b1010
`define NPC_OP_RI          4'b1011
`define NPC_OP_OV          4'b1100
`define NPC_OP_TR          4'b1101

// new pc: interrupt address
`define NPC_ADDR_HARD0       32'h00000300
`define NPC_ADDR_HARD1       32'h000001c0
`define NPC_ADDR_HARD2       32'h00000240
`define NPC_ADDR_HARD3       32'h00000100
`define NPC_ADDR_HARD4       32'h00000040
`define NPC_ADDR_HARD5       32'h00000280
`define NPC_ADDR_SOFT0       32'h00000000
`define NPC_ADDR_SOFT1       32'h00000000
`define NPC_ADDR_SYS         32'h00000000
`define NPC_ADDR_ERET        32'h00000000
`define NPC_ADDR_RI          32'h00000000
`define NPC_ADDR_OV          32'h00000000
`define NPC_ADDR_TR          32'h00000000


/* --- io memory --- */
`define IO_ADDR_DISPLAY     10'h000
`define IO_ADDR_LED         10'h001
`define IO_ADDR_SWITCH      10'h002
`define IO_ADDR_BUTTON      10'h003
`define IO_ADDR_BUF         10'h004
`define BUF_LENGTH          1023


/* --- exception --- */

// 7 segment display
`define VAL_0               7'b0000001
`define VAL_1               7'b1001111
`define VAL_2               7'b0010010
`define VAL_3               7'b0000110
`define VAL_4               7'b1001100
`define VAL_5               7'b0100100
`define VAL_6               7'b0100000
`define VAL_7               7'b0001111
`define VAL_8               7'b0000000
`define VAL_9               7'b0000100
`define VAL_A               7'b0001000
`define VAL_B               7'b1100000
`define VAL_C               7'b0110001
`define VAL_D               7'b1000010
`define VAL_E               7'b0110000
`define VAL_F               7'b0111000
`define VAL_DEF             7'b1111111

// io device 
`define DISPLAY_INIT     32'h00000000
`define LED_INIT         32'h00000001 