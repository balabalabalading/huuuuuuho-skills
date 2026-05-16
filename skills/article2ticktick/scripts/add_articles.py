#!/usr/bin/env python3
"""
add_articles.py

解析标准格式的文章 markdown 并直接添加到 TickTick。
支持批量周报模式（--input）和单篇文章模式（--task）。

字段映射：
  title   : **[文章标题](链接)** → 去掉 **，保留 [文章标题](链接)
  content : 所有 - bullet 行 → 去掉 "- " 前缀、去掉 [[]]，逗号合并为单行
  list    : ## 二级标题
  tags    : ### 三级标题（无 H3 则不传此参数）

用法（批量模式）：
  python3 add_articles.py --input new_articles.md            # 从文件读取
  cat new_articles.md | python3 add_articles.py              # 从 stdin 读取
  pbpaste | python3 add_articles.py                          # 从剪贴板读取
  python3 add_articles.py --input new_articles.md --dry-run  # 仅预览不添加

用法（单篇模式）：
  python3 add_articles.py --task \\
    --title "[文章标题](https://example.com/article)" \\
    --list "SwiftUI" \\
    --tags "状态管理与观察" \\
    --desc "这篇文章介绍了..." \\
    --desc "出自：用户自添加"

  python3 add_articles.py --task --title "[标题](url)" --list "SwiftUI" --dry-run
"""

import argparse
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path
from urllib.parse import quote


def strip_wikilinks(text: str) -> str:
    """去掉 [[...]] 双方括号，保留内部文本"""
    return re.sub(r'\[\[(.+?)\]\]', r'\1', text)


def parse_articles(text: str) -> list[dict]:
    articles = []
    current_h2 = None
    current_h3 = None
    current_article = None

    def flush():
        nonlocal current_article
        if current_article and current_article.get('title'):
            articles.append(dict(current_article))
        current_article = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        # H2 → list
        m = re.match(r'^## (.+)', line)
        if m:
            flush()
            current_h2 = m.group(1).strip()
            current_h3 = None
            continue

        # H3 → tags
        m = re.match(r'^### (.+)', line)
        if m:
            flush()
            current_h3 = m.group(1).strip()
            continue

        # 文章标题行：**[title](url)**
        m = re.match(r'^\*\*(\[.+?\]\(.+?\))\*\*\s*$', line)
        if m:
            flush()
            current_article = {
                'title': m.group(1),
                'content_parts': [],
                'list': current_h2 or '',
                'tags': current_h3,
            }
            continue

        # bullet 正文行
        if current_article is not None and line.startswith('- '):
            text_part = strip_wikilinks(line[2:].strip())
            current_article['content_parts'].append(text_part)

    flush()
    return articles


def build_url(article: dict) -> str:
    title = article['title']
    today = date.today().strftime('%Y-%m-%d')
    content = f"{today}，" + '，'.join(article['content_parts'])
    list_name = article['list']
    tags = article['tags']

    params = (
        f"title={quote(title, safe='')}"
        f"&content={quote(content, safe='')}"
        f"&list={quote(list_name, safe='')}"
    )
    if tags:
        params += f"&tags={quote(tags, safe='')}"
    return f"ticktick://x-callback-url/v1/add_task?{params}"


def run_single_task(args) -> None:
    """单篇文章模式：直接构造一条任务并添加到 TickTick"""
    if not args.title:
        print("错误：--task 模式需要 --title 参数，格式：[文章标题](URL)", file=sys.stderr)
        sys.exit(1)
    if not args.list_name:
        print("错误：--task 模式需要 --list 参数（滴答清单名）", file=sys.stderr)
        sys.exit(1)

    article = {
        'title': args.title,
        'content_parts': args.desc or [],
        'list': args.list_name,
        'tags': args.tags,
    }
    url = build_url(article)

    if args.dry_run:
        content_preview = '，'.join(article['content_parts'])
        print("[单篇预览]")
        print(f"  title  : {article['title']}")
        print(f"  list   : {article['list']}")
        print(f"  tags   : {article['tags'] or '（无）'}")
        print(f"  content: {content_preview[:80]}{'...' if len(content_preview) > 80 else ''}")
        print(f"  url    : {url[:120]}...")
    else:
        print("正在添加到 TickTick，请确保 TickTick 在前台运行...")
        subprocess.run(['open', url], check=True)
        print(f"\n✓ 已添加：{article['title']}")


def main():
    parser = argparse.ArgumentParser(
        description='解析文章 markdown 并直接添加到 TickTick',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 批量模式
    batch_group = parser.add_argument_group('批量模式')
    batch_group.add_argument('--input', type=Path,
                             help='输入文件路径（不指定则从 stdin 读取）')

    # 单篇模式
    single_group = parser.add_argument_group('单篇模式（--task）')
    single_group.add_argument('--task', action='store_true',
                              help='单任务模式：直接添加单篇文章，无需 markdown 文件')
    single_group.add_argument('--title',
                              help='文章标题，格式为 [文章标题](URL)')
    single_group.add_argument('--list', dest='list_name',
                              help='滴答清单名（必须与 TickTick 中的列表名完全一致）')
    single_group.add_argument('--tags',
                              help='标签（对应 TickTick 的 tags 字段）')
    single_group.add_argument('--desc', action='append', dest='desc',
                              metavar='描述',
                              help='描述内容（可多次传入，每次对应一条 bullet）')

    # 通用
    parser.add_argument('--dry-run', action='store_true',
                        help='仅预览解析结果，不实际打开 TickTick')
    parser.add_argument('--delay', type=float, default=0.5,
                        help='批量模式：每条任务间隔秒数（默认 0.5）')

    args = parser.parse_args()

    # 单篇模式
    if args.task:
        run_single_task(args)
        return

    # 批量模式
    if args.input:
        if not args.input.exists():
            print(f"错误：文件不存在：{args.input}", file=sys.stderr)
            sys.exit(1)
        text = args.input.read_text(encoding='utf-8')
    else:
        text = sys.stdin.read()

    articles = parse_articles(text)
    if not articles:
        print("未解析到任何文章，请检查输入格式", file=sys.stderr)
        sys.exit(1)

    urls = [build_url(a) for a in articles]
    print(f"共解析到 {len(urls)} 篇文章\n")

    if args.dry_run:
        for i, (a, url) in enumerate(zip(articles, urls), 1):
            content_preview = '，'.join(a['content_parts'])
            print(f"[{i:02d}] {a['title']}")
            print(f"      list : {a['list']}")
            print(f"      tags : {a['tags'] or '（无）'}")
            print(f"      content: {content_preview[:70]}{'...' if len(content_preview) > 70 else ''}")
            print(f"      url  : {url[:100]}...")
            print()
        return

    print(f"开始添加到 TickTick，请确保 TickTick 在前台运行...\n")
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] 正在添加...")
        subprocess.run(['open', url], check=True)
        if i < len(urls):
            time.sleep(args.delay)

    print(f"\n✓ 全部 {len(urls)} 条任务添加完成")


if __name__ == '__main__':
    main()
