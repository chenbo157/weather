project/
├── app.py                  # FastAPI 后端主程序
├── requirements.txt        # Python依赖包列表
├── templates/
│   └── index.html          # 前端 HTML 页面
├── static/                 # 静态资源（JS、CSS）
├── split/                  # 按天拆分的 NetCDF 数据文件夹
├── Dockerfile              # Docker 构建脚本
├── split_nc.py             # 按天拆分的 NetCDF 数据代码
├── extract_lz4.py          # 解压代码
└── README.md               # 项目说明


1. 克隆项目
git clone https://github.com/chenbo157/weather.git
cd weather

2. 准备数据
确保 split/ 目录中已经有按日期拆分的 NetCDF 文件，例如：
split/
├── day_2025-06-01.nc
├── day_2025-06-02.nc
└── ...

3. 本地运行（可选）
pip install -r requirements.txt
uvicorn main:app

4. 使用 Docker 部署
构建镜像 
docker build -t weather_v1 .
运行容器（挂载数据）
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/split:/app/split \
  --name weather_container \
  weather_v1
访问：http://localhost:8000

