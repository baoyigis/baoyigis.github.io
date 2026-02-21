---
layout: post
title: "Lesson 0: 构建现代空间数据科学环境"
permalink: /blog/2025/lesson0/
date: 2026-02-06 10:00:00 +0800
categories: [空间分析, 环境配置]
tags: [VSCode, uv, Python, GeoPandas, 空间分析]
---

## 第一部分：课前技术博客 (Pre-class Technical Blog)

### 1. 引言：工程化思维的引入

在理论课程中，我们讨论了空间分析从定性描述向定量计算的演进。为了处理大规模、高异质性的地理数据，我们需要从图形界面（GUI）转向脚本代码（Code）模式。这不仅是为了效率（如批量处理），更是为了确保分析过程的**可复现性 (Reproducibility)** 与 **可扩展性 (Scalability)**。

本学期我们将采用业界现代化的 Python 数据科学技术栈。

### 2. 工具链选型

我们精选了以下两款核心工具，旨在为您提供一个轻量、高效且标准化的开发环境：

- **Visual Studio Code (VS Code)**

  - **定位**：目前最主流的轻量级代码编辑器（IDE）
  - **作用**：提供代码编写、调试、Jupyter Notebook 渲染及文件管理功能

- **uv**
  - **定位**：基于 Rust 编写的高性能 Python 包与项目管理器
  - **优势**：相比传统的 Conda，uv 的依赖解析速度极快，且能通过 `uv.lock` 文件严格锁定环境版本，彻底解决"在他电脑上能跑，在我电脑上跑不通"的环境一致性问题

### 3. 环境配置指南 (Configuration Guide)

请按照以下步骤完成环境初始化。

#### Step 1: 安装基础软件

**1. 安装 VS Code**

访问 [code.visualstudio.com](https://code.visualstudio.com/) 下载并安装。

_配置插件_：启动 VS Code，点击左侧扩展图标（Extensions），搜索并安装 **Python** 和 **Jupyter** 插件。

**2. 安装 uv**

打开终端（Windows 用户请打开 PowerShell，Mac 用户打开 Terminal），复制并运行以下命令：

- **Windows**: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Mac/Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`

#### Step 2: 初始化课程项目

在你的磁盘中新建一个文件夹（例如命名为 `spatial_analysis`），在 VS Code 中打开该文件夹，然后使用 `Ctrl+~` (Mac 为 `Cmd+~`) 唤起内置终端，执行以下命令：

**1. 初始化项目环境**

```bash
uv init
```

此命令会创建 `pyproject.toml` 配置文件，用于记录项目依赖。

**2. 创建虚拟环境**

```bash
# 创建名为 .venv 的虚拟环境
uv venv
```

**3. 激活虚拟环境**

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

激活后，终端提示符前会显示 `(.venv)` 标识。

**4. 安装空间分析依赖栈**

```bash
uv add geopandas matplotlib folium mapclassify jupyterlab ipykernel geodatasets
```

**库说明**：

| 库名称        | 主要用途     | 核心功能                                         |
| :------------ | :----------- | :----------------------------------------------- |
| `geopandas`   | 空间数据处理 | 矢量数据读写、坐标转换、空间运算（交集、缓冲区） |
| `matplotlib`  | 静态可视化   | 绘制分级统计图、散点图、直方图等静态图表         |
| `folium`      | 交互式地图   | 生成交互式 Web 地图，支持缩放、平移、点击查询    |
| `mapclassify` | 统计分级     | 提供自然断点法、分位数法等数据分级算法           |
| `jupyterlab`  | 开发环境     | 代码执行、Markdown 文档、可视化预览              |
| `ipykernel`   | Jupyter 内核 | 连接 Python 虚拟环境与 Jupyter Notebook          |
| `geodatasets` | 示例数据集   | 提供纽约市行政区等空间分析示例数据               |

**技术栈关系**：

```
geopandas (空间数据处理)
    ├── matplotlib (静态可视化)
    ├── folium (交互式可视化)
    └── mapclassify (统计分级算法)

jupyterlab (开发环境容器)
```

**注意**：虚拟环境需要在激活状态下才能通过 `uv add` 安装依赖包。

#### Step 3: 验证环境

在终端输入以下命令启动 Jupyter Lab 服务，若浏览器自动弹出并显示界面，即表示配置成功：

```bash
uv run jupyter lab
```

---

## 第二部分：课堂实操 Notebook (In-class Lab)

**文件名**：`Lab1_Data_Structure_and_Visualization.ipynb`

**教学目标**：在 VS Code 中运行 Jupyter Notebook，理解矢量数据结构，实现静态与交互式地图渲染。

### 1. 环境连接与库导入 (Setup)

**操作提示**：
打开 `.ipynb` 文件后，点击右上角的 **Select Kernel**。在弹出的选项中，务必选择 **Python Environments** 下带有 `.venv` 标识的选项（这是 uv 创建的隔离环境）。

```python
# 导入空间数据处理核心库
import geopandas as gpd

# 导入绘图库，用于解决潜在的中文显示问题（可选）
import matplotlib.pyplot as plt

print("Environment loaded successfully.")
```

### 2. 数据加载 (Data Loading)

**注意**：GeoPandas 1.0+ 已移除内置数据集。使用 `geodatasets` 包获取示例数据：

```python
# 导入 geodatasets 包
import geodatasets

# 读取纽约市5个行政区边界数据
# nybb = New York Borough Boundaries
nybb = gpd.read_file(geodatasets.get_path('nybb'))

# 检查数据加载状态
print(f"Data CRS: {nybb.crs}")
print(f"Shape: {nybb.shape}")  # 5个行政区
print(f"Columns: {nybb.columns.tolist()}")

# 查看行政区名称
print(nybb[['BoroName', 'BoroCode']].head())
```

本课程使用 **纽约市行政区数据 (nybb)** 进行演示，数据量小且属性完整。

### 3. 核心数据结构解析 (The GeoDataFrame)

空间分析的核心在于理解 **GeoDataFrame** 结构。它在普通 DataFrame 的基础上增加了一个几何列。

```python
# 查看前 5 行数据
nybb.head()
```

**关键技术点解析**：

- **Attribute Columns (属性列)**：如 `BoroName` (行政区名), `BoroCode` (行政区代码)，与常规表格数据无异
- **Geometry Column (几何列)**：
  - 这是 GeoDataFrame 的核心
  - 存储格式通常为 WKT (Well-Known Text) 对象，如 `POLYGON ((...))`
  - 空间操作（如计算面积、求交集）均基于此列进行

### 4. 静态可视化 (Static Visualization)

基于 `matplotlib` 引擎的快速制图，用于数据探索。

```python
# 基础绘图：直接映射 Geometry 列
nybb.plot()

# 按行政区名称着色（类似分级统计图）
# column: 指定用于着色的属性列（此处为行政区名）
# legend: 显示图例
# figsize: 指定画布尺寸 (英寸)
nybb.plot(column='BoroName', legend=True, figsize=(10, 6), cmap='Set3')
```

### 5. 交互式可视化 (Interactive Visualization)

基于 `folium` (Leaflet.js) 的 Web 地图渲染。这对应了课件中提到的 **LBS (Location-Based Services)** 的前端展现形式。

```python
# 使用 .explore() 方法生成交互式地图
# 该方法会自动处理坐标投影转换，生成 Leaflet 地图对象
m = nybb.explore(
    column='BoroName',          # 按行政区名着色
    tooltip=['BoroName', 'BoroCode'], # 悬浮显示信息
    cmap='Set3',                # 配色方案
    tiles='CartoDB positron'    # 底图样式
)

# 渲染地图对象
m
```

**操作**：

- 尝试缩放和平移地图
- 观察这种可视化方式与静态图片的区别（更适合展示多尺度空间细节）

### 6. 总结 (Summary)

本节课我们完成了现代空间分析环境的搭建，并验证了从数据读取到交互式可视化的完整链路。

**Next Step**：

请确保你的 VS Code 能成功运行上述代码，并熟悉 Jupyter Notebook 的基本操作（Cell 的执行与新建），为下周深入的数据清洗课程做准备。
