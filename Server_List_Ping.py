#导入库
import socket
import time
import re
#pip install dnspython
import dns.resolver

#SRV无端口域名解析
def SRV_DNS(data):
    if re.compile(r':\d+').search(data):
        host, port = data.split(':')
        return host, int(port)
    else:
        domain = "_minecraft._tcp." + data
        try:
            answers = dns.resolver.resolve(domain, 'SRV')
            rdata = answers[0]  # 获取第一个记录
            host = str(rdata.target)
            port = rdata.port
            return host,port
        except Exception as e:
            print(f"解析SRV{domain}错误: {e}")
            return None
#服务器Ping        
def ServerList (host, port):
    try:
        #请求
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)#超时:1秒
        s.connect((host, port))
        start_time = time.time()
        s.sendall(b'\xFE\x01')
        data = s.recv(1024).split(b'\x00\x00')
        end_time = time.time()
        s.close()
        
        #请求耗时
        request_time = round(end_time - start_time, 2)
        #协议
        Protocol = data[1].decode('utf-16be', 'ignore')
        Protocol = Protocol if Protocol == 127 else "不兼容"
        #版本
        version = data[2].decode('utf-16be', 'ignore')
        #motd
        motd = data[3].decode('utf-16be', 'ignore')
        #当前人数
        numplayers = data[4].decode('utf-16be', 'ignore')
        #最大人数
        maxplayers = data[5].decode('utf-16be', 'ignore')
        return request_time,Protocol,version,motd,numplayers,maxplayers
    except Exception as e:
        print("服务器Ping错误:",e)
        return None
#服务器ping打印
def ServerList_print(host, port):
    data = ServerList(host, port)
    if data != None:
        data = f"IP:{host}:{port} 状态在线\n响应耗时:{data[0]}\n协议版本:{data[1]}\n游戏版本:{data[2]}\nMOTD:{data[3]}\n游戏人数:{data[4]}/{data[5]}"
        return print(data)
    else:
        print("IP:%s:%s" %(host, port),"状态离线")


#调用示例
def main():
    data = ["127.0.0.1:25565","127.0.0.1:25566"]
    for i in data :
        host, port = SRV_DNS(i)
        ServerList_print(host, port)    
    return

if __name__ == '__main__':
    main()
