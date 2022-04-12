##!/bin/bash
to_remove=($(find ./results -maxdepth 1 -type d))

for i in "${to_remove[@]}"
do
    if [ "$i" = "./results" ] || [ "$i" = "./results/implemented.md" ]; then
        continue
    else
        rm -r "$i"
    fi
done
