/*
 *  ======== gtz.c ========
 */

#include <xdc/std.h>
#include <xdc/runtime/System.h>

#include <ti/sysbios/BIOS.h>
#include <ti/sysbios/knl/Clock.h>
#include <ti/sysbios/knl/Task.h>

#include <xdc/runtime/Types.h>
#include <xdc/runtime/Timestamp.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "gtz.h"

void clk_SWI_Read_Data(UArg arg0);
void clk_SWI_GTZ_All_Freq(UArg arg0);

extern void task0_dtmfGen(void);
extern void task1_dtmfDetect(void);

extern int sample, tdiff, tdiff_final, gtz_out[8];
extern short coef[8];
extern int flag;

short data[NO_OF_SAMPLES];
short *buffer;

/*
 *  ======== main ========
 */
int main() {
	System_printf("\n System Start\n");
	System_flush();

	/* Read binary data file */
	FILE* fp = fopen("../data.bin", "rb");
	if(fp==0) {
		System_printf("Error: Data file not found\n");
		System_flush();
		return 1;
	}
	fread(data, 2, NO_OF_SAMPLES, fp);
	buffer = (short*)malloc(2*8*10000);

	/* Create a Clock Instance */
	Clock_Params clkParams;

	/* Initialise Clock Instance with time period and timeout (system ticks) */
	Clock_Params_init(&clkParams);
	clkParams.period = 1;
	clkParams.startFlag = TRUE;

	/* Instantiate ISR for tone generation  */
	Clock_create(clk_SWI_Read_Data, TIMEOUT, &clkParams, NULL);

	/* Instantiate 8 parallel ISRs for each of the eight Goertzel coefficients */
	Clock_create(clk_SWI_GTZ_All_Freq, TIMEOUT, &clkParams, NULL);

	/* Start SYS_BIOS */
	BIOS_start();
}

/*
 *  ====== clk_SWI_Generate_DTMF =====
 *  Dual-Tone Generation
 *  ==================================
 */
void clk_SWI_Read_Data(UArg arg0) {
	static int tick;
	tick = Clock_getTicks();
	sample = data[tick%NO_OF_SAMPLES];
}

/*
 *  ====== clk_SWI_GTZ =====
 *  gtz sweep
 *  ========================
 */
void clk_SWI_GTZ_All_Freq(UArg arg0) {
	// define variables for timing
	static int start, stop;

	// define feedback times as N
	static int N = 0;

   	//Record start time
	start = Timestamp_get32();

	static int Goertzel_Value[8] = {0};
	short input = (short) (sample);	// TODO: consider sizing this down?

	/* TODO 1. Complete the feedback loop of the GTZ algorithm*/
	/* ========================= */
	int n;
	static int prod1[8], prod2[8], prod3[8] = {0};	// need to be int to hold large products
	static short delay[8], delay_1[8], delay_2[8] = {0};	// can be short due to small variable size to conserve memory

	for (n = 0; n < 8; n++) {
		prod1[n] = (delay_1[n]*coef[n])>>14;
		delay[n] = input + (short)prod1[n] - delay_2[n];

		//update delayed variables
		delay_2[n] = delay_1[n];
		delay_1[n] = delay[n];
	}
	/* ========================= */
	N++;

	//Record stop time
	stop = Timestamp_get32();
	//Record elapsed time
	tdiff = stop-start;

	if (N == 206) {
	   	//Record start time
		start = Timestamp_get32();

		/* TODO 2. Complete the feedforward loop of the GTZ algorithm*/
		/* ========================= */
		for (n = 0; n < 8; n++) {
			//int *testpointer;
			//testpointer = &coef;

			prod1[n] = (delay[n] * delay[n]);
			prod2[n] = (delay_1[n] * delay_1[n]);
			prod3[n] = (delay[n] * delay_1[n] * coef[n]) >> 14;

			Goertzel_Value[n] = (prod1[n] + prod2[n] - prod3[n]) >> 8;
			//Goertzel_Value <<= 4;  // scale up for sensitivity. Check??

			gtz_out[n] = Goertzel_Value[n];
		}
		//reset all!
		int k;
		for(k=0; k<8; k++) {
			prod1[k] = 0;
			prod2[k] = 0;
			prod3[k] = 0;
			delay[k] = 0;
			delay_1[k] = 0;
			delay_2[k] = 0;
		}

		/* ========================= */
		flag = 1;
		N = 0;

		//Record stop time
		stop = Timestamp_get32();
		//Record elapsed time
		tdiff_final = stop-start;

	}
}
