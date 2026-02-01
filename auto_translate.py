#!/usr/bin/env python3
"""
Automatic Translation Orchestrator for Claude Code
Automatically triggers translation of all chunks in the current Claude Code session.

Author: Austin Morrissey
Co-Authored-By: Claude <noreply@anthropic.com>
"""

import json
import sys
from pathlib import Path
import argparse


def load_progress(project_dir):
    """Load progress.json file."""
    progress_file = Path(project_dir) / 'progress.json'

    if not progress_file.exists():
        print("Error: progress.json not found. Run extract_pdf.py first.", file=sys.stderr)
        sys.exit(1)

    with open(progress_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_untranslated_chunks(progress, project_dir):
    """Get list of chunks that need translation."""
    translations_dir = Path(project_dir) / 'translations'
    translations_dir.mkdir(exist_ok=True)
    untranslated = []

    for chunk in progress['chunks']:
        chunk_num = chunk['chunk_num']
        trans_file = translations_dir / f"chunk_{chunk_num:03d}_translation.md"

        if not trans_file.exists():
            untranslated.append(chunk_num)

    return untranslated


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Automatic translation using Claude Code (like AUTOCLAUDE)'
    )
    parser.add_argument(
        '--project-dir',
        default='.',
        help='Project directory (default: current directory)'
    )

    args = parser.parse_args()

    # Load project
    project_dir = Path(args.project_dir).expanduser().resolve()
    progress = load_progress(project_dir)

    # Get translation info
    source_lang = progress.get('source_lang_name', 'source language')
    target_lang = progress.get('target_lang_name', 'target language')
    total_chunks = len(progress['chunks'])

    # Get untranslated chunks
    untranslated = get_untranslated_chunks(progress, project_dir)

    if not untranslated:
        print("=" * 80)
        print("✅ ALL CHUNKS TRANSLATED!")
        print("=" * 80)
        print()
        print("Next step: Assemble final output")
        print("  python3 assemble_output.py")
        print("=" * 80)
        return

    # Display info
    print("=" * 80)
    print("🤖 AUTOMATIC TRANSLATION MODE")
    print("=" * 80)
    print(f"Document: {progress['metadata'].get('title', 'Unknown')}")
    print(f"Translation: {source_lang} → {target_lang}")
    print(f"Total chunks: {total_chunks}")
    print(f"Already done: {total_chunks - len(untranslated)}")
    print(f"Remaining: {len(untranslated)}")
    print(f"Project dir: {project_dir}")
    print("=" * 80)
    print()

    # Create the instruction file that Claude Code will detect
    instruction = {
        "action": "translate_all_chunks",
        "project_dir": str(project_dir),
        "source_lang": source_lang,
        "target_lang": target_lang,
        "chunks_to_translate": untranslated,
        "total_chunks": total_chunks
    }

    instruction_file = project_dir / '.translation_task.json'
    with open(instruction_file, 'w', encoding='utf-8') as f:
        json.dump(instruction, f, indent=2, ensure_ascii=False)

    print("🚀 TRIGGERING AUTOMATIC TRANSLATION...")
    print()
    print(f"Claude Code: Please translate all {len(untranslated)} remaining chunks")
    print(f"from {source_lang} to {target_lang}.")
    print()
    print(f"Chunks to translate: {untranslated}")
    print()
    print("Task details saved to: .translation_task.json")
    print()
    print("=" * 80)
    print("⏳ Waiting for Claude Code to start translation...")
    print("=" * 80)


if __name__ == '__main__':
    main()
