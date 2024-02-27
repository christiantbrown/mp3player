
import socket


LIST=2
PLAY=3
EXIT=4
SHUTDOWN=5

done=False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect(("127.0.0.1", 1337))
except:
    exit("server not connected\n"
         "you probably forgot to turn it on")
def send(cmd):
    sig=cmd.to_bytes(4,"big")
    sock.send(sig)

send(1)#initial connect
res = sock.recv(4096)
print(res.decode("ascii"))#first server response on connect

while(not done):
    print("1.\tList Songs\n"
          "2.\tPlay song\n"
          "3.\tExit\n"
          "4.\tShutdown")
    
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
            send(EXIT)
            done=True
        elif(cmd=="4"):
            send(SHUTDOWN)
            done=True
        try:
            res=sock.recv(4096)
        except:
            res="No Response".encode("ascii")
        print(res.decode("ascii"))    

                
    else:
        print("not digit")
    



sock.close()