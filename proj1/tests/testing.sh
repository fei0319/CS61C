#!/bin/bash

file='all_tests.txt'
all_text=`cat $file`
text_len="$(wc -w <<< $all_text)"
#echo "$text_len"

if [ $text_len -eq 0 ]
then
    echo "No tests to run"
else
    count=1
    while read -ra line; 
    do
        check=${#line[@]}
        if [ $check -ne 0 ] && [ $check -ne 3 ]
        then
            echo "Incorrect number of arguments for test $count"
        elif [ $check -ne 0 ]
        then
            dict="${line[0]}"
            #echo "$dict"
            inp="${line[1]}"
            #echo "$inp"
            ref="${line[2]}"
            #echo "$ref"
            test_name="$(cut -d'/' -f1 <<<"$dict")"
            echo "$test_name"
            out_name="$test_name/$test_name.out"
            #echo "$out_name"

            touch $out_name
            rm $out_name
            echo "================Running Program...================="
            cat $inp | ../philphix $dict > $out_name
            echo "================Program Finished!=================="
            echo ""
            echo "Difference between test output and reference output"
            echo "---------------------------------------------------"
            diff $out_name $ref && echo "------------------Test $count: $test_name Passed!--------------------" || echo "------------------Test $count: $test_name Failed!--------------------"
            
            echo
            echo
            count=`expr $count \+ 1`
        fi
    done < $file
fi
