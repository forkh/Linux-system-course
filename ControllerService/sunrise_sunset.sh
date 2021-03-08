#!/bin/bash --

# Credits to Yr:
# «Weather forecast from Yr, delivered by the Norwegian Meteorological Institute and NRK» (english).
# Website: https://www.yr.no/

# Script that fetches sunrise, sunset and various other data from the norwegian weather service Yr.no

# Base URL:
YR_URL='https://api.met.no/weatherapi/sunrise/2.0/.json?lat=62.011667&lon=-6.7675&date='

# Timezone offset:
OFFSET='&offset=+00:00'

# Getting the next date:
NEXT_DATE=$(date -d 'tomorrow' +%Y-%m-%d)

# Full link:
FULL_LINK="$YR_URL$NEXT_DATE$OFFSET"

# Options:
OPTIONS='-X GET'

# Fetching the data:
JSON=$(curl $OPTIONS $FULL_LINK)

# JSON filename
#OUTPUT_FILE=$NEXT_DATE.json

# Saving data to JSON file:
#echo $JSON > $OUTPUT_FILE
#echo $JSON
# Sunset part:
SUNSET=$(echo $JSON | jq '.location.time[0].sunset.time')
_TIME=$(echo $SUNSET |grep -oP '(\d{2}:\d{2})' | head -1)
_DATE=$(echo $SUNSET |grep -oP '(\d{4}-\d{2}-\d{2})')
read _YEAR _MONTH _DAY <<< $( echo "$_DATE" | awk '{split($0,a,"-"); print a[1],a[2],a[3]}' )
DATE_CORRECT_FORMAT="$_DAY.$_MONTH.$_YEAR"

# Send web request to create sunrise and sunset timer for next day.
TIMER_URL="http://192.168.8.241:3001/create"
FEEDBACK=$(curl --data "alias=7E&time=$_TIME&date=$DATE_CORRECT_FORMAT&status=on&comment=Sunset&deletable=1" $TIMER_URL)
echo $FEEDBACK

# Sunrise part:
SUNRISE=$(echo "$JSON" | jq '.location.time[0].sunrise.time')
_TIME=$(echo $SUNRISE |grep -oP '(\d{2}:\d{2})' | head -1)
_DATE=$(echo $SUNRISE |grep -oP '(\d{4}-\d{2}-\d{2})')
read _YEAR _MONTH _DAY <<< $( echo "$_DATE" | awk '{split($0,a,"-"); print a[1],a[2],a[3]}' )
DATE_CORRECT_FORMAT="$_DAY.$_MONTH.$_YEAR"

# Send web request to create sunrise and sunset timer for next day.
TIMER_URL="http://192.168.8.241:3001/create"
FEEDBACK=$(curl --data "alias=7E&time=$_TIME&date=$DATE_CORRECT_FORMAT&status=off&comment=Sunrise&deletable=1" $TIMER_URL)
echo $FEEDBACK
