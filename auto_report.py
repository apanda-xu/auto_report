from selenium import webdriver
import time
from datetime import datetime
import pytz
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 用于邮件通知
def mail_to_you(result):
    # set login info
    mail_host = "smtp.qq.com"		# qq邮箱服务器，其他邮箱请自行查阅
    mail_user = "qq账号"
    mail_pass = "qq邮箱授权码"
    # set sender and reciver
    sender = "xxx@qq.com"			# 发送者邮箱	
    recivers = ["xxx@qq.com"]		# 接收者邮箱。收发邮箱可以相同，也即自己给自己发邮件。
    # write content
    msg = MIMEText(result, "plain", "utf-8")
    msg["From"] = Header("疫情自动填报程序", "utf-8")
    msg["to"] = Header("小熊猫", "utf-8")
    msg["Subject"] = Header("填报结果通知", "utf-8")
    # send email
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)		# 邮箱服务地址和端口，qq邮箱端口一般是465，其他邮箱请自行查阅
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, recivers, msg.as_string())
        print("邮件发送成功。")
    except Exception as e:
        print("邮件发送失败。\n", e)


# 获取东八区时间戳
def get_date():
    # Shanghai
    t = datetime.fromtimestamp(int(time.time()), pytz.timezone(
        'Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S %Z%z')
    date = t.split(" ")[0]
    return t, date

# 模拟浏览器进行填报
def report():
    # set chrome
    option = webdriver.ChromeOptions()
    option.add_experimental_option(
        "excludeSwitches", ['enable-automation', 'enable-logging'])     # hide some unimportant warnings
    option.add_argument("--headless")       # hide browser
    # if you are on windows, please use the code of following three lines
    '''
    chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver, options=option)
    '''
    # on linux
    driver = webdriver.Chrome(options=option)
    try:
        # enter the website address
        url = r'http://yqtb.nwpu.edu.cn/wx/xg/yz-mobile/index.jsp'
        driver.get(url)
        driver.maximize_window()
        # login
        username = driver.find_element_by_id("username")
        password = driver.find_element_by_id("password")
        stu_number = "xxx"					# 登陆账号
        stu_password = "xxx"	# 登陆密码
        username.send_keys(stu_number)
        password.send_keys(stu_password)
        driver.find_element_by_name("submit").click()
        # the information of health will be save if you have been filled the form. So, we don't need to care that.
        # submit
        try:
            driver.find_element_by_xpath('//*[@id="tz_div"]/div[2]/button[2]').click()
        except:
            pass
        driver.find_element_by_link_text("每日填报").click()
        driver.find_element_by_link_text("提交填报信息").click()
        driver.find_element_by_xpath(
            '//div[@class="weui-cells weui-cells_checkbox"]').click()
        driver.find_element_by_link_text("确认提交").click()
        time.sleep(5)
        result = "今日已完成疫情填报。"
        print(result)
        driver.close()
        driver.quit()
        mail_to_you(result)
        return True
    except Exception as e:
        result = "疫情填报失败: " + str(e)
        print(result)
        driver.close()
        driver.quit()
        mail_to_you(result)
        return False

# 程序入口
if __name__ == "__main__":
    pre_date = "2021-09-22"
    while(True):
        try:
            t, date = get_date()
            print(pre_date + "->" + t)
            if not(date == pre_date) and report():
                pre_date = date
        except Exception as e:
            result = "请检查程序是否出现问题: " + str(e)
            print(result)
            mail_to_you(result)
        time.sleep(2 * 3600)		# 设定每两个小时检查一次是否填报
