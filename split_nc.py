import xarray as xr
import pandas as pd
import os

# 打开文件时默认是懒加载的（unless load() 被调用）
ds = xr.open_dataset("2025-06-01T00_00_00_cn_flatted.nc", engine="netcdf4")

# 确保输出目录存在
os.makedirs("split", exist_ok=True)

# 获取所有唯一日期
unique_dates = pd.to_datetime(ds.time.values).normalize().unique()

for date in unique_dates:
    # 用字符串格式化文件名
    date_str = date.strftime("%Y-%m-%d")
    output_path = f"split/day_{date_str}.nc"

    # 按天筛选数据，仍然是懒加载方式
    ds_day = ds.sel(time=slice(date, date + pd.Timedelta(days=1)))

    # 保存为新的 NetCDF 文件
    ds_day.to_netcdf(output_path)
    print(f"Saved: {output_path}")
