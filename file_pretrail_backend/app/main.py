
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import routes

app = FastAPI(title="Flower FastAPI Project")

# 配置 CORS
origins = [
    "http://localhost:3000",  # 前端开发服务器地址（Vue 或其他）
    # 如果你有生产环境，可以再加上允许的生产环境地址
    # "https://yourfrontenddomain.com",
]

# 添加 CORS 中间件，允许指定的来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的源
    allow_credentials=True,  # 是否允许携带 cookie
    allow_methods=["*"],  # 允许的 HTTP 方法 (GET, POST, PUT, DELETE, PATCH, etc.)
    allow_headers=["*"],  # 允许的头部
)
app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1",port=8000)