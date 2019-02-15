#!/bin/bash
# Archive all matlab and coefficient files from runs

FILES=$(find . -name "*.m" -o -name "*.coe")
zip files.zip $FILES
tar -czf files.tgz $FILES
# sha256 and md5 sums
sha256sum files.zip files.tgz > files.sha256
md5sum files.zip files.tgz > files.md5
