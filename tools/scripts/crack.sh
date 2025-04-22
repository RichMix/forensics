#! /usr/bin/env bash

hashfile='hashes.txt' #Hashes for the challenge
wordlist='fullDictUniformWords.lst' #Default wordlist
wordlist_digit='fullDictUniformWords_d.lst' #Wordlist masked with ?d
specialFile='specialHexcodes.lst' #Possible special chars


for i in {1..10} #change 10 to number of special chars to try
do
        special=$(cat $specialFile | head -n$i | tail -1)

        #Type 4
        #liber8_word#_word
        hashcat -m 0 -a 1 -d 1 -w 3 -j "^$special ^8 ^r ^e ^b ^i ^l" -k "^$special" $hashfile $wordlist_digit $wordlist

        #word#_liber8_word
        hashcat -m 0 -a 1 -d 1 -w 3 -j "\$$special \$l \$i \$b \$e \$r \$8 \$$special" $hashfile $wordlist_digit $wordlist

        #word#_word_liber8
        hashcat -m 0 -a 1 -d 1 -w 3 -j "\$$special" -k "\$$special \$l \$i \$b \$e \$r \$8" $hashfile $wordlist_digit $wordlist

        #liber8_word_word#
        hashcat -m 0 -a 1 -d 1 -w 3 -j "^$special ^8 ^r ^e ^b ^i ^l" -k "^$special" $hashfile $wordlist $wordlist_digit

        #word_liber8_word#
        hashcat -m 0 -a 1 -d 1 -w 3 -j "\$$special \$l \$i \$b \$e \$r \$8 \$$special" $hashfile $wordlist $wordlist_digit

        #word_word#_liber8
        hashcat -m 0 -a 1 -d 1 -w 3 -j "\$$special" -k "\$$special \$l \$i \$b \$e \$r \$8" $hashfile $wordlist $wordlist_digit


        #Types 1+2+3
        #liber8_word_word
        hashcat -m 0 -a 1 -d 1 -w 3 -j "^$special ^8 ^r ^e ^b ^i ^l" -k "^$special" $hashfile $wordlist $wordlist

        #word_liber8_word
        hashcat -m 0 -a 1 -d 1 -w 3 -j "\$$special \$l \$i \$b \$e \$r \$8 \$$special" $hashfile $wordlist $wordlist

        #word_word_liber8
        hashcat -m 0 -a 1 -d 1 -w 3 -j "\$$special" -k "\$$special \$l \$i \$b \$e \$r \$8" $hashfile $wordlist $wordlist
done
