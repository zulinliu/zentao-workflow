# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-26

### Added

- Initial release of zentao-workflow skill
- Dual runtime support (Java 8+ and Python 3.6+)
- Automatic environment detection and runtime selection
- Interactive Zentao server configuration
- Download stories, tasks, and bugs with attachments
- Download embedded images in content
- Generate development technical solution documents
- Cross-platform support (Windows, macOS, Linux)
- Java project analysis guide
- React project analysis guide
- Technical plan template

### Features

- **Smart Triggering**: Automatically activates on keywords like "禅道", "需求", "任务", "Bug"
- **Dual Runtime**: Built-in Java and Python versions, auto-selects best runtime
- **Attachment Download**: Downloads all attachments and embedded images
- **Technical Solution**: Generates detailed development plans based on project code analysis
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Technical Details

- Java version: Built with Maven, requires Java 8+
- Python version: Pure Python with requests library
- Markdown export with proper relative paths for attachments
- Correct path handling: `../attachments/{type}/{id}/` format
