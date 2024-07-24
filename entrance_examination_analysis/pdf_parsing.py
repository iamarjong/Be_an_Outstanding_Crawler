# https://steam.oxxostudio.tw/category/python/example/pdfplumber.html 
''' 
conda activate penguin_web
pip install pdfplumber
'''

import key

import pdfplumber
pdf = pdfplumber.open(key.pdf路徑)

所有的資料 = {}



def 篩選標準_parse(篩選標準raw:str): 
    
    #篩選標準raw= '1. 數學 A(均標)\n或\n數學 B(均標)' 
    篩選標準raw = 篩選標準raw.replace(' ','') 

    i = 1 
    敘述 = []
    while True: 
        v = 篩選標準raw.find(str(i+1)+'.') 

        if v>0: 
            敘述.append(篩選標準raw[2:v]) 
            篩選標準raw = 篩選標準raw[v:]
        else: 
            break 
    敘述.append(篩選標準raw[2:])

    答案 = [] 
    for stmt in 敘述: 
        stmt=stmt.replace('\n或\n',' ')
        stmt=stmt.replace('\n','')
        stmt=stmt.replace('(',' ')
        stmt=stmt.replace(')','')
        stmt = stmt.split(' ')
        答案.append(stmt)

    return 答案   

def  採計_parse(s:str): 
    
    if s == '--': 
        return []
        
    # s = '國 文(學測) x 1.50'
    s=s.replace(' ','') 
    s=s.replace('(',' ') 
    s=s.replace(')x',' ')  
    l = s.split(' ') 
    l[-1] = float(l[-1]) 
    return l  


# 開始抽取pdf 第 pp 頁的系所篩選資料
# [26,238]
for pp in range(26,238): 
    print('pp=',pp)
    page = pdf.pages[pp-1]
    table = page.extract_table()

    #print(len(table)) 

    
    # 先檢查有沒有 '本頁以下空白' , 如同 pp41 的情況
    for i in range(len(table) ): 
        #print(table[i][0])  
        if type(table[i][0])==str:
            if table[i][0].startswith('本頁以下空白'):
                table = table[:i+1]   
                break 

    table_middle = table[2:-1] 
    N = len(table_middle )
    一頁的資料 = [] 



    u = table[0][0].find('：') 
    校名 = table[0][0][u+1:] 
    v = 校名.find('(')
    校名=校名[0:v]
    校名


    for now in range(0,N-2 ,5): 
        print('  now=',now)  

        系名 = table_middle[now][0].replace('\n','') 
        篩選標準raw = table_middle[now][1]

        採計 = [採計_parse(table_middle[now][2] ) ,
            採計_parse(table_middle[now+1][2]  ),
            採計_parse(table_middle[now+2][2] ) ,
            採計_parse(table_middle[now+3][2])  ,
            採計_parse(table_middle[now+4][2] )
                ] 
        while(採計[-1]==[]):
            採計.pop(-1) 
        英聽 = table_middle[now+4][1] 
        if 英聽 == '---':
            英聽=None 

        一頁的資料.append(     {'校名': 校名 ,'系名':系名, '篩選標準':篩選標準_parse( 篩選標準raw), '採計':採計,'英聽':英聽}  )
    一頁的資料, len(一頁的資料) 
    所有的資料.update({pp:一頁的資料}) 

所有的資料
