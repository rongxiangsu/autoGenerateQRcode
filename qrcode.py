# -*- coding:utf-8 -*-
import pycurl,urllib,StringIO,requests

def downloadImageFile(localpath,imgUrl):  
    local_filename = imgUrl.split('/')[-1]
    r = requests.get(imgUrl, stream=True)
    with open(localpath+local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        f.close()  
    return local_filename

def postQRimg(website):
	buf = StringIO.StringIO()
	url = 'http://www.wwei.cn/Qrcode/create.html'
	post_data_dic = {
		"t":website,
		"dt":"text",
		"f":"#000000",
		"b":"#FFFFFF",
		"pt":"#000000",
		"inpt":"#000000",
		"s":1,
		"lap":0,
		"eap":0,
		"level":"L"
		}
	postfield = urllib.urlencode(post_data_dic)
	p_curl = pycurl.Curl()
	p_curl.setopt(pycurl.WRITEFUNCTION, buf.write)
	p_curl.setopt(pycurl.POST, 1)
	p_curl.setopt(pycurl.URL, url)
	p_curl.setopt(pycurl.HTTPHEADER, ["Content-Type:application/x-www-form-urlencoded"])
	p_curl.setopt(pycurl.POSTFIELDS, postfield)
	p_curl.perform()
	content = buf.getvalue()
	img_url = content.split(",")[1].split(":")[1].split("\"")[1].replace('\\','')
	download_link = "http://www.wwei.cn/"+img_url
	buf.close()
	p_curl.close()
	return download_link

def main(website,localpath):
	download_link = postQRimg(website)
	downloadImageFile(localpath,download_link)
	print('Pic Saved!')

if __name__ == '__main__':
	website = "http://www.baidu.com"
	localpath = "E:/"
	main(website,localpath)