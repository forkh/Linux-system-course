#!/bin/bash --

# Database path
DB="/home/rkh/docker/ControllerService_production/timers.db"

# Timer Delete URL
TIMER_DELETE_URL="http://192.168.8.241:3001/remove/"

# Getting all the timers
timers="$(
    sqlite3 /home/rkh/docker/ControllerService_production/timers.db \
        'SELECT time,date,deletable,tid FROM timers' \
    )"

# Getting the current time in timestamp form
CURTS=$(date +'%s')

# Looping through all the timers
for timer in $timers; do
    # Getting data into variables
    read _tid _deletable _date _time <<< $( echo "$timer" | awk '{split($0,a,"|"); print a[4],a[3],a[2],a[1]}' )
    # Checking if the timer is deletable
    if [ "$_deletable" != "0" ]; then
        # Reformatting date and time into proper format
        read _year _month _day <<< $( echo "$_date" | awk '{split($0,a,"."); print a[3],a[2],a[1]}' )
        read _minute _hour <<< $( echo "$_time" | awk '{split($0,a,":"); print a[2],a[1]}' )
        # Converting to timestamps
        TS="$_year-$_month-$_day""T""$_hour:$_minute:00Z"
        TZ=$(date --date "$TS" +'%s')
        # Checking if the timer is in the future or in the past.
        if [[ $TZ -lt $CURTS ]]; then
            # If the timer is in the past, delete it.
            curl -X GET $TIMER_DELETE_URL$_tid
        fi 
    fi
done

