## 简单的消息队列处理Worker服务 ##
---
> 使用 `Python` 实现的一个基于 `Redis消息队列` 的 `异步` Worker服务.  
> 一个极度简单且可分布式的异步协同处理服务, 完全支持pypy.
> 
 
### 适用场景: 
---  
> * 同步进程中的非阻塞异步任务处理. 如: 发邮件, 推送消息,发短信验证码等.  
> * 分布式任务调度,跨机器协同处理同类任务.  
> * 实在编不下去了...

### 目前已支持服务:
---
> * `JPUSH` 极光消息推送  
> * `Baidu` 百度短信服务  
> 
> 其实只要去写个Worker处理一下具体任务, 就可以干活了,真的简单到没有朋友了... 



## mService.py ##
> 守护处理Workers
> 多进程
> mService.silent.sh 安静模式 (Supervisor时托管使用)
> mService.verbose.sh 啰嗦模式 (Debugging时使用)

--------------

## scheduler.py ##
>  测试添加数据到Worker
>  TaskServer依赖本程序

--------------

## TaskServer.py ##
> 开启一个http服务来承接外部程序添加任务到Worker队列
> 默认为 http://127.0.0.1:5000
> 外部使用请用nginx 做反向代理

--------------

##  其他 ##
```
task/scheduler  Task Enqueue  (for scheduler, TaskServer)
task/worker     Task Worker   (for mService)

tool/clean.py              Debugging时, 清除pyo,pyc,log文件
tool/check.py              代码规范检测, 有第三方库,基本无用
tool/requires_install.sh   自动安装Python库依赖
tool/redis_clean.sh        Ubuntu下, 强制清楚redis数据.就是删除dump.rdb后重启
```