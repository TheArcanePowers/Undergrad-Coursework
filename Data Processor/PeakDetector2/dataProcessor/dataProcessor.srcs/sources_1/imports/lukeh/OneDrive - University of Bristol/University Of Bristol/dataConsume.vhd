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
  SIGNAL postbitCounter, indexCounter, dataInt, curInt, mainIndex, maxIndex0, maxIndex1, maxIndex2, maxbytePos, singleCounter, tensCounter, hundredsCounter: integer;
  SIGNAL en_postbitCounter, res_postbitCounter, en_indexCounter, res_indexCounter: bit;
  SIGNAL threePrev: std_logic_vector(23 downto 0);
  SIGNAL maxByte, lastByte: std_logic_vector(7 downto 0);
  SIGNAL BCD0, BCD1, BCD2: std_logic_vector(3 downto 0);
  SIGNAL prevctrlIn, xorIn, newPeak, newInt, recentInt, postbitcounterTrack, newReg, singleLast, tensLast, convProcess: std_logic;
BEGIN 
  NextStateLogic: PROCESS(curState, postbitCounter, indexCounter, start, xorIn, newInt, recentInt, postbitcounterTrack, singleCounter, tensCounter)
  BEGIN
    en_postbitCounter<='0';
    en_indexCounter<='0';
    res_postbitCounter<='0';
    res_indexCounter<='0';
    newReg<='0';
    convProcess<='0';
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
            en_indexCounter<='1';
            nextState<=S2;
          ELSE
            nextState<=S1;
          END IF;
        ELSE
          nextState<=S0;
        END IF;
      
      WHEN S1 =>
        IF xorIn='1' THEN
          en_indexCounter<='1';
          nextState<=S2;
        ELSE
          nextState<=S1;
        END IF;
      
      WHEN S2 =>
        byte<=data;
        newReg<='1';
        curInt<=to_integer(signed(maxByte));
        dataInt<=to_integer(signed(data));
        convProcess<='1';
        IF recentInt='1' OR postbitCounter=3 THEN
          res_postbitCounter<='1';
        ELSIF postbitcounterTrack='1' THEN
          en_postbitCounter<='1';
        END IF;
        nextState<=S3;
        
        
      WHEN S3 =>
        lastByte<=data;
        IF singleCounter=9 THEN
          singleLast <= '1';
        ELSE
          singleLast<='0';
        END IF;
        IF tensCounter=9 THEN
          tensLast<='1';
        ELSE
          tensLast<='0';
        END IF;
        IF newInt='1' OR indexCounter=1 THEN
          dataResults(3)<=data;
          en_postbitCounter<='1';
          recentInt<='1';
          postbitcounterTrack<='1';
          maxByte<=data;
          maxbytePos<=indexCounter;
          maxIndex(2)<=BCD0;
          maxIndex(1)<=BCD1;
          maxIndex(0)<=BCD2;
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
            recentInt<='0';
            IF indexCounter=mainIndex THEN
            seqDone<='1';
            res_indexCounter<='1';
              nextState<=S0;
            ELSE 
              nextState<=S0;
            END IF;
          ELSIF postbitCounter=1 THEN
            dataResults(5)<=data;
            IF indexCounter=mainIndex THEN
              seqDone<='1';
              res_indexCounter<='1';
              nextState<=S0;
            ELSE 
              nextState<=S0;
          END IF;
          ELSIF postbitCounter=2 THEN
            dataResults(6)<=data(7 downto 0);
            postbitcounterTrack<='0';
            res_postbitCounter<='1';
            IF indexCounter=mainIndex THEN
              seqDone<='1';
              res_indexCounter<='1';
              nextState<=S0;
            ELSE 
              nextState<=S0;
            END IF;
          ELSE
            IF indexCounter=mainIndex THEN
              seqDone<='1';
              res_indexCounter<='1';
              nextState<=S0;
            ELSE 
              nextState<=S0;
            END IF;
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
      singleCounter<= 0;
      tensCounter<= 0;
      hundredsCounter<= 0;
    ELSIF clk'EVENT AND clk='1' THEN
      IF en_indexCounter='1' AND singleLast='0' AND tensLast='0' THEN
        indexCounter <= indexCounter+1;
        singleCounter <= singleCounter+1;
      ELSIF en_indexCounter='1' AND singleLast='0' AND tensLast='1' THEN
        indexCounter <= indexCounter+1;
        singleCounter <= singleCounter+1;
      ELSIF en_indexCounter='1' AND singleLast='1' AND tensLast='0' THEN 
        indexCounter <= indexCounter+1;
        singleCounter <= 0;
        tensCounter <= tensCounter+1;
      ELSIF en_indexCounter='1' AND singleLast='1' AND tensLast='1' THEN 
        indexCounter <= indexCounter+1;
        singleCounter <= 0;
        tensCounter <= 0;
        hundredsCounter <= hundredsCounter+1;
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
   
   --BCD Converter--
   BDC_Convert: PROCESS(clk)
   BEGIN
     IF clk='1' AND clk'EVENT THEN
       IF convProcess='1' THEN
         CASE hundredsCounter IS
           WHEN 9 => BCD0 <= "1001";
           WHEN 8 => BCD0 <= "1000";
           WHEN 7 => BCD0 <= "0111";
           WHEN 6 => BCD0 <= "0110";
           WHEN 5 => BCD0 <= "0101";
           WHEN 4 => BCD0 <= "0100";
           WHEN 3 => BCD0 <= "0011";
           WHEN 2 => BCD0 <= "0010";
           WHEN 1 => BCD0 <= "0001";
           WHEN 0 => BCD0 <= "0000";
           WHEN OTHERS => BCD0 <= "0000";
         END CASE;
         CASE tensCounter IS
           WHEN 9 => BCD1 <= "1001";
           WHEN 8 => BCD1 <= "1000";
           WHEN 7 => BCD1 <= "0111";
           WHEN 6 => BCD1 <= "0110";
           WHEN 5 => BCD1 <= "0101";
           WHEN 4 => BCD1 <= "0100";
           WHEN 3 => BCD1 <= "0011";
           WHEN 2 => BCD1 <= "0010";
           WHEN 1 => BCD1 <= "0001";
           WHEN 0 => BCD1 <= "0000";
           WHEN OTHERS => BCD1 <= "0000";
         END CASE;
         CASE singleCounter IS
           WHEN 9 => BCD2 <= "1001";
           WHEN 8 => BCD2 <= "1000";
           WHEN 7 => BCD2 <= "0111";
           WHEN 6 => BCD2 <= "0110";
           WHEN 5 => BCD2 <= "0101";
           WHEN 4 => BCD2 <= "0100";
           WHEN 3 => BCD2 <= "0011";
           WHEN 2 => BCD2 <= "0010";
           WHEN 1 => BCD2 <= "0001";
           WHEN 0 => BCD2 <= "0000";
           WHEN OTHERS => BCD2 <= "0000";
         END CASE;
       END IF;
     END IF; 
   END PROCESS; 
  
  --BCD Calcualtor--
  BCD_Calc: PROCESS(clk)
  BEGIN
    IF clk='1' AND clk'EVENT THEN
      maxIndex0<=to_integer(unsigned(numWords_bcd(0)));
      maxIndex1<=to_integer(unsigned(numWords_bcd(1)));
      maxIndex2<=to_integer(unsigned(numWords_bcd(2)));
      mainIndex<=(maxIndex2*100)+(maxIndex1*10)+(maxIndex0);
    END IF;
  END PROCESS;

END;

