
扫公众号关注不迷路：    
![https://img-blog.csdnimg.cn/20201019162545488.jpg](https://img-blog.csdnimg.cn/20201019162545488.jpg)
回复：pythontb

目前有了更好的方式(不会被风控)，推荐大家用这个：  
[Chrome插件的使用【天猫超市抢购飞天茅台】](https://chenhx.blog.csdn.net/article/details/112489954)  

# 更新记录 

## 20210104
- 时间格式修改
- 优化倒计时  
- 集成pyautogui，避免被淘宝检测出是无头浏览器的点击（解决提交结算无效的情况，此原因由淘宝检测导致）
    - 安装命令：```python -m pip install pyautogui```
- 增加getxy.py文件，输出自己电脑屏幕的宽高  
- 增加四个参数，config.ini文件中配置
  - 屏幕的宽高，单位：毫米
  - 结算按钮的宽高，单位：毫米
  - （浏览器全屏，在购物车页面，量出结算按钮的坐标。购物车只有一个商品的情况）

目前教程还在准备中，可以先关注专栏：  
https://blog.csdn.net/qq_26525215/category_10710827.html  

教程出来后，专栏便会更新  

以上是基于原作者的代码进行的一些优化和修改。  

以下为原作者的说明：

# taobao_seckill
淘宝、天猫半价抢购，抢电视、抢茅台，干死黄牛党
## 依赖
1. 安装chrome浏览器
2. 安装chromedriver到python的路径里
```
2.1. 记住`which python`跑出的路径，比如`usr/local/bin/python`。
2.2. 然后去chrome的软件选择`About Google Chrome`记住你的chrome的版本，比如我的是`Version 93.0.4577.63`。
2.3. 再去找到版本对应的[chromedriver](https://chromedriver.storage.googleapis.com/index.html)下载到本地。
2.4. 解压这个文件包之后，把chromedriver这个文件挪去你的python安装路径，比如`usr/local/bin/`。
2.5. 如果显示无法打开“python3.8”，那是因为MacOS里无法验证开发者，你可以跑`xattr -d com.apple.quarantine usr/local/bin/chromedriver`
```
3. 如果是MacOS系统用户，需要通过`brew install python-tk`安装_tinker

## 使用说明
1. 抢购前需要校准本地时间，然后把需要抢购的商品加入购物车  
2. 如果要打包成可执行文件，可使用pyinstaller自行打包  
3. 不需要打包的，直接在项目根目录下 执行 python3 main.py  
4. 程序运行后，会打开淘宝登陆页，需要自己手动点击切换到扫码登陆  

## 其他
### 淘宝有针对selenium的检测，如果遇到验证码说明被反爬了，遇到这种情况应该换一个方案，凡是用到selenium的都会严重依赖网速、电脑配置。
### 如果想直接绕过淘宝的检测，可以手动打开浏览器登陆淘宝，然后再用selenium接管浏览器。只提供思路，具体实现大佬们可以自己摸索。

