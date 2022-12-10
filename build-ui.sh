#!/usr/bin/env bash
echo "- generating ui scripts"

for ui in $(find src/main/python/presentation/ui/ -name "*.ui");
do
    echo "-- $ui > ${ui/.ui/.py}"
    pyuic6 ${ui} -o ${ui/.ui/.py}
done