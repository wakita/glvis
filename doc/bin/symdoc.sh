#!/bin/sh

sympy=$1
md=`echo $sympy | sed -e 's|glvis|glvis/doc/note|' -e 's|\.py$|.md|'`

mkdir -p `dirname $md`

python $sympy
