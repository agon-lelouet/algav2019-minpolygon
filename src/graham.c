#include <stdio.h>
#include <stdlib.h>

struct point {
	int x;
	int y;
};

struct pointc {
	int x;
	int y;
	struct pointc *next;
};

struct point pref;

int distcarree(struct point *p1, struct point *p2);
int orientation(struct point *p1, struct point *p2, struct point *p3);
void echange(struct point *p1, struct point *p2);
int comparaison(const void *vp1, const void *vp2);
struct pointc *empiler(struct point *ptr, struct pointc *tete);
struct pointc *depiler(struct pointc *tete);
void imprimerpile(struct pointc *tete);

int main(int argc, char *argv[])
{
	if (argc < 2) return 22;

	long int ptnbr = strtol(argv[1], NULL, 10);

	struct point *points = malloc(ptnbr * sizeof(struct point));

	for (int i = 0; i < ptnbr ; i++) {
		scanf("%d %d", &((points+i)->x), &((points+i)->y));
	}

	pref = *points;

	qsort(points+1, ptnbr-1, sizeof(struct point), comparaison);

	long int mptnbr = 1;

	for (int i = 1; i < ptnbr; ++i) {
		while ((i < ptnbr-1) && (!orientation(&pref,points+i,points+i+1)))
			++i;
		*(points+mptnbr) = *(points+i);
		++mptnbr;
	}

	if (mptnbr < 3) return 1;

	struct pointc *head = NULL;

	head = empiler(points, head);
	head = empiler(points+1, head);
	head = empiler(points+2, head);

	for (int i = 3; i < mptnbr; ++i) {

		while (orientation((struct point *)head->next, (struct point *)head, points+i) != 2)
			head = depiler(head);

		head = empiler(points + i, head);
	}

	imprimerpile(head);

	free(points);
	return 0;
}

int
distcarree(struct point *p1, struct point *p2)
{
	return (p1->x - p2->x)*(p1->x - p2->x) +
		(p1->y - p2->y)*(p1->y - p2->y);
}

int
orientation(struct point *p1, struct point *p2, struct point *p3)
{
	int val = (p2->y - p1->y) * (p3->x - p2->x) -
		(p2->x - p1->x) * (p3->y - p2->y);

	if (val == 0) return 0;
	if (val > 0) return 1;
	return 2;
}

void
echange(struct point *p1, struct point *p2)
{
	struct point temp = *p1;
	*p1 = *p2;
	*p2 = temp;
}

int
comparaison(const void *vp1, const void *vp2)
{
	struct point *p1 = (struct point *)vp1;
	struct point *p2 = (struct point *)vp2;

	int o = orientation(&pref, p1, p2);

	if (o == 0) return (distcarree(&pref, p2) >= distcarree(&pref, p1))? -1 : 1;
	return (o == 2)? -1: 1;
}

struct pointc *
empiler(struct point *ptr, struct pointc *tete)
{
	struct pointc *noeud = malloc(sizeof(struct pointc));
	noeud->next = tete;
	noeud->x = ptr->x;
	noeud->y = ptr->y;

	return noeud;
}

struct pointc *
depiler(struct pointc *tete)
{
	if (tete == NULL) return NULL;
	struct pointc *temp = tete->next;
	free(tete);
	return temp;
}

void
imprimerpile(struct pointc *tete)
{
	for (; tete != NULL; tete=tete->next) {
		printf("%d %d\n", tete->x, tete->y);
	}
}
