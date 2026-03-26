#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禅道数据抓取工具 - 主入口

从禅道系统下载任务、需求、Bug详情到本地Markdown文件，支持图片和附件自动下载。
"""

import argparse
import os
import sys
from typing import List

from .config import ChandaoConfig
from .service import ChandaoService


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="禅道数据抓取工具 - 下载需求/任务/Bug到本地Markdown文件"
    )

    # 连接参数
    parser.add_argument(
        "--url", "-u",
        help="禅道服务器地址 (如 https://zentao.example.com)"
    )
    parser.add_argument(
        "--username",
        help="登录用户名"
    )
    parser.add_argument(
        "--password",
        help="登录密码"
    )
    parser.add_argument(
        "--output", "-o",
        help="输出目录 (默认当前工作目录)"
    )
    parser.add_argument(
        "--config", "-c",
        help="配置文件路径"
    )

    # 操作参数
    parser.add_argument(
        "--type", "-t",
        choices=["story", "task", "bug"],
        help="内容类型: story(需求), task(任务), bug(缺陷)"
    )
    parser.add_argument(
        "--id", "-i",
        type=int,
        help="单个ID"
    )
    parser.add_argument(
        "--ids",
        help="批量ID，逗号分隔 (如: 123,456,789)"
    )

    # 选项
    parser.add_argument(
        "--no-attachment",
        action="store_true",
        help="不下载附件"
    )
    parser.add_argument(
        "--no-image",
        action="store_true",
        help="不下载图片"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="详细输出"
    )

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    # 确定工作区目录（用于查找工作区配置文件）
    workspace_dir = args.output if args.output else os.getcwd()

    # 加载配置（优先级：命令行指定 > 工作区配置 > 全局配置）
    config = ChandaoConfig.load(workspace_dir=workspace_dir, config_path=args.config)

    # 命令行参数覆盖配置文件
    if args.url:
        config.base_url = args.url
    if args.username:
        config.username = args.username
    if args.password:
        config.password = args.password
    if args.output:
        config.output_dir = args.output

    # 检查配置是否已初始化
    if not config.is_initialized():
        print(config.get_init_prompt())
        sys.exit(1)

    # 如果提供了新的凭据，保存配置
    if args.url or args.username or args.password:
        # 默认保存到工作区配置
        config.save_to_workspace(workspace_dir)

    # 解析ID列表
    ids: List[int] = []
    if args.id:
        ids.append(args.id)
    if args.ids:
        ids.extend([int(x.strip()) for x in args.ids.split(",") if x.strip()])

    # 验证参数
    if not args.type:
        print("错误: 必须指定内容类型 (-t story/task/bug)")
        sys.exit(1)

    if not ids:
        print("错误: 必须指定ID (-i 或 --ids)")
        sys.exit(1)

    # 执行服务
    try:
        service = ChandaoService(config)
        service.execute(
            content_type=args.type,
            ids=ids,
            download_attachments=not (args.no_attachment and args.no_image)
        )
        print("任务执行完成")
    except Exception as e:
        print(f"执行失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
