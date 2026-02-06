# Blog样式问题解决方案

## 问题说明

删除模板blog后，blog页面可能看起来样式丢失，这是因为需要重新构建网站。

## 解决方案

### 1. 重新构建网站

```bash
# 清理旧构建
bundle exec jekyll clean

# 安装依赖
bundle install

# 构建网站
bundle exec jekyll build

# 启动本地服务器
bundle exec jekyll serve
```

### 2. 检查blog文章配置

确保blog文章的front matter包含必要的配置：

```yaml
---
title: "Lesson 0: 构建现代空间数据科学环境"
permalink: /blog/2025/lesson0/
date: 2025-02-06 10:00:00 +0800
categories: [空间分析, 环境配置]
tags: [VSCode, uv, Python, GeoPandas, 空间分析]
---
```

### 3. 代码高亮配置

Jekyll已配置使用Rouge作为代码高亮器：

```yaml
# _config.yml
markdown: kramdown
highlighter: rouge
kramdown:
  input: GFM
  syntax_highlighter_opts:
    css_class: "highlight"
```

### 4. 代码块格式

使用正确的Markdown代码块格式：

\```python
import geopandas as gpd
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
```

\```bash
uv add geopandas matplotlib folium
```

**重要提示**：
- 使用三个反引号 ` ``` `
- 指定语言名称（bash, python, yaml等）
- 代码块前后空一行

### 5. 样式文件位置

确保以下CSS文件存在于 `assets/css/`：
- `bootstrap.min.css` - 主样式
- `jupyter-grade3.css` - Jupyter代码高亮样式
- `jekyll-pygments-themes-github.css` - GitHub风格代码高亮

### 6. 如果样式仍然不显示

#### 检查HTML输出

在浏览器中：
1. 打开blog页面
2. 右键 → 检查元素
3. 查看Console是否有CSS加载错误

#### 强制刷新浏览器

- Mac: `Cmd + Shift + R`
- Windows: `Ctrl + F5`

#### 清除浏览器缓存

浏览器设置 → 清除浏览数据 → 缓存的图像和文件

## Blog文章模板

### 基础模板

```markdown
---
title: "文章标题"
permalink: /blog/2025/article-title/
date: 2025-02-06 10:00:00 +0800
categories: [分类1, 分类2]
tags: [标签1, 标签2, 标签3]
---

## 一级标题

### 二级标题

文章正文内容...

#### 代码示例

```python
import geopandas as gpd
```

#### 列表示例

- 项目1
- 项目2
  - 子项目2.1
  - 子项目2.2

#### 链接示例

[南京大学](https://www.nju.edu.cn)
```

### 高级功能

#### 添加目录

在front matter中添加：

```yaml
toc:
  sidebar: left
  beginning: true
```

#### 添加PDF附件

```yaml
pdf: /assets/pdf/example.pdf
```

#### 添加缩略图

```yaml
thumbnail: /assets/img/thumbnail.jpg
```

## 常见问题

### Q1: 代码块没有高亮

**A**: 确保代码块格式正确：

````python
代码在这里
````
```

而不是：

``(python)  # 错误格式
代码在这里
```
```

### Q2: 样式在某些浏览器中不显示

**A**:
1. 清除浏览器缓存
2. 尝试其他浏览器
3. 检查浏览器Console是否有错误

### Q3: 图片不显示

**A**: 确保图片路径正确：

```markdown
![图片描述](/assets/img/image.jpg)
```

### Q4: 数学公式不渲染

**A**: 确保使用LaTeX格式：

```markdown
行内公式：$E = mc^2$

独立公式：
$$
E = mc^2
$$
```

## 最佳实践

1. **本地测试**：每次修改后本地预览
2. **代码格式化**：使用4个空格缩进，不使用Tab
3. **文件命名**：使用 `YYYY-MM-DD-title.md` 格式
4. **定期构建**：推送代码后让GitHub Actions自动构建

## 相关命令

```bash
# 本地预览（推荐）
bundle exec jekyll serve

# 构建网站
bundle exec jekyll build

# 清理构建文件
bundle exec jekyll clean

# 检查链接
bundle exec htmlproof ./_site

# 格式化代码
npx prettier --write _posts/
```

## 下一步

1. 运行 `bundle exec jekyll serve` 本地预览
2. 访问 http://localhost:4000/blog/
3. 检查样式和代码高亮是否正常
4. 如果正常，推送到GitHub触发自动部署
