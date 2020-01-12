CC=gcc

all: executables/graham executables/tripixel executables/ritter

executables/ritter: src/ritter.c
	$(CC) $< -lm -o $@ 

executables/%: src/%.c 
	$(CC) $< -o $@ 
