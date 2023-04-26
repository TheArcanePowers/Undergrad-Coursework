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
  SIGNAL postbitCounter, indexCounter, dataInt, curInt, mainIndex, maxIndex0, maxIndex1, maxIndex2, singleCounter, tensCounter, hundredsCounter: integer;
  SIGNAL en_postbitCounter, res_postbitCounter, en_indexCounter, res_indexCounter: bit;
  SIGNAL threePrev: std_logic_vector(23 downto 0); -- uesd to hold 3 prev values
  SIGNAL maxByte, lastByte: std_logic_vector(7 downto 0);
  SIGNAL BCD0, BCD1, BCD2: std_logic_vector(3 downto 0);
  SIGNAL prevctrlIn, xorIn, newInt, recentInt, postbitcounterTrack, en_Reg, singleLast, tensLast, convProcess: std_logic;
BEGIN 
  NextStateLogic: PROCESS(curState, postbitCounter, indexCounter, start, xorIn, newInt, recentInt, postbitcounterTrack, singleCounter, tensCounter)
  BEGIN
    en_postbitCounter<='0'; --assigning some default values
    en_indexCounter<='0';
    res_postbitCounter<='0';
    res_indexCounter<='0';
    en_Reg<='0'; -- the enable of the 24-bit register 
    convProcess<='0'; --the enable of the integer to BCD converter
    CASE curState IS
      WHEN S0 =>
        seqDone<='0';
        dataReady<='0';
        IF indexCounter=0 THEN
          ctrlOut<=ctrlIn;
        END IF;
        IF start='1' THEN --changes ctrlOut to tell data gen to request new data
          ctrlOut<=NOT ctrlIn;
          IF xorIn='1' THEN
            en_indexCounter<='1'; --enables counter and gets ready to change to S2
            nextState<=S2;
          ELSE
            nextState<=S1;
          END IF;
        ELSIF start='0' THEN
          ctrlOut<=ctrlIn;
          nextState<=S0;
        ELSE 
          nextState<=S0;
        END IF;
      
      WHEN S1 => --this state is used to check the again if ctrlIn has changed (so if there is new data in the generator)
        IF xorIn='1' THEN
          en_indexCounter<='1'; --counts up the index if there is new data.
          nextState<=S2;
        ELSE
          nextState<=S1;
        END IF;
      
      WHEN S2 =>  --this state mainly covers enabling the BCD converter and enabling the 24-bit register 
        byte<=data;
        en_Reg<='1'; --this is used as an enable for the 24-bit register to load the values into the register.
        curInt<=to_integer(signed(maxByte)); --curInt is the current max byte in signed integer form.
        dataInt<=to_integer(signed(data)); --dataInt is the byte thats currently in the data generator in singed integer form.
        convProcess<='1'; --enables conversion to BCD of the current byte position.
        IF recentInt='1' OR postbitCounter=3 THEN
          res_postbitCounter<='1'; --resets the postbti counter if a new peak bit is detected
        ELSIF postbitcounterTrack='1' THEN
          en_postbitCounter<='1';
        END IF;
        nextState<=S3;
        
        
      WHEN S3 =>
        lastByte<=data; --holds this new byte 
        dataReady<='1'; 
        IF singleCounter=9 THEN
          singleLast <= '1'; --checks if single counter is 9, if so puts signleLast high so next time the single counter tries to incremnet it resets
        ELSE
          singleLast<='0'; --else leaves it low
        END IF;
        IF tensCounter=9 THEN
          tensLast<='1';  --checks if tens counter is 9, if so puts tensLast high so next time the tens counter tries to incremnet it resets
        ELSE
          tensLast<='0';
        END IF;
        IF newInt='1' OR indexCounter=1 THEN
          dataResults(3)<=data; --if the byte in data gen is the new highest byte or if its the first one, replace the peak bit in dataResults
          en_postbitCounter<='1'; --enable postbitCounter (
          recentInt<='1'; --ths shows a new peak bit is now, and is used for the postbitCounter.
          postbitcounterTrack<='1'; --this will enable the post counter bit for the next time we reach S3 for the next set of data, unless new peak bit next time.
          maxByte<=data; --used to store the new peak byte in another spot except for reg
          maxIndex(2)<=BCD0; --Loads the convert the new peak byte to BCD and assign it to maxIndex
          maxIndex(1)<=BCD1;
          maxIndex(0)<=BCD2;
          dataResults(6)<=threePrev(7 downto 0); --load in the 3 previous bits from the data register
          dataResults(5)<=threePrev(15 downto 8);
          dataResults(4)<=threePrev(23 downto 16);
        ELSIF newInt='0' THEN -- if the new byte isn't bigger than the current peak
          IF postbitcounterTrack='1' AND postbitCounter=0 THEN --used to store the first byte after the peak
            dataResults(2)<=data; --loads first byte after peak
            recentInt<='0';
          ELSIF postbitCounter=1 THEN
            dataResults(1)<=data; --loads second byte after peak
          ELSIF postbitCounter=2 THEN
            dataResults(0)<=data(7 downto 0);  --loads third byte after peak
            postbitcounterTrack<='0';  --sets back to 0 to show all post peak bits have been counted through
            res_postbitCounter<='1'; --resets the postbit Coutner
          END IF;   
        END IF;
        IF indexCounter=mainIndex THEN --if indexCounter=mainIndex (mainIndex is numWords_bcd in integer form) resets counters
          seqDone<='1'; --overall sequence done
          res_indexCounter<='1'; --resets indexCounter
          nextState<=S0;
        ELSE 
          nextState<=S0; --all go back to initial state
        END IF;
                   
    END CASE;
  END PROCESS;
            
  --State Register--
  stateRegister: PROCESS(reset, clk)
  BEGIN
    IF reset='1' THEN
      curState<=S0; --Goes back to S0 on reset
    ELSIF clk'EVENT AND clk='1' THEN
      curState<=nextState; --Advances to nextState on the rising edge of each clock cycle
    END IF;
  END PROCESS;
  
  --Flip-flop to hold previous ctrlIn value and to XOR it with current ctrlIn-
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
      threePrev<="000000000000000000000000"; --resets the bit register to be filled with 0's on reset
    ELSIF clk'EVENT AND clk='1' AND en_Reg='1' THEN
      FOR i IN 15 DOWNTO 0 LOOP
        threePrev(i)<=threePrev(i+8); --moves bits 8 along e.g. if postition was previously threePrev(17) it will move to threePrev(9)
      END LOOP;
      threePrev(23 DOWNTO 16)<=lastByte; --moves in previous data into register 
    END IF;
  END PROCESS;
     
     
      

  --Post Bit Counter-- (this counter beings to enbale 3 times after a new peak bit, and is used to help store the 3 bits after a peak bit.)
  postBit_Counter: PROCESS(clk)
  BEGIN 
    IF reset='1' or res_postbitCounter='1' THEN
      postbitCounter <= 0; --resets to 0 when any reset is high.
    ELSIF clk'EVENT AND clk='1' THEN
      IF en_postbitCounter='1' THEN --when clock is high and enable is high, increment the counter by 1.
        postbitCounter <= postbitCounter+1;
      END IF;
    END IF;
  END PROCESS;
  
  --Index Counter--
  Index_Counter: PROCESS(clk)
  BEGIN
    IF reset='1' or res_indexCounter='1' THEN --if resets are high, reset all counters 
      indexCounter <= 0; --this counter is used for the whole index, goes up to 500
      singleCounter<= 0; --this counter is used to count up the first digit of the counter, needed to convert the peak position to BCD e.g. if indexCount is 367 this would hold integer value of 7
      tensCounter<= 0;  --this counter is used to count up the digit in the tens column of the counter, needed to convert the peak position to BCD e.g. if indexCount is 367 this would have integer value of 6
      hundredsCounter<= 0;  --this counter is used to count up the digit in the hundreds column of the counter, needed to convert the peak position to BCD e.g. if indexCount is 367 this would have value of 3
    ELSIF clk'EVENT AND clk='1' THEN
      IF en_indexCounter='1' AND singleLast='0' AND tensLast='0' THEN
        indexCounter <= indexCounter+1; --if the tens digit and the current first digit aren't 9
        singleCounter <= singleCounter+1;
      ELSIF en_indexCounter='1' AND singleLast='0' AND tensLast='1' THEN
        indexCounter <= indexCounter+1; --if the tens digit is a 9 but the singular digit isn't 9
        singleCounter <= singleCounter+1; --only the singular counter increments
      ELSIF en_indexCounter='1' AND singleLast='1' AND tensLast='0' THEN 
        indexCounter <= indexCounter+1; --if the tens isn't 9 and the singualr digit is, this will cause the signular counter to 
        singleCounter <= 0; --reset whereas the tens counter increments by 1
        tensCounter <= tensCounter+1;
      ELSIF en_indexCounter='1' AND singleLast='1' AND tensLast='1' THEN 
        indexCounter <= indexCounter+1; --if the tens column and signle column is 9
        singleCounter <= 0; --both the single and tens counters are reset and the hundreds counter increments up.
        tensCounter <= 0;
        hundredsCounter <= hundredsCounter+1;
      ELSIF en_indexCounter='1' THEN
        indexCounter<=indexCounter+1;
      
      END IF;
    END IF;
  END PROCESS;
  
  --Int Comparator--
  Int_Calc: PROCESS(clk)
  BEGIN
    IF clk='1' and clk'EVENT THEN
      IF dataInt>curInt THEN --Calculates which is bigger between the current max byte and the one coming from the data generator
        newInt<='1'; --if the new byte is bigger this acts as enable to load it in.
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
         CASE hundredsCounter IS --converts to BCD the current integer values in all the counters
           WHEN 9 => BCD0 <= "1001"; --selects the binary value for each counter based on current int value they hold.
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
      maxIndex0<=to_integer(unsigned(numWords_bcd(0))); --calculates what the total of number of words in the sequence there is and 
      maxIndex1<=to_integer(unsigned(numWords_bcd(1))); --converts it from BCD to int
      maxIndex2<=to_integer(unsigned(numWords_bcd(2)));
      mainIndex<=(maxIndex2*100)+(maxIndex1*10)+(maxIndex0);
    END IF;
  END PROCESS;

END;

