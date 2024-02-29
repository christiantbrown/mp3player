import socket
import os

#SIGNALS
#commands are 4 bytes, big endian

CONNECT=1
LIST=2
PLAY=3
EXIT=4
SHUTDOWN=5
VOLUME=6

songs={}

#your music directory here

dir = 'Music'

#volume goes from 0-10

curVolume=3

#iterate over filenames and add mp3 and wav files to the list of songs
for filename in os.listdir(dir):
    f=os.path.join(dir, filename)
    if os.path.isfile(f):
        name, format = os.path.splitext(filename)
    #print(f"{name}, {format}")
    if format in (".mp3", ".wav"):
        songs[name]=f


#formatted string we send to client
songlist=""
for song in songs.keys():
    songlist += f"{song}\n"
print(songlist)

done=False




try:
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(("127.0.0.1", 1337))
    serv.listen(5)
    
    cli,_ = serv.accept()

    #i wish there were switch statements in python
    
    while (not done):
        command=int.from_bytes(cli.recv(4), "big")
        #greeting
        if(command==CONNECT):
            cli.send("HI".encode("ascii"))
            
        #send over the list of songs
        elif(command==LIST):
            cli.send(songlist.encode("ascii"))
        #send await a songname from client (in ascii), send response
        elif(command==PLAY):
            try:
                song=cli.recv(256).decode("ascii")
                #//TODO: actually play the mp3
                if(song  in songs.keys()):
                    res=f"playing {song}"
                else:
                    res=f"could not find {song}"    
            except:
                res=f"communication error, please send request again"
            cli.send(res.encode("ascii"))
        #send volume settings, await new volume
        elif(command==VOLUME):
            cli.send(f"Current Volume: {curVolume}\nSelect volume from 1-10".encode("ascii"))
            #client sends over new volume as bytes
            try: newVol=int.from_bytes(cli.recv(4),"big")
            except: newVol=curVolume
            curVolume=newVol
            #TODO: implement volume change
            cli.send(f"Current Volume: {curVolume}".encode("ascii"))
            
        #send bye message
        elif(command==EXIT):
            cli.send("Bye!".encode("ascii"))
        #remotely initiated shutdown
        elif(command==SHUTDOWN):
            cli.send("Shutting Down".encode("ascii"))
            print("Initiated Remote Shutdown")
            done=True
        #reset command or the loop will run again
        else:
            cli.send("Invalid Command".encode("ascii"))            
        command=0    
    cli.close()
    
    
except KeyboardInterrupt as e:
    serv.close()
    serv = None

finally:
    if serv is not None:
        serv.close()