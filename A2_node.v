module A2_node #(
    parameter A_B_W = 32;
)(
    input rst,
    input clk,
    input[A_B_W-1:0] i1,
    input[A_B_W-1:0] i2,
    output reg[A_B_W-1:0] o,
);

initial begin
    o<=0;
end

always@(posedge clk) begin
    if(rst) begin
        o <= 0;
    end else begin
        o <= i1+i2;
    end
end

endmodule;
