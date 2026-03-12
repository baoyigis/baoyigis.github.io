---
layout: post
title: "Lesson 1: OSMnx 实战 - 从数据获取到空间分析"
permalink: /blog/2026/lesson1/
date: 2026-03-12 16:00:00 +0800
categories: [空间分析, Python]
tags: [OSMnx, GeoPandas, 空间数据, Python, 坐标系]
---

## 第一部分：课前技术博客 (Pre-class Technical Blog)

### 1. 引言：从 GUI 到 Code 的思维转变

在 Lesson 0 中，我们搭建了现代空间数据科学环境。今天，我们将进入实战环节——**从零开始完成一个完整的空间分析流程**。

传统的 GIS 课程往往从"打开软件、加载数据、点击按钮"开始。但在真实的数据科学工作中，我们面临的是更复杂的挑战：

- **数据从哪里来？** 不是老师给的 Shapefile，而是需要从开放数据源（如 OpenStreetMap）实时获取
- **数据质量如何？** 众包数据存在缺失值、拓扑错误、坐标系不一致等问题
- **如何保证可复现？** 点点鼠标的操作难以记录，代码才能确保分析流程透明

本节课将以**苏州市姑苏区**为例，演示一个完整的工作流：**数据下载 → 格式转换 → 坐标系投影 → 拓扑检查 → 空间分析**。

### 2. 工具链：OSMnx + GeoPandas

| 工具 | 定位 | 核心功能 |
|------|------|----------|
| **OSMnx** | OpenStreetMap 数据获取 | 下载路网、POI、建筑等矢量数据 |
| **GeoPandas** | 空间数据处理 | 读写、投影转换、空间运算 |
| **Shapely** | 几何操作 | 拓扑关系判断、缓冲区计算 |
| **Folium** | 交互式可视化 | Web 地图渲染 |

**技术栈关系**：

```
OSMnx (数据获取)
    ↓
GeoPandas (数据处理)
    ├── 坐标系转换 (pyproj)
    ├── 几何操作 (Shapely)
    └── 空间连接 (rtree)
        ↓
Folium (交互式可视化)
```

### 3. 为什么选择 OpenStreetMap？

OpenStreetMap (OSM) 是全球最大的开源地图项目，具有以下优势：

1. **免费开放**：无需 API Key，数据完全免费
2. **覆盖全球**：包括中国在内的全球数据
3. **持续更新**：社区驱动，数据质量不断提升
4. **丰富标签**：道路类型、POI 分类、建筑属性等

**OSM 数据模型**：
- **Node (节点)**：点要素（如 POI、路口）
- **Way (路径)**：线/面要素（如道路、建筑轮廓）
- **Relation (关系)**：复杂要素（如公交线路、行政边界）

---

## 第二部分：课堂实操 Notebook (In-class Lab)

**文件名**：`Week2_OSMnx_Spatial_Analysis.ipynb`

**教学目标**：掌握 OSMnx 数据获取、坐标系转换、拓扑检查、空间分析的完整流程。

### 1. 数据下载：获取苏州市姑苏区路网

**Step 1：导入库**

```python
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt

print(f"OSMnx version: {ox.__version__}")
print(f"GeoPandas version: {gpd.__version__}")
```

**Step 2：下载路网数据**

```python
# 设置地点（苏州市姑苏区）
place_name = "Gusu District, Suzhou, China"

# 下载路网（drive类型 = 机动车道路）
print("正在下载路网数据...")
G = ox.graph_from_place(place_name, network_type='drive')

# 转换为 GeoDataFrame（只保留边，不保留节点）
roads_gdf = ox.graph_to_gdfs(G, nodes=False)

print(f"路网记录数: {len(roads_gdf)}")
print(f"路网坐标系: {roads_gdf.crs}")
```

**输出示例**：
```
正在下载路网数据...
路网记录数: 5949
路网坐标系: epsg:4326
```

**关键技术点**：
- `network_type` 参数：
  - `'drive'`：机动车道路
  - `'walk'`：步行道路
  - `'bike'`：自行车道
  - `'all'`：所有道路
- `graph_to_gdfs()` 返回两个 GeoDataFrame：节点（nodes）和边（edges）
- OSMnx 默认使用 **WGS84 (EPSG:4326)** 坐标系

### 2. 数据保存：多格式对比

**Step 3：保存为 GeoJSON 和 GeoPackage**

```python
import os

# 创建输出目录
output_dir = 'data/suzhou_gusu'
os.makedirs(output_dir, exist_ok=True)

# 保存为 GeoJSON
roads_gdf.to_file(f'{output_dir}/roads.geojson', driver='GeoJSON')

# 保存为 GeoPackage
roads_gdf.to_file(f'{output_dir}/roads.gpkg', driver='GPKG')

# 对比文件大小
def get_file_size(filepath):
    """获取文件大小（KB）"""
    return os.path.getsize(filepath) / 1024

print("文件大小对比:")
print(f"  roads.geojson: {get_file_size(f'{output_dir}/roads.geojson'):.1f} KB")
print(f"  roads.gpkg:    {get_file_size(f'{output_dir}/roads.gpkg'):.1f} KB")
```

**格式对比**：

| 格式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **GeoJSON** | 文本格式、易读、Web 友好 | 文件较大、单文件 | Web 开发、数据交换 |
| **GeoPackage** | 单文件、压缩率高、支持栅格 | 二进制格式、不易读 | 大数据存储、本地分析 |
| **Shapefile** | 兼容性好 | 多文件、字段名限制、2GB 上限 | ❌ 遗留系统（不推荐） |

**思考题**：为什么 GeoPackage 文件更小？（答案：列式存储 + 压缩）

### 3. 坐标系转换：从 WGS84 到 UTM

**Step 4：计算投影坐标系**

苏州市姑苏区位于东经 120.5°，应该使用 **UTM Zone 51N**（EPSG:32651）。

**UTM 分带规则**：
- 经度范围：`zone = floor((longitude + 180) / 6) + 1`
- 苏州：`floor((120.5 + 180) / 6) + 1 = 51`

```python
# 查询坐标系信息
print(f"原始坐标系: {roads_gdf.crs}")
print(f"EPSG:4326 = WGS84 (经纬度坐标)")

# 转换为 UTM Zone 51N
roads_utm = roads_gdf.to_crs(epsg=32651)

print(f"\n转换后坐标系: {roads_utm.crs}")
print(f"EPSG:32651 = WGS84 / UTM Zone 51N (投影坐标)")
```

**Step 5：计算道路长度（单位：米）**

```python
# 计算道路长度（只有在投影坐标系下才有意义）
roads_utm['length_m'] = roads_utm.geometry.length

print(f"道路长度统计:")
print(f"  总长度: {roads_utm['length_m'].sum():.1f} 米")
print(f"  平均长度: {roads_utm['length_m'].mean():.1f} 米")
print(f"  最长道路: {roads_utm['length_m'].max():.1f} 米")
```

**为什么必须转换坐标系？**

- **WGS84 (EPSG:4326)**：经纬度坐标，单位是度
  - 1° 经度 ≈ 111 km × cos(纬度)
  - 在苏州（31°N）：1° 经度 ≈ 95 km
  - 直接计算距离会得到错误的单位（度）
- **UTM (EPSG:32651)**：投影坐标，单位是米
  - x, y 坐标直接表示距离
  - 计算长度、面积才有物理意义

### 4. POI 数据获取与清洗

**Step 6：下载餐饮 POI**

```python
# 下载餐饮 POI
print("正在下载餐饮POI...")
restaurants = ox.features_from_place(
    place_name, 
    tags={"amenity": "restaurant"}
)

print(f"餐饮POI数: {len(restaurants)}")
print(f"POI坐标系: {restaurants.crs}")
```

**Step 7：数据清洗**

```python
# 转换为 UTM 坐标系
restaurants_utm = restaurants.to_crs(epsg=32651)

# 删除无名称的记录
restaurants_clean = restaurants_utm[restaurants_utm['name'].notna()].copy()

print(f"\n数据清洗:")
print(f"  清洗前POI数: {len(restaurants_utm)}")
print(f"  清洗后POI数: {len(restaurants_clean)}")

# 检查几何类型
print(f"\n几何类型分布:")
print(restaurants_clean.geometry.type.value_counts())
```

**常见清洗操作**：

| 操作 | 代码 | 说明 |
|------|------|------|
| **删除缺失值** | `gdf.dropna(subset=['name'])` | 删除指定字段为空的记录 |
| **删除重复值** | `gdf.drop_duplicates(subset=['osmid'])` | 按 OSM ID 去重 |
| **修复拓扑错误** | `gdf['geometry'].buffer(0)` | 修复自相交等错误 |
| **筛选几何类型** | `gdf[gdf.geometry.type == 'Point']` | 只保留点要素 |

### 5. 空间分析：缓冲区与叠加

**Step 8：创建道路缓冲区**

```python
# 创建 50 米缓冲区
roads_utm['buffer_50m'] = roads_utm.geometry.buffer(50)

print("✅ 已创建50米缓冲区")
```

**Step 9：空间连接 - 找出缓冲区内的餐厅**

```python
# 将缓冲区设为几何列
roads_buffer_gdf = roads_utm[['osmid', 'name', 'buffer_50m']].copy()
roads_buffer_gdf = roads_buffer_gdf.set_geometry('buffer_50m')
roads_buffer_gdf.crs = roads_utm.crs

# 空间连接
restaurants_near_roads = gpd.sjoin(
    restaurants_clean,
    roads_buffer_gdf,
    how='left',
    predicate='within'
)

# 统计每条道路附近的餐厅数量
restaurant_count = restaurants_near_roads.groupby('osmid').size()
roads_utm['restaurant_count'] = roads_utm['osmid'].map(restaurant_count).fillna(0).astype(int)

print(f"\n道路餐厅统计:")
print(f"  有餐厅的道路: {(roads_utm['restaurant_count'] > 0).sum()} 条")
print(f"  最多餐厅的道路: {roads_utm['restaurant_count'].max()} 家")
```

**空间连接类型**：

| Predicate | 含义 | 示例 |
|-----------|------|------|
| `within` | A 完全在 B 内 | 餐厅在缓冲区内 |
| `intersects` | A 与 B 相交 | 餐厅与缓冲区有交集 |
| `contains` | A 完全包含 B | 行政区包含 POI |
| `touches` | A 与 B 边界接触 | 地块相邻 |

### 6. 可视化

**Step 10：绘制路网与餐厅分布图**

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 10))

# 绘制道路（按餐厅数量着色）
roads_utm.plot(
    ax=ax,
    column='restaurant_count',
    cmap='YlOrRd',
    linewidth=2,
    legend=True,
    legend_kwds={'label': '餐厅数量'}
)

# 绘制餐厅
restaurants_clean.plot(
    ax=ax,
    markersize=30,
    color='blue',
    alpha=0.7,
    marker='o',
    label='餐厅'
)

ax.set_title('苏州市姑苏区路网与餐饮分布', fontsize=14, fontweight='bold')
ax.legend(loc='upper right')
ax.set_xlabel('东向 (m)')
ax.set_ylabel('北向 (m)')

plt.tight_layout()
plt.savefig(f'{output_dir}/road_restaurant_analysis.png', dpi=300)
plt.show()

print(f"\n✅ 可视化已保存到 {output_dir}/road_restaurant_analysis.png")
```

### 7. 进阶：九交模型（DE-9IM）

**拓扑关系的数学基础**

九交模型（Dimensionally Extended 9-Intersection Model）是描述两个几何对象拓扑关系的标准方法。

**矩阵结构**：

```
        B Interior | B Boundary | B Exterior
    -------------------------------------------
A Interior |    II    |     IB     |    IE
A Boundary |    BI    |     BB     |    BE
A Exterior |    EI    |     EB     |    EE
```

**维度编码**：
- `2`：面（2维）
- `1`：线（1维）
- `0`：点（0维）
- `F`：空（False）

**示例：重叠关系**

```python
from shapely.geometry import Polygon

# 创建两个重叠的正方形
poly1 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
poly2 = Polygon([(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)])

# 计算九交矩阵
matrix = poly1.relate(poly2)
print(f"九交矩阵: {matrix}")
# 输出: '212101212'

# 判断拓扑关系
print(f"是否相交: {poly1.intersects(poly2)}")  # True
print(f"是否重叠: {poly1.overlaps(poly2)}")    # True
print(f"是否包含: {poly1.contains(poly2)}")    # False
```

---

## 第三部分：坐标系偏移问题（中国特有）

### 火星坐标系

在中国使用地图服务时，你会发现一个奇怪的现象：**GPS 坐标和地图上的位置不匹配**。这是因为中国使用了加密的坐标系。

**三种坐标系**：

| 坐标系 | 说明 | 使用者 |
|--------|------|--------|
| **WGS84** | GPS 原始坐标 | OpenStreetMap、Google Earth |
| **GCJ-02** | 加密坐标（火星坐标） | 高德地图、腾讯地图 |
| **BD-09** | 二次加密 | 百度地图 |

**偏移示例**：

```python
# 南京大学鼓楼校区
wgs_lon, wgs_lat = 118.7969, 32.0603

# WGS84 → GCJ-02
gcj_lon, gcj_lat = wgs_to_gcj(wgs_lon, wgs_lat)

print(f"WGS84: ({wgs_lon:.6f}, {wgs_lat:.6f})")
print(f"GCJ-02: ({gcj_lon:.6f}, {gcj_lat:.6f})")
print(f"偏移距离: ~{(gcj_lon - wgs_lon) * 111000:.1f} 米")
```

**实际影响**：
- 使用 Google Maps 在中国导航时，道路和底图错位
- 从百度地图导出的坐标无法直接用于 OSMnx 分析
- **解决方案**：统一使用 WGS84 坐标系，必要时进行坐标转换

---

## 第四部分：总结与作业

### 本节课要点

1. **数据获取**：OSMnx 可以快速下载 OpenStreetMap 数据
2. **数据格式**：GeoJSON（Web友好） vs GeoPackage（高效存储）
3. **坐标系转换**：WGS84 → UTM，计算距离/面积才有意义
4. **数据清洗**：缺失值、重复值、拓扑错误
5. **空间分析**：缓冲区、空间连接、拓扑关系

### 完整工作流

```
1. 数据获取 (OSMnx)
   ↓
2. 数据保存 (GeoJSON/GeoPackage)
   ↓
3. 坐标系转换 (WGS84 → UTM)
   ↓
4. 数据清洗 (去重、补缺、修复)
   ↓
5. 空间分析 (缓冲区、叠加、拓扑)
   ↓
6. 可视化 (matplotlib/folium)
```

### 参考资料

- [OSMnx 官方文档](https://osmnx.readthedocs.io/)
- [GeoPandas 官方文档](https://geopandas.org/)
- [EPSG.io - 坐标系查询](https://epsg.io/)
- [OpenStreetMap Wiki](https://wiki.openstreetmap.org/)
