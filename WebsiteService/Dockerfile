FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3005

#RUN apt-get update && apt-get upgrade -y && apt-get install -y nmap net-tools netcat
CMD [ "python", "./run.py", "&" ]
#CMD [ "bash", "./hs100.sh", "-i 192.168.8.106", "check" ]
#CMD [ "ping -c 3 192.168.8.106" ]
