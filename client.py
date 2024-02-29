
import socket

CONNECT=1
LIST=2
PLAY=3
EXIT=4
SHUTDOWN=5
VOLUME=6



done=False



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect(("127.0.0.1", 1337))
except:
    exit("server not connected\n"
         "you probably forgot to turn it on")

#sends an int coverted into bytes
def send(cmd):
    sig=cmd.to_bytes(4,"big")
    sock.send(sig)

send(CONNECT)#initial connect
res = sock.recv(4096)
print(res.decode("ascii"))#first server response on connect

def printResponse():
    try:
        res=sock.recv(4096)
    except:
        res="No Response".encode("ascii")
    print(res.decode("ascii"))

while(not done):
    print("1.\tList Songs\n"
          "2.\tPlay song\n"
          "3.\tSet Volume\n"
          "4.\tExit\n"
          "5.\tShutdown")
    
    cmd=input("Enter command: ")
    if(cmd.isdigit()):
        if(cmd=="1"):
            send(LIST)
            print("list\n")
        elif(cmd=="2"):
            send(PLAY)
            song=input("Which Song?\n")
            sock.send(song.encode("ascii"))
            res=""
        elif(cmd=="3"):
            send(VOLUME)
            printResponse()
            v=input("Set Volume: ")
            while(not v.isdigit()):v=input("Set Volume: ")
            v=int(v)
            if(v > 10):v=10
            if(v<0): v=0
            print("sending over volume")
            send(v)

        elif(cmd=="4"):
            send(EXIT)
            done=True
        elif(cmd=="5"):
            send(SHUTDOWN)
            done=True
        printResponse()

                
    else:
        print("not digit")
    



sock.close()