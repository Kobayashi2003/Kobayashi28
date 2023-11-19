`define CLK_MAIN_DELAY 16'hff
`define CLK_CPU_DELAY  16'hffff
`define BTN_EFCT_DELAY 32'd100_000
`define GO_BTN_DELAY   32'hffffff

`define ARRAY_SIZE 16
`define NUM_SIZE   16

// 7-segment display delay 
`define SEG_DELAY 16'hffff

// Segment Number
`define SEG_SIZE 4
`define SEG_1st  4'b0111
`define SEG_2nd  4'b1011
`define SEG_3rd  4'b1101
`define SEG_4th  4'b1110
`define SEG_DEF  4'b1111

// Segment Value
`define SEG_VAL_0    7'b0000001
`define SEG_VAL_1    7'b1001111
`define SEG_VAL_2    7'b0010010
`define SEG_VAL_3    7'b0000110
`define SEG_VAL_4    7'b1001100
`define SEG_VAL_5    7'b0100100
`define SEG_VAL_6    7'b0100000
`define SEG_VAL_7    7'b0001111
`define SEG_VAL_8    7'b0000000
`define SEG_VAL_9    7'b0000100
`define SEG_VAL_A    7'b0001000
`define SEG_VAL_B    7'b1100000
`define SEG_VAL_C    7'b0110001
`define SEG_VAL_D    7'b1000010
`define SEG_VAL_E    7'b0110000
`define SEG_VAL_F    7'b0111000
`define SEG_VAL_DEF  7'b1111111