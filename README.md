# Aria Gen 1 Assistive AI

> **Note:** For detailed setup, usage, and troubleshooting instructions, see [aria_ai_caption/README.md](aria_ai_caption/README.md).

## Project Overview
- Real-time captioning pipeline for visually impaired users
- Runs locally on macOS M3 Pro, later scalable to GPU cluster

## Repository Structure
- `/sdk/`     → Aria SDK setup and helper scripts  
- `/models/`   → Vision-Language model wrappers (e.g. BLIP, mPLUG)  
- `/scripts/`  → Data-capture and inference scripts  
- `/notebooks/` → Jupyter notebooks for prototyping  
- `/docs/`    → Design docs, diagrams, any UML

## Getting Started
1. Install Aria Gen 1 SDK (see `/sdk/INSTALL.md`)  
2. Create a Python virtual environment  
3. Run `python capture_inference.py` to test camera feed  
4. ...
