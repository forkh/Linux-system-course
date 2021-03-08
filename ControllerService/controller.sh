#!/bin/bash --

DEVICE_API_ADDRESS='http://192.168.8.241:3000'

HS100_LOCATION='/home/rkh/docker/ControllerService_production/hs100/hs100.sh'

timers="$(
    sqlite3 /home/rkh/docker/ControllerService_production/timers.db \
        'SELECT alias,time,date,status FROM timers' \
    )"

CURTIME=$(date +%H:%M)
CURDATE=$(date +%d.%m.%Y)

echo "Current time: $CURTIME - $CURDATE"

for timer in $timers; do
    echo "$timer"
    read _option _date _time _device <<< $( echo "$timer" | awk '{split($0,a,"|"); print a[4],a[3],a[2],a[1]}' )
    echo "_option: $_option | _date: $_date | _time: $_time | _device: $_device"
    echo "Timer time: $_time - $_date"
    if [ "$CURTIME" = "$_time" ] && [ "$_date" = "." ]; then
        IP=$(curl -X GET "$DEVICE_API_ADDRESS/ip/$_device")
        cmd="$HS100_LOCATION -i $IP $_option"
        eval $cmd
        echo "$cmd"
    elif [ "$CURTIME" = "$_time" ] && [ "$CURDATE" = "$_date" ]; then
        IP=$(curl -X GET "$DEVICE_API_ADDRESS/ip/$_device")
        cmd="$HS100_LOCATION -i $IP $_option"
        eval $cmd
        echo "$cmd"
    fi
done
