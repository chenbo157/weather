import xarray as xr

# 打开 NetCDF 文件（建议使用 dask 延迟加载）
ds = xr.open_dataset("./2025-06-01T00_00_00_cn_flatted.nc")
try:
	# 查看变量
	print(ds)               # 显示整个文件的结构
	print("-"*100)
	print(ds.variables)     # 所有变量（气象要素）

	# # 示例：查看温度字段
	# print(ds['t2m'])        # t2m: 2 meter temperature
	#
	# # 读取时间、纬度、经度
	# print(ds.time.values)   # 时间坐标
	# print(ds.latitude.values)    # 纬度数组
	# print(ds.longitude.values)    # 经度数组

	# latitude = 17.01
	# longitude = 120.2
	#
	# # 创建一个 dict 保存所有变量的时间序列
	# all_point_data = {}
	#
	# for var in ds.data_vars:
	# 	try:
	# 		data = ds[var].sel(latitude=latitude, longitude=longitude, method='nearest')
	# 		all_point_data[var] = {}
	# 		for t, v in zip(data.time.values, data.values):
	# 		# 存储每个变量的时间序列数据
	# 			all_point_data[var][str(t)] = float(v)
	# 			print(var, ":", str(t), "=", float(v))
	# 	except Exception as e:
	# 		print(f"跳过变量 {var}: {e}")
except Exception as e:
	print(e)

ds.close()
