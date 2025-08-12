# file_preTrail_demo

# 项目运行说明

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
