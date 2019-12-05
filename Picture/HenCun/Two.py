from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import cv2
import numpy as np
dir_path = "/home/peng/图片/congqian/"
def headers():
    header = {
        "User-Agent":"Mozilla / 5.0(Linux;Android 6.0;Nexus 5 Build / MRA58N) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 78.0.3904.70 Mobile Safari / 537.36"
    }
    return header

def GetPictionUrl():
    Urls = []
    url = "http://m.pufei.net/manhua/292/"
    text = requests.get(url,headers = headers())
    soup = BeautifulSoup(text.content,"html.parser")
    div = soup.find(attrs={"class":"chapter-list"})
    lis = div.find_all("li")
    for li in lis:
        temp = {}
        temp["number"] = li.find("a").get("title")
        temp["url"] = li.find("a").get("href")
        Urls.append(temp)
    return Urls

def Parser(url,name):
    i = 1
    temp_url = []
    while(i<14):
        temp_url.append(url+"?af="+str(i))
        i = i + 1
    imgs = []
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    for temp in temp_url:
        try:
            browser.get(temp)
            browser.implicitly_wait(2)
            PictureUrl = browser.find_element_by_xpath('//*[@id="manga"]/img').get_attribute("src")
            imgs.append(PictureUrl)
        except:
            print("fail" + name)
    browser.close()
    browser.quit()
    return imgs

def SavePicture(urls):

    number = urls["number"]
    url = "http://m.pufei.net" + urls["url"]
    path = dir_path + number + ".jpg"
    img = Parser(url,number)
    imgs = list(set(img))
    imgs.sort(key=img.index)
    tag = True
    for img in imgs:
        if tag == True:
            tag = False
            with open(path, "wb") as file:
                file.write(requests.get(img, headers=headers()).content)
        else:
            with open("1.jpg", "wb") as file:
                file.write(requests.get(img, headers=headers()).content)
            img1 = cv2.imread(path)
            img2 = cv2.imread("1.jpg")
            try:
                len(img2)
                v = np.vstack((img1, img2))
                cv2.imwrite(path, v)
            except:
                print("\t!-!\t")

    print("success "+number)

if __name__ == "__main__":
    Urls = GetPictionUrl()
    for urls in Urls[366:505]:
        SavePicture(urls)
    pass
