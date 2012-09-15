#!/bin/bash

#first is the training, second is the validation, third is the iterations, fourth is the nodefile, fifth is the datadir

for i in $(cat $1 | wc -l)
do
   awk 'NR=='$i $1 | tr "," "\n" | python makegraph.py $4 $5 $(awk 'NR=='$i'{print $1}' $2) $3
done