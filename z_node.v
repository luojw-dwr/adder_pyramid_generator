module z_node #(
    parameter A_B_W = 32;
)(
    input rst,
    input clk,
    input[A_B_W-1:0] i,
    output reg[A_B_W-1:0] o
)

initial begin
    o<=0;
end

always@(posedge clk) begin
    if(rst) begin
        o <= 0;
    end else begin
        o <= i;
    end
end

endmodule;
