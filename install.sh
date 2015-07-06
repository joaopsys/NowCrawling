#!/bin/bash
if [ -z "$1" ]
  then
	PREFIX=/usr/bin
  else
	PREFIX=$1
fi
cp nowcrawling.py nowcrawling $PREFIX
chmod +x $PREFIX/nowcrawling
