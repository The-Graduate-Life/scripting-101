#!/usr/bin/env bash
# 02_variables_args.sh — variables, quoting, positional arguments, arithmetic, exit codes.
#
# Usage: ./02_variables_args.sh NAME [REPEAT]
# Example: ./02_variables_args.sh "Ada Lovelace" 3

# $# = number of arguments. Stop with a helpful message if NAME is missing.
if [[ $# -lt 1 ]]; then
    echo "Usage: $0 NAME [REPEAT]" >&2
    exit 1                           # non-zero exit code = failure
fi

name=$1                              # no spaces around '=' !
repeat=${2:-2}                       # default value of 2 if $2 is empty/unset

# validate that REPEAT is a positive integer using a regular expression
if ! [[ $repeat =~ ^[0-9]+$ ]] || (( repeat == 0 )); then
    echo "Error: REPEAT must be a positive integer, got '$repeat'" >&2
    exit 2
fi

for (( i = 1; i <= repeat; i++ )); do
    echo "[$i/$repeat] Hello, $name"   # double quotes keep "Ada Lovelace" as ONE word
done

total=$(( repeat * ${#name} ))      # arithmetic expansion and string length
echo "Printed ${#name} characters x $repeat times = $total characters"
echo 'Single quotes are literal: $name is not expanded here'
exit 0
