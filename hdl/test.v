//`include "timescale.v"

module test;

//**********************************
//
//				reg
reg		clk;
reg  	rst_n;
reg 	Last_Block;
reg 	ld_Block,ld_Key;
reg		[7:0]Last_Block_Len;
reg		[127:0]TextIn;

//**********************************
//
//				wire

wire Done;
wire TextOut;

//**********************************
//
//				simulate
initial 
begin
clk<=0;
rst_n<=0;
ld_Block<=0;
ld_Key<=0;
Last_Block<=0;
Last_Block_Len<=0;
TextIn=128'h0;
//RESET
repeat(4) @(posedge clk);
rst_n<=1;
repeat(2) @(posedge clk);
// load key
ld_Key<=1;
 @(posedge clk);
ld_Key<=0;
 @(negedge Done);
 //******************************************
 //
 // 					Test
 
 //test1
  #500;
 ld_Block<=1;
Last_Block<=1;
TextIn=128'h6bc1bee22e409f96e93d7e117393172a;
Last_Block_Len<=0;
@(posedge clk);
#1;
 ld_Block<=0;
Last_Block<=0;
TextIn=128'h0;
Last_Block_Len<=0;
@(negedge Done);

//test2
 #500;
 ld_Block<=1;
Last_Block<=1;
TextIn=128'h6bc1bee22e409f96e93d7e117393172a;
Last_Block_Len<=128;
@(posedge clk);
#1;
 ld_Block<=0;
Last_Block<=0;
TextIn=128'h0;
Last_Block_Len<=0;
@(negedge Done);

//test3
//block1
#500;
 ld_Block<=1;
Last_Block<=0;
TextIn=128'h6bc1bee22e409f96e93d7e117393172a;
Last_Block_Len<=128;
@(posedge clk);
#1;
 ld_Block<=0;
Last_Block<=0;
TextIn=128'h0;
Last_Block_Len<=0;
@(negedge Done);
//block2
#500;
 ld_Block<=1;
Last_Block<=0;
TextIn=128'hae2d8a571e03ac9c9eb76fac45af8e51;
Last_Block_Len<=128;
@(posedge clk);
#1;
 ld_Block<=0;
Last_Block<=0;
TextIn=128'h0;
Last_Block_Len<=0;
@(negedge Done);
//block3
#500;
 ld_Block<=1;
Last_Block<=1;
TextIn=128'h30c81c46a35ce411e5fbc1191a0a52ef;
Last_Block_Len<=64;
@(posedge clk);
#1;
 ld_Block<=0;
Last_Block<=0;
TextIn=128'h0;
Last_Block_Len<=0;
@(negedge Done);


end
//clock
always #5 clk<=~clk;

CMAC_Top  CMAC(
						.CLK(clk),
						.ld_Key(ld_Key),
						.ld_Block(ld_Block),
						.Rst_n(rst_n),
						.Done(Done),
						.Last_Block(Last_Block),
						.KEY(128'h2b7e151628aed2a6abf7158809cf4f3c),
						.TextIn(TextIn),
						.TextOut(TextOut),
						.Last_Block_Len(Last_Block_Len)

);

CMAC_Top_v2  CMAC_v2(
						.CLK(clk),
						.cm_ld_Key(ld_Key),
						.cm_ld_Block(ld_Block),
						.Rst_n(rst_n),
						.Done(),
						.cm_Last_Block(Last_Block),
						.cm_KEY(128'h2b7e151628aed2a6abf7158809cf4f3c),
						.cm_TextIn(TextIn),
						.TextOut(),
						.cm_Last_Block_Len(Last_Block_Len)

);
endmodule


