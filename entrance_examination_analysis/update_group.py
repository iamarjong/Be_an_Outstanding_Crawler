#test3.py

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
import key 

driver = webdriver.Chrome()
driver.get(key.學群查詢網址)
driver.implicitly_wait(6)
# https://acodingirl.blogspot.com/2020/09/pythonselenium-textbox.html 


大學 = input('輸入大學正確名稱')
check = input('"'+大學+'"，確定輸入正確? ')
if 大學 =='':
    大學= '國立成功大學'


driver.find_element(By.XPATH, '//input[@id="searchInput"]').send_keys(大學) 
# https://selenium-python-zh.readthedocs.io/en/latest/locating-elements.html 

clk = driver.find_element(By.XPATH, '//button[@id="searchbtn"]') 
clk.click() 

import time 

clk.send_keys(Keys.END) 
time.sleep(1) 
clk.send_keys(Keys.END) 
time.sleep(1) 
clk.send_keys(Keys.END) 
time.sleep(1) 
clk.send_keys(Keys.END) 
time.sleep(1) 
clk.send_keys(Keys.END) 
time.sleep(1) 
clk.send_keys(Keys.END) 

a = driver.find_element(By.XPATH, '//div[@id="BoxListView"]') 
html = a.get_attribute('outerHTML')   

'''  
得到搜尋完大學的相關資料 html 碼
開始用美麗湯分析
'''

from bs4 import BeautifulSoup
 
soup = BeautifulSoup(html, 'html.parser') 

# https://blog.gtwang.org/programming/python-beautiful-soup-module-scrape-web-pages-tutorial/2/
p_tag = soup.find_all("p", class_="relCollegeMajor") 
# p_tag 

links = []
for i, tag in enumerate(p_tag): 
    link = tag.find_all('a')
    #print(len(link))  
    if len(link)==3:
        links.append([i,[a for a in link ]])
        


print('目前要處理者如下: \n\n')

answer = []
for obj in links: 
    sub_soup_1 = BeautifulSoup(
    str(soup.find_all('div',class_='scard well well-add-card')[obj[0]+1]) 
        , 'html.parser') 
        
    print( "( item" ,obj[0],") ", \
            sub_soup_1.find_all('a')[0].string[len(大學):] \
                ,":", obj[1][0].string , '跨' ,obj[1][1].string )  
    answer.append([sub_soup_1.find_all('a')[0].string[len(大學):],obj[1][0].string,obj[1][1].string])

print('\n\n共',len(answer),'項。', end='')


''' 
已取得 answer 列表
底下將以 answer 為主
answer 示例: 
e.g. answer = [['第一個系','第一個學群','第二個學群'],...] (憑印象想的)
'''

# 開另一個chrome視窗進入B卡的後台
driver1 = webdriver.Chrome() 
driver1.get(key.網址
            )
ac = driver1.find_element(By.XPATH, '//input[@id="account"]').send_keys(key.帳號)
rq = input("??") 
pw = driver1.find_element(By.XPATH, '//input[@id="password"]').send_keys(key.密碼)  
rq = input("??") 
sb = driver1.find_element(By.XPATH, '//input[@type="submit"]')
time.sleep(1) 
sb.click() 

print('\n\n好的我們正式開始: \n\n')

from selenium.webdriver.support.ui import Select

j=0
one_or_two = 1  # 有兩個學群，這個變數在控制要選哪一個
N=len(answer) 
勘誤表= {'地球環境學群': ['地球與環境學群'], '建築設計學群': ['建築與設計學群'], '文史哲學群': ['文史哲學學群'], '遊憩運動學群': [ '遊憩與運動學群']}
# 還可再增
勘誤成功 = False

# 還沒被其他人新增到的
新增 = []  
連續新增次數 = 0 
while j<N: 
    勘誤成功 = False 

    print('開始做', answer[j][0],'(j=' ,j,')新增到',answer[j][one_or_two],end=': ')

    # 找到新增鍵並按下
    try:
        b = driver1.find_element(By.XPATH, '//a[@class="shortcut-button"]') 
        time.sleep(1) 
        b.click()
        print('點下新增按扭',end='')

        #只是區別 j 是否是0而已。 
        try: 
            新增.append(answer[j-1])
            連續新增次數 +=1 
            print('，代表前一輪新增了其他人沒新增到的(\n\n        ',answer[j-1],'\n\n)' ,end='→ ')
        except: 
            print('→ ',end='')

    except: 
        print('找不到新增鍵。應該是剛才的系是重覆新增的',end='→ ') 
        print('現在應該是填系的頁面',end='→ ')
        連續新增次數 = 0

    try: 
        print('開始 key 系名校名跟學群',end='→ ')

        driver1.find_element(By.XPATH, '//input[@name="departTitle"]').send_keys('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b')
        driver1.find_element(By.XPATH, '//input[@name="departTitle"]').send_keys(answer[j][0])  


        select = Select(driver1.find_element(By.NAME, 'schoolId'))
        select.select_by_visible_text(大學) 
        select = Select(driver1.find_element(By.NAME, 'groupId'))
        
        try: 
            select.select_by_visible_text(answer[j][one_or_two])  
        except: 
            print("學群錯誤，進入更正區",end='→')
            

            錯誤學群 = answer[j][one_or_two] 
            # e.g.  錯誤學群 = '地球環境學群' 

            if 錯誤學群 not in 勘誤表:   
                勘誤表.update({錯誤學群:[]})
            
            while 勘誤成功!=True: 
                for alter in 勘誤表[錯誤學群]:
                    try:
                        select.select_by_visible_text(alter)  
                        print("成功更正為",alter,end='→')
                        勘誤成功 = True 
                        break 
                    except: 
                        ...
                if 勘誤成功==False:
                    新加入 = input('手動勘誤! 直接輸入學群名:')
                    勘誤表[錯誤學群].append(新加入)
                    print('加入新元素, 勘誤表=',勘誤表)

        print('key 完',end='→ ')

    except: 
        print('key失敗。')
        break 

    ''' 
    注意!!! 
    小心!!!
    此為送出!!! 
    '''
    time.sleep(0.5)
    #check = input('注意！小心！此為送出！')
    if True: # check == '': 
        print('正在送出',end='→ ')
        x = driver1.find_element(By.XPATH, '//input[@type="submit"]')
        time.sleep(1)
        x.click() 
        print('已按送出請查收',end='。\n\n')

        time.sleep(4)

    j = j if one_or_two==1 else j+1 
    one_or_two = 1 if one_or_two==2 else 2

    if 連續新增次數 ==3 : 
        check = input("檢查為什麼會連續新增次數 = 3，輸入 end 代表結束並看報告，否則隨意輸入") 
        if check =='end': 
            break


# 確認最後一個是不是沒人新增的
# 找到新增鍵並按下
try:
    b = driver1.find_element(By.XPATH, '//a[@class="shortcut-button"]') 
    time.sleep(1) 
    b.click()
    print('點下新增按扭',end='')

    #只是區別 j 是否是0而已。 
    try: 
        新增.append(answer[j-1])
        連續新增次數 +=1 
        print('，代表前一輪新增了其他人沒新增到的', end='→ ')
    except: 
        print('→ ',end='')

except: 
    print('找不到新增鍵。應該是剛才的系是重覆新增的',end='→ ') 
    print('現在應該是填系的頁面',end='→ ')
    連續新增次數 = 0

print()
print()
fileName = str(time.time())+'.'+大學+'.txt'
print(大學, ':完成。其中 answer = ', answer, '; 新增=', 新增,'; 正在寫入'+fileName+'，檔內格式為[answer,新增,勘誤表]。') 

f=open(fileName,'w')
f.write('[')
f.write(str(answer))
f.write(',')
f.write(str(新增))
f.write(',')
f.write(str(勘誤表))
f.write(']')
f.close() 

print('\n\n完成。 \n\n\n')
# [註]
# "新增" 改成 "這次新增" 

# conda activate penguin_web && cd "C:\Users\User\OneDrive\myvscode_onedrive\240721_爬蟲_??????????????????????????????????????????落點分析" &&  python "C:\Users\User\OneDrive\myvscode_onedrive\240721_爬蟲_??????????????????????????????????????????落點分析\test3.py"
