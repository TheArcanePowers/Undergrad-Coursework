----------------------------------------------------------------------------------
--Luke Hayes
-- 
----------------------------------------------------------------------------------


library IEEE;
use ieee.STD_LOGIC_1164.all;
use work.common_pack.all;
use ieee.numeric_std.all;

entity dataConsume is
port (
  clk:		in std_logic;
  reset:        in std_logic; -- synchronous reset
  start: in std_logic; -- goes high to signal data transfer
  numWords_bcd: in BCD_ARRAY_TYPE(2 downto 0);
  ctrlIn: in std_logic;
  ctrlOut: out std_logic;
  data: in std_logic_vector(7 downto 0);
  dataReady: out std_logic;
  byte: out std_logic_vector(7 downto 0);
  seqDone: out std_logic;
  maxIndex: out BCD_ARRAY_TYPE(2 downto 0);
  dataResults: out CHAR_ARRAY_TYPE(0 to RESULT_BYTE_NUM-1) -- index 3 holds the peak
);
end dataConsume;

ARCHITECTURE Behavioural OF dataConsume IS
  TYPE state_type IS (S0, S1, S2, S3);
  SIGNAL curState, nextState: state_type;
  SIGNAL postbitCounter, indexCounter, dataInt, curInt, mainIndex, maxIndex0, maxIndex1, maxIndex2, maxbytePos: integer;
  SIGNAL en_postbitCounter, res_postbitCounter, en_indexCounter, res_indexCounter: bit;
  SIGNAL threePrev: std_logic_vector(23 downto 0);
  SIGNAL maxByte, lastByte: std_logic_vector(7 downto 0);
  SIGNAL prevctrlIn, xorIn, newPeak, newInt, recentInt, test1, postbitcounterTrack, newReg: std_logic;
BEGIN 
  NextStateLogic: PROCESS(curState, postbitCounter, indexCounter, start, xorIn, newInt, recentInt, postbitcounterTrack)
  BEGIN
    en_postbitCounter<='0';
    en_indexCounter<='0';
    res_postbitCounter<='0';
    res_indexCounter<='0';
    newReg<='0';
    CASE curState IS
      WHEN S0 =>
        seqDone<='0';
        IF indexCounter=0 THEN
          ctrlOut<='0';
        END IF;
        dataReady<='0';
        IF start='1' THEN
          ctrlOut<=NOT ctrlIn;
          IF xorIn='1' THEN
            nextState<=S2;
          ELSE
            nextState<=S1;
          END IF;
        ELSE
          nextState<=S0;
        END IF;
      
      WHEN S1 =>
        IF xorIn='1' THEN
          nextState<=S2;
        ELSE
          nextState<=S1;
        END IF;
      
      WHEN S2 =>
        byte<=data;
        en_indexCounter<='1';
        newReg<='1';
        curInt<=to_integer(signed(maxByte));
        dataInt<=to_integer(signed(data));
        IF recentInt='1' OR postbitCounter=3 THEN
          res_postbitCounter<='1';
        ELSIF postbitcounterTrack='1' THEN
          en_postbitCounter<='1';
        END IF;
        nextState<=S3;
        
        
      WHEN S3 =>
      lastByte<=data;
        IF newInt='1' OR indexCounter=1 THEN
          dataResults(3)<=data;
          en_postbitCounter<='1';
          recentInt<='1';
          postbitcounterTrack<='1';
          maxByte<=data;
          maxbytePos<=indexCounter;
          dataResults(0)<=threePrev(7 downto 0);
          dataResults(1)<=threePrev(15 downto 8);
          dataResults(2)<=threePrev(23 downto 16);
          IF indexCounter=mainIndex THEN
            seqDone<='1';
            res_indexCounter<='1';
            nextState<=S0;
          ELSE 
            nextState<=S0;
          END IF;
        ELSIF newInt='0' THEN
          IF postbitcounterTrack='1' AND postbitCounter=0 THEN
            dataResults(4)<=data;
            test1<='1';
            recentInt<='0';
            nextState<=S0;
          ELSIF postbitCounter=1 THEN
            dataResults(5)<=data;
            nextState<=S0;
          ELSIF postbitCounter=2 THEN
            dataResults(6)<=data(7 downto 0);
            postbitcounterTrack<='0';
            res_postbitCounter<='1';
            nextState<=S0;
          ELSE
            nextState<=S0;
          END IF;   
        END IF;     
    END CASE;
  END PROCESS;
            
  --State Register--
  stateRegister: PROCESS(reset, clk)
  BEGIN
    IF reset='1' THEN
      curState<=S0;
    ELSIF clk'EVENT AND clk='1' THEN
      curState<=nextState;
    END IF;
  END PROCESS;
  
  --Register-
  prev_ctrlIn: PROCESS(clk)
  BEGIN
    IF clk'EVENT AND clk='1' THEN
      prevctrlIn<=ctrlIn;
      xorIn<= prevctrlIn XOR ctrlIn;
    END IF;
  END PROCESS;
  
  --24 Bit-Reg--
  reg24: PROCESS(clk)
  BEGIN 
    IF reset='1' THEN
      threePrev<="000000000000000000000000";
    ELSIF clk'EVENT AND clk='1' AND newReg='1' THEN
      FOR i IN 15 DOWNTO 0 LOOP
        threePrev(i)<=threePrev(i+8);
      END LOOP;
      threePrev(23 DOWNTO 16)<=lastByte;
    END IF;
  END PROCESS;
     
     
      

  --Post Bit Counter--
  postBit_Counter: PROCESS(clk)
  BEGIN 
    IF reset='1' or res_postbitCounter='1' THEN
      postbitCounter <= 0;
    ELSIF clk'EVENT AND clk='1' THEN
      IF en_postbitCounter='1' THEN
        postbitCounter <= postbitCounter+1;
      END IF;
    END IF;
  END PROCESS;
  
  --Index Counter--
  Index_Counter: PROCESS(clk)
  BEGIN
    IF reset='1' or res_indexCounter='1' THEN
      indexCounter <= 0;
    ELSIF clk'EVENT AND clk='1' THEN
      IF en_indexCounter='1' THEN
        indexCounter <= indexCounter+1;
      END IF;
    END IF;
  END PROCESS;
  
  --Int Comparator--
  Int_Calc: PROCESS(clk)
  BEGIN
    IF clk='1' and clk'EVENT THEN
      IF dataInt>curInt THEN
        newInt<='1';
      ELSE
        newInt<='0';
      END IF;
    END IF;
  END PROCESS;
      
  
  --BCD Calcualtor--
  BCD_Calc: PROCESS(clk)
  BEGIN
    maxIndex0<=to_integer(unsigned(numWords_bcd(0)));
    maxIndex1<=to_integer(unsigned(numWords_bcd(1)));
    maxIndex2<=to_integer(unsigned(numWords_bcd(2)));
    mainIndex<=(maxIndex2*100)+(maxIndex1*10)+(maxIndex0);
  END PROCESS;

END;
