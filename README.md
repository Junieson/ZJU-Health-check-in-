# ZJU-Health-check-in-
ZJU Health check-in浙江大学浙大健康打卡自动程序，一个.exe程序，一键打卡，简单易用
-------------------------
# 使用
使用win自带任务计划程序运行 '打卡.exe' 程序，也可以部署到windows.sever 服务器

也可以修改源码使用pyinstaller 打包成.exe程序
-------------------------
## 1. 思路介绍
思路简单，使用模拟浏览器自动登录，自动选择问卷，自动获取位置，最后提交。然后打包成.exe文件，最后用windows自动定时任务启动程序，技术比较简单
## 2. 依赖介绍
[pyppeteer介绍](https://blog.csdn.net/freeking101/article/details/93331204)
[tkinter介绍](https://www.cnblogs.com/beile/p/14474808.html)
## 3. 优点
 - 只有一个exe文件
 - 第一次运行可以自动安装chromiu，不需要安装其他环境
 - 账号密码保存本地
 - 运行比较稳定
 ## 4.有待改进
 
 - 加上自动选择打卡地点，而不是通过浏览器H5位置接口获取
 - 打包成其他平台的可执行文件
 - 邮件提醒，现在只有截图弹窗提醒
 - 部署服务器上
 
## 4. 解决问题
 （1）首次运行pyppeteer 下载chromium太慢卡死
		 [更换淘宝源](https://www.168seo.cn/python/25259.html)
（2）打包.exe文件出现相对路径不对的情况
在桌面打开终端当前路径是system32，不是desktop，所有路径问题需要解决
[获取工作环境目录](https://blog.csdn.net/wangziyang777/article/details/106998390/)
（3）自动关闭弹窗
多线程自动执行主窗口关闭任务
## 5. 展示
![在这里插入图片描述](https://img-blog.csdnimg.cn/bb27090d6e06445c993504867fc32958.png)![在这里插入图片描述](https://img-blog.csdnimg.cn/38cc32489f71435ea03e4beb208173be.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBASnVuaWVzb24=,size_13,color_FFFFFF,t_70,g_se,x_16)
