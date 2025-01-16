## QUICK START
### CLONE

```sh
git clone git@github.com:MypreferORG/Finance.git

cd Finance
```
### CONFIG

修改`.env`文件中的`MYSQL_HOST` `CACHE_HOST`

### BUILD & RUN

#### DOCKER 自动部署

```sh
docker compose up --build
```
或 后台运行:
```sh
docker compose up --build -d
```

第一次运行后, 再次运行可以不带`--build`参数

#### 手动部署

```sh
conda create -n <env_name> python=3.8.20

conda activate <env_name>

pip install -r requirements.txt

python main.py
```

