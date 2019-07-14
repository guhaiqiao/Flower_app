# Flower_app URL

**/index**

 首页

 接收参数：None

 返回参数（成功）：msg, pictures

    其中pictures为图片列表

 返回参数（失败）：None

**/index**

 首页筛选

 接收参数：like, dislike

 返回参数（成功）：msg, pictures

    其中pictures为图片列表

 返回参数（失败）：msg, error

**/auth/register**

 注册

 接收参数：phone_number, password

 返回参数（成功）：msg

 返回参数（失败）：msg, error

**/auth/login**

 登陆

 接收参数：phone_number, password

 返回参数（成功）：msg, id, phone_number, password, sex, nickname, level, EXPoint, friend, age, region, personal_description, head

 返回参数（失败）：msg, error

**/auth/personal_info**

 修改个人信息

 接收参数：id, phone_number, nickname, img, personal_description, sex, age, region

 返回参数（成功）：msg, id, phone_number, nickname, img, sex, personal_description, age, region

 返回参数（失败）：msg, error

**/auth/password_update**

 修改密码

 接收参数：id, new_password, old_password

 返回参数（成功）：msg, new_password

 返回参数（失败）：msg, error

**/auth/query**

 查询某一用户

 接收参数：id, type('phone_number' or 'nickname' or 'id'), user

 返回参数（成功）：msg, users

    其中users为字典的列表：phone_number, nickname, level, EXPoint, personal_description, sex, age, region, head

 返回参数（失败）：msg, error

**/auth/friend**

 添加/删除好友

 接收参数：id, type('phone_number' or 'nickname'), method('add' or 'delete'), friend

 返回参数（成功）：msg, friends

    其中friends为朋友的id列表

 返回参数（失败）：msg, error

**/auth/logout**

 登出

 接收参数：id

 返回参数（成功）：msg

 返回参数（失败）：msg, error

**/auth/check_status**

 检查登录状态

 接收参数：id

 返回参数（成功）：flag

 返回参数（失败）：None

**/blog/get_all**

 获取所有blog

 接收参数：None

 返回参数（成功）：msg, blogs

    其中blogs为字典列表 'id', 'title', 'body', 'created', 'author_id', 'nickname', 'like', 'liker', 'comment', 'image', 'image_size'
    liker为字典列表 'nickname', 'id'
    comment为字典列表 'nickname', 'id', 'comment'
    image，image_size为列表

 返回参数（失败）：None

**/blog/get_one**

 获取某一blog

 接收参数：p_id

 返回参数（成功）：msg, blog

    其中blog为字典 'id', 'title', 'body', 'created', 'author_id', 'nickname', 'like', 'liker', 'comment', 'image', 'image_size'
    liker为字典列表 'nickname', 'id'
    comment为字典列表 'nickname', 'id', 'comment'
    image，image_size为列表
 返回参数（失败）：msg, error

**/blog/create**

 发表blog

 接收参数：id, title, body, image

    其中image为用逗号分隔的图片字符串

 返回参数（成功）：msg

 返回参数（失败）：msg, error

**/blog/like**

 点赞某一blog

 接收参数：id, p_id

 返回参数（成功）：msg

 返回参数（失败）：msg, error

**/blog/comment**

 评论某一blog

 接收参数：id, p_id, comment

 返回参数（成功）：msg

 返回参数（失败）：msg, error

**/blog/image**

 查看大图

 接收参数：p_id, index

 返回参数（成功）：image, msg

 返回参数（失败）：msg, error

**/flower/query**

 查询某种花

 接收参数：flower_name

 返回参数（成功）：msg, cn_name, en_name, type, description, flower_language, image, price, similar, combined

 返回参数（失败）：msg, error

**/flower/auto_match**

 自动搭配

 接收参数：like, dislike, price

 返回参数（成功）：msg, flower(list)

 返回参数（失败）：msg, error


blog：'id', 'title', 'body', 'created', 'author_id', 'nickname', 'like', 'liker', 'comment', 'image', 'image_size'