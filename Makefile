CC=gcc
COMPILEFLAGS=-O0 -g3 -Wall -c

all: executables/graham executables/tripixel

executables/%: objects/%.o 
	$(CC) $^ -o $@

objects/%.o : src/%.c
	$(CC) $(COMPILEFLAGS) -o $@ $<