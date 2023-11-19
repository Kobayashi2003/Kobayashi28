`timescale 1ns / 1ps

module ALUControl(
    input [1:0] ALUOp, // come from Control
    input [5:0] funct, // come from instruction [5:0]
    output reg [3:0] ALUControl // send to ALU
    );

    always @(*) begin
        case (ALUOp)
            2'b00: begin // lw
                ALUControl <= 4'b0010;
            end
            2'b01: begin // sw
                ALUControl <= 4'b0010;
            end
            2'b10: begin // R-type
                case (funct)
                    6'b100000: begin // add
                        ALUControl <= 4'b0010;
                    end
                    6'b100010: begin // sub
                        ALUControl <= 4'b0110;
                    end
                    6'b100100: begin // and
                        ALUControl <= 4'b0000;
                    end
                    6'b100101: begin // or
                        ALUControl <= 4'b0001;
                    end
                    6'b101010: begin // slt
                        ALUControl <= 4'b0111;
                    end
                    default: begin
                        ALUControl <= 4'b0010;
                    end
                endcase
            end
            default: begin
                ALUControl <= 4'b0010;
            end
        endcase
    end 
endmodule
