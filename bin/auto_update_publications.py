#!/usr/bin/env python
"""
自动监控谷歌学术并更新论文列表
Monitor Google Scholar and automatically add new publications to BibTeX file
"""

import os
import sys
import yaml
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
from datetime import datetime
from scholarly import scholarly
import re


def load_scholar_user_id() -> str:
    """从配置文件加载谷歌学术用户ID"""
    config_file = "_data/socials.yml"
    if not os.path.exists(config_file):
        print(f"❌ 配置文件 {config_file} 不存在")
        sys.exit(1)

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    scholar_user_id = config.get("scholar_userid")
    if not scholar_user_id:
        print("❌ 在 _data/socials.yml 中未找到 'scholar_userid'")
        sys.exit(1)

    return scholar_user_id


def load_existing_bibtex(bibtex_file: str) -> set:
    """加载现有的BibTeX文件，返回所有文章标题集合"""
    if not os.path.exists(bibtex_file):
        print(f"⚠️  BibTeX文件 {bibtex_file} 不存在，将创建新文件")
        return set()

    with open(bibtex_file, 'r', encoding='utf-8') as f:
        db = bibtexparser.load(f)

    existing_titles = set()
    for entry in db.entries:
        if 'title' in entry:
            # 标准化标题（去除空格、标点，转小写）用于比较
            normalized_title = normalize_title(entry['title'])
            existing_titles.add(normalized_title)

    print(f"📚 现有文献数量: {len(existing_titles)}")
    return existing_titles


def normalize_title(title: str) -> str:
    """标准化标题用于比较"""
    # 转小写，去除多余空格和常见标点
    title = title.lower().strip()
    title = re.sub(r'[{}",\.\s]+', ' ', title)
    title = ' '.join(title.split())
    return title


def create_bibtex_entry(pub: dict) -> bibtexparser.model.Entry:
    """从谷歌学术数据创建BibTeX条目"""
    bib = pub.get('bib', {})
    title = bib.get('title', 'Untitled')

    # 生成BibTeX key（作者缩写+年份+关键词）
    author = bib.get('author', '')
    year = bib.get('pub_year', 'n.d.')

    # 提取第一作者姓氏
    if author:
        first_author = author.split(' and ')[0]
        # 处理 "Last, First" 格式
        if ',' in first_author:
            last_name = first_author.split(',')[0].strip()
        else:
            # 处理 "First Last" 格式
            last_name = first_author.split()[-1] if first_author.split() else 'Unknown'
    else:
        last_name = 'Unknown'

    # 从标题提取关键词
    title_words = re.sub(r'[{}",\.\s]+', ' ', title).split()
    keyword = title_words[0] if title_words else 'key'

    # 创建唯一的BibTeX key
    bibtex_key = f"{last_name}{year}_{keyword}"
    bibtex_key = re.sub(r'[{}",\.\s]+', '', bibtex_key)

    # 确定文献类型
    pub_type = bib.get('pubtype', 'article')
    if pub_type == 'article' or 'journal' in bib.get('venue', '').lower():
        entry_type = 'article'
    elif 'conference' in pub_type.lower() or 'proceedings' in bib.get('venue', '').lower():
        entry_type = 'inproceedings'
    else:
        entry_type = 'article'

    # 创建BibTeX条目
    entry = bibtexparser.model.Entry()
    entry.key = bibtex_key
    entry.type = entry_type

    # 添加字段
    entry['author'] = author
    entry['title'] = f"{{{title}}}"  # 用大括号保护标题大小写
    entry['year'] = year

    if 'journal' in bib:
        entry['journal'] = bib['journal']
    elif 'venue' in bib:
        entry['journal'] = bib['venue']

    if 'volume' in bib:
        entry['volume'] = bib['volume']
    if 'number' in bib:
        entry['number'] = bib['number']
    if 'pages' in bib:
        entry['pages'] = bib['pages']
    if 'publisher' in bib:
        entry['publisher'] = bib['publisher']

    # 添加URL
    if 'pub_url' in pub:
        entry['url'] = pub['pub_url']
    elif 'eprint' in pub:  # arXiv
        entry['eprint'] = pub['eprint']
        entry['archivePrefix'] = 'arXiv'

    # 添加摘要（如果存在）
    if 'abstract' in bib:
        entry['abstract'] = bib['abstract']

    return entry


def fetch_new_publications(scholar_id: str, existing_titles: set) -> list:
    """从谷歌学术获取新文章"""
    print(f"🔍 正在从谷歌学术获取文章...")
    print(f"📌 学者ID: {scholar_id}")

    scholarly.set_timeout(15)
    scholarly.set_retries(3)

    try:
        author = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(author, sections=['publications'])
    except Exception as e:
        print(f"❌ 获取学者数据失败: {e}")
        sys.exit(1)

    if 'publications' not in author:
        print("❌ 未找到任何出版物")
        sys.exit(1)

    new_publications = []
    total_count = len(author['publications'])
    print(f"📊 谷歌学术文章总数: {total_count}")

    for i, pub in enumerate(author['publications'], 1):
        try:
            bib = pub.get('bib', {})
            title = bib.get('title', 'Unknown Title')

            # 标准化标题进行比较
            normalized_title = normalize_title(title)

            if normalized_title not in existing_titles:
                print(f"✨ 发现新文章 [{i}/{total_count}]: {title}")
                new_publications.append(pub)
            else:
                print(f"✓ 已存在 [{i}/{total_count}]: {title}")

        except Exception as e:
            print(f"⚠️  处理文章时出错: {e}")
            continue

    return new_publications


def update_bibtex_file(bibtex_file: str, new_pubs: list):
    """将新文章添加到BibTeX文件"""
    if not new_pubs:
        print("ℹ️  没有新文章需要添加")
        return

    print(f"\n📝 准备添加 {len(new_pubs)} 篇新文章到 {bibtex_file}")

    # 加载现有数据库
    db = BibDatabase()
    if os.path.exists(bibtex_file):
        with open(bibtex_file, 'r', encoding='utf-8') as f:
            db = bibtexparser.load(f)

    # 添加新条目
    added_count = 0
    for pub in new_pubs:
        try:
            entry = create_bibtex_entry(pub)

            # 检查key是否已存在，如果存在则生成新key
            existing_keys = [e.key for e in db.entries]
            if entry.key in existing_keys:
                base_key = entry.key
                suffix = 1
                while f"{base_key}_{suffix}" in existing_keys:
                    suffix += 1
                entry.key = f"{base_key}_{suffix}"

            db.entries.append(entry)
            added_count += 1
            print(f"  ✓ 添加: {entry['title']}")

        except Exception as e:
            print(f"  ⚠️  添加条目失败: {e}")
            continue

    # 写入文件
    writer = BibTexWriter()
    writer.indent = '  '
    writer.order_entries_by = ('year', 'author', 'title')

    with open(bibtex_file, 'w', encoding='utf-8') as f:
        f.write(writer.write(db))

    print(f"\n✅ 成功添加 {added_count} 篇新文章到 {bibtex_file}")


def main():
    """主函数"""
    print("=" * 60)
    print("🎓 谷歌学术自动更新工具")
    print("=" * 60)
    print(f"⏰ 运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 加载配置
    scholar_id = load_scholar_user_id()
    bibtex_file = "_bibliography/papers.bib"

    # 加载现有文章
    existing_titles = load_existing_bibtex(bibtex_file)

    # 获取新文章
    new_publications = fetch_new_publications(scholar_id, existing_titles)

    # 更新BibTeX文件
    update_bibtex_file(bibtex_file, new_publications)

    print()
    print("=" * 60)
    print("✨ 完成！")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
