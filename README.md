# Flower_app
## User
| URL                       | 用途          | 接收参数                                                                | 返回参数(成功)                                                                                                         | 返回参数(失败) |
| ------------------------- | ------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | -------------- |
| **/auth/register**        | 注册          | phone_number, password                                                  | msg                                                                                                                    | msg, error     |
| **/auth/login**           | 登陆          | phone_number, password                                                  | msg, error, id, phone_number, password, nickname, level, EXPoint, friend, personal_description, sex, age, region, head | msg, error     |
| **/auth/personal_info**   | 修改个人信息  | id, phone_number, nickname, img, personal_description, sex, age, region | msg, id, phone_number, nickname, img, personal_description, sex, age, region                                           | msg, error     |
| **/auth/password_update** | 修改密码      | id, new_password, old_password                                          | msg, new_password                                                                                                      | msg, error     |
| **/auth/query**           | 查询某一用户  | id, type, User                                                          | msg, phone_number, nickname, level, EXPoint, personal_description, sex, age, region, head                              | msg, error     |
| **/auth/friend**          | 添加/删除好友 | id, type, method, friend                                                | msg, friends                                                                                                           | msg, errr      |
| **/auth/logout**          | 登出          | id                                                                      | msg                                                                                                                    | msg, error     |
| **/auth/check_status**    | 检查登录状态  | id                                                                      | flag                                                                                                                   |

- **/auth/register**
  接收参数：phone_number, password

  返回参数：msg，若有error则返回error
- **/auth/login**

  接收参数：phone_number, password

  返回参数：

    成功则返回msg, id, phone_number, password, nickname, level, EXPoint, friend, personal_description, sex, age, region, head,

    失败则返回msg, error


- **/auth/personal_info**
