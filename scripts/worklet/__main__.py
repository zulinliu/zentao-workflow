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
from .env import EnvDetector
from .service import WorkletService
from .sources.base import SourceRegistry
from .sources.zentao import ZentaoSource
from .input import InputParser, InputType


def resolve_source(identifier: str, config: WorkletConfig):
    """Resolve identifier to appropriate source instance.

    Uses InputParser.detect() to determine type, then dispatches
    to correct Source via SourceRegistry.
    """
    input_type = InputParser.detect(identifier)

    if input_type == InputType.UNKNOWN:
        raise ValueError(f"Cannot determine input type for: {identifier}")

    registry = SourceRegistry()

    if input_type == InputType.ZENTAO:
        source_cls = registry.get('zentao')
        if source_cls is None:
            raise ValueError("Zentao source not available")
        # Parse Zentao ID (handles bare numbers like "38817")
        parsed = InputParser.parse_zentao_id(identifier)
        if parsed is None:
            raise ValueError(f"Invalid Zentao ID: {identifier}")
        zentao_type, numeric_id = parsed
        resolved_id = f"{zentao_type}-{numeric_id}"
        return source_cls(config), resolved_id

    elif input_type == InputType.FILE:
        from .sources.file import FileSource
        return FileSource(), identifier

    elif input_type == InputType.FOLDER:
        from .sources.folder import FolderSource
        return FolderSource(), identifier

    raise ValueError(f"Unsupported input type: {input_type}")


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

    # Environment detection with caching (ENV-01, ENV-02, ENV-03)
    env_detector = EnvDetector()
    env_result = env_detector.detect()

    if env_result.superpowers_available:
        print(f"[ENV] superpowers {env_result.superpowers_version} available")
    else:
        print("[ENV] superpowers not available, using basic mode")

    # Save config if new credentials provided
    if args.url or args.username or args.password:
        config.save_to_workspace(workspace_dir)

    # Collect identifiers (ID list becomes raw identifiers for auto-detect)
    identifiers: list[str] = []
    if args.id:
        identifiers.append(str(args.id))
    if args.ids:
        identifiers.extend([x.strip() for x in args.ids.split(",") if x.strip()])

    if not identifiers:
        print("Error: must specify identifier (-i or --ids)")
        sys.exit(1)

    # Execute with auto-detect or explicit mode
    try:
        download_attachments = not (args.no_attachment and args.no_image)

        if args.type:
            # Explicit mode (backward compatible) - use -t flag
            registry = SourceRegistry()
            zentao_source_cls = registry.get('zentao')

            if zentao_source_cls:
                source = zentao_source_cls(config)
                for item_id in identifiers:
                    id_str = f"{args.type}-{item_id}"
                    worklet = source.fetch(id_str, download_attachments=download_attachments)
                    print(f"Fetched: {worklet.title}")
                print("Done")
            else:
                service = WorkletService(config)
                service.execute(
                    content_type=args.type,
                    ids=[int(x) for x in identifiers],
                    download_attachments=download_attachments
                )
                print("Done")
        else:
            # Auto-detect mode - use InputParser to determine type
            for identifier in identifiers:
                source, resolved_id = resolve_source(identifier, config)
                worklet = source.fetch(resolved_id, download_attachments=download_attachments)
                print(f"Fetched: {worklet.title}")
            print("Done")
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
