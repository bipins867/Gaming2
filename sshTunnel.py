import MySQLdb
import sshtunnel
import mysql.connector 
sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

def genMdb():
    with sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
        ssh_username='bipins8671', ssh_password='Bipin@867',
        remote_bind_address=('bipins8671.mysql.pythonanywhere-services.com', 3306)
    ) as tunnel:
        print(tunnel.local_bind_port)
        mydb=MySQLdb.connect(
            host='127.0.0.1',
            db='bipins8671$GamingWorld',
            user='bipins8671',
            passwd='shivangisingh',
            port=tunnel.local_bind_port,
            #charset='utf8'
            )
        print("OKay")
        # Do stuff
        #mydb.close()
        return mydb
tun=sshtunnel.SSHTunnelForwarder(('ssh.pythonanywhere.com'),
                                 ssh_username='bipins8671',
                                 ssh_password='Bipin@867',
                                 remote_bind_address=('bipins8671.mysql.pythonanywhere-services.com', 3306),
                                 )
tunn.start()

mydb=MySQLdb.connect(
            host='127.0.0.1',
            db='bipins8671$GamingWorld',
            user='bipins8671',
            passwd='shivangisingh',
            port=tun.local_bind_port,
            #charset='utf8'
            )
