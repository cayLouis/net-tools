import minimumTFTP

def tftpserver(dir):
    tftpServer = Server(dir)
    tftpServer.run()

if __name__ == "__main__":
    tftpserver("/root")
