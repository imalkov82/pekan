#!/usr/bin/env bash
echo 'PEKAN START'
echo $@
python2.7 pekan.py $@ 1>&2
