# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**EasyDL** is a structured deep learning curriculum project based on the "Easy Deep Learning" textbook by 혁펜하임. The project combines Obsidian for note-taking, VSCode for code implementation, and automated Git workflows for version control.

**Primary Goal**: Systematic learning of deep learning fundamentals from Chapter 1 (Perceptrons) through Chapter 8 (RNN & Transformers), with hands-on implementation in TensorFlow and PyTorch.

---

## Environment Setup

### Virtual Environment
```bash
# Activate the virtual environment (required before any Python work)
source activate_env.sh

# Test environment setup
python test_environment.py
```

### Python Version & Key Dependencies
- **Python**: 3.12.5
- **Deep Learning**: TensorFlow ≥2.13.0, PyTorch ≥2.0.0
- **Data Science**: NumPy, Pandas, Matplotlib, Seaborn
- **Notebooks**: Jupyter, ipykernel

### Installing Dependencies
```bash
pip install -r requirements.txt
```

---

## Repository Structure

The repository follows a chapter-based organization:

```
EasyDL/
├── 00_학습_가이드/              # Learning guides and curriculum
├── 01_Chapter1_딥러닝_시작/     # Chapter folders follow this pattern
│   ├── notes/                  # Obsidian markdown notes
│   ├── code/                   # Python implementation files
│   └── assets/                 # Images, graphs, resources
├── 02_Chapter2_인공신경망/
├── 03_Chapter3_Gradient_Descent_최적화/
├── 04_Chapter4_이진분류와_다중분류/
├── 05_Chapter5_Universal_Approximation_Theorem/
├── 06_Chapter6_딥러닝_문제와_해결방안/
├── 07_Chapter7_CNN/
├── 08_Chapter8_RNN_Transformer/
├── 99_부록_수학_기초/
├── scripts/                    # Automation scripts
│   ├── auto_commit.sh         # Git auto-commit with smart categorization
│   ├── setup_github.sh        # GitHub repository setup
│   ├── claude_logger.py       # Claude conversation logging
│   └── tistory_poster.py      # Blog posting automation
└── templates/                  # Obsidian note templates
```

### Key Files
- `activate_env.sh`: Virtual environment activation script
- `test_environment.py`: Environment validation (imports TensorFlow, PyTorch, etc.)
- `requirements.txt`: Python dependencies
- `templates/학습_노트_템플릿.md`: Obsidian note template with frontmatter

---

## Git Workflow

### Branch Strategy

This project uses a **two-branch workflow**:

| Branch | Purpose | Commit Frequency |
|--------|---------|------------------|
| **develop** | Daily learning, experiments, code implementation | Automatic (every 10 minutes) |
| **main** | Completed chapters, important milestones | Manual (weekly/monthly) |

**Default branch**: `develop` - All daily work happens here.

### Daily Workflow (develop branch)
```bash
# Ensure you're on develop
git checkout develop

# Work normally - Obsidian Git plugin auto-commits every 10 minutes
# Or manually trigger:
./scripts/auto_commit.sh
```

### Chapter Completion (merge to main)
```bash
# After completing a full chapter
git checkout main
git merge develop
git tag -a v1.0-chapter1 -m "Chapter 1 완료: 딥러닝 시작"
git push origin main --tags
git checkout develop  # Return to develop
```

### Auto-Commit Script Features
The `auto_commit.sh` script intelligently categorizes changes:
- Detects changes in `notes/*.md` (learning notes)
- Detects changes in `code/*.py` (code implementations)
- Detects changes in `assets/` (images/graphs)
- Generates structured commit messages with counts

---

## Development Commands

### Running Code
```bash
# Activate environment first
source activate_env.sh

# Run a specific chapter's code
python 01_Chapter1_딥러닝_시작/code/perceptron.py

# Run with Jupyter (if using notebooks)
jupyter notebook
```

### Testing Environment
```bash
# Verify all dependencies are installed and working
python test_environment.py
```

This script tests:
- TensorFlow and PyTorch imports and basic operations
- NumPy, Pandas, Matplotlib availability
- Matrix multiplication in both frameworks

### Git Operations
```bash
# Manual commit with categorization
./scripts/auto_commit.sh

# Setup GitHub remote (first time)
./scripts/setup_github.sh

# Check current branch
git branch --show-current

# View branch differences
git diff main..develop
```

---

## Code Implementation Patterns

### File Naming Convention
Place implementations in the appropriate chapter's `code/` directory:
- `XX_ChapterX_Topic/code/descriptive_name.py`
- Example: `01_Chapter1_딥러닝_시작/code/perceptron.py`

### Dual Framework Implementation
Most code should support **both TensorFlow and PyTorch** when relevant:
```python
# TensorFlow implementation
import tensorflow as tf
# ... TF code

# PyTorch implementation
import torch
# ... PyTorch code
```

### Code Structure
Follow the template structure from `templates/학습_노트_템플릿.md`:
1. **Theory explanation** - Document in notes/
2. **Code implementation** - Implement in code/
3. **Execution results** - Store outputs/graphs in assets/
4. **Analysis** - Document findings back in notes/

---

## Obsidian Integration

### Note Template Usage
Notes follow a structured template with:
- **Frontmatter**: chapter, topic, lecture_url, date, status, tags
- **Learning objectives**: Checkboxes for goals
- **Theory section**: Core concepts and mathematical background
- **Code implementation**: File paths and execution methods
- **Experimental results**: Graphs and analysis
- **Q&A section**: Claude interactions
- **Key takeaways**: Summary

### Linking Notes
Use Obsidian's internal linking:
```markdown
[[01_퍼셉트론]]
[[다음_주제_링크]]
```

---

## Working with Claude Code

### Typical Workflow
1. **Learning**: User watches lecture, reads textbook
2. **Note-taking**: User writes notes in Obsidian using template
3. **Code implementation**: Claude assists with implementation
4. **Q&A**: Claude answers questions about concepts
5. **Auto-save**: Changes auto-commit to develop branch

### When Implementing Code
- Ask which framework to prioritize (TensorFlow vs PyTorch) if not specified
- Place code in the correct chapter's `code/` directory
- Include clear comments and docstrings
- Provide execution instructions
- Consider adding visualization (matplotlib/seaborn) for results

### When Explaining Concepts
- Reference the lecture URLs from README.md or chapter notes
- Use mathematical notation when appropriate (LaTeX in markdown)
- Connect to previous chapters when relevant
- Suggest practical experiments or modifications

---

## Automation Scripts

### auto_commit.sh
- Detects file changes and categorizes them
- Generates structured commit messages with timestamps
- Optionally pushes to remote
- **Usage**: `./scripts/auto_commit.sh`

### setup_github.sh
- One-time GitHub repository setup
- Configures remote origin
- Pushes initial commit
- **Usage**: `./scripts/setup_github.sh`

### claude_logger.py
- Logs Claude Code conversations for learning records
- **Note**: May need configuration before use

### tistory_poster.py
- Automates blog posting to Tistory (Korean blogging platform)
- **Note**: Requires API credentials setup

---

## Curriculum Overview

### Chapter Sequence
1. **Chapter 1**: 딥러닝 시작 (Perceptron, Neural Network Basics, TensorFlow Basics)
2. **Chapter 2**: 인공신경망 (Understanding ANNs, Linear Regression, Gradient Descent)
3. **Chapter 3**: Gradient Descent 최적화 (SGD, Mini-batch GD, Momentum, RMSProp, Adam)
4. **Chapter 4**: 이진분류와 다중분류 (Binary & Multi-class Classification)
5. **Chapter 5**: Universal Approximation Theorem
6. **Chapter 6**: 딥러닝 문제와 해결방안 (Problems & Solutions)
7. **Chapter 7**: CNN (Convolutional Neural Networks)
8. **Chapter 8**: RNN & Transformer

### Lecture Videos
Each chapter has corresponding YouTube lectures. Links are available in:
- `README.md` (overview)
- `00_학습_가이드/커리큘럼.md` (detailed)
- Individual note frontmatter (lecture_url field)

---

## Important Conventions

### Language
- **Documentation**: Korean (Obsidian notes, README files)
- **Code**: English (variable names, function names, comments can be mixed)
- **Commits**: Korean for auto-commits, English for manual milestone commits

### Status Indicators (in notes)
- 🔄 학습중 (Currently learning)
- ✅ 완료 (Completed)
- ⏳ 대기중 (Pending)

### File Organization
- **Never** commit environment files (EasyDL/ virtual environment directory is in .gitignore)
- **Always** place code in chapter-specific `code/` directories
- **Always** place notes in chapter-specific `notes/` directories
- **Always** place images/graphs in chapter-specific `assets/` directories

---

## Quick Reference

### Most Common Commands
```bash
# Start working
source activate_env.sh
code .  # Open VSCode

# Run code
python XX_ChapterX_Topic/code/file.py

# Test environment
python test_environment.py

# Commit changes
./scripts/auto_commit.sh

# Check branch
git branch --show-current
```

### Key Paths
- Virtual environment: `./EasyDL/`
- Learning guides: `./00_학습_가이드/`
- Templates: `./templates/학습_노트_템플릿.md`
- Scripts: `./scripts/`

---

## Notes for Claude Code

### When Creating New Code
1. Always ask which chapter the code belongs to
2. Use the chapter's `code/` directory
3. Ensure virtual environment activation instructions are clear
4. Test imports before implementing complex logic
5. Provide both TensorFlow and PyTorch versions when applicable

### When Debugging
1. Verify virtual environment is activated
2. Check Python version compatibility (3.12.5)
3. Confirm dependencies are installed via `test_environment.py`
4. Check file paths relative to repository root

### When Explaining
1. Reference the specific lecture video if known
2. Use Korean for explanations (user's primary language)
3. Include mathematical formulas in LaTeX when needed
4. Connect concepts to previous chapters
5. Suggest visualization or experimentation

### Branch Awareness
- **Always** check current branch before suggesting commits
- **Recommend** staying on `develop` for daily work
- **Only suggest** merging to main after chapter completion
- **Never** commit directly to main during active learning
