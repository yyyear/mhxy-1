# mhxy
爬取梦幻西游藏宝阁寄售账号信息

项目简单，可以直接运行爬虫
主要参数说明：
'_' : 时间戳， 代码中已使用time模块进行封装
'level_min&max': 账号等级区间， 可选69 89 109 129 159 175
'page': 页码可以动态输入
其他参数为固定参数


这里个人不建议登录爬取：
  1.携带cookie一方面没有现成的cookie池，
  2.此方案采用代理池与随机User_agent进行爬取，同一个cookie不间断更换Ip与User_agent容易触发将军令验证（网易1分钟随机变更的验证码）


无账号爬取，合理的控制爬取速度个人验证没有出现过验证码反爬

使用账号昵称作为_id主键插入mongodb能够对重复出现的账号进行简单过滤，已存在账号将不会插入到数据库中
一般搜索后只提供100页数据，页码也可以根据个人设置

爬虫使用的IP代理池项目内容可以在我另外的IPProxyPool项目中查看