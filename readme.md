# mitm_server_for_QL
## How to install

#### 进入青龙容器，以下在容器内执行命令
#### docker exec -it qinglong bash
#### 安装依赖
#### npm config set registry https://registry.npm.taobao.org && apk add --no-cache build-base g++ cairo-dev pango-dev giflib-dev python3 zlib-dev gcc jpeg-dev python3-dev musl-dev freetype-dev libressl-dev musl-dev libffi-dev openssl-dev gcompat && npm install -g npm png-js date-fns axios crypto-js ts-md5 tslib @types/node requests tough-cookie jsdom download tunnel fs ws form-data && pip3 install wheel requests tomli tomli_w toml jieba aiohttp pywebio==1.5.2 mitmproxy==5.3.0 markupsafe==2.0.1 -i https://pypi.douban.com/simple --trusted-host=pypi.douban.com
#### 初始化
#### git clone https://github.com/HanEightTurtle/mitm_server_ql.git /ql/scripts/HanEightTurtle_mitm_server_ql_main
#### cd /ql/scripts/HanEightTurtle_mitm_server_ql_main
#### mkdir tomls
#### mkdir temp
#### mkdir .mitmproxy
#### 运行一次mitmdump，会自动在/root/.mitmproxy生成证书
#### mitmdump
#### 把证书拷贝到当前目录，其中mitmproxy-ca.pem拷给手机用，p12给windows
#### \cp -rf /root/.mitmproxy/* .mitmproxy/
#### 退出交互模式
#### 编辑青龙容器配置 文件位置 ql/qlconf.toml
#### 拉库，有支持新的抓包阔以及时更新
#### ql repo https://github.com/HanEightTurtle/mitm_server_ql.git "main" "" "addons|Oreomeow_checkinpanelql|mitm_utils|myfunc|notify_mtr" "main"
#### 禁用main脚本，然后启动main脚本阔以一直挂起
#
## How to use
#### 容器40082端口是web界面，需要通过web界面发起抓包请求，不同用户用以区别和不重复抓包
![image](https://github.com/HanEightTurtle/mitm_server_ql/raw/main/IMG/login.png)
#### 点击抓包后，会在容器40080端口开放http代理，用户名和密码即为http认证
#### 40081端口阔以显示抓包信息
![image](https://github.com/HanEightTurtle/mitm_server_ql/raw/main/IMG/mitmweb.png)
#### 抓包完成后，会优先读取用户toml里的通知参数，然后通知，如果用户没有添加通知参数，会读取容器环境变量
#### 添加通知参数的步骤：点击编辑，在AppData里添加(通知可用参数同config.sh)
#### [["通知"]]
#### QYWX_AM = “xxxxx”
#### PUSH_KEY = "xxxx"
#
## 开发教程
#### 如果需要为新的sheep fur抓包，需要修改的地方有
#### addons文件夹添加新的addon
#### 如果是为Oreomeow_checkinpanel抓包，不需要做更改，如果抓包要求类似“'xxx=yyy'多用户用'@'隔开”这种，需要去ql/ql_sample.py添加相应格式

