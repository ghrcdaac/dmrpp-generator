#!/bin/bash
for file in *.nc
do
dmrpp_file="${file}.dmrpp"
get_dmrpp -b `pwd` -o "${dmrpp_file}" -u "file://"`pwd`"/${file}" "${file}"
done
