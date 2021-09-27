# 西工大疫情自动填报程序
## 1.免责声明
**本程序仅用于学习交流，为控制和战胜疫情，请坚持手动填报！**

## 2.实现原理
程序模拟浏览器操作，以完成疫情填报。浏览器可以选择Chrome或者Firefox，两者存在一些区别，推荐使用Chrome。

## 3.环境准备
（1）python3.8。<br>
（2）安装下列python库：selenium、datetime、pytz、smtplib、email。<br>
（3）安装chrome浏览器和对应版本的[chromedriver](https://chromedriver.chromium.org/downloads)，并配置好路径。<br>
## 4.一些说明
（1）本文使用的是linux系统，但也支持windows，在代码中启用注释掉的部分即可。<br>
（2）本文使用的是qq邮箱，收发邮箱是一个账号。如何申请邮箱授权码，请参阅[官方说明](https://service.mail.qq.com/cgi-bin/help?subtype=1&id=28&no=1001256)。<br>
（3）程序设定每两个小时检查一次是否需要填报。如果今天已经填报，则只输出时间戳而不执行其他操作。如果今天还未填报，则会填报并邮件通知填报结果。若填报失败，则会邮件通知失败原因并在两个小时后重新尝试填报。可自行修改填报时间。<br>
（4）若未收到邮件通知，请检查程序是否正常运行和网络状态。<br>
