# coding:utf-8
# -*- coding: utf-8 -*-
# @Time    : 2021/12/16 16:31
# @Author  : Junieson
# @File    : healthreporter.py
# @Software: PyCharm

import asyncio
import datetime
import os
import random
import sys
import threading
import time
import tkinter
from tkinter import Tk, Label, Entry, CENTER, Button
from tkinter import messagebox
from pyppeteer import launch
from faker import Factory
from PIL import Image, ImageTk

f = Factory.create()


class load:
    id = ''
    pw = ''
    # 是否可视化
    vis = 1
    def __init__(self):
        self.root = Tk()
        self.root.title("首次登录输入账号密码")
        self.root.geometry("300x150+600+300")
        # 设置用户账号输入框
        self.ID = Label(self.root, text="账号：")
        self.ID.place(relx=0.2, rely=0.2, anchor=CENTER)
        self.text1 = Entry(self.root)
        self.text1.place(relx=0.55, rely=0.2, anchor=CENTER, width=160, height=25)

        # 设置用户密码码输入框
        self.password = Label(self.root, text="密码：")
        self.password.place(relx=0.2, rely=0.4, anchor=CENTER)
        self.text2 = Entry(self.root)
        self.text2.place(relx=0.55, rely=0.4, anchor=CENTER, width=160, height=25)

        # 设置登录按钮
        self.enter = Button(self.root, text="登录", command=self.submit, width=15, height=1)
        self.enter.place(relx=0.55, rely=0.83, anchor=CENTER)

        # 是否可视化
        self.isvis = Label(self.root, text="可视化：")
        self.isvis.place(relx=0.22, rely=0.6, anchor=CENTER)
        self.r = tkinter.IntVar()
        self.r.set(1)
        self.male_select = tkinter.Radiobutton(self.root, text='是', value=1, variable=self.r, command=self.func)
        self.male_select.place(relx=0.45, rely=0.6, anchor=CENTER)
        self.female_select = tkinter.Radiobutton(self.root, text='否', value=0, variable=self.r, command=self.func)
        self.female_select.place(relx=0.7, rely=0.6, anchor=CENTER)

    # 定义选择后执行的函数
    def func(self):
        self.vis = self.r.get()

    def submit(self):
        self.id = self.text1.get()
        self.pw = self.text2.get()
        messagebox.showinfo('提示', '保存成功，修改在“user_info.text”文件！')
        self.root.quit()
        self.root.destroy()

    def show(self):
        self.root.mainloop()


async def main():
    # 创建浏览器对象
    id, pw, isvis = get_info()
    browser = await launch(headless=not bool(int(isvis)), args=['--disable-infobars', f'--window-size={415},{1050}'],
                           dumpio=True)
    # 打开新的标签页
    page = await browser.newPage()
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    # 设置视图大小
    await page.setViewport({'width': 400, 'height': 1000})

    # 设置UserAgent
    await page.setUserAgent(f.user_agent())

    # 访问页面
    url = 'https://healthreport.zju.edu.cn/ncov/wap/default/index'
    response = await page.goto(url)
    await asyncio.sleep(2)
    print("打开页面...")
    # 登录
    # input_user = await page.xpath('//*[@id="username"]')
    # await input_user[0].type('22160170', {'delay': random.randint(100, 151) - 50})
    try:
        a = await page.xpath('//*[@id="username"]')
        if not a:
            while not await page.xpath('//*[@id="username"]'):
                page = await browser.newPage()
                await page.setViewport({'width': 400, 'height': 1000})
                await page.goto(url)
                print('请求非法')
    except:
        while not await page.xpath('//*[@id="username"]'):
            page = await browser.newPage()
            await page.setViewport({'width': 400, 'height': 1000})
            await page.goto(url)
            print('请求非法')

    await page.type('#username', id, {'delay': random.randint(10, 30)})
    await page.type('#password', pw, {'delay': random.randint(10, 30)})
    print("输入账号密码...")
    await page.click('#dl')
    await asyncio.sleep(3)
    try:
        x = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[4]/div/div/div[1]')
        if not x:
            root = Tk().withdraw()
            messagebox.showinfo('提示', '出错请可视化手动登录')
            while not await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[4]/div/div/div[1]'):
                pass
    except:
        root = Tk().withdraw()
        messagebox.showinfo('提示', '出错请可视化手动登录')
        while not await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[4]/div/div/div[1]'):
            pass
    print("登录中...")
    # 接种
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[4]/div/div/div[1]')
    await choice[0].click()
    # 不是不宜接种
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[5]/div/div/div[5]')
    await choice[0].click()
    # 当前已完成接种
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[6]/div/div/div[2]')
    await choice[0].click()
    # 不是未返校
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[7]/div/div/div[2]')
    await choice[0].click()
    # 不是未到岗
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[8]/div/div/div[2]')
    await choice[0].click()
    # 不是发热
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[9]/div/div/div[2]')
    await choice[0].click()
    # 不是隔离
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[10]/div/div/div[2]')
    await choice[0].click()
    # 不是居家
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[11]/div/div/div[2]')
    await choice[0].click()
    # 没值得注意
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[12]/div/div/div[2]')
    await choice[0].click()
    # 已经申请健康码
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[13]/div/div/div[1]')
    await choice[0].click()
    await asyncio.sleep(2)
    # 绿码
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[14]/div/div/div[1]')
    await choice[0].click()
    # 在校
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[15]/div/div/div[1]')
    await choice[0].click()
    # 所在地
    print("获取地理位置...")
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[16]/div/div/div[1]')
    await choice[0].click()
    # await page.evaluateOnNewDocument(
    #     '''() =>{ Object.defineProperties(p,{ accuracy:{ get: () => null } }) }''')
    await asyncio.sleep(2)
    # 获取地理位置
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[19]/div')
    await choice[0].click()
    time.sleep(2)
    # 无密接
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[22]/div/div/div[2]')
    await choice[0].click()
    # 承诺书
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[34]/div/div/div')
    await choice[0].click()
    # # 提交
    choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[5]/div')
    await choice[0].click()
    try:
        choice = await page.xpath('//*[@id="wapcf"]/div/div[2]/div[2]')
        await choice[0].click()
    except:
        pass
    while not await page.xpath('//*[@id="wapat"]'):
        choice = await page.xpath('/html/body/div[1]/div[1]/div/section/div[5]/div')
        await choice[0].click()

    print("打卡...")
    # 截图
    nowdir = os.path.dirname(os.path.realpath((sys.executable)))
    await page.screenshot({'path': nowdir + '/shortcut.png'})
    await browser.close()  # 关闭浏览器
    show_res()
    print('恭喜！打卡成功')
    sys.exit()


def stop(root, label, times):
    for i in range(10):
        label['text'] = "恭喜打卡成功\n" + times + '\n倒计时关闭' + str(10 - i) + '秒'
        time.sleep(1)
    root.quit()


def get_info():
    nowdir = os.path.dirname(os.path.realpath((sys.executable)))
    try:
        with open(nowdir + '/user_info.txt', 'r', encoding='utf-8') as f:
            user_name = f.readline().replace('\n', '')
            user_password = f.readline().replace('\n', '')
            isvis = f.readline().replace('\n', '')
            f.close()
    except:
        with open(nowdir + '/user_info.txt', 'w', encoding='utf-8') as f:
            window = load()
            window.show()
            user_name, user_password, isvis = window.id, window.pw, window.vis
            if isvis == 0:
                print('当前不可视的静默模式，修改值为1可见')
            f.write(user_name + '\n')
            f.write(user_password + '\n')
            f.write(str(isvis) + '\n')
            f.close()
    return user_name, user_password, isvis


def show_res():
    root = Tk()
    nowdir = os.path.dirname(os.path.realpath((sys.executable)))
    print('当前目录',nowdir)
    img_open = Image.open(nowdir + "/shortcut.png")
    img_png = ImageTk.PhotoImage(img_open)
    now_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    label_img = tkinter.Label(root, text="恭喜打卡成功\n" + now_time, font=("微软雅黑", 20), fg="green", image=img_png,
                              compound='center')
    label_img.pack()
    t = threading.Thread(target=stop, args=(root, label_img, now_time))
    t.start()
    root.mainloop()


# show_res()
asyncio.get_event_loop().run_until_complete(main())
