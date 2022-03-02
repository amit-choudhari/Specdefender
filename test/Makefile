CC=aarch64-linux-gnu-gcc
CFLAGS=-Wall -g3 -march=native -static -O0 # -I../
#CFLAGS=-Wall -g3 -march=-march=armv8.2-a+sb -static -O0 # -I../

all: arm

arm:
	$(CC) $(CFLAGS) -c main.c										-o main.o
	$(CC) $(CFLAGS) -c spectre_pht_sa_ip.c							-o spectre_pht_sa_ip.o
	$(CC) $(CFLAGS) -c util.c										-o util.o
	$(CC) $(CFLAGS) -c asm.c										-o asm.o
	$(CC) $(CFLAGS) -c perf.c										-o perf.o
	$(CC) $(CFLAGS) -c test.c										-o test.o
	$(CC) $(CFLAGS) main.o spectre_pht_sa_ip.o util.o asm.o perf.o test.o	-o spectre

clean:
	rm -f main.o spectre_pht_sa_ip.o util.o asm.o perf.o spectre.o test.o spectre
