#!/bin/bash
# flip position $1 of the witness; print pos, grower mono5 count, direct mono5 count
i=$1; d=$(mktemp -d); W=submitted/k5_w1513.txt
tr -cd '01' < $W | python3 -c "import sys; s=list(sys.stdin.read()); i=$i-1; s[i]='1' if s[i]=='0' else '0'; print(''.join(s))" > $d/f.txt
g=$(checks/fs_grow $d/f.txt 5 | awk '/j=5/{split($3,a,"=");split($4,b,"=");print a[2]+b[2]}')
x=$(checks/fs5_direct $d/f.txt | awk '/mono5/{split($3,a,"=");split($4,b,"=");print a[2]+b[2]}')
echo -e "$i\t$g\t$x"; rm -rf $d
