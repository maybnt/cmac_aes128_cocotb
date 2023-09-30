module AES_cihper_v2(CLK,ld,Rst_n,Done,KEY,TextIn,TextOut);

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
reg [7:0]a_box_mux[3:0];
wire [7:0]a_box_sb_mux[3:0];

reg [7:0]a0_sb[3:0];						//array
reg [7:0]a1_sb[3:0];
reg [7:0]a2_sb[3:0];
reg [7:0]a3_sb[3:0];

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
wire        aes_covt_valid;

reg [1:0]  a_mux = 0; 

///////////////////////////////////////
//
always@(posedge CLK) begin
    if(ldr || aes_covt_valid)
      a_mux <= 0;
    else if(GO)
	  a_mux <= a_mux + 1;
end

assign aes_covt_valid = &a_mux;

//				cnt
always@(posedge CLK)
begin
if(~Rst_n)
	cnt<=4'h0;
else if(ld)
	cnt<=4'ha;
else if(GO && aes_covt_valid) 
	cnt<=cnt-4'h1;
end

always@(posedge CLK)
begin
	if(~Rst_n)
		GO<=1'b0;
	else if(ld)
		GO<=1'b1;
	else if(cnt==4'h1 && aes_covt_valid)
		GO<=1'b0;
end

//assign Done=Rst_n&(~GO);
always@(posedge CLK)Done= !(|cnt[3:1]) && cnt[0] && !ld && aes_covt_valid;
always@(posedge CLK)	ldr<= ld;											//
always@(posedge CLK)	if(ld) 	KEYr<=  KEY;
always@(posedge CLK)	if(ld)	TextInr<=  TextIn;
//////////////////////////////////////////////////////////////////
//
//						begin &  AddFirstRoundKey
always@(posedge CLK)
begin
a0[0]<= ldr? TextInr[127:120]^Wk0[31:24]:aes_covt_valid? a0_next[0]:a0[0];
a1[0]<= ldr? TextInr[119:112]^Wk0[23:16]:aes_covt_valid? a1_next[0]:a1[0];
a2[0]<= ldr? TextInr[111:104]^Wk0[15:08]:aes_covt_valid? a2_next[0]:a2[0];
a3[0]<= ldr? TextInr[103:096]^Wk0[07:00]:aes_covt_valid? a3_next[0]:a3[0];

a0[1]<= ldr? TextInr[095:088]^Wk1[31:24]:aes_covt_valid? a0_next[1]:a0[1];
a1[1]<= ldr? TextInr[087:080]^Wk1[23:16]:aes_covt_valid? a1_next[1]:a1[1];
a2[1]<= ldr? TextInr[079:072]^Wk1[15:08]:aes_covt_valid? a2_next[1]:a2[1];
a3[1]<= ldr? TextInr[071:064]^Wk1[07:00]:aes_covt_valid? a3_next[1]:a3[1];

a0[2]<= ldr? TextInr[063:056]^Wk2[31:24]:aes_covt_valid? a0_next[2]:a0[2];
a1[2]<= ldr? TextInr[055:048]^Wk2[23:16]:aes_covt_valid? a1_next[2]:a1[2];
a2[2]<= ldr? TextInr[047:040]^Wk2[15:08]:aes_covt_valid? a2_next[2]:a2[2];
a3[2]<= ldr? TextInr[039:032]^Wk2[07:00]:aes_covt_valid? a3_next[2]:a3[2];

a0[3]<= ldr? TextInr[031:024]^Wk3[31:24]:aes_covt_valid? a0_next[3]:a0[3];
a1[3]<= ldr? TextInr[023:016]^Wk3[23:16]:aes_covt_valid? a1_next[3]:a1[3];
a2[3]<= ldr? TextInr[015:008]^Wk3[15:08]:aes_covt_valid? a2_next[3]:a2[3];
a3[3]<= ldr? TextInr[007:000]^Wk3[07:00]:aes_covt_valid? a3_next[3]:a3[3];

end

////////////////////////////////////////////////////////
// 						 module aes_sbox(a,d);
//   						subByte

genvar i;
generate 
	for(i=0;i<4;i=i+1) begin: abox_mux
always@(*) begin
	case(a_mux)
	0:begin
		a_box_mux[i] = a0[i];
		a0_sb[i] = a_box_sb_mux[i];
	end
	1:begin
		a_box_mux[i] = a1[i];
		a1_sb[i] = a_box_sb_mux[i];
	end
	2:begin
		a_box_mux[i] = a2[i];
		a2_sb[i] = a_box_sb_mux[i];
	end
	3:begin
		a_box_mux[i] = a3[i];
		a3_sb[i] = a_box_sb_mux[i];
	end
	default:begin
		a_box_mux[i] = a0[i];
		a0_sb[i] = a_box_sb_mux[i];
	end
	endcase
end
aes_sbox    s00(.a(a_box_mux[i]),.d(a_box_sb_mux[i]));
end
endgenerate
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
aes_keyexpand128_v2 key(.CLK(CLK),.ld(ld),.KEY(KEY),.Wk0(Wk0),.Wk1(Wk1),.Wk2(Wk2),.Wk3(Wk3));
////////////////////////////////////////////////////////////////
//
//							TextOut

always@(posedge CLK)
begin
TextOut<= {		a0_sr[0]^Wk0[31:24],a1_sr[0]^Wk0[23:16],a2_sr[0]^Wk0[15:08],a3_sr[0]^Wk0[07:00],
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
