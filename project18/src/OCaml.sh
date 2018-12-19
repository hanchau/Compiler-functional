#!/bin/sh
bin/irgen $1 > comp_files/tac.ir
bin/codegen comp_files/tac.ir > comp_files/assem.s
sed -i '/%:/d' comp_files/assem.s
sed -i '/=:/d' comp_files/assem.s
sed -i '/^$/d' comp_files/assem.s
gcc -o assem -m32 comp_files/assem.s
