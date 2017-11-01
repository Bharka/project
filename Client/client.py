import socket,ftplib,sys,base64,json
port = 7770
host = '18.216.86.74'#'127.0.0.1'#socket.gethostname()

s=socket.socket();
# inital server connection STARTTTTTTTTTTTTTTTTTTT
s.connect((host,port))
print "socket created"
filename=sys.argv[1]
size = bytes(len(filename));
f = open(filename,'rb')
b64Data=""
l = f.read(1024)
while (l):
    b64Data+=base64.b64encode(l)
    l = f.read(1024)
f.close()
JsonOfFile=json.dumps({"Type":"clientUpload","Data":{"Name":filename,"size":size,"data":b64Data}});
s.send(JsonOfFile)
print JsonOfFile
s.close() # Close the socket when done
# inital server connection ENDDDDDDDDDDDDDDDDDDDD
#s.shutdown(socket.SHUT_WR)
#new connection to proxy 
# new_port=21617
# s.connect((host,new_port)) 
# print "socket created"
# if(sys.argv[1]=="get"):
# 	print ("fle name to downoad",sys.argv[2])
# 	JsonGet=json.dumps({"Type":"get","Data":{"Name":sys.argv[2]}});
# 	s.send(JsonGet)
# else:
# 	filename=sys.argv[1]
# 	size = bytes(len(filename));
# 	f = open(filename,'rb')
# 	b64Data=""
# 	l = f.read(1024)
# 	while (l):
# 	    b64Data+=base64.b64encode(l)
# 	    l = f.read(1024)
# 	f.close()
# 	JsonOfFile=json.dumps({"Type":"post","Data":{"Name":filename,"size":size,"data":b64Data}});
# 	s.send(JsonOfFile)
# 	print JsonOfFile
# s.close()        
        
