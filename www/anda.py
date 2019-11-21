
import subprocess
import os
import signal
import time
import re

songs = []
for root, folders, files in os.walk("songs/"):
    folders.sort()
    files.sort()
    for filename in files:
        if re.search(".(wav)$", filename) != None:
            songs.append(filename)

print(songs)
print(len(songs))
k=0
iniciado=0

while(True):
    f = open("comunicar.txt", "r")
    signal=f.read()
    f.close()
    if((signal=="Iniciar") and (iniciado==0)):
        print("Iniciar")
        cmd = "/home/pi/SpaceFM/www/fm_transmitter -f 87.5 /home/pi/SpaceFM/www/songs/"+songs[k]
        #cmd = "fm_transmitter -f 87.5 songs
        pwd = "raspberry"
        print(cmd)
        p=subprocess.Popen('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)
        #print("fin proceso")
        iniciado=1
        k=k+1
        print("Fin Iniciar")

    elif((signal == "Detener") and (iniciado==1)):
        print("Detener")
        f = open("detenertransmision.txt", "w")
        f.write("d")
        f.close()
        iniciado=0
        print("Fin Detener")

    elif((signal == "Siguiente") and (iniciado==1)):
        print("Siguiente")
        if(k==len(songs)):
            k=0
        cmd = "/home/pi/SpaceFM/www/fm_transmitter -f 87.5 /home/pi/SpaceFM/www/songs/"+songs[k]
        pwd = "raspberry"
        p=subprocess.Popen('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)
        f = open("comunicar.txt", "w")
        f.write("Nada")
        f.close()
        k=k+1
        print("Fin Siguiente k:",k)
    elif(iniciado==1):#Esta Reproduciendo

        f = open("fintransmision.txt", "r")
        signalTransmitter=f.read()
        f.close()
        if(signalTransmitter=="fin"):
            print("Inicio Reproduciendo")

            if(k==len(songs)):
                k=0
            cmd = "/home/pi/SpaceFM/www/fm_transmitter -f 87.5 /home/pi/SpaceFM/www/songs/"+songs[k]
            pwd = "raspberry"
            p=subprocess.Popen('echo {} | sudo -S {}'.format(pwd, cmd),preexec_fn=os.setsid, shell=True)
            k=k+1
            print("Fin Reproduciendo")

    #print(signal)
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
