from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from selenium.webdriver.chrome.options import Options


#阅读文章
def read_articles():
    urls=["https://www.xuexi.cn/xxqg.html?id=36a1bf1b683942fe917fc1866f13fc21","https://www.xuexi.cn/xxqg.html?id=2813415f8e1c48b4b47e794aca7b7bb5"]
    for num, url in enumerate(urls):
        driver.get(url)
        driver.implicitly_wait(10)
        articles=driver.find_elements_by_xpath("//div[@class='text-link-item-title']")
        for index, article in enumerate(articles):
            if index > 4:
                break 
            article.click()
            all_handles = driver.window_handles
            driver.switch_to_window(all_handles[-1])
            driver.get(driver.current_url)
            driver.save_screenshot('article'+str(num)+'_'+str(index)+'.png')
            for i in range(0, 2000, 100):
                js_code = "var q=document.documentElement.scrollTop=" + str(i)
                driver.execute_script(js_code)
                time.sleep(3)
            for i in range(2000, 0, -100):
                js_code = "var q=document.documentElement.scrollTop=" + str(i)
                driver.execute_script(js_code)
                time.sleep(3)
            time.sleep(10)
            driver.close()
            driver.switch_to_window(all_handles[0])
    print("阅读文章完毕\n")

def watch_videos():
    titles=['新闻联播','学习新视界','学习专题报道','重要活动视频专辑']
#"""观看视频"""#视频好像会需要每天都看新的，前一天看的算旧的，今天再看不算任务
    driver.get('https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html')
    driver.implicitly_wait(10)
    for indexs, title in enumerate(titles):
        driver.find_elements_by_xpath("//*[contains(text(), '"+title+"')]")[0].click()
#这个是直接打开页面，是图文
        time.sleep(2)
        videos = driver.find_elements_by_xpath("//div[@class='textWrapper']")
        time.sleep(2)
#上面是图文选取，如果你想点到列表里面选取，则改为以下代码：
    #titles=driver.find_elements_by_xpath("//*[contains(text(), '列表')]")[0]
    #titles.click()
    #videos = driver.find_elements_by_xpath("//div[@class='text-link-item-title']")
        for i, video in enumerate(videos):
            if i > 2:
                break
            video.click()
            all_handles = driver.window_handles
            driver.switch_to_window(all_handles[-1])
#模拟点击播放，因为直接点开连接播放，积分不会增长，可能也是因为反爬机制，必须刷新页面后，点击播放才算做是观看一次
            driver.get(driver.current_url)
            driver.find_element_by_xpath("//div[@class='outter']").click()
            time.sleep(3)
            driver.save_screenshot('vidoes'+str(indexs)+'_'+str(i)+'.png')

#可以获取视频当前时长，但是没有必要，只要看3分钟就好了
            #video_current_time_str = driver.find_element_by_xpath("//span[@class='current-time']").get_attribute('innerText')
            #print(video_current_time_str)
            #video_duration = int(video_duration_str.split(':')[0]) * 60 + int(video_duration_str.split(':')[1])

#每个视频开启后停留190秒，然后把所有句柄关闭
            time.sleep(180)
            driver.close()
            driver.switch_to_window(all_handles[0])



# 保持学习，直到视频结束
        #time.sleep(video_duration + 3)
    print("播放视频完毕\n")

def get_scores():
    """获取当前积分"""
    driver.get('https://pc.xuexi.cn/points/my-points.html')
    time.sleep(2)
    gross_score = driver.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div[2]/div[2]/span[1]").get_attribute('innerText')
    today_score = driver.find_element_by_xpath("//span[@class='my-points-points']").get_attribute('innerText')
    print("当前总积分：" + str(gross_score))
    print("今日积分：" + str(today_score))
    print("获取积分完毕，即将退出\n")

if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

#如果是linux就改成./chromedriver，如果是windows就是./chromedriver.exe
    driver= webdriver.Chrome('./chromedriver',chrome_options=chrome_options)

    driver.get('https://pc.xuexi.cn/points/login.html')
    driver.execute_script("var q=document.documentElement.scrollTop=950")
    driver.execute_script("var q=document.documentElement.scrollLeft=225")
    time.sleep(3)
    driver.save_screenshot('./1.png')
    time.sleep(15)

#设置三轮一分钟等待时间，每分钟一次刷新，三分钟过后退出脚本
    for i in [1,2,3]:
        try:
            WebDriverWait(driver,60).until(EC.title_is(u"我的学习"))
            print('\n')
            print('登录成功')
            print('\n')
            break
        except:
            driver.find_elements_by_xpath("//span[@class='refresh']")[0].click()
            time.sleep(1.5)
            driver.save_screenshot('./1.png')
            if(i==3):
                print('登录超时，脚本退出')
                driver.quit()
    driver.get("https://www.xuexi.cn/")
    driver.implicitly_wait(10)
    read_articles()     # 阅读文章
    watch_videos()      # 观看视频
    get_scores()        # 获得今日积分
    driver.quit()