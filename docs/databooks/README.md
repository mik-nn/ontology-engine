---
databook:
  created: '2026-04-20'
  hierarchy: 3
  id: README
  layer: meta
  process:
    transformer: human
  scope: project
  synced_at: '2026-04-21T14:11:17.445955+00:00'
  title: Readme
  type: plain-doc
  version: '0.1'
---

# Excalidraw Library Tools

This directory contains scripts for working with Excalidraw libraries, enabling efficient token usage by AI assistants and streamlined diagram creation processes.

## Project Overview

The project comprises several Python scripts designed to manipulate Excalidraw library files (`*.excalidrawlib`). These scripts facilitate the splitting of library files into individual icon JSON files and the addition of icons and arrows to existing `.excalidraw` diagrams. The tools are particularly useful for integrating visual elements into AI-driven workflows, ensuring that each step is efficient and organized.

## System Requirements

- **Operating Systems**: Windows, macOS, Linux
- **Python Version**: 3.6 or higher
- **Dependencies**: No additional dependencies required (uses only standard library)

## Installation Instructions

### On Windows

1. **Install Python**:
   - Download the latest version of Python from [python.org](https://www.python.org/downloads/).
   - Ensure that "Add Python to PATH" is selected during installation.

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/excalidraw-diagram-generator.git
   cd excalidraw-diagram-generator/scripts
   ```

### On macOS

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**:
   ```bash
   brew install python
   ```

3. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/excalidraw-diagram-generator.git
   cd excalidraw-diagram-generator/scripts
   ```

### On Linux

1. **Install Python** (using your package manager):
   - For Ubuntu/Debian:
     ```bash
     sudo apt update
     sudo apt install python3
     ```
   - For Fedora:
     ```bash
     sudo dnf install python3
     ```

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/excalidraw-diagram-generator.git
   cd excalidraw-diagram-generator/scripts
   ```

## Usage

### split-excalidraw-library.py

Splits an Excalidraw library file into individual icon JSON files for efficient token usage by AI assistants.

**Prerequisites**:
- Python 3.6 or higher
- No additional dependencies required (uses only standard library)

**Usage**:
```bash
python split-excalidraw-library.py <path-to-library-directory>
```

**Step-by-Step Workflow**:

1. **Create library directory**:
   ```bash
   mkdir -p skills/excalidraw-diagram-generator/libraries/aws-architecture-icons
   ```

2. **Download and place library file**:
   - Visit: https://libraries.excalidraw.com/
   - Search for "AWS Architecture Icons" and download the `.excalidrawlib` file
   - Rename it to match the directory name: `aws-architecture-icons.excalidrawlib`
   - Place it in the directory created in step 1

3. **Run the script**:
   ```bash
   python skills/excalidraw-diagram-generator/scripts/split-excalidraw-library.py skills/excalidraw-diagram-generator/libraries/aws-architecture-icons/
   ```

### add-icon-to-diagram.py

Adds a specific icon from a split Excalidraw library into an existing `.excalidraw` diagram. The script handles coordinate translation and ID collision avoidance, and can optionally add a label under the icon.

**Prerequisites**:
- Python 3.6 or higher
- A diagram file (`.excalidraw`)
- A split icon library directory (created by `split-excalidraw-library.py`)

**Usage**:
```bash
python add-icon-to-diagram.py <diagram-path> <icon-name> <x> <y> [OPTIONS]
```

**Options**:
- `--library-path PATH` : Path to the icon library directory (default: `aws-architecture-icons`)
- `--label TEXT` : Add a text label below the icon
- `--use-edit-suffix` : Edit via `.excalidraw.edit` to avoid editor overwrite issues (enabled by default; pass `--no-use-edit-suffix` to disable)

### add-arrow.py

Adds a straight arrow between two points in an existing `.excalidraw` diagram. Supports optional labels and line styles.

**Prerequisites**:
- Python 3.6 or higher
- A diagram file (`.excalidraw`)

**Usage**:
```bash
python add-arrow.py <diagram-path> <from-x> <from-y> <to-x> <to-y> [OPTIONS]
```

**Options**:
- `--style {solid|dashed|dotted}` : Line style (default: `solid`)
- `--color HEX` : Arrow color (default: `#1e1e1e`)
- `--label TEXT` : Add a text label on the arrow
- `--use-edit-suffix` : Edit via `.excalidraw.edit` to avoid editor overwrite issues (enabled by default; pass `--no-use-edit-suffix` to disable)

## License Considerations

When using third-party icon libraries:
- **AWS Architecture Icons**: Subject to AWS Content License
- **GCP Icons**: Subject to Google's terms
- **Other libraries**: Check each library's license

This script is for personal/organizational use. Redistribution of split icon files should comply with the original library's license terms.

## Troubleshooting

**Error: File not found**
- Check that the file path is correct
- Make sure the file has a `.excalidrawlib` extension

**Error: Invalid library file format**
- Ensure the file is a valid Excalidraw library file
- Check that it contains a `libraryItems` array
