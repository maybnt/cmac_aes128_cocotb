module CMAC_Top(
						CLK,
						ld_Key,
						ld_Block,
						Rst_n,
						Done,
						Last_Block,
						KEY,
						TextIn,
						TextOut,
						Last_Block_Len

);
//*****************************************
//
//							input & output 
input CLK,ld_Key,ld_Block,Rst_n,Last_Block;
input [7:0]Last_Block_Len;
input [127:0] TextIn,KEY;
output [127:0]TextOut;
output  Done;
//*****************************************
//
//							parameter
parameter s0=2'b00;	//IDLE
parameter s1=2'b01;	//generate k1,k2
parameter s2=2'b10;	//caculate the front n block
parameter s3=2'b11;	//caculate the last block

//*****************************************
//
//							wire
wire  [127:0]TextIn_temp;
wire  [127:0]TextIn_CBC;
wire  [127:0]TextIn_Last;
wire  [127:0]TextIn_Filled;
wire  [127:0]k1_temp,k2_temp,k1_k2_reg_shift1,k1_temp_shift1;
wire 	[127:0]k1_k2_Select;//the result of caculate with the Key is K and content is all zero
wire ld_temp;
//*****************************************
//
//							reg
reg [127:0] k1_k2_reg,IV_reg;
reg [1:0]		state,state_next;
reg [127:0]		Set_1_Num,Clear_0_Num;
//*****************************************
//
//						assign 
assign ld_temp=ld_Key|ld_Block;
assign TextIn_CBC=IV_reg^TextIn;
assign k1_k2_Select=(Last_Block_Len[7])?k1_temp:k2_temp;
assign TextIn_Filled=(TextIn&Clear_0_Num)|Set_1_Num;
assign TextIn_Last=IV_reg^TextIn_Filled^k1_k2_Select;
assign TextIn_temp=(Last_Block==1'b1)?TextIn_Last:TextIn_CBC;
//*****************************************
//
//						Set_1_Num,Clear_0_Num
//閸氬孩婀℃担璺ㄦ暏鏉烆垯娆㈤悽鐔稿灇
always@(Last_Block or Last_Block_Len)
begin
if(Last_Block==1'b0)
	Set_1_Num<=128'd0;
else
	begin
	case(Last_Block_Len)
8'd64:Set_1_Num<=128'h00000000000000008000000000000000;

default:Set_1_Num<=128'h00000000000000000000000000000000;
	endcase
	end

end

always@(Last_Block or Last_Block_Len)
begin
if(Last_Block==1'b0)
	Clear_0_Num<=128'd0;
else
	begin
	case(Last_Block_Len)
8'd64:Clear_0_Num<=128'hffffffffffffffff8000000000000000;
default:Clear_0_Num<=128'hffffffffffffffffffffffffffffffff;
	endcase 
	end

end

//*****************************************
//
//							state transform
always@(posedge CLK or negedge Rst_n)
begin 
if(~Rst_n)
state<=s0;
else
state<=state_next;
end


always@(posedge CLK or negedge Rst_n)
begin 
if(~Rst_n)
	state_next<=s0;
else if((state==s0 |(state==s1 & Done ==1'b1)|state==s1&state_next==s2|state==s2 |(state_next==s0 & state==s3))& ld_Block==1'b1 & Last_Block ==1'b1)
	state_next<=s3;
else if((state==s0 |state==s2 & state_next==s2|(state_next==s0 & state==s3 ) ) &(ld_Block==1'b1 & Last_Block ==1'b0 )| state==s1 & Done==1'b1)
	state_next<=s2;
else if((state==s0& state_next==s0 |state==s3& state_next==s0) & ld_Key==1'b1)
	state_next<=s1;
else if(state==s3 & Done==1'b1)
	state_next<=s0;
else
	state_next<=state_next;
end
//*****************************************
//
//							k1_k2_reg generate

always@(posedge CLK or negedge Rst_n)
begin 
if(~Rst_n)
k1_k2_reg<=128'b0;
else if(state==s1 & Done==1'b1)
k1_k2_reg<=TextOut;
else
k1_k2_reg<=k1_k2_reg;
end
// k1_temp and k2_temp generate
assign k1_k2_reg_shift1={k1_k2_reg[126:0],1'b0};
assign k1_temp=(k1_k2_reg[127]==1'b1)? k1_k2_reg_shift1^128'h87:k1_k2_reg_shift1;
assign k1_temp_shift1={k1_temp[126:0],1'b0};
assign k2_temp=(k1_temp[127]==1'b1)? k1_temp_shift1^128'h87:k1_temp_shift1;
//*****************************************
//
//							IV_reg generate 
always@(posedge CLK or negedge Rst_n)
begin 
if(~Rst_n)
IV_reg<=128'b0;
else if(state==s2 & Done==1'b1)
IV_reg<=TextOut;
else
IV_reg<=IV_reg;
end

//*****************************************
//
//							AES module
AES_cihper u0(
					CLK,
					ld_temp,
					Rst_n,
					Done,
					KEY,
					TextIn_temp,
					TextOut);



endmodule