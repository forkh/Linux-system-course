FROM tiangolo/uwsgi-nginx-flask:python3.7
RUN apt-get update && apt-get upgrade -y && apt-get install -y bash vim
#WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#RUN apt-get update && apt-get upgrade -y && apt-get install -y nmap net-tools netcat
#CMD [ "python", "./run.py", "&" ]
#CMD [ "bash", "./hs100.sh", "-i 192.168.8.106", "check" ]
#CMD [ "ping -c 3 192.168.8.106" ]
