CC=gcc
COMPILEFLAGS=-O2 -Wall -lm

all: executables/graham executables/tripixel executables/ritter

executables/%: src/%.c 
	$(CC) $(COMPILEFLAGS) $< -o $@ 
