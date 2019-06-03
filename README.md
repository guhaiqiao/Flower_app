# Flower_app

<style>table th:first-of-type {width: 10px;}</style>
<style>table th:nth-of-type(2) {width: 100px;}</style>
<style>table th:nth-of-type(3) {width: 80px;}</style>
<style>table th:nth-of-type(4) {width: 90px;}</style>
<style>table th:nth-of-type(5) {width: 60px;}</style>
| URL                       | 用途          | 接收参数                                                                | 返回参数(成功)                                                                                                  | 返回参数(失败) |
| ------------------------- | ------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | -------------- |
| **/index**                | 首页          | None                                                                    | msg, pictures                                                                                                   | None           |
| **/auth/register**        | 注册          | phone_number, password                                                  | msg                                                                                                             | msg, error     |
| **/auth/login**           | 登陆          | phone_number, password                                                  | msg, id, phone_number, password, sex, nickname, level, EXPoint, friend, age, region, personal_description, head | msg, error     |
| **/auth/personal_info**   | 修改个人信息  | id, phone_number, nickname, img, personal_description, sex, age, region | msg, id, phone_number, nickname, img, sex, personal_description, age, region                                    | msg, error     |
| **/auth/password_update** | 修改密码      | id, new_password, old_password                                          | msg, new_password                                                                                               | msg, error     |
| **/auth/query**           | 查询某一用户  | id, type('phone_number' or 'nickname'), User                            | msg, phone_number, nickname, level, EXPoint, personal_description, sex, age, region, head                       | msg, error     |
| **/auth/friend**          | 添加/删除好友 | id, type, method('add' or 'delete'), friend                             | msg, friends                                                                                                    | msg, error     |
| **/auth/logout**          | 登出          | id                                                                      | msg                                                                                                             | msg, error     |
| **/auth/check_status**    | 检查登录状态  | id                                                                      | flag                                                                                                            | None           |
| **/blog/get_all**         | 获取所有blog  | None                                                                    | msg, blogs                                                                                                      | None           |
| **/blog/create**          | 发表blog      | id, title, body, image                                                  | msg                                                                                                             | msg, error     |
| **/blog/like**            | 点赞某一blog  | id, p_id                                                                | msg                                                                                                             | msg, error     |
| **/flower/query**         | 查询某种花    | flower_name                                                             | msg, cn_name, en_name, type, description, flower_language, image, price, similar, combined                      | msg, error     |

