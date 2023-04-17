----------------------------------------------------------------------------------
-- Creator: Leonardo Coppi <zq21377@bristol.ac.uk>
-- 
-- Create Date: 20.03.2023 10:49:18
-- Design Name: Command Processor V1.0.0
-- Module Name: cmdProc - Behavioral
-- Description: Needs to be checked for bugs which will I'm sure will be everywhere.
--              Coded according to https://drive.google.com/file/d/1QkyLtYWADuGfPm52DExJHWDSIFzv5yYI/view?usp=sharing
-- 
-- Revision 1.01 - Bug checked, needs testing
-- Revision: 1.00 - Needs to be bug checked!
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;
use work.common_pack.all; -- BDC_ARRAY-TYPE

entity cmdProc is
    port(
      clk:		    in std_logic;
      reset:		in std_logic;
      -- Rx --
      rxNow:		in std_logic;                     -- (rx) valid?
      rxData:		in std_logic_vector (7 downto 0);
      rxDone:		out std_logic;
      ovErr:		in std_logic;
      framErr:	    in std_logic;
     -- Tx --
      txData:		out std_logic_vector (7 downto 0);
      txNow:		out std_logic;
      txDone:		in std_logic;
      -- Data Processor --
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
    -- SIGNAL DECLARATIONS
    TYPE state_type IS (S0, S1, S2, S3, S4, S5, S6, S7);
    signal curState, nextState: state_type;
    --
    signal globalCount: integer;
    signal en_globalCount, res_globalCount: bit;
    signal threeCount: integer;
    signal en_threeCount, res_threeCount: bit;
    -- S0 
    signal dataReg: std_logic_vector(7 downto 0);
	-- S2
    signal bcdReg: BCD_ARRAY_TYPE(2 downto 0); -- for numWords and maxIndex
	signal commandValid: bit;
    signal secondInputMode: bit;
    -- S4
    signal finalDataReg: CHAR_ARRAY_TYPE(0 to RESULT_BYTE_NUM-1); --same as dataResults
    
    --S5
    signal tempData: std_logic_vector(7 downto 0);
    signal secondPhaseDone: bit;
    --signal secondChar: bit;
    
    --signal comReg_count: integer;
    --
    function hexToAscii(fourBitHex: std_logic_vector(3 downto 0)) return std_logic_vector is
        variable eightBitAscii: std_logic_vector(7 downto 0);
    begin
        IF UNSIGNED(fourBitHex) >= 10 THEN
            eightBitAscii := std_logic_vector( UNSIGNED(fourBitHex) + 55);
        ELSE
            eightBitAscii := std_logic_vector( UNSIGNED(fourBitHex) + 48);
        END IF;
    
    end function;
BEGIN

-- State Logic
nextState_logic: process(curState)
BEGIN
    -- set default variables
    -- external signals
    rxDone <= '0';
    txNow <= '0';
    -- internal signals
    en_globalCount <= '0';
    res_globalCount <= '0';
    en_threeCount <= '0';
    res_threeCount <= '0';
    --
    CASE curState IS
        WHEN S0 =>  -- AWAIT FOR INPUT
            IF rxNow='1' AND NOT(ovErr='1' OR framErr='1') THEN
                dataReg <= rxData;                      -- Load in data. Comes in ASCII, we output in ASCII
                rxDone <= '1';                          -- Can start recieving next bit
                txData <= dataReg;                      -- Prepare to output data
                txNow <= '1';                           -- Can transmit data
                nextState <= S1;
            ELSE
                nextState <= S0;
            END IF;
        
        WHEN S1 =>  -- AWAIT FOR SUCCESSFULL ECHO
            IF txDone='1' THEN
                nextState <= S2;
            ELSE
                nextState <= S1;
            END IF;
        
        WHEN S2 => -- INPUT PARSER
            IF dataReg = x"41" OR dataReg = x"61" THEN
                -- VALID A --
                commandValid <= '1';                    -- Recived A/a. Number register now valid
                res_globalCount <= '1';                 -- Resets counter
                nextState <= S0;
            ELSIF dataReg >= x"30" AND dataReg <= x"39" and commandValid = '1' THEN
                -- 0-9 and A/a previously recived --
                --(does std_logic_vector pick the right width)?
              	IF globalCount = 0 THEN
              	bcdReg(2) <= std_logic_vector(unsigned(dataReg) - 48);
              	en_globalCount <= '1'; 		-- enables up counter.
              	ELSIF globalCount = 1 THEN
              	bcdReg(1) <= std_logic_vector(unsigned(dataReg) - 48);
              	en_globalCount <= '1';
              	ELSIF globalCount = 2 THEN
              	bcdReg(0) <= std_logic_vector(unsigned(dataReg) - 48);
                    -- FULL COMMAND RECIEVED --
                    res_globalCount <= '1';             -- Reset counter, no longer needed
                    commandValid <= '0';                -- Need another a/A to continue
                    start <= '1';                       -- Starts Data Processor
                    secondInputMode <= '1';             -- Internal Signal
                    nextState <= S3;
                ELSE
                    nextState <= S0;                    -- Await next input
                END IF;
            ELSIF (dataReg = x"50" OR dataReg = x"70" OR dataReg = x"4C" or dataReg = x"6C") AND (secondInputMode = '1') THEN
                -- P/p/L/l and Full Command previously recieved -- 
                res_globalCount <= '1';
                res_threeCount <= '1';
                nextState <= S5;
            ELSE
                -- assume interrupts semi-valid sequence. Must reset everything --
                res_globalCount <= '1';
                commandValid <= '0';
                nextState <= S0;
            END IF;
            
        WHEN S3 =>  -- DATA PROCESSOR PHASE --
            IF dataReady = '0' THEN
                nextState <= S3;
            ELSE
                start <= '0';                           -- Stop data processor while we print received byte
                IF globalCount = 0 THEN
                    txData <= hexToAscii(byte(3 downto 0));    -- Loads up ascii hex for first 4 bits
                ELSIF globalCount = 1 THEN 
                    txData <= hexToAscii(byte(7 downto 4));    -- Loads up ascii hex for second 4 bits
                ELSE
                    txData <= x"20";                     -- Loads up ascii space
                    res_globalCount <= '1';              -- Resets counter so we can do hex print and space again
                END IF;
                en_globalCount <= '1';                  -- Increment counter
                txNow <= '1';                           -- Start transmitting
                nextState <= S4;
            END IF;
            
        WHEN S4 =>  -- AWAIT FOR TRANSMISSION --
            IF txDone = '0' THEN
                nextState <= S4;
            ELSE
                IF seqDone = '0' THEN
                    start <= '1';                       -- Resume data processor
                    nextState <= S3;                    -- Go to S3 to wait for next byte
                ELSE
                    -- DATA FINISHED PROCESSING --
                    finalDataReg <= dataResults; 
                    bcdReg <= maxIndex; 	-- (do we get maxIndex from data proc at this stage??)
                    nextState <= S0;                    -- Go to S0 to wait for second command
                END IF;
            END IF;
            
        WHEN S5 =>
        -- Was horrifically complicated, so added extra state (S6)
            IF dataReg = x"50" or dataReg = x"70" THEN  -- P or p
                IF globalCount = 0 THEN                 -- Loads peak value in tempData. Goes to S6 which prints it
                    tempData <= finalDataReg(3); 
                    nextState <= S6;
                ELSIF globalCount = 1 THEN
                    IF threeCount = 0 THEN
                   	txData <= std_logic_vector(unsigned(bcdReg(2)) + 48); --converts BCD value to ASCII 
                    en_threeCount <= '1';
                    ELSIF threeCount = 1 THEN
                    txData <= std_logic_vector(unsigned(bcdReg(1)) + 48);				
                    en_threeCount <= '1';
                    ELSIF threeCount = 2 THEN
                    txData <= std_logic_vector(unsigned(bcdReg(0)) + 48);
                    secondPhaseDone <= '1';
                    END IF;
                    nextState <= S7;
                ELSE
                    nextState <= S0;                    -- error catching
                END IF;
            ELSIF dataReg = x"4C" or dataReg = x"6C" THEN   -- L or l
            	IF globalCount = 0 THEN
                tempData <= finalDataReg(6);   -- Loads certain byte in tempData. Checks if phase done. Goes to S6.
                ELSIF globalCount = 1 THEN
                tempData <= finalDataReg(5);   -- From MSB (leftmost byte value)
                ELSIF globalCount = 2 THEN
                tempData <= finalDataReg(4);
                ELSIF globalCount = 3 THEN
                tempData <= finalDataReg(3);   -- Peak
                ELSIF globalCount = 4 THEN
                tempData <= finalDataReg(2);
                ELSIF globalCount = 5 THEN
                tempData <= finalDataReg(1);
                ELSIF globalCount = 6 THEN
                tempData <= finalDataReg(0);   -- To LSB (rightmost byte value)
                    secondPhaseDone <= '1';
                ELSE null; -- avoid undefined states
                END IF;
                nextState <= S6;
            ELSE
                nextState <= S0;                        -- error catching
            END IF;          
            
        WHEN S6 =>
            IF threeCount = 0 THEN
                txData <= hexToAscii(tempData(3 downto 0));
            ELSIF threeCount = 1 THEN
                txData <= hexToAscii(tempData(7 downto 4));
            ELSE
            -- When threeCounter reaches 2, it's finished its cycle and can move onto next byte of dataResult.
                txData <= x"20";
                en_globalCount <= '1';
            END IF;
            nextState <= S7;
            
        WHEN S7 =>
            IF txDone = '0' THEN
                nextState <= S6;
            ELSE
                IF secondPhaseDone = '1' THEN
                    nextState <= S0;
                    res_globalCount <= '1';
                ELSE
                    nextState <= S5;
                END IF;
            END IF;
            
    END CASE;
END PROCESS;

-- State Register
State_register: process (reset, clk)
BEGIN
    IF reset='1' THEN
      curState <= S0;
      -- All signals set to 0 --
    ELSIF rising_edge(clk) THEN
        -- Could set all signals to default here as well--
        curState <= nextState;
    END IF;
END PROCESS;

-- Combinational Output Logic (all covered in next state logic above)
--combi_out: PROCESS(curState)
--BEGIN
--END PROCESS; -- combi_outputend Behavioral;

threeCounter: process(clk, res_threeCount)
-- literally goes 0, 1, 2, 0, 1, 2 --
BEGIN
    IF res_threeCount = '1' THEN
        threeCount <= 0;
    ELSIF rising_edge(clk) THEN
        IF en_threeCount = '1' THEN
            IF threeCount = 2 THEN
                threeCount <= 0;
            ELSE
                threeCount <= threeCount + 1;
            END IF;
        END IF;
    END IF;
END PROCESS;

globalCounter: process(clk, res_globalCount)
-- Added check for reset just to be sure that if reset and enable are both on, reset takes priority.
BEGIN
    IF res_globalCount = '1' THEN
        globalCount <= 0;
    ELSIF rising_edge(clk) THEN
        IF en_globalCount = '1' and res_globalCount ='0' THEN
            globalCount <= globalCount + 1;
        END IF;
    END IF;
END PROCESS;

end Behavioral;