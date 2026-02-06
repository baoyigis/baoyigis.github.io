# 自动更新谷歌学术文章功能说明

## 功能概述

这个功能会自动监控你的谷歌学术个人资料，一旦发现有新文章，就会自动添加到你的 BibTeX 文件中（`_bibliography/papers.bib`）。

## 工作原理

1. **自动监控**：GitHub Actions 每周一和周四自动运行
2. **智能对比**：脚本会对比谷歌学术和现有的 BibTeX 文件
3. **自动添加**：发现新文章后，自动生成标准格式的 BibTeX 条目
4. **提交更新**：如果有新文章，自动提交并推送到仓库

## 使用方法

### 方法1：自动运行（推荐）

什么都不用做！GitHub Actions 会在以下时间自动运行：
- 每周一午夜（UTC时间）
- 每周四午夜（UTC时间）

### 方法2：手动触发

1. 访问 GitHub 仓库页面
2. 点击 **Actions** 标签
3. 选择 **Auto Update Publications from Google Scholar** 工作流
4. 点击 **Run workflow** 按钮
5. 选择分支（通常是 `main`）
6. 点击 **Run workflow** 确认

### 方法3：本地运行

你也可以在本地手动运行脚本：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行脚本
python bin/auto_update_publications.py
```

## 配置要求

确保在 `_data/socials.yml` 中配置了你的谷歌学术用户ID：

```yaml
scholar_userid: "你的谷歌学术ID"  # 例如: "Xj72kFkAAAAJ"
```

## 脚本特性

### ✨ 智能识别

- 自动检测新文章（通过标题标准化比较）
- 自动识别文章类型（期刊论文、会议论文等）
- 自动生成规范的 BibTeX key

### 🔧 自动处理

- 自动从谷歌学术提取文章元数据
- 自动处理标题大小写保护
- 自动避免重复添加（通过标题标准化）

### 📝 支持的BibTeX字段

- 作者（author）
- 标题（title）
- 年份（year）
- 期刊/会议（journal）
- 卷号（volume）
- 期号（number）
- 页码（pages）
- 出版社（publisher）
- URL链接（url）
- arXiv预印本（eprint）
- 摘要（abstract）

## 输出示例

运行成功时，你会看到类似这样的输出：

```
============================================================
🎓 谷歌学术自动更新工具
============================================================
⏰ 运行时间: 2025-02-06 12:00:00

📚 现有文献数量: 28
🔍 正在从谷歌学术获取文章...
📌 学者ID: Xj72kFkAAAAJ
📊 谷歌学术文章总数: 30
✓ 已存在 [1/30]: Urban spatiotemporal big data mining
✨ 发现新文章 [2/30]: High-resolution quantification of building stock
✓ 已存在 [3/30]: Big geodata revealed spatial patterns
...

📝 准备添加 2 篇新文章到 _bibliography/papers.bib
  ✓ 添加: High-resolution quantification of building stock
  ✓ 添加: Machine learning for urban analysis

✅ 成功添加 2 篇新文章到 _bibliography/papers.bib

============================================================
✨ 完成！
============================================================
```

## 注意事项

⚠️ **重要提示**：

1. **首次运行**：第一次运行时，如果 BibTeX 文件不存在，脚本会创建新文件
2. **手动检查**：建议首次运行后手动检查生成的 BibTeX 条目，确保格式正确
3. **冲突处理**：如果手动修改了 BibTeX 文件，确保使用标准格式，避免脚本无法解析
4. **网络限制**：谷歌学术可能有反爬虫机制，脚本已设置随机延迟和重试机制

## 故障排查

### 问题：找不到 scholar_userid

**解决方案**：检查 `_data/socials.yml` 文件，确保包含正确的谷歌学术ID

### 问题：无法连接到谷歌学术

**解决方案**：
- 检查网络连接
- 稍后重试（谷歌学术可能暂时限制了访问）
- 使用手动触发功能重新运行

### 问题：BibTeX 格式错误

**解决方案**：
- 备份现有的 `papers.bib` 文件
- 手动编辑修复格式问题
- 确保使用标准的 BibTeX 格式

## 高级配置

### 修改自动运行频率

编辑 `.github/workflows/auto-update-publications.yml`，修改 cron 表达式：

```yaml
schedule:
  - cron: "0 0 * * 1"  # 每周一
  - cron: "0 0 * * 4"  # 每周四
```

### 添加更多定时任务

```yaml
schedule:
  - cron: "0 0 * * *"   # 每天午夜
  - cron: "0 12 * * *"  # 每天中午
```

## 相关文件

- `bin/auto_update_publications.py` - 主脚本
- `.github/workflows/auto-update-publications.yml` - GitHub Actions 工作流
- `requirements.txt` - Python 依赖
- `_bibliography/papers.bib` - BibTeX 文件
- `_data/socials.yml` - 配置文件

## 更新日志

- **2025-02-06**: 初始版本，支持自动从谷歌学术添加新文章
