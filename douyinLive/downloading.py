# 原 "抖音直播6_流程.ipynb" 
# =======================================================


# 浩宇種田
import socket
import ssl
 

''' 
[說明]
在抖音直播頁面按 F12，開啟chrome 的開發人員工具，點選 network，並以大小排序，最大檔案應該會是個 FLV，右鍵，取得它的連結，如下↓ 
https://pull-flv-l6.douyincdn.com/third/stream-115272286748803111_ld.flv?k=c0b666231386a922&t=1718297695&abr_pts=-800&_session_id=037-202406070054553F7678EA780D3E568164.1717692894909.58638

將 "https://"  去掉，第一節 ("pull-flv-l6.douyincdn.com") 取出來，作為 target_host， 剩餘部份作為要讓 socket send 的訊息中， GET 後面的部份。 

由於現今的網站都是 ssl 加密 (OSI 模型的第六層)， 因此傳送的訊息不會以明文的方式，而是要加密，而 https，在初始時會有類似 TCP 的三次交握，會交換一些訊息，包括網站方的CA評證(密碼學的東西，不是紙張)，以及RSA的密鑰等。 這些當然可以自己寫，由其是RSA的部份，但是CA的格式我暫且不熟，直接用套件吧。 

所以下述才會多了 "ssl wrap the socket" 那兩行，並換成用 client 來使用 send 功能(method) 等。 
''' 

target_host = "pull-flv-l6.douyincdn.com"
target_port = 443

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect the client
client.connect((target_host, target_port))

# ssl wrap the socket
context = ssl.create_default_context()
client = context.wrap_socket(client, server_hostname=target_host)

client.send(
    f"GET /third/stream-115272286748803111_ld.flv?k=c0b666231386a922&t=1718297695&abr_pts=-800&_session_id=037-202406070054553F7678EA780D3E568164.1717692894909.58638 HTTP/1.1\r\nHost:{target_host}\r\n\r\n".encode())

# receive some data
response = b''
for i in range(256*100): 
    data = client.recv(16384)   # 16 kb 
    if i % 200 == 0: 
        print(i) 
        #print(f'receiving {len(data)} bytes data...')

        # 手動跳出迴圈
        f=open('是否跳出迴圈.txt','r')
        s = f.readline() 
        f.close() 
        if s!='': 
            f=open('是否跳出迴圈.txt','w')
            f.write('') 
            f.close() 
            break
    response += data
    if not data:
        client.close()
        break

http_response = repr(response)
http_response_len = len(http_response)

# display the response
# print(f"http_response_len={http_response_len}, http_response={http_response}")


存檔檔名 = '抖音直播6_浩宇240606___001.bytes'
''' 
這個一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改一定要改
'''

f=open(存檔檔名, 'wb') 
f.write(response) 
f.close() 
len(response) 


