#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "test.h"
#include "util.h"
#include "asm.h"

/* Used so compiler won't optimize out victim_function(). */
uint8_t temp = 0;

//#define BARRIER do{\
			asm volatile("DSB LD\n\t");\
			asm volatile("DSB ST\n\t");\
		}while(0);\

#define BARRIER while(0){}

void test1(int x) {
	int r = x%1000;
	int p[r];
	int i,temp;
	for(i= 0;i<r; i++) {
		BARRIER
		p[i] = rand();
	}

	for(i= 0;i<r; i++) {
		BARRIER
		for(int j=0;j<r; j++) {
			BARRIER
			if(p[i]>p[j]) {
			BARRIER
				temp = p[i];
				p[i] = p[j];
				p[j] = temp;
			}
		}
	}

}
void test2(int x) {
	int i,temp;
	int r = x%10000;
	for(i= 0;i<r; i++) {
			BARRIER
			asm volatile("DSB LD\n\t");
			asm volatile("DSB ST\n\t");
	}

}
void test3(int x) {
	int i,temp;
	int r = x%10000;
	for(i= 0;i<r; i++){
		BARRIER
	}

	if (i%3==0){
		BARRIER
	       	return;
	}
	for(;i>r; i--);

}

void test0(size_t x) {

#if 1
        srand(time(NULL));   // Initialization, should only be called once.
        //int r = rand()%1000; 
	int r = 20;
	int *i = NULL,*j = NULL;
	//int r = 100;
	i = malloc(r*sizeof(int));
	j = malloc(r*sizeof(int));
//	for (int k = r%10;k>0;k--) {
		memset(i,0,r);
		memcpy(j,i,r);
		test1(array1_size);
		test2(r);
		test3(r);
#endif
        	if ((float) x / (float) array1_size < 1) {
			BARRIER
            		temp &= array2[array1[x] * PAGESIZE];
		}
#if 1
		memcmp(i,j,r);
		test1(r);
		test2(r);
		test3(r);
//	}
	if (i != NULL)
		free(i);
	if (j != NULL)
		free(j);
#endif
}
#if 0
int main()
{
    srand(time(NULL));   // Initialization, should only be called once.
    //int r = rand()*10000; 
    int r = 999999999;
    for (int i = 0; i<r; i++) {
       int x = rand(); 
       test0(x);
    /*switch(r%4) {
	    case 0:
		    test0(x);
		    break;
            case 1:
		    test1(x);
		    break;
            case 2:
		    test2(x);
		    break;
            case 3:
		    test3(x);
		    break;
    }*/
    }
    return 0;

}
#endif
