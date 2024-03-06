#!/bin/bash

echo "Hey"
   echo "Ho"



function what_a_way() {
  echo "For us to go"
}


what_a_way

content=$(cat ./dmrpp_generator/version.py)
[[ $content =~ ([0-9]+.[0-9]+.[0-9]+) ]]

echo "${BASH_REMATCH[1]}"