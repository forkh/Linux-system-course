

if [ "$(date +%H)" = "12" ]; then
    IP=$(curl -X GET "http://192.168.8.241:3000/ip/7e")
    echo "$IP"
    _status="on"
    cmd="/home/rkh/docker/ControllerService/hs100/hs100.sh -i $IP $_status"
    echo "$IP"
    eval $cmd
    #output=$(/home/rkh/docker/ControllerService/hs100/hs100.sh -i "$IP" "$_status")
    #echo "$output"
    #eval $cmd
fi
