#ifndef _TEST_H_
/** Page size. Can be obtain at runtime by 'pagesize =
    sysconf(_SC_PAGESIZE);'. */
#define PAGESIZE (256) // TODO Test 256, 512, 4096. It's called PAGESIZE, which
                       // I though initially. Currently, I don't thought that
                       // anymore. What this number really is?

/** Cache line size. Can be obtain with the architecture manual. */
#define CACHELINE (64)

uint8_t unused1[CACHELINE];
uint8_t array1[160] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
uint8_t unused2[CACHELINE];
uint8_t array2[256 * PAGESIZE];
char *secret = "All we have to decide is what to do with the time!";
//char *secret = "ecole polytechnique!";
/* Size of the shared array used for the offset. */
unsigned int array1_size = 16;

#endif
