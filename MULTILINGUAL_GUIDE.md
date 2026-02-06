# 双语网站使用指南

## 概述

本网站已配置为**中英双语**网站，使用 `jekyll-polyglot` 插件实现多语言支持。

## 功能特性

- ✅ **自动语言路由**：英文（默认）和中文两个版本
- ✅ **语言切换器**：导航栏右上角的语言切换下拉菜单
- ✅ **URL结构**：
  - 英文：`https://baoyigis.github.io/` 或 `https://baoyigis.github.io/en/`
  - 中文：`https://baoyigis.github.io/zh/`

## 如何添加多语言页面

### 方法1：创建语言特定的页面文件

为每个页面创建不同语言版本，使用语言后缀：

```
_pages/
├── about.md         # 英文版（默认）
├── about.zh.md      # 中文版
├── publications.md  # 英文版
└── publications.zh.md  # 中文版
```

### 方法2：在Front Matter中指定语言

在每个页面的front matter中添加 `lang` 字段：

```yaml
---
title: About
lang: en
permalink: /
---
```

中文版本：

```yaml
---
title: 关于
lang: zh
permalink: /zh/
---
```

## Blog文章多语言支持

### 创建多语言Blog文章

为每篇blog创建不同语言版本：

```
_posts/
├── 2025-02-06-lab0-environment-setup.md  # 英文版
└── 2025-02-06-lab0-huanjing-peizhi.md    # 中文版
```

在front matter中指定语言：

**英文版**：
```yaml
---
title: "Lab 0: Environment Setup"
lang: en
categories: [Spatial Analysis]
tags: [VSCode, Python, GeoPandas]
---
```

**中文版**：
```yaml
---
title: "Lab 0: 环境配置"
lang: zh
categories: [空间分析]
tags: [VSCode, Python, GeoPandas]
---
```

## 配置说明

### _config.yml 配置

```yaml
# 多语言配置
languages: ["en", "zh"]
default_lang: "en"
exclude_from_localization: ["javascript", "images", "css", "assets"]
parallel_localization: true
```

**参数说明**：
- `languages`: 支持的语言列表
- `default_lang`: 默认语言（英文）
- `exclude_from_localization`: 不需要翻译的资源文件
- `parallel_localization`: 并行处理语言版本（提高构建速度）

## URL结构说明

### 根路径（英文）
- `/` → 英文首页
- `/publications/` → 英文发表文章页
- `/cv/` → 英文简历页

### 中文路径
- `/zh/` → 中文首页
- `/zh/publications/` → 中文发表文章页
- `/zh/cv/` → 中文简历页

## 页面翻译指南

### 1. About页面

已创建示例：
- [`about.md`](_pages/about.md) - 英文版
- [`about.zh.md`](_pages/about.zh.md) - 中文版

### 2. 其他页面

需要翻译的页面：
- `publications.md` → `publications.zh.md`
- `projects.md` → `projects.zh.md`
- `cv/` 目录下的页面 → `cv.zh/` 或添加 `lang: zh` 字段

### 3. 导航栏和菜单

导航栏会自动根据当前语言显示相应版本的页面标题。

## 组件说明

### 语言切换器

位置：`_includes/language_switcher.liquid`

功能：
- 自动检测当前页面语言
- 显示当前语言（🇺🇸 English 或 🇨🇳 中文）
- 下拉菜单显示所有可用语言
- 点击切换到对应语言的当前页面

## 注意事项

### ⚠️ 构建要求

1. **安装依赖**：
   ```bash
   bundle install
   ```

2. **构建网站**：
   ```bash
   bundle exec jekyll build
   ```

3. **本地预览**：
   ```bash
   bundle exec jekyll serve
   ```

### ⚠️ 文件命名规范

- 英文版（默认）：`filename.md`
- 中文版：`filename.zh.md`
- 其他语言：`filename.{lang}.md`（如 `filename.fr.md`）

### ⚠️ Permalink设置

确保不同语言版本的permalink不同：

- 英文：`permalink: /`
- 中文：`permalink: /zh/`

### ⚠️ 避免重复内容

确保每个页面只有一个默认语言版本，其他语言版本使用明确的语言后缀。

## 测试双语功能

### 本地测试

1. 启动本地服务器：
   ```bash
   bundle exec jekyll serve
   ```

2. 访问测试：
   - 英文版：http://localhost:4000/
   - 中文版：http://localhost:4000/zh/

3. 测试语言切换：
   - 点击导航栏右上角的语言切换器
   - 验证页面是否正确切换到对应语言版本

### 部署后测试

部署到GitHub Pages后，测试：
- https://baoyigis.github.io/ （英文）
- https://baoyigis.github.io/zh/ （中文）

## 常见问题

### Q1: 如何添加更多语言？

A: 在 `_config.yml` 中添加新语言到 `languages` 数组：
```yaml
languages: ["en", "zh", "fr"]  # 添加法语
```

### Q2: 某些页面不想翻译怎么办？

A: 不创建该页面的语言版本即可，或者将页面路径添加到 `exclude_from_localization`。

### Q3: Blog文章如何组织？

A: 为每篇blog创建独立的语言版本文件，使用不同的文件名或语言后缀。

### Q4: 如何统计不同语言版本的访问？

A: 可以使用Google Analytics等分析工具，通过URL路径区分语言版本。

## 相关文件

- `Gemfile` - 添加了 `jekyll-polyglot` 插件
- `_config.yml` - 多语言配置
- `_includes/language_switcher.liquid` - 语言切换器组件
- `_includes/header.liquid` - 导航栏（包含语言切换器）
- `_pages/about.md` - 英文About页面
- `_pages/about.zh.md` - 中文About页面

## 下一步

建议翻译的页面（按优先级）：

1. ✅ About页面（已完成）
2. 📝 Publications页面
3. 📝 Projects页面
4. 📝 CV页面
5. 📝 Blog文章（选择性翻译重要文章）

## 参考资料

- [Jekyll Polyglot 文档](https://github.com/untra/polyglot)
- [Jekyll 官方文档](https://jekyllrb.com/docs/)
