
import subprocess
import os
import signal
import time

iniciado=0

print(signal.SIGTERM)
print(signal.SIGKILL)
HOLA = signal.SIGTERM
CHAU = signal.SIGKILL

while(True):
    f = open("comunicar.txt", "r")
    signal=f.read()
    f.close()
    if((signal=="Iniciar") and (iniciado==0)):
        cmd = "/home/pi/SpaceFM/www/fm_transmitter -f 87.5 /home/pi/SpaceFM/www/heroe.wav"
        pwd = "raspberry"
        print("Iniciando proceso")
        p=subprocess.Popen('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True,   stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=-1)
        #print("fin proceso")
        iniciado=1
    elif((signal =="") and (iniciado==1)):
        print("matando proceso",p.pid)
        os.kill(p.pid,signal.CTRL_C_EVENT)
        #os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        #p.terminate()
        #p.send_signal(signal.SIGINT)


    else :
        pass
    print(signal)
    time.sleep(1)
print("fin programa")

#preexec_fn=os.setsid
#fpid = os.fork()
#fpid=0
#command = './home/pi/SpaceFM/www/fm_transmitter -f 87.5 /home/pi/SpaceFM/www/heroe.wav'.split()
#subprocess.Popen(command, shell=True)

#p=subprocess.Popen('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)

#print(p.pid)


"""
RUN apt-get update && apt-get -y install sudo
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
USER docker
CMD /bin/bash

FROM ubuntu:17.04



RUN apt-get update
RUN apt-get install sudo

RUN adduser --disabled-password --gecos '' admin
RUN adduser admin sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER admin




"""
