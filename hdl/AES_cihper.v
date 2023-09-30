module AES_cihper(CLK,ld,Rst_n,Done,KEY,TextIn,TextOut);

input CLK,ld,Rst_n;
input [127:0] TextIn,KEY;
output reg[127:0]TextOut;
output reg Done;


//////////////////////////////////////////////////////////
//local   wire
//
reg [3:0]cnt=4'b0;
reg GO;
reg [127:0]KEYr,TextInr;
reg ldr;
reg [7:0]a0[3:0];						//array
reg [7:0]a1[3:0];
reg [7:0]a2[3:0];
reg [7:0]a3[3:0];

wire [7:0]a0_sb[3:0];						//array
wire [7:0]a1_sb[3:0];
wire [7:0]a2_sb[3:0];
wire [7:0]a3_sb[3:0];

wire [7:0]a0_sr[3:0];						//array
wire [7:0]a1_sr[3:0];
wire [7:0]a2_sr[3:0];
wire [7:0]a3_sr[3:0];

wire [7:0]a0_mc[3:0];						//array
wire [7:0]a1_mc[3:0];
wire [7:0]a2_mc[3:0];
wire [7:0]a3_mc[3:0];

wire [7:0]a0_next[3:0];						//array
wire [7:0]a1_next[3:0];
wire [7:0]a2_next[3:0];
wire [7:0]a3_next[3:0];

wire [31:0]Wk0,Wk1,Wk2,Wk3;

///////////////////////////////////////
//
//				cnt
always@(posedge CLK)
begin
if(~Rst_n)
	cnt<=4'h0;
else if(ld)
	cnt<=4'hb;
else if(GO) 
	cnt<=cnt-4'h1;
end

always@(posedge CLK)
begin
	if(~Rst_n)
		GO<=1'b0;
	else if(ld)
		GO<=1'b1;
	else if(cnt==4'h1)
		GO<=1'b0;
end

//assign Done=Rst_n&(~GO);
always@(posedge CLK)Done= #1 !(|cnt[3:1]) & cnt[0] & !ld;
always@(posedge CLK)	ldr<=#1 ld;											//
always@(posedge CLK)	if(ld) 	KEYr<= #1 KEY;
always@(posedge CLK)	if(ld)	TextInr<= #1 TextIn;
//////////////////////////////////////////////////////////////////
//
//						begin &  AddFirstRoundKey
always@(posedge CLK)
begin
a0[0]<=#1 ldr? 	TextInr[127:120]^Wk0[31:24]:a0_next[0];
a1[0]<=#1 ldr? 	TextInr[119:112]^Wk0[23:16]:a1_next[0];
a2[0]<=#1 ldr? 	TextInr[111:104]^Wk0[15:08]:a2_next[0];
a3[0]<=#1 ldr? 	TextInr[103:096]^Wk0[07:00]:a3_next[0];

a0[1]<=#1 ldr? 	TextInr[095:088]^Wk1[31:24]:a0_next[1];
a1[1]<=#1 ldr? 	TextInr[087:080]^Wk1[23:16]:a1_next[1];
a2[1]<=#1 ldr? 	TextInr[079:072]^Wk1[15:08]:a2_next[1];
a3[1]<=#1 ldr? 	TextInr[071:064]^Wk1[07:00]:a3_next[1];

a0[2]<=#1 ldr? 	TextInr[063:056]^Wk2[31:24]:a0_next[2];
a1[2]<=#1 ldr? 	TextInr[055:048]^Wk2[23:16]:a1_next[2];
a2[2]<=#1 ldr? 	TextInr[047:040]^Wk2[15:08]:a2_next[2];
a3[2]<=#1 ldr? 	TextInr[039:032]^Wk2[07:00]:a3_next[2];

a0[3]<=#1 ldr? 	TextInr[031:024]^Wk3[31:24]:a0_next[3];
a1[3]<=#1 ldr?  TextInr[023:016]^Wk3[23:16]:a1_next[3];
a2[3]<=#1 ldr? 	TextInr[015:008]^Wk3[15:08]:a2_next[3];
a3[3]<=#1 ldr? 	TextInr[007:000]^Wk3[07:00]:a3_next[3];

end
////////////////////////////////////////////////////////
// 						 module aes_sbox(a,d);
//   						subByte
aes_sbox    s00(.a(a0[0]),.d(a0_sb[0]));
aes_sbox    s01(.a(a0[1]),.d(a0_sb[1]));
aes_sbox    s02(.a(a0[2]),.d(a0_sb[2]));
aes_sbox    s03(.a(a0[3]),.d(a0_sb[3]));

aes_sbox    s10(.a(a1[0]),.d(a1_sb[0]));
aes_sbox    s11(.a(a1[1]),.d(a1_sb[1]));
aes_sbox    s12(.a(a1[2]),.d(a1_sb[2]));
aes_sbox    s13(.a(a1[3]),.d(a1_sb[3]));

aes_sbox    s20(.a(a2[0]),.d(a2_sb[0]));
aes_sbox    s21(.a(a2[1]),.d(a2_sb[1]));
aes_sbox    s22(.a(a2[2]),.d(a2_sb[2]));
aes_sbox    s23(.a(a2[3]),.d(a2_sb[3]));

aes_sbox    s30(.a(a3[0]),.d(a3_sb[0]));
aes_sbox    s31(.a(a3[1]),.d(a3_sb[1]));
aes_sbox    s32(.a(a3[2]),.d(a3_sb[2]));
aes_sbox    s33(.a(a3[3]),.d(a3_sb[3]));

//////////////////////////////////////////////////////////
//
//							shiftrow
assign {a0_sr[0],a0_sr[1],a0_sr[2],a0_sr[3]}={a0_sb[0],a0_sb[1],a0_sb[2],a0_sb[3]};
assign {a1_sr[0],a1_sr[1],a1_sr[2],a1_sr[3]}={a1_sb[1],a1_sb[2],a1_sb[3],a1_sb[0]};
assign {a2_sr[0],a2_sr[1],a2_sr[2],a2_sr[3]}={a2_sb[2],a2_sb[3],a2_sb[0],a2_sb[1]};
assign {a3_sr[0],a3_sr[1],a3_sr[2],a3_sr[3]}={a3_sb[3],a3_sb[0],a3_sb[1],a3_sb[2]};
/////////////////////////////////////////////////////
//
//							mixcloumns

function [7:0] xtime;
input [7:0]b;
xtime=(b[6:0]<<1)^({8{b[7]}}&8'h1b);
endfunction

assign 	a0_mc[0]=xtime(a0_sr[0])^xtime(a1_sr[0])^a1_sr[0]^a2_sr[0]^a3_sr[0];
assign 	a1_mc[0]=a0_sr[0]^xtime(a1_sr[0])^xtime(a2_sr[0])^a2_sr[0]^a3_sr[0];
assign 	a2_mc[0]=a0_sr[0]^a1_sr[0]^xtime(a2_sr[0])^xtime(a3_sr[0])^a3_sr[0];
assign  a3_mc[0]=xtime(a0_sr[0])^a0_sr[0]^a1_sr[0]^a2_sr[0]^xtime(a3_sr[0]);

assign 	a0_mc[1]=xtime(a0_sr[1])^xtime(a1_sr[1])^a1_sr[1]^a2_sr[1]^a3_sr[1];
assign 	a1_mc[1]=a0_sr[1]^xtime(a1_sr[1])^xtime(a2_sr[1])^a2_sr[1]^a3_sr[1];
assign 	a2_mc[1]=a0_sr[1]^a1_sr[1]^xtime(a2_sr[1])^xtime(a3_sr[1])^a3_sr[1];
assign  a3_mc[1]=xtime(a0_sr[1])^a0_sr[1]^a1_sr[1]^a2_sr[1]^xtime(a3_sr[1]);

assign 	a0_mc[2]=xtime(a0_sr[2])^xtime(a1_sr[2])^a1_sr[2]^a2_sr[2]^a3_sr[2];
assign 	a1_mc[2]=a0_sr[2]^xtime(a1_sr[2])^xtime(a2_sr[2])^a2_sr[2]^a3_sr[2];
assign 	a2_mc[2]=a0_sr[2]^a1_sr[2]^xtime(a2_sr[2])^xtime(a3_sr[2])^a3_sr[2];
assign  a3_mc[2]=xtime(a0_sr[2])^a0_sr[2]^a1_sr[2]^a2_sr[2]^xtime(a3_sr[2]);

assign 	a0_mc[3]=xtime(a0_sr[3])^xtime(a1_sr[3])^a1_sr[3]^a2_sr[3]^a3_sr[3];
assign 	a1_mc[3]=a0_sr[3]^xtime(a1_sr[3])^xtime(a2_sr[3])^a2_sr[3]^a3_sr[3];
assign 	a2_mc[3]=a0_sr[3]^a1_sr[3]^xtime(a2_sr[3])^xtime(a3_sr[3])^a3_sr[3];
assign  a3_mc[3]=xtime(a0_sr[3])^a0_sr[3]^a1_sr[3]^a2_sr[3]^xtime(a3_sr[3]);

////////////////////////////////////////////////////////////////////
//
//								AddRoundKey

assign a0_next[0]=a0_mc[0]^Wk0[31:24];
assign a1_next[0]=a1_mc[0]^Wk0[23:16];
assign a2_next[0]=a2_mc[0]^Wk0[15:08];
assign a3_next[0]=a3_mc[0]^Wk0[07:00];

assign a0_next[1]=a0_mc[1]^Wk1[31:24];
assign a1_next[1]=a1_mc[1]^Wk1[23:16];
assign a2_next[1]=a2_mc[1]^Wk1[15:08];
assign a3_next[1]=a3_mc[1]^Wk1[07:00];

assign a0_next[2]=a0_mc[2]^Wk2[31:24];
assign a1_next[2]=a1_mc[2]^Wk2[23:16];
assign a2_next[2]=a2_mc[2]^Wk2[15:08];
assign a3_next[2]=a3_mc[2]^Wk2[07:00];

assign a0_next[3]=a0_mc[3]^Wk3[31:24];
assign a1_next[3]=a1_mc[3]^Wk3[23:16];
assign a2_next[3]=a2_mc[3]^Wk3[15:08];
assign a3_next[3]=a3_mc[3]^Wk3[07:00];

///////////////////////////////////////////////////////////////////
//
//							keyexpand
aes_keyexpand128 key(.CLK(CLK),.ld(ld),.KEY(KEY),.Wk0(Wk0),.Wk1(Wk1),.Wk2(Wk2),.Wk3(Wk3));
////////////////////////////////////////////////////////////////
//
//							TextOut

always@(posedge CLK)
begin
TextOut<=#1 {		a0_sr[0]^Wk0[31:24],a1_sr[0]^Wk0[23:16],a2_sr[0]^Wk0[15:08],a3_sr[0]^Wk0[07:00],
					a0_sr[1]^Wk1[31:24],a1_sr[1]^Wk1[23:16],a2_sr[1]^Wk1[15:08],a3_sr[1]^Wk1[07:00],
					a0_sr[2]^Wk2[31:24],a1_sr[2]^Wk2[23:16],a2_sr[2]^Wk2[15:08],a3_sr[2]^Wk2[07:00],
					a0_sr[3]^Wk3[31:24],a1_sr[3]^Wk3[23:16],a2_sr[3]^Wk3[15:08],a3_sr[3]^Wk3[07:00]


};

end

/*
assign  TextOut={	a0_sr[0]^Wk0[31:24],a1_sr[0]^Wk0[23:16],a2_sr[0]^Wk0[15:08],a3_sr[0]^Wk0[07:00],
					a0_sr[1]^Wk1[31:24],a1_sr[1]^Wk1[23:16],a2_sr[1]^Wk1[15:08],a3_sr[1]^Wk1[07:00],
					a0_sr[1]^Wk2[31:24],a1_sr[1]^Wk2[23:16],a2_sr[1]^Wk2[15:08],a3_sr[1]^Wk2[07:00],
					a0_sr[1]^Wk3[31:24],a1_sr[1]^Wk3[23:16],a2_sr[1]^Wk3[15:08],a3_sr[1]^Wk3[07:00]
};
*/
endmodule
