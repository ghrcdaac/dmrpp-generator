content=$(cat dmrpp_generator/version.py)
[[ $content =~ ([0-9]+.[0-9]+.[0-9]+) ]]
echo "${BASH_REMATCH[1]}"