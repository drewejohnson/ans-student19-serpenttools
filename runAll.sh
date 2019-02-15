#!/bin/bash
# Run all input files

START="$(pwd)"
FILES=(simple det/det dep/dep history/hist sens/sens)
SSS2_OPTS="-noplot -omp 2"

if [ -z $SSS2_EXE ]; then
    echo "Export SSS2_EXE variable"
    exit 1
fi

if [ -z $SERPENT_DATA ]; then
    echo "Export SERPENT_DATA variable"
    exit 1
fi

echo $START

for ff in ${FILES[*]}; do
    echo $ff
    cd $(dirname $ff)
    
    $SSS2_EXE $SSS2_OPTS $(basename $ff)

    cd $START
done
