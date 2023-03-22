----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 20.03.2023 10:49:18
-- Design Name: 
-- Module Name: cmdProc - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;
use work.common_pack.all; -- BDC_ARRAY-TYPE

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity cmdProc is
    port(
      clk:		    in std_logic;
      reset:		in std_logic;
      rxNow:		in std_logic;
      rxData:		in std_logic_vector (7 downto 0);
      txData:		out std_logic_vector (7 downto 0);
      rxDone:		out std_logic;
      ovErr:		in std_logic;
      framErr:	    in std_logic;
      txNow:		out std_logic;
      txDone:		in std_logic;
      start:        out std_logic;
      numWords_bcd: out BCD_ARRAY_TYPE(2 downto 0);
      dataReady:    in std_logic;
      byte:         in std_logic_vector(7 downto 0);
      maxIndex:     in BCD_ARRAY_TYPE(2 downto 0);
      dataResults:  in CHAR_ARRAY_TYPE(0 to RESULT_BYTE_NUM-1);
      seqDone:      in std_logic
      );
end cmdProc;

architecture Behavioral of cmdProc is
    -- SIGNAL DECLERATIONS
    TYPE state_type IS (S0, S1, S2, S3);
    signal curState, nextState: state_type;
    --
    signal dataReg: std_logic_vector (7 downto 0);
--    signal res_dataReg, en_dataReg: bit;
    signal comReg: std_logic_vector (23 downto 0);
    signal comReg_input: std_logic_vector (7 downto 0);
    signal res_comReg, en_comReg, comReg_valid: bit;
    signal comReg_count: integer;
    --
    signal test: std_logic_vector (3 downto 0);

begin

--State Logic
nextState_logic: process(curState)
BEGIN
    CASE curState IS
        WHEN S0 =>
            IF rxNow='1' AND ovErr='0' AND framErr='0' THEN
                dataReg <= rxData; -- Load in data. Comes in ASCII, we output in ASCII
                txData <= rxData; -- Prepare to output data
                rxDone <= '1'; -- Can start recieving next bit
                txNow <= '1'; -- Can transmit data
                nextState <= S1;
            ELSE
                nextState <= S0;
            END IF;
        
        WHEN S1 =>
            IF txDone='1' THEN
                nextState <= S2;
            ELSE
                nextState <= S1;
            END IF;
        
        WHEN S2 =>
            IF dataReg = x"41" OR dataReg = x"61" THEN
                res_comReg <= '1';
                comReg_valid <= '1';
                nextState <= S0;
            ELSIF dataReg >= x"30" AND dataReg <= x"39" and comReg_valid = '1' THEN
                comReg_input <= dataReg;
                en_comReg <= '1';
                IF comReg_count = 3 THEN
                    nextState <= S3;
                    res_comReg <= '1';
                    comReg_valid <= '0';
                ELSE
                    nextState <= S0;
                END IF;
            ELSE
                res_comReg <= '1';
                comReg_valid <= '0';
            END IF;
            
        WHEN S3 =>
--           std_logic_vector('0000');
           --numWords_bcd(1) <= '0000';
           --numWords_bcd(2) <= '0000';
           
--           TO_INTEGER(comReg(7 downto 0));
--           numWords_bcd(0) <= std_logic_vector(comReg(7 downto 0) - 16#30#);
--           numWords_bcd(1) <= comReg(15 downto 8);
--           numWords_bcd(2) <= comReg(23 downto 16);
            
    END CASE;
END PROCESS;

-- State Register
State_register: process (reset, clk)
BEGIN
    IF reset='0' THEN
      curState <= S0;
    ELSIF rising_edge(clk) THEN
      curState <= nextState;
    END IF;
END PROCESS;

-- Combinational Output Logic
combi_out: PROCESS(curState)
BEGIN
END PROCESS; -- combi_outputend Behavioral;

-- Need a RxReg 8 bits long for data recieved
--dataRegister: process(clk, res_dataReg, en_dataReg)
--BEGIN
--    IF res_dataReg = '1' THEN
--        dataReg <= "00000000";
--    ELSIF rising_edge(clk) THEN
--        IF en_dataReg = '1' THEN
--            dataRegister
        
        
--    END IF;
--END PROCESS;
comRegister: process(clk, res_comReg)
BEGIN
    IF res_comReg = '1' THEN
        comReg <= x"000";
        comReg_count <= 0;
    ELSIF rising_edge(clk) THEN
        IF en_comReg = '1' THEN
            -- shift left
            comReg(23 downto 16) <= comReg(15 downto 8);
            comReg(15 downto 8) <= comReg(7 downto 0);
            -- add 8 bits
            comReg(7 downto 0) <= comReg_input;
            -- increment count
            comReg_count <= comReg_count + 1;
        END IF;
    END IF;
END PROCESS;

end Behavioral;