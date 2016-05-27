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