#!/usr/bin/env python3
"""
Automatic Translation Orchestrator for Claude Code
Provides a simple command to translate all chunks using Claude Code session.

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
    untranslated = []

    for chunk in progress['chunks']:
        chunk_num = chunk['chunk_num']
        trans_file = translations_dir / f"chunk_{chunk_num:03d}_translation.md"

        if not trans_file.exists():
            untranslated.append(chunk_num)

    return untranslated


def show_translation_command(progress, untranslated, project_dir):
    """Display the command to give to Claude Code."""
    total_chunks = len(progress['chunks'])
    source_lang = progress.get('source_lang_name', 'source language')
    target_lang = progress.get('target_lang_name', 'target language')

    print("=" * 80)
    print("AUTOMATIC TRANSLATION - CLAUDE CODE")
    print("=" * 80)
    print(f"Document: {progress['metadata'].get('title', 'Unknown')}")
    print(f"Translation: {source_lang} → {target_lang}")
    print(f"Remaining chunks: {len(untranslated)}/{total_chunks}")
    print(f"Chunks to translate: {untranslated[:10]}{'...' if len(untranslated) > 10 else ''}")
    print("=" * 80)
    print()
    print("📋 INSTRUCTIONS FOR CLAUDE CODE:")
    print()
    print("Copy and paste this command to Claude Code:")
    print()
    print("─" * 80)

    if len(untranslated) <= 5:
        chunks_list = ", ".join(map(str, untranslated))
        print(f'Translate chunks {chunks_list} from {source_lang} to {target_lang} and save them automatically.')
    else:
        print(f'Translate all {len(untranslated)} remaining chunks from {source_lang} to {target_lang} automatically.')

    print("─" * 80)
    print()
    print("💡 Claude Code will:")
    print("  1. Read each chunk source file")
    print(f"  2. Translate from {source_lang} to {target_lang}")
    print("  3. Save to translations/ directory")
    print("  4. Continue with next chunk")
    print("  5. Report progress after each chunk")
    print()
    print("When complete, run:")
    print("  python3 assemble_output.py")
    print("=" * 80)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Show command for automatic translation using Claude Code'
    )
    parser.add_argument(
        '--project-dir',
        default='.',
        help='Project directory (default: current directory)'
    )

    args = parser.parse_args()

    # Load project
    project_dir = Path(args.project_dir).expanduser()
    progress = load_progress(project_dir)

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

    # Show command
    show_translation_command(progress, untranslated, project_dir)


if __name__ == '__main__':
    main()
