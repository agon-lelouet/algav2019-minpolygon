#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

struct point {
	double x;
	double y;
};

double distcarree(struct point *p1, struct point *p2);
struct point midpoint(struct point *p1, struct point *p2);
struct point *furthest(struct point *ref, struct point *set, long int size);
long int circleremoval(struct point *center, double radius, struct point *set,
		       long int size);
struct point barycentre(struct point *center, double radius,
			struct point *outlier);

int
main(int argc, char *argv[])
{
	if (argc < 2) return 22;

	long int ptnbr = strtol(argv[1], NULL, 10);

	struct point *points = malloc(ptnbr * sizeof(struct point));

	for (int i = 0; i < ptnbr ; i++) {
		scanf("%lf %lf", &((points+i)->x), &((points+i)->y));
	}

	clock_t start = clock();

	struct point *p = furthest(points, points, ptnbr);
	struct point *q = furthest(p, points, ptnbr);
	struct point c = midpoint(p,q);
	ptnbr = circleremoval(&c, distcarree(&c,p), points, ptnbr);

	while (ptnbr > 0) {
		c = barycentre(&c, hypot(c.x - p->x, c.y - p->y), points);
		ptnbr = circleremoval(&c, distcarree(&c,points), points, ptnbr);
	}

	clock_t end = clock();

	double time = (double)(end - start) / CLOCKS_PER_SEC; 

	printf("%f\n", time);
	printf("%lf %lf %lf\n", c.x, c.y, hypot(c.x - p->x, c.y - p->y));

	free(points);

	return 0;
}

double
distcarree(struct point *p1, struct point *p2)
{
	return (p1->x - p2->x)*(p1->x - p2->x) +
		(p1->y - p2->y)*(p1->y - p2->y);
}

struct point
midpoint(struct point *p1, struct point *p2)
{
	struct point temp = {
		(p1->x + p2->x)/2,
		(p1->y + p2->y)/2,
	};

	return temp;
}

struct point *
furthest(struct point *ref, struct point *set, long int size)
{
	struct point *temp = ref;

	for (int i = 0; i < size; ++i) {
		if (distcarree(ref, set+i) > distcarree(ref, temp))
			temp = set+i;
	}

	return temp;
}

long int
circleremoval(struct point *center, double radiussq, struct point *points,
	      long int size)
{
	long int mptnbr = 0;

	for (int i = 0 ; i < size ; ++i) {
		if ((distcarree(center, points + i)) > radiussq) {
			*(points + mptnbr) = *(points + i);
			++mptnbr;
		}
	}

	return mptnbr;
}

struct point
barycentre(struct point *center, double radius, struct point *outlier)
{
	double co = hypot(center->x - outlier->x, center->y - outlier->y);

	struct point temp = {
		(center->x * (co + radius) / (2 * co)) +
		(outlier->x * (co - radius) / (2 * co)),
		(center->y * (co + radius) / (2 * co)) +
		(outlier->y * (co - radius) / (2 * co))
	};

	return temp;
}
