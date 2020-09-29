## 项目结构

> 本项目目录结构参考**官方全栈项目框架生成器**生成的简洁版后端框架

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
├── pyproject.toml
└── requirements.txt
```



## 快速开始

1. **安装依赖**

```shell
pip install -r requirements.txt
```

2. **数据库迁移**

   **参照下一大节**

3. **运行**

   ```shell
   uvicorn app.main:app --reload
   ```



## 数据库迁移

此项目使用`alembic`管理数据库

1. 先初始化`alembic`仓库

   ```shell
   # 项目根目录下
   alembic init alembic
   ```

   > 第一个alembic是alembic语法，类似git。第二个init代表初始化，第三个alembic代表仓库名，你也可以命名其它名字，这里为了方便理解，所以采用了alembic这一名字

   项目下多了一个**alembic文件夹**和**alembic.ini文件**

2. 找到`alembic.ini`配置文件,修改`sqlalchemy.url`

   ```shell
   sqlalchemy.url = mysql+pymysql://root:123456@localhost/face_api
   ```

   或者直接在`alembic/env.py`下增加

   ```shell
   config.set_main_option("sqlalchemy.url", str(settings.SQLALCHEMY_DATABASE_URI))	# 推荐
   ```

3. 找到`alembic/env.py`文件，修改`target_metadata`参数

   ```shell
   # 把当前项目路径加入到path中
   sys.path.append(os.path.dirname(os.path.dirname(__file__)))
   
   from app.db.base import Base    # noqa
   from app.core.config import settings    # noqa
   
   target_metadata = Base.metadata
   ```

4. **生成一个迁移文件**

   ```shell 
   # 终端
   alembic revision --autogenerate -m "first commit"
   ```

   创建成功会在version目录下创建一个迁移文件

5. **将迁移文件映射到数据库中**

   **注意：要先创建好数据库**

   ```shell
   alembic upgrade head
   ```




## 接口相关

**Swagger UI**：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**ReDoc**：[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)



## TODO列表
- [x] SQLAlchemy+MySQL
- [ ] token验证
- [x] alembic数据库迁移
- [ ] Celery 队列,定时任务等



## 相关项目

**官方全栈项目框架生成器：** [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql)

**GitHub上已经生成好的项目框架：**[fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app)

