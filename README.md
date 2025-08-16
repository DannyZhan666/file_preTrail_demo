# file_preTrail_demo

# 项目说明

## 前端运行流程
1. 使用 npm 安装依赖：
   ```bash
   npm install

2. 启动前端项目：
   ```bash
   npm run serve

## 后端运行流程
1. 使用 pip 安装依赖
   ```bash
   pip install -r requirements.txt
3. 复制.env到项目的根目录（app）中
   ```bash
   -->直接拷贝即可，什么配置都不需要
   -->拷贝到根目录，与requirements.txt同级
5. 配置好数据库mysql
   ```bash
   -->使用ide连接数据库，如果没有mysql则需要另外下载
   -->使用file_task.sql中的DDL，复制到console中，创建mysql数据库
   -->数据在data文件夹中，复制到console中进行数据插入
7. 运行main.py中的if __name__函数
   ```bash
   if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1",port=8000)

## 网页对应前端文件
1. 主页面
```bash
src/pages/HomePage.vue
```
2. 注册页面
```bash
src/pages/user/userRegisterPage.vue
```
3. 登录页面
```bash
src/pages/user/userLogin.vue
```
-----------------------------------
客户
1. 已建工单
```bash
src/pages/client/JobManage.vue
```
2. 已接工单
```bash
src/pages/client/NewJobListForClient.vue
```
3. 工单创建
```bash
src/pages/client/JobCreate.vue

```
4. 订单管理
```bash
src/pages/client/OrderList.vue
```
5. 律师列表
```bash
src/pages/client/LawyerList.vue
```
6. 个人信息
```bash
src/pages/client/UserInfo.vue
```
7. 工单详情（已接）
```bash
src/pages/client/JobDetails_client_origin.vue
```
8. 工单详情（未接）
```bash
src/pages/client/JobDetails_client_accept.vue
```
9. 订单详情
```bash
src/pages/client/orderDetails_client.vue
```
-----------------------------------
律师
1. 工单列表
```bash
src/pages/lawyer/JobList.vue
```
2. 工单列表（已确认）
```bash
src/pages/lawyer/JobListForAccept.vue
```
3. 订单管理
```bash
src/pages/lawyer/OrderList_lawyer.vue
```
4. 个人信息
```bash
src/pages/lawyer/UserInfo_lawyer.vue
```
5. 工单详情（未接）
```bash
src/pages/lawyer/JobDetails.vue
```
6. 工单详情（已接）
```bash
src/pages/lawyer/JobDetailsForAccept.vue
```

## 功能对应后端文件
1. 用户功能
```bash
app/api/user.py
```
2. 文件上传功能
```bash
app/api/file.py
```
3. 工单功能
```bash
app/api/job.py
```
4. 订单功能
```bash
app/api/order.py
```

## 前端重要文件说明（src目录下）
1. api：包含client和user的请求方法
   ```bash
   ex：用户注册请求
   
   export const userRegister = async (params: any) => {
   return await myAxios.request({
    url: "/user/register",
    method: "POST",
    data: params,
   });
   };
2. assets：项目中用到的图片
3. components：网页的页眉和页脚
   ```bash
   Globalheader_user
   
4. layouts：网页的主要框架
5. models：用户类别
6. pages:里面包含client/lawyer/user
   ```bash
   user:
   
   注册 --> userRegisterPage
   登录 --> userLogin
   ```
-------------------------------
   ```bash
   律师页面 --> lawyer文件
   客户页面 --> client文件
   ```
7. router: 路由文件，控制网页之间的跳转
8. services：与api类似，优化时可以将两个合并
9. states与store：变量状态的存储
10. views：没有使用到

## 后端重要文件说明
1. api：接口层
```bash
接口名称对应其功能
```
3. service：数据处理层
4. core：用户&数据库配置
5. data：mysql数据
6. models：对应数据库的对象
7. schemas：Python中处理的对象
8. utils：工具类
```bash
-->阿里云配置
-->报错信息处理
-->分页配置
-->结果统一生成
```
