from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import xarray as xr
import numpy as np
import pandas as pd
import uvicorn
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

# 挂载静态目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 设置模板目录
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class WeatherRequest(BaseModel):
    lat: float
    lon: float
    time: str
    vars: List[str]
    hours: Optional[int] = 24
    resolution: Optional[int] = 1


@app.post("/weather")
def get_weather(req: WeatherRequest):
    try:
        # date_str_raw = "2025-06-01T00:00:00Z"
        date = pd.to_datetime(req.time)
        date_str = date.strftime("%Y-%m-%d")

        # 预加载数据（可以改为延迟加载或切片加载以节省内存）
        ds = xr.open_dataset(f"split/day_{date_str}.nc", engine="netcdf4")

        # 将输入时间统一为 pandas Timestamp，再转换为 numpy.datetime64
        start_time = pd.to_datetime(req.time)
        start_time_np = np.datetime64(start_time)
        end_time_np = start_time_np + np.timedelta64(req.hours - 1, "h")

        result = {
            "lat": req.lat,
            "lon": req.lon,
            "start_time": start_time.isoformat(),
            "data": {}
        }

        for var in req.vars:
            if var not in ds:
                continue  # 忽略无效变量

            var_data = ds[var].sel(
                latitude=req.lat,
                longitude=req.lon,
                method="nearest"
            ).sel(time=slice(start_time_np, end_time_np))


            # values = [
            #     {
            #         "time": pd.to_datetime(str(t)).isoformat(),
            #         "value": float(v)
            #     }
            #     for t, v in zip(var_data["time"].values, var_data.values)
            # ]
            #
            # result["data"][var] = {
            #     "unit": ds[var].attrs.get("units", ""),
            #     "values": values
            # }

            # 应用 resolution 下采样（按索引步长切片）
            res = req.resolution
            times = var_data["time"].values[::res]
            vals = var_data.values[::res]

            values = [
                {
                    "time": pd.to_datetime(str(t)).isoformat(),
                    "value": float(v)
                }
                for t, v in zip(times, vals)
            ]

            result["data"][var] = {
                "unit": ds[var].attrs.get("units", ""),
                "values": values
            }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
