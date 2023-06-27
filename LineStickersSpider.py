from bs4 import BeautifulSoup
import os
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver=webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
b=input("輸入LINE網址的號碼:")
img_list=[]
driver.get(f"https://store.line.me/stickershop/product/{b}/zh-Hant")
# driver.get(f"https://store.line.me/stickershop/product/23504109/zh-Hant")
soup=BeautifulSoup(driver.page_source,"html.parser")
title=soup.find_all("p",class_="mdCMN38Item01Ttl")
soup=soup.find_all("span",class_="mdCMN09Image")
title_str="".join(title[0])
print(title_str)
# print(soup)
for i in range(0,len(soup),2):
    img_list.append(soup[i].get("style"))
for i in range(len(img_list)):
    img_list[i]=img_list[i][img_list[i].index("https"):len(img_list[i])-2]
# print(img_list)
##檢查與輸入同名資料夾有無存在
dir_list=[]
my_path="./"
file=os.listdir(my_path)
for i in file:
    all_path=os.path.join(my_path,i)
    if os.path.isdir(all_path):
        dir_list.append(i)
        # print("is dir",i)
if(dir_list.count(title_str)==0):
    os.mkdir(f"./{title_str}")
##
for i in range(len(img_list)):
    ##沒設置下面那一行(User-Agent)會回報403錯誤，加上就是回報200意即解決了
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    local_img=requests.get(img_list[i],headers=headers)
    # print(local_img)
    print(img_list[i])
    page=f"{i+1}"
    with open(f"./{title_str}/{page.zfill(2)}.png","wb") as f:
        f.write(local_img.content)

