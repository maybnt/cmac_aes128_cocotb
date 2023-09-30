module aes_keyexpand128(CLK,ld,KEY,Wk0,Wk1,Wk2,Wk3);
//aes_keyexpand128 key(.CLK(CLK),.ld(ld),.KEY(KEYr),.Wk0(Wk0),.Wk1(Wk1),.Wk2(Wk2),.Wk3(Wk3));
input CLK,ld;
input [127:0]KEY;
output [31:0]Wk0,Wk1,Wk2,Wk3;

////////////////////////////////////////////////////////////////
//
//		reg
reg[31:0]Wk0r,Wk1r,Wk2r,Wk3r;
reg [3:0]cnt;
wire [31:0]Wk0_next,Wk1_next,Wk2_next,Wk3_next;
wire [31:0]Wk3_sb;

always@(posedge CLK)  
begin
Wk0r<=#1 ld? KEY[127:096] :Wk0_next;
Wk1r<=#1 ld? KEY[095:064] :Wk1_next;
Wk2r<=#1 ld? KEY[063:032] :Wk2_next;
Wk3r<=#1 ld? KEY[031:000] :Wk3_next;
end
/////////////////////////////////////////////////////
//
//						RotByte & SubByte
aes_sbox    s0(.a(Wk3r[23:16]),.d(Wk3_sb[31:24]));
aes_sbox    s1(.a(Wk3r[15:08]),.d(Wk3_sb[23:16]));
aes_sbox    s2(.a(Wk3r[07:00]),.d(Wk3_sb[15:08]));
aes_sbox    s3(.a(Wk3r[31:24]),.d(Wk3_sb[07:00]));

/////////////////////////////////////////////////////////
//
//							rcon

always@(posedge CLK)
begin
if(ld)
cnt<=4'h0;
else if(cnt==4'h9)
cnt<=cnt;
else
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
assign Wk0_next=Wk3_sb^Wk0r^rcon(cnt);
assign Wk1_next=Wk3_sb^Wk0r^rcon(cnt)^Wk1r;
assign Wk2_next=Wk3_sb^Wk0r^rcon(cnt)^Wk1r^Wk2r;
assign Wk3_next=Wk3_sb^Wk0r^rcon(cnt)^Wk1r^Wk2r^Wk3r;
//////////////////////////////////////////////////////
//
//		output   Wk0,Wk1,Wk2,Wk3
assign Wk0=Wk0r;assign Wk1=Wk1r;assign Wk2=Wk2r;assign Wk3=Wk3r;

endmodule
