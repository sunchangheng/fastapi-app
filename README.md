


## 快速开始

1. **安装依赖**

   ```shell
   pip install -r requirements.txt
   ```

2. **数据库迁移**

   ```shell
   alembic revision --autogenerate -m "first commit"	# 生成一个迁移文件
   alembic upgrade head	# 将迁移文件映射到数据库
   ```

3. **运行**

   ```shell
   uvicorn app.main:app --reload
   ```


## 接口相关

**Swagger UI**：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**ReDoc**：[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)


## TODO列表
- [x] SQLAlchemy+MySQL
- [x] token验证
- [x] alembic数据库迁移
- [ ] Celery 队列,定时任务等


## 项目结构

> 本项目目录结构参考 [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql) 生成的简洁版后端框架

```shell
.
├── README.md
├── __init__.py
├── alembic					# 数据库迁移
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── alembic.ini
├── app
│   ├── api					# 业务逻辑
│   │   ├── __init__.py
│   │   ├── api_v1
│   │   │   ├── __init__.py
│   │   │   ├── endpoints
│   │   │   │   ├── __init__.py
│   │   │   │   ├── items.py
│   │   │   │   ├── login.py
│   │   │   │   └── users.py
│   │   │   └── routers.py
│   │   └── deps.py
│   ├── core				# 配置文件 + Token操作
│   │   ├── config.py
│   │   └── security.py
│   ├── crud				# 数据库crud
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── item.py
│   │   └── user.py
│   ├── db					# 数据库相关
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── base_class.py
│   │   └── session.py
│   ├── models				# ORM models
│   │   ├── __init__.py
│   │   ├── item.py
│   │   └── user.py
│   ├── schemas				# schemas for using in web routes.
│   │   ├── __init__.py
│   │   ├── item.py
│   │   ├── token.py
│   │   └── user.py
│   └── services
├── main.py
└── requirements.txt
```


## 相关项目

**官方全栈项目框架生成器：** [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql)

**fastapi-realworld-example-app：**[fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app)

