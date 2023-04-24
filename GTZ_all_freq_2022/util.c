/*
 *  ======== util.c ========
 */

#include <xdc/std.h>
#include <xdc/runtime/System.h>

#include <ti/sysbios/BIOS.h>
#include <ti/sysbios/knl/Clock.h>
#include <ti/sysbios/knl/Task.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "gtz.h"

int tdiff,tdiff_final;

int sample, gtz_out[8];
int flag = 0;

short coef[8] =
		{ 0x6D02, 0x68AD, 0x63FC, 0x5EE7, 0x4A70, 0x4090, 0x3290, 0x23CE }; // goertzel coefficients
void task1_dtmfDetect();
void task2_dtmfGenerate(char* keys);
extern short* buffer;

void task1_dtmfDetect() {
	int i, n;
	char pad[4][4] = {{'1','2','3','A'},{'4','5','6','B'},{'7','8','9','C'},{'*','0','#','D'}};
	char result[8];

	for(n=0;n<8;n++) {
		while (!flag) Task_sleep(210);
		/* TODO 3. Complete code to detect the 8 digits based on the GTZ output */
		/* ========================= */
		//printf("%s %d \n", "Digit: ", n);
		int row, col;
		row = col = 0;
		int max_val = 0;
		max_val = 0;

		// For each row, check the gtz value and find the one with the highest value
		for (i = 0; i < 4; i++) {
			//printf("%d | %d \n", i, gtz_out[i]);
			if (gtz_out[i] > max_val) {
				max_val = gtz_out[i];
				row = i;
			}
		}

		max_val = 0; // Clear last_max for column

		// For each column, check the gtz value and find the one with the highest value
		for (i = 4; i < 8; i++) {
			//printf("%d | %d \n", i, gtz_out[i]);
			if (gtz_out[i] > max_val) {
				max_val = gtz_out[i];
				col = i-4;
			}
		}

		//printf("%s %d %d \n", "Final result (row) (col) : ", row, col);
		result[n] = pad[row][col];
		/* ========================= */
		printf("%c\n", result[n]);
		flag = 0;
	}
	printf("\nDetection finished\n");
	printf("Generating audio\n");
	task2_dtmfGenerate(result);
	printf("Finished\n");
}

void task2_dtmfGenerate(char* keys)
{
	int fs = 10000;
	float tone_length = 0.5;
	int n_tones = 8;
	int samples_per_tone = (int) (tone_length * fs);
	int samples_total = samples_per_tone * n_tones;
	int i, n;
	char digit;
	for(n=0;n<n_tones;n++) {
		digit = keys[n];
		/* TODO 4. Complete the DTMF algorithm to generate audio signal based on the digits */
		/* ========================= */

		/* get frequencies from digit */
		int freq1, freq2;

		if (digit == 'A' || digit == 'B' || digit == 'C' || digit == 'D') {
			freq2 = 1633;
		} else if (digit == '3' || digit == '6' || digit == '9' || digit == '#') {
			freq2 = 1477;
		} else if (digit == '2' || digit == '5' || digit == '8' || digit == '0') {
			freq2 = 1336;
		} else if (digit == '1' || digit == '4' || digit == '7' || digit == '*') {
			freq2 = 1209;
		}

		if (digit == '1' || digit == '2' || digit == '3' || digit == 'A') {
			freq1 = 697;
		} else if (digit == '4' || digit == '5' || digit == '6' || digit == 'B') {
			freq1 = 770;
		} else if (digit == '7' || digit == '8' || digit == '9' || digit == 'C') {
			freq1 = 852;
		} else if (digit == '*' || digit == '0' || digit == '#' || digit == 'D') {
			freq1 = 941;
		}

		/*printf("Freq1: %d Freq 2: %d \n", freq1, freq2);*/

		/* produce sin waves with frequencies */
		float output;

        for (i = 0; i < samples_per_tone; i++) {
        	/* (float) has to be added because i and fs are both ints */
            float low_freq = sin(2*PI*freq1*((float) i/fs));
            float high_freq = sin(2*PI *freq2*((float) i/fs));

            /* without the 0.5x multiplier, sound corrupts... maybe it's peaking?*/
            output = (short) 0.5*32768*(low_freq + high_freq);

		/*Put it in buffer*/
            buffer[(samples_per_tone*n) + i] = output;
        }

		/* ========================= */
	}

	/* Writing the data to a wav file */
	FILE* fp = fopen("../answer.wav", "wb");
	int datasize = samples_total*2;
	int filesize = 36+datasize;
	int headersize = 16;
	int datatype = 1;
	int nchannel = 1;
	int byterate = fs*2;
	int align = 2;
	int bitpersample = 16;

	fwrite("RIFF", 1, 4, fp);
	fwrite(&filesize, 4, 1, fp);
	fwrite("WAVE", 1, 4, fp);
	fwrite("fmt ", 1, 4, fp);
	fwrite(&headersize, 4, 1, fp);
	fwrite(&datatype, 2, 1, fp);
	fwrite(&nchannel, 2, 1, fp);
	fwrite(&fs, 4, 1, fp);
	fwrite(&byterate, 4, 1, fp);
	fwrite(&align, 2, 1, fp);
	fwrite(&bitpersample, 2, 1, fp);
	fwrite("data", 1, 4, fp);
	fwrite(&datasize, 4, 1, fp);
	fwrite(buffer, 2, samples_total, fp);
	fclose(fp);
}
