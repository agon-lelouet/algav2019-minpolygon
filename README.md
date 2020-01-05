# Objective

Implementation of the AKL-Toussaint and Ritter algorithm (minimum polygons) for [this college project](https://www-apr.lip6.fr/~buixuan/files/algav2019/projet_indiv2.pdf) (Sorbonne university, Master of Computer Science, 2019)

# HOW TO

For a first run on a Linux system : 
- ensure you have python3 installed
- run the initialize.sh file
- And then `python3 src/main.py` to run the project.

# Preparations

The utilities assume a POSIX-compliant system.

The implementation of the pixel cleaning and the Graham quickhull scan are made in C99.

You need a C compiler, and any implementation of the C standard library :

``` shell
gcc -Wall -O2 tripixel.c -lm -o tripixel
gcc -Wall -O2 graham.c -lm -o graham
```

The tripixel and the graham utilities can only read from standard input, and only write to standard output.

The tripixel utility only works if the entries with same reference coordinate are adjacent.

The graham utility assumes that the entry with the lowest y coordinate (the leftmost of them if there are several) is the first entry, and assume one point per line, x then y, separated by a space. The parser won't work otherwise.

The following POSIX shell command should prepare everything correctly :

``` shell
cat $input | sort -S 80% --parallel=8 -n -s -k1,1 | uniq | /path/to/tripixel | awk '{print $2, $1}' | sort -S 80% --parallel=8 -n -s -k1,1 | /path/to/tripixel | awk '{print $2, $1}' > cleandata
```

The following command should print the convex hull to standard output, one point per line (CW) :

``` shell
cat $cleandata | /path/to/graham "$(wc -l $cleandata | awk '{print $1}')"
```

You will need of course the following unix commands :
- sort (GNU version preferably, remove -S and --parallel option if non-GNU)
- uniq
- awk
- cat
- wc

All these commands are supposed to be installed on a POSIX system.

