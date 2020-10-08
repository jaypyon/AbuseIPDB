#아이피의 군영향성평가를위한 abuseipdb에 대한 조회.
#정보보호 19-4기 박재용
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time

start = time.time()#start time
print('''사용방법: 
1.조회를 희망하는 아이피들을 input.txt파일에 엔터를 구분자로 차례대로 입력한다.
2.결과로 output.txt 파일이 생성되며, 해당 파일은 json형식으로 저장되어있다.
3.{IP:조회결과}의 JSON(파이썬에서의 딕셔너리) 형식으로 추출된다.

주의사항
1.2020.05.27 오전 3시47분 기준으로 2223개의 IP 조회에 385+8초 소요됨을 확인함.
ㄴ 두번밖에 테스트 하지 못한 결과라 아직 안정성은 보장할 수 없음.
ㄴ 만약 Error 429 Too many request 발생시 sleep 시간을 더 연장 조정할것.

2020.06.14 업데이트 이력 : whitelist인 IP에 대해서 whitelist로 출력하도록 업데이트.
기존 json 출력에서 가독성이 떨어짐을 느끼고 간단하게 변경.
''')

rf= open("input.txt",'r')#파일 읽기
f= open("output.txt",'w')#쓸 파일 입력


tempString=rf.read()
userInput=tempString.split('\n') #오리지널 아이피
targetPage=[] #조회하는 유알엘
resultReports=[]
baseUrlObject="https://www.abuseipdb.com/check/"

length = len(userInput)
for i in userInput:
    targetPage.append(baseUrlObject+i)
dic ={}
counter = 0;
kaisuu=0;
countIp=0;
for i in targetPage:
    counter+=1
    if(counter==30):
        time.sleep(17)
        print("진행경과",float((kaisuu+1)*30)/float(len(targetPage)))
        counter =0
        kaisuu+=1
    html = urlopen(i)
    bsObject = BeautifulSoup(html,"html.parser")
    judgeWhitelist = str(bsObject.select("#report-wrapper > div:nth-child(1) > div:nth-child(1) > div > p"))
    whiteFlag = judgeWhitelist.find("hitelist")
    if(whiteFlag!=-1):
        resultReports.append("Whitelist")
        countIp+=1
        print(countIp," / ",length)
    else:        
        theNumOfReports = str(bsObject.select("#report-wrapper > div:nth-child(1) > div:nth-child(1) > div > p:nth-child(2) > b:nth-child(1)"))
        resultNum =""
        for j in theNumOfReports :
            if(48<=ord(j)<=57):
                resultNum=resultNum+j
            else:       
                continue
        countIp+=1
        print(countIp," / ",length)
        resultReports.append(resultNum)
        
    
        #print(resultNum)
#print(resultReports)


#dic=dict(zip(userInput,resultReports))
for i in range(len(userInput)):
    f.write(str(userInput[i])+" : "+str(resultReports[i])+"\r")
print("파일 추출완료","소요시간",time.time()-start)
#f.write(str(dic))
f.close()