import time
import cv2
import requests
import base64
import re
from selenium  import webdriver

vpnUrl = 'https://sslvpn.bnu.edu.cn'
reserveUrl = 'http://172.16.213.7/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id=2&item_id=5326&time_date=2021-09-12&userType=&viewType=m'
user1 = '201811940319'
password1 = 'yuanyue123456'
user = '201811080242'
password = '2052cong'

date = '2021-09-23'
targetField1 = '羽2'
targetField2 = '羽2'
targetTime1 = '19:00-20:00'
targetTime2 = '20:00-21:00'

#检查vpn是否被重复登录
def avoidRepeatLogin():
    try:
        continueButton = driver.find_element_by_name('btnContinue')
        continueButton.click()
    except Exception as e:
        return
    return

#对字符串的格式进行检查
def isCalculation(str):
    ans=re.match(r'^\d{1,2}[+|-]+\d{1,2}',str)
    if(ans!=None):
        return True
    else: return False

def calculate(str):
    ans = re.match(r'^\d{1,2}.+\d{1,2}', str)
    str = str[ans.regs[0][0]:ans.regs[0][1]]
    return eval(str)





#init
driver = webdriver.Chrome()

#vpn page
driver.get(vpnUrl)

userText = driver.find_element_by_name('username')
passwordText = driver.find_element_by_name('password')
loginButton = driver.find_element_by_id('btnSubmit_6')

userText.send_keys(user1)
passwordText.send_keys(password1)
loginButton.click()

#避免vpn被重复登录
avoidRepeatLogin()

#跳转到预约页面
time.sleep(0.1)
urlText = driver.find_element_by_id('browseUrl')
jumpButton = driver.find_element_by_id('btnBrowse_3')
urlText.send_keys(reserveUrl)
jumpButton.click()

#登录统一身份认证平台
userText = driver.find_element_by_id('un')
passwordText = driver.find_element_by_id('pd')
loginButton = driver.find_element_by_id('index_login_btn')

userText.send_keys(user)
passwordText.send_keys(password)
loginButton.click()

agreeButton = driver.find_element_by_class_name('btn')
agreeButton.click()



#查看是否刷新，相应时间点是否出现时间点
isFlashed = False
while(isFlashed == False):
    time.sleep(0.2)
    # 选择目标
    # 此时参数，'1'兵乓球，'2'网球，'3'羽毛球
    try:
        target = driver.find_element_by_xpath('//*[@id="tabs"]/ul/li[3]')
        target.click()
        # 此时对时间点进行选择
        timeItems = driver.find_elements_by_xpath('//*[@id="box-0"]/div/div/div[6]/a')
        for item in timeItems:
            if (item.get_attribute('value') == date):
                isFlashed = True
                item.click()
                break
    except Exception as e:
        print(e)
    if(isFlashed == False):
        driver.refresh()

#填写信息
time.sleep(1)
iframe = driver.find_element_by_css_selector('iframe')
driver.switch_to.frame(iframe)
# selector1 = driver.find_element_by_xpath('//*[@id="resourceTd_69062"]')
# selector1.click()
selector = driver.find_elements_by_class_name('resourceTd')
for item in selector:
    if((item.get_attribute('fieldname')==targetField1 and item.get_attribute('time_session')==targetTime1) or
    item.get_attribute('fieldname')==targetField2 and item.get_attribute('time_session')==targetTime2):
        item.click()
driver.switch_to.default_content()
nextButton = driver.find_element_by_xpath('//*[@id="resBook2"]/span/a/span/span')
nextButton.click()

#填写验证信息
# img = driver.find_element_by_id('kaptchaImage')
checkText = driver.find_element_by_name('checkcodeuser')
imgElement = driver.find_element_by_id('kaptchaImage')
submitButton = driver.find_element_by_xpath('//*[@id="companionDiv"]/div/a[1]')

time.sleep(1)
driver.get_screenshot_as_file('a.jpg')
img = cv2.imread('a.jpg')
cropped = img[imgElement.location['y']*2:imgElement.location['y']*2+imgElement.rect['height']*2,imgElement.location['x']*2:imgElement.location['x']*2+imgElement.rect['width']*2]
cv2.imwrite('a.jpg',cropped)


request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage"
# 二进制方式打开图片文件
f = open('a.jpg', 'rb')
img = base64.b64encode(f.read())


access_token = '24.d38f8cc32bc2c8c083b66c563c235709.2592000.1634370451.282335-24851630'
params = {"image":img}
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    ans = response.json()['words_result'][0]['words']
    print(ans)

if(isCalculation(ans)==True):
    print(calculate(ans))
    checkText.send_keys(calculate(ans))
    submitButton.click()





