#!/bin/sh

set -e

if [ "$1" = "--initialize" ]; then
    # symbolic links to ephemeral student submission files in /speller_workspace
    ln -sf -T "/$SPELLER_WS/_dictionary.c" "/$SPELLER/dictionary.c"
    ln -sf -T "/$SPELLER_WS/_dictionary.h" "/$SPELLER/dictionary.h"
    
    # symbolic link to version of speller.c we will be using
    ln -sf -T "/$SPELLER_WS/$SPELLER_C_FILENAME" "/$SPELLER/speller.c"

    # compile benchmark version of dictionary.c -- we only need to do this once at initialization
    ln -sf -T "/$SPELLER_WS/$DICTIONARY_H_FILENAME" "/$SPELLER_WS/_dictionary.h"
    ln -sf -T "/$SPELLER_WS/$DICTIONARY_C_BENCHMARK_FILENAME" "/$SPELLER/$DICTIONARY_C_BENCHMARK_FILENAME"

    cd "/$SPELLER"

    echo "Compiling benchmark executable..."

    clang   -ggdb3 -gdwarf-4 -O0 -Qunused-arguments -std=c11 -Wall -Werror              \
            -Wextra -Wno-gnu-folding-constant -Wno-sign-compare -Wno-unused-parameter   \
            -Wno-unused-variable -Wshadow -c -o speller.o speller.c                     

    clang   -ggdb3 -gdwarf-4 -O0 -Qunused-arguments -std=c11 -Wall -Werror              \
            -Wextra -Wno-gnu-folding-constant -Wno-sign-compare -Wno-unused-parameter   \
            -Wno-unused-variable -Wshadow -c -o                                         \
            benchmark_dictionary.o "$DICTIONARY_C_BENCHMARK_FILENAME"

    clang   -ggdb3 -gdwarf-4 -O0 -Qunused-arguments -std=c11 -Wall -Werror              \
            -Wextra -Wno-gnu-folding-constant -Wno-sign-compare -Wno-unused-parameter   \
            -Wno-unused-variable -Wshadow -o                                            \
            $BENCHMARK_EXECUTABLE benchmark_dictionary.o speller.o -lm

    echo "Success: initialized symbolic links and compiled benchmark executable"
elif [ "$1" = "--compile-submission" ]; then
    cd /"$SPELLER"

    # Use CS50 Makefile, but make sure everything is recompiled for each submission
    make -B
fi
#     ./speller [-i iters] [-d dictionary] [-s signature] texts/holmes.txt

#     echo "Benchmark:"
#     ./$BENCHMARK_EXECUTABLE 5 texts/holmes.txt