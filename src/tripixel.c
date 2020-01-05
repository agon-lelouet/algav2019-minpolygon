#include <stdio.h>
#include <stdlib.h>

struct bucket {
	long int ref;
	long int highpos;
	long int lowpos;
	char cbv;
};

void printbucket(struct bucket* mybucket);

int
main(int argc, char *argv[])
{
	long int curbucket;
	long int curpos;

	struct bucket mybucket = {
		.ref = 0,
		.highpos = 0,
		.lowpos = 0,
		.cbv = 0,
	};

	while (scanf("%ld %ld", &curbucket, &curpos) != EOF) {

		if ((curbucket != mybucket.ref) || (!mybucket.cbv)) {
			printbucket(&mybucket);
			mybucket.cbv = 1;
			mybucket.ref = curbucket;
			mybucket.highpos = curpos;
			mybucket.lowpos = curpos;
			continue;
		}

		if (curpos > mybucket.highpos) {
			mybucket.highpos = curpos;
			continue;
		}

		if (curpos < mybucket.lowpos) {
			mybucket.lowpos = curpos;
			continue;
		}
	}

	printbucket(&mybucket);

	return 0;
}

void
printbucket(struct bucket* mybucket)
{
	if (!mybucket->cbv) return;

	if (mybucket->lowpos == mybucket->highpos) {
		printf("%ld %ld\n", mybucket->ref, mybucket->lowpos);
		return;
	}

	printf("%ld %ld\n", mybucket->ref, mybucket->lowpos);
	printf("%ld %ld\n", mybucket->ref, mybucket->highpos);
	return;
}
