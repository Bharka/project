import socket,os,sys,json,base64

#API code:


def GETServer(serverList,conn):
    with open(serverList) as i:
        msg=json.load(i)
    response_headers = {
        'Content-Type': 'application/json',
        'Content-Length': len(msg),
        'Connection': 'close',
    }
    response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())
    response_proto = 'HTTP/1.1'
    response_status = '200'
    response_status_text = 'OK' # this can be random
    # sending all this stuff
    r = '%s %s %s' % (response_proto, response_status, response_status_text)
    conn.send(r)
    conn.send(response_headers_raw)
    conn.send('\r\n') # to separate headers from body
    servers_Array=msg['Servers']
    print("thois is array",servers_Array)
    sendingString="["
    for x in range(0,len(servers_Array)):
        sendingString+='{host:'+servers_Array[x]['host']+','+'port:'+str(servers_Array[x]['port'])+'}'
        if(x!=len(servers_Array)-1):
            sendingString+=','
    sendingString+=']'
    conn.send(json.dumps({"Servers":sendingString}))
    conn.close()
    
# send data to each server 
def eachServer(host,port,filejson):
    new_socket=socket.socket();
    new_socket.connect((host,int(port)))
    serverCommunication=json.dumps(filejson);
    new_socket.send(serverCommunication)
    print "Done Sending"
    new_socket.close();

def allServers(filejson):
    list_ofServers=sys.argv[1];
    with open(sys.argv[1]) as i:
        data=json.load(i)
        print(data)
    for x in range(0,len(data['Servers'][0])):
        a=data['Servers'][x]['host'];
        eachServer(data['Servers'][x]['host'],data['Servers'][x]['port'],filejson);

s=socket.socket();
port = 7772
host = ''                     
print host;
try:
    s.bind((host, port))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
s.listen(5)
while True:
    filename=""
    conn, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    getting_data=""
    data=conn.recv(1024)
    data1=data.split('\n')
    for x in range (0,len(data1)-1):
        print(data1[x]);
    find_url=data1[0].split(' ')
    #print((urlFind[1])[1:]);
    #print("request completed"); 
    #print (data1[len(data1)-1])   
    #Server API 
    if(str(data1[0]).find('GET')!=-1 and ((find_url[1])[1:]).find('serversDetails')!=-1):
        #print "in get request with url "+(urlFind[1])[1:]
        serversFile=sys.argv[1]
        with open(sys.argv[1]) as i:
            data=json.load(i)
            print(data)
        GETServer(serversFile,c)
        #c,addr =s.accept()
    elif(str(data1[0]).find('POST')!=-1 and ((find_url[1])[1:]).find('setServerDetails')!=-1):
        print("post data is ")
        jsonDataPost=data1[len(data1)-1]
        value_we_got=json.loads(jsonDataPost)
        print("Value is ",value_we_got)
        postRequestArray=value_we_got['Servers']
        serversFile=sys.argv[1]
        with open(serversFile) as i:
            msg=json.load(i)
        servers_Array=msg['Servers']
        print("Server array is ",servers_Array)
        print("POSTTTT array is ",postRequestArray)
        for x in range(0,len(servers_Array)):
            servers_Array[x]['host']=postRequestArray[x]['host']
            servers_Array[x]['port']=postRequestArray[x]['port']
        msg['Servers']=servers_Array
        print("the final msg is ",msg)
        f = open(sys.argv[1],'wb')
        f.write(json.dumps(msg))
        f.close()
        conn.send("Values Changed");
        conn.close();
    elif(data.find('clientUpload')!=-1):
        while(data!=""):
            print("in while loop data is ",data)
            getting_data+=data
            data=c.recv(1024)
        print ("the data which we got is ",getting_data)
        JsonData=json.loads(getting_data)
        print("this Json data",JsonData)
        if(JsonData['Type']=='clientUpload'): 
            f = open(JsonData['Data']['Name'],'wb')
            f.write(base64.b64decode(JsonData['Data']['data']))
            f.close()
            print "Done Receiving"
            conn.send('Thank you for connecting')
            conn.close()
            JsonData['Type']='serverSend'
            allServers(JsonData);
    elif(data.find('serverSend')!=-1):
        while(data!=""):
            print("in while loop data is ",data)
            getting_data+=data
            data=conn.recv(1024)
        print ("the data which we got is ",getting_data)
        JsonData=json.loads(getting_data)
        print("this Json data",JsonData)
        if(JsonData['Type']=='serverSend'): 
            f = open(JsonData['Data']['Name'],'wb')
            f.write(base64.b64decode(JsonData['Data']['data']))
            f.close()
            print "Done Receiving"
            conn.send('Thank you for connecting')
            conn.close()
    else:
        conn.send("Bad Request")
        conn.close();

    
    