#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Worklet - CLI entry point

Usage:
    python -m worklet -t story -i 38817
    python -m worklet -t task --ids 12345,12346
    python -m worklet -t bug -i 67890 -o ~/my-output
"""

import argparse
import os
import sys

from .config import WorkletConfig
from .service import WorkletService


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Worklet - download requirements/tasks/bugs to local Markdown files"
    )

    # Connection parameters
    parser.add_argument(
        "--url", "-u",
        help="Zentao server URL (e.g., https://zentao.example.com)"
    )
    parser.add_argument(
        "--username",
        help="Username"
    )
    parser.add_argument(
        "--password",
        help="Password"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output directory (default: current working directory)"
    )
    parser.add_argument(
        "--config", "-c",
        help="Config file path"
    )

    # Operation parameters
    parser.add_argument(
        "--type", "-t",
        choices=["story", "task", "bug"],
        help="Content type: story, task, or bug"
    )
    parser.add_argument(
        "--id", "-i",
        type=int,
        help="Single ID"
    )
    parser.add_argument(
        "--ids",
        help="Batch IDs, comma-separated (e.g., 123,456,789)"
    )

    # Options
    parser.add_argument(
        "--no-attachment",
        action="store_true",
        help="Skip attachment download"
    )
    parser.add_argument(
        "--no-image",
        action="store_true",
        help="Skip image download"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_args()

    # Determine workspace directory
    workspace_dir = args.output if args.output else os.getcwd()

    # Load configuration (priority: CLI args > workspace config > global config)
    config = WorkletConfig.load(workspace_dir=workspace_dir, config_path=args.config)

    # Override with CLI arguments
    if args.url:
        config.base_url = args.url
    if args.username:
        config.username = args.username
    if args.password:
        config.password = args.password
    if args.output:
        config.output_dir = args.output

    # Check if config is initialized
    if not config.is_initialized():
        print(config.get_init_prompt())
        sys.exit(1)

    # Save config if new credentials provided
    if args.url or args.username or args.password:
        config.save_to_workspace(workspace_dir)

    # Parse ID list
    ids: list[int] = []
    if args.id:
        ids.append(args.id)
    if args.ids:
        ids.extend([int(x.strip()) for x in args.ids.split(",") if x.strip()])

    # Validate arguments
    if not args.type:
        print("Error: must specify content type (-t story/task/bug)")
        sys.exit(1)

    if not ids:
        print("Error: must specify ID (-i or --ids)")
        sys.exit(1)

    # Execute service
    try:
        service = WorkletService(config)
        service.execute(
            content_type=args.type,
            ids=ids,
            download_attachments=not (args.no_attachment and args.no_image)
        )
        print("Done")
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
