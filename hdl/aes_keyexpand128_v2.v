module aes_keyexpand128_v2(
    input CLK,
    input ld,
    input [127:0]KEY,
    output [31:0]Wk0,
    output [31:0]Wk1,
    output [31:0]Wk2,
    output [31:0]Wk3
    );

////////////////////////////////////////////////////////////////
//
//		reg
reg[31:0]Wk0r,Wk1r,Wk2r,Wk3r;
reg [3:0]cnt;
reg [1:0] Wk3r_mux = 0;
wire [31:0]Wk0_next,Wk1_next,Wk2_next,Wk3_next;
reg [31:0]Wk3_sb = 0;
wire [7:0]Wk3_sb_aes;
wire [1:0] Wk3r_mux_aes;
wire aes_keycovt_valid;

always@(posedge CLK) begin
if(ld) begin
Wk0r<=KEY[127:096];
Wk1r<=KEY[095:064];
Wk2r<=KEY[063:032];
Wk3r<=KEY[031:000];
end
else if(&Wk3r_mux) begin
Wk0r<=Wk0_next;
Wk1r<=Wk1_next;
Wk2r<=Wk2_next;
Wk3r<=Wk3_next;    
end
end
/////////////////////////////////////////////////////
//

always@(posedge CLK) begin
    if(ld || aes_keycovt_valid)
      Wk3r_mux <= 0;
    else
      Wk3r_mux <= Wk3r_mux + 1;
end
assign aes_keycovt_valid = &Wk3r_mux;
assign Wk3r_mux_aes = Wk3r_mux + 1;
//						RotByte & SubByte
aes_sbox    s0(.a(Wk3r[8*Wk3r_mux+:8]),.d(Wk3_sb_aes));

always@(*) begin
    case(Wk3r_mux_aes)
    0: Wk3_sb[7:0] = Wk3_sb_aes;
    1: Wk3_sb[15:8] = Wk3_sb_aes;
    2: Wk3_sb[23:16] = Wk3_sb_aes;
    3: Wk3_sb[31:24] = Wk3_sb_aes;
    default:Wk3_sb[7:0] = Wk3_sb_aes;
    endcase
end

/////////////////////////////////////////////////////////
//
//							rcon

always@(posedge CLK)
begin
if(ld)
cnt<=4'h0;
else if(cnt==4'h9)
cnt<=cnt;
else if(aes_keycovt_valid)
cnt<=cnt+4'h1;
end

function [31:0]rcon;
input [3:0]b;
case(b)
4'h0:rcon=32'h01_00_00_00;
4'h1:rcon=32'h02_00_00_00;
4'h2:rcon=32'h04_00_00_00;
4'h3:rcon=32'h08_00_00_00;
4'h4:rcon=32'h10_00_00_00;
4'h5:rcon=32'h20_00_00_00;
4'h6:rcon=32'h40_00_00_00;
4'h7:rcon=32'h80_00_00_00;
4'h8:rcon=32'h1b_00_00_00;
4'h9:rcon=32'h36_00_00_00;
default:rcon=32'h00_00_00_00;
endcase
endfunction

//////////////////////////////////////////////////////
//
//		output   Wk0,Wk1,Wk2,Wk3_next
assign Wk0_next=(aes_keycovt_valid || ld)?Wk3_sb^Wk0r^rcon(cnt):Wk0_next;
assign Wk1_next=(aes_keycovt_valid || ld)?Wk3_sb^Wk0r^rcon(cnt)^Wk1r:Wk1_next;
assign Wk2_next=(aes_keycovt_valid || ld)?Wk3_sb^Wk0r^rcon(cnt)^Wk1r^Wk2r:Wk2_next;
assign Wk3_next=(aes_keycovt_valid || ld)?Wk3_sb^Wk0r^rcon(cnt)^Wk1r^Wk2r^Wk3r:Wk3_next;
//////////////////////////////////////////////////////
//
//		output   Wk0,Wk1,Wk2,Wk3
assign Wk0=Wk0r;assign Wk1=Wk1r;assign Wk2=Wk2r;assign Wk3=Wk3r;

endmodule
