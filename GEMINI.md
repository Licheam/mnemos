# Mnemos Project Context

This document provides instructional context for Gemini when working on the Mnemos project.

## Project Overview

Mnemos is a Python-based library and CLI tool designed to provide AI agents with a persistent memory system. It organizes memory into:
- **Short-term Memory (`short_term.md`):** Automatically generated from Git commit history, tracking recent activities with hotspot analysis and commit type grouping.
- **Long-term Memory (`long_term.md`):** Structured storage for high-level project information.
- **Configuration (`.mnemos.toml`):** Project-specific settings for valid sections, git analysis windows, and search parameters.

The system is designed to be lightweight, human-readable (Markdown), and integrated directly into the target project's repository.

### Main Technologies
- **Python:** 3.10+
- **Git:** Used for activity tracking and commit summarization.
- **Hatch:** Used as the build system and package manager.
- **Markdown:** The primary format for memory storage and communication.

### Architecture
- `mnemos/cli.py`: Command-line interface logic.
- `mnemos/memory.py`: Core functions for reading and writing memory files.
- `mnemos/git.py`: Integration with Git to extract and summarize recent activities with smart categorization.
- `mnemos/search.py`: Cross-memory full-text search engine.
- `mnemos/config.py`: Configuration management from `.mnemos.toml`.
- `mnemos/compress.py`: Utilities for managing memory growth and transitioning old short-term memory to long-term storage.
- `templates/`: Contains the default directory structure and files used when initializing a new project.

## Building and Running

### Development Setup
```bash
# Install in editable mode
pip install -e .
# Important: When developing, always pipx reinstall mnemos after changes!
```

### CLI Commands
- `mnemos init [path]`: Sets up the memory directories and `.mnemos.toml`.
- `mnemos init [path] --only-skills`: Updates `.agent/skills/` without overwriting memory.
- `mnemos update [path]`: Summarizes Git commits into structured `short_term.md`.
- `mnemos show [path] [-t type]`: Displays memory content.
- `mnemos search "keyword"`: Searches across all memory files with context.
- `mnemos write [path] -s <section> [-c <content> | -f <file>] [-a]`: Updates or appends to long-term sections.
- `mnemos compress [path] [-d days]`: Extracts old memory for summarization.

### Public Python API
The core functionality is exposed via the `mnemos` package:
```python
from mnemos import read_memory, summarize_commits, update_long_term_memory
```

## Development Conventions

### Coding Style
- Follow standard Python (PEP 8) conventions.
- Use type hints for all function signatures.
- Keep the core logic in `mnemos/` and CLI interactions in `mnemos/cli.py`.

### Memory Structure
- **Long-term Sections:** Only specific sections are allowed by default: `项目概述`, `架构决策`, `代码风格与约定`, `技术选型`, `重要约束与注意事项`.
- **Short-term Format:** Managed by `mnemos.git`, grouped by date, and includes commit hashes and messages.

### Skill Integration
Mnemos is designed to work with `gemini-cli` by providing context via the `.agent/skills/` directory, which contains skill definitions that the CLI can utilize.

## TODO / Future Improvements
- [ ] Add unit tests for git log parsing and memory file manipulation.
- [ ] Improve the summarization logic with better LLM-friendly formatting.
- [ ] Support for non-git based activity tracking.
