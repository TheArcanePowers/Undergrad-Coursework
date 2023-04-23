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
    TYPE state_type IS (S0, S1, S2, S3, S4, S5, S6, S7, S8);
    signal curState, nextState: state_type;
    -- Counters
    signal globalCount: integer;
    signal en_globalCount, res_globalCount: bit;
    signal threeCount: integer;
    signal en_threeCount, res_threeCount: bit;
    -- S0 
    --signal dataReg: std_logic_vector(7 downto 0);
	-- S2
    signal bcdReg: BCD_ARRAY_TYPE(2 downto 0); -- for maxIndex (numWords can be asserted immediately as an output)
	signal commandValid: bit;
    signal secondInputMode: bit;
    -- S3
    --signal byteDone: bit;
    -- S4
    signal finalDataReg: CHAR_ARRAY_TYPE(0 to RESULT_BYTE_NUM-1); --same as dataResults
    --S5
    signal secondPhaseDone: bit;
    --signal secondChar: bit;
    --signal rxNow_reg, txDone_reg: std_logic;
    --signal rxData_reg: std_logic_vector (7 downto 0);
    
    --signal comReg_count: integer;
    --
    function hexToAscii(fourBitHex: std_logic_vector(3 downto 0)) return std_logic_vector is
        variable eightBitAscii: std_logic_vector(7 downto 0);
    begin
        IF UNSIGNED(fourBitHex) >= 10 THEN
            eightBitAscii := "0100" & std_logic_vector(unsigned(fourBitHex) - unsigned'("1001"));    --std_logic_vector(RESIZE(UNSIGNED(fourBitHex) + 55, 8));
        ELSE
            eightBitAscii := "0011" & std_logic_vector(fourBitHex);
        END IF;
        return eightBitAscii;
    end function;
BEGIN

-- TODO TO IMPROVE--
-- 1. Can remove dataReg
-- 2. hexToAscii has stopped working!!!
-- 3. ight be able to get rid of finalwordbcd if i don't have the last start on the last start run
-- 5. Add newlines when triggering S3 and S6

-- State Logic
nextState_logic: process(curState, rxNow, txDone, dataReady, seqDone)
BEGIN
    CASE curState IS
        WHEN S0 =>  -- AWAIT FOR INPUT
            IF rxNow='1' THEN -- AND NOT(ovErr='1' OR framErr='1') THEN
                nextState <= S1;
            ELSE
                nextState <= S0;
            END IF;
        
        WHEN S1 =>
            IF txDone = '1' THEN
                nextState <= S2;
            ELSE
                nextState <= S1;
            END IF;
        
        WHEN S2 =>  -- AWAIT FOR SUCCESSFULL ECHO -- COMBINE WITH S2
            IF rxData >= x"30" AND rxData <= x"39" and commandValid = '1' THEN
                IF globalCount = 2 THEN
                -- 3 numbers and A/a previously recived. Full Command ---
                    nextState <= S3;
                ELSE
                    nextState <= S0;
                END IF;
            ELSIF (rxData = x"50" OR rxData = x"70" OR rxData = x"4C" or rxData = x"6C") AND (secondInputMode = '1') THEN
                -- P/p/L/l and First Command previously recieved -- 
                nextState <= S6;
            ELSE
                -- incorrect sequence or need more inputs --
                nextState <= S0;
            END IF;
        
        -- TODO: ADD NEWLINE
            
        WHEN S3 =>  -- WAIT FOR DataReady from Data Processor --
            IF dataReady = '1' AND txDone = '1' THEN     --wait for transmission complete AND data ready
                nextState <= S4;
            ELSE
                nextState <= S3;    -- Loops
        END IF;
                
        WHEN S4 =>  -- Load Bits for Printing-- TODO: CAN THIS BE REMOVED??
            nextState <= S5;
            
        WHEN S5 =>  -- AWAIT FOR TRANSMISSION --
            IF txDone = '1' THEN --XNOR seqDone ='0' THEN --XNOR allows to skip this when seqDone='1'
                IF secondInputMode = '1' and threeCount = 2 THEN
                    -- Skip everything, we've just outputted last space.
                    nextState <= S0;
                ELSE
                    IF threeCount = 2 THEN
                        nextState <= S3;    -- await next byte
                    ELSE
                        nextState <= S4;    -- Proceed with next transmission in 'queue'
                        -- Theoretically could put bit loading here surely? And first transmission being a new line
                    END IF;
                END IF;
            ELSE
                nextState <= S5;    -- loop
            END IF;
            
        WHEN S6 =>
            IF rxData = x"50" or rxData = x"70" THEN  -- P or p
                nextState <= S7;
            ELSIF rxData = x"4C" or rxData = x"6C" THEN   -- L or l
                nextState <= S7;
            ELSE
                nextState <= S0;                        -- error catching
            END IF;          
            
        WHEN S7 =>
            IF txDone = '1' THEN
                IF secondPhaseDone = '1' AND threeCount = 2 THEN
                    nextState <= S0;
                ELSE
                    nextState <= S6;
                END IF;
            ELSE
                nextState <= S7;    -- loop
            END IF;
            
        WHEN OTHERS =>
            nextState <= S0;
    END CASE;
END PROCESS;

-- State Register
State_register: process (reset, clk)
BEGIN
    IF reset='1' THEN
      curState <= S0;
    ELSIF rising_edge(clk) THEN
        -- Could set all signals to default here as well--
        --rxNow_reg   <= rxNow;
        curState <= nextState;
    END IF;
END PROCESS;

-- Combinational Output Logic (all covered in next state logic above)
combi_out: PROCESS(curState, rxNow, txDone, seqDone)
BEGIN
    -- set default variables
    -- external signals
    rxDone <= '0';
    txNow <= '0';
    start <= '0'; -- FOR DATA PROCESSOR TO INITIALIZE. THEN TO ALWAYS TURN START OFF AFTER 1 CLK CYCLE
    -- internal signals
    en_globalCount <= '0';
    res_globalCount <= '0';
    en_threeCount <= '0';
    res_threeCount <= '0';
    --
    CASE curState IS
        WHEN S0 =>  -- AWAIT FOR INPUT
            en_globalCount <= '0'; -- FIND BETTER PLACE?
            secondPhaseDone <= '0';
            IF rxNow='1' THEN -- AND NOT(ovErr='1' OR framErr='1') THEN
                --dataReg <= rxData;                      -- Load in data. Comes in ASCII, we output in ASCII.
                rxDone <= '1';                          -- Can start receiving next bit.
                txData <= rxData;   -- dataReg does not get updated value from rxData until end of process so rxData is used for instant Echo transmission.
                txNow <= '1';                           -- Can transmit data.
            END IF;
                    
        WHEN S2 =>
            IF rxData = x"41" OR rxData = x"61" THEN  -- VALID A --
                commandValid <= '1';                        -- Recived A/a. Number register now valid
                res_globalCount <= '1';                     -- Resets counter
            ELSIF rxData >= x"30" AND rxData <= x"39" and commandValid = '1' THEN -- 0-9 and A/a previously recived --
                en_globalCount <= '1';
                IF globalCount = 0 THEN
                    numWords_bcd(2) <= rxData(3 downto 0);
                ELSIF globalCount = 1 THEN
                     numWords_bcd(1) <= rxData(3 downto 0);
                ELSIF globalCount = 2 THEN  -- FULL COMMAND RECIEVED --
                     numWords_bcd(0) <= rxData(3 downto 0);
                    --numWords_bcd <= bcdReg; -- initiates seqDone signal from Data Processor
                    res_globalCount <= '1';             -- Reset counter, no longer needed
                    res_threeCount <= '1';
                    commandValid <= '0';                -- Need another a/A to continue
                    start <= '1';                       -- Starts data processor
                ELSE
                    res_globalCount <= '0';
                END IF;
            ELSIF (rxData = x"50" OR rxData = x"70" OR rxData = x"4C" or rxData = x"6C") AND (secondInputMode = '1') THEN
                -- P/p/L/l and Full Command previously recieved -- 
                res_globalCount <= '1';
                res_threeCount <= '1';
            ELSE
                -- assume interrupts semi-valid sequence. Must reset everything --
                res_globalCount <= '1';
                commandValid <= '0';
            END IF;
                
        WHEN S4 =>  -- Load Bits for Printing--
            IF threeCount = 0 THEN
                txData <= hexToAscii(byte(7 downto 4));    -- Loads up ascii hex for first 4 bits
            ELSIF threeCount = 1 THEN 
                txData <= hexToAscii(byte(3 downto 0));    -- Loads up ascii hex for second 4 bits
            ELSE
                txData <= x"20";                     -- Loads up ascii space
            END IF;
            en_threeCount <= '1';                  -- Increment counter
            txNow <= '1';                           -- Start transmitting
            
        WHEN S5 =>  -- AWAIT FOR TRANSMISSION --
            IF txDone = '1' THEN --XNOR seqDone ='0' THEN --XNOR allows to skip this when seqDone='1'
                IF secondInputMode = '1' and threeCount = 2 THEN
                    -- Skip everything, we've just outputted last space.
                    res_threeCount <= '1';
                ELSE
                    IF seqDone = '1' THEN
                        secondInputMode <= '1'; -- tells us it's the last run
                        finalDataReg <= dataResults;    -- Load registers
                        bcdReg <= maxIndex;             -- Load registers
                    END IF;
                    IF threeCount = 2 THEN
                        -- might need to change to only happen if seqdone != 1
                        start <= '1';
                    END IF;
                END IF;
            END IF;

            
        WHEN S6 =>
            IF rxData = x"50" or rxData = x"70" THEN  -- P or p
                IF globalCount = 0 THEN -- Prints Peak BYTE IN HEX FORMAT
                    IF threeCount = 0 THEN
                        txData <= hexToAscii(finalDataReg(3)(7 downto 4));
                    ELSIF threeCount = 1 THEN
                        txData <= hexToAscii(finalDataReg(3)(3 downto 0));
                    ELSE
                        txData <= x"20";
                        en_globalCount <= '1';
                    END IF;
                ELSIF globalCount = 1 THEN -- PRINTS BYTE INDEX IN ASCII FORMAT
                    IF threeCount = 0 THEN
                   	    txData <= "0011" & bcdReg(2); --converts BCD value to ASCII 
                    ELSIF threeCount = 1 THEN
                        txData <= "0011" & bcdReg(1);				
                    ELSIF threeCount = 2 THEN
                        txData <= "0011" & bcdReg(0);
                        secondPhaseDone <= '1';
                        --res_threeCount <= '1';
                    END IF;
                END IF;
                txNow <= '1';
                --en_threeCount <= '1';
            ELSIF rxData = x"4C" or rxData = x"6C" THEN   -- L or l
                IF threeCount = 0 THEN
                    txData <= hexToAscii(finalDataReg(globalCount)(7 downto 4));
                ELSIF threeCount = 1 THEN
                    txData <= hexToAscii(finalDataReg(globalCount)(3 downto 0));
                ELSE
                -- When threeCounter reaches 2, it's finished its cycle and can move onto next byte of dataResult.
                    txData <= x"20";
                    en_globalCount <= '1';
                END IF;
                txNow <= '1';
                --en_threeCount <= '1';
                IF globalCount = 6 THEN
                    secondPhaseDone <= '1';
                END IF;
            END IF;
            
        WHEN S7 =>
            IF txDone = '1' THEN
                en_threeCount <= '1';
                IF secondPhaseDone = '1' AND threeCount = 2 THEN
                    res_globalCount <= '1';
                END IF;
            END IF;
            
        WHEN OTHERS =>
            -- THIS IS WRONG. MAKE SURE TO FIX
            rxDone <= '0';
            txNow <= '0';
            start <= '0'; -- FOR DATA PROCESSOR TO INITIALIZE. THEN TO ALWAYS TURN START OFF AFTER 1 CLK CYCLE
            -- internal signals
            en_globalCount <= '0';
            res_globalCount <= '0';
            en_threeCount <= '0';
            res_threeCount <= '0';
            
    END CASE;
END PROCESS; -- combi_outputend Behavioral;

-- TODO: COMBINE STATE S2 & S3 because nothing calls specifically to S2
-- TODO: Optimize states?

threeCounter: process(clk)
-- literally goes 0, 1, 2, 0, 1, 2 --
-- purposefully fully synchronous - we get logic errors if not --
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

globalCounter: process(clk) -- can be fully synchronous too
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