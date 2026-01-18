#!/usr/bin/env python3
"""
PDF Text Extraction and Chunking Tool
Extracts text from PDFs and splits into manageable chunks for translation.

Author: Austin Morrissey
Co-Authored-By: Claude <noreply@anthropic.com>
"""

import json
import PyPDF2
from pathlib import Path
import argparse
import sys


# Common languages with full names
LANGUAGES = {
    'en': 'English',
    'fr': 'Français',
    'es': 'Español',
    'de': 'Deutsch',
    'it': 'Italiano',
    'pt': 'Português',
    'ru': 'Русский',
    'zh': '中文',
    'ja': '日本語',
    'ko': '한국어',
    'ar': 'العربية',
    'hi': 'हिन्दी',
    'nl': 'Nederlands',
    'pl': 'Polski',
    'sv': 'Svenska',
    'tr': 'Türkçe',
    'other': 'Other'
}


def ask_language_interactive(prompt_text):
    """Ask user to select a language interactively."""
    print("\n" + "=" * 80)
    print(prompt_text)
    print("=" * 80)
    print("\nAvailable languages:")

    # Display languages in a nice format
    lang_codes = [code for code in LANGUAGES.keys() if code != 'other']
    for i, code in enumerate(lang_codes, 1):
        print(f"  {i:2d}. {code:3s} - {LANGUAGES[code]}")
    print(f"  {len(lang_codes) + 1:2d}. other - Other (type manually)")

    while True:
        try:
            choice = input(f"\nEnter number (1-{len(lang_codes) + 1}): ").strip()
            choice_num = int(choice)

            if 1 <= choice_num <= len(lang_codes):
                selected_code = lang_codes[choice_num - 1]
                print(f"✓ Selected: {LANGUAGES[selected_code]} ({selected_code})")
                return selected_code, LANGUAGES[selected_code]
            elif choice_num == len(lang_codes) + 1:
                custom_code = input("Enter language code (e.g., 'vi' for Vietnamese): ").strip().lower()
                custom_name = input("Enter language name (e.g., 'Tiếng Việt'): ").strip()
                print(f"✓ Selected: {custom_name} ({custom_code})")
                return custom_code, custom_name
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(lang_codes) + 1}.")
        except (ValueError, KeyboardInterrupt):
            print("\nCancelled.")
            sys.exit(0)


class PDFExtractor:
    """Handles PDF text extraction and chunking."""

    def __init__(self, pdf_path, output_dir, chunk_size=20, source_lang=None, target_lang=None,
                 source_lang_name=None, target_lang_name=None):
        """
        Initialize the PDF extractor.

        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save chunks
            chunk_size: Number of pages per chunk
            source_lang: Source language code
            target_lang: Target language code
            source_lang_name: Source language full name
            target_lang_name: Target language full name
        """
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)
        self.chunk_size = chunk_size
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.source_lang_name = source_lang_name
        self.target_lang_name = target_lang_name
        self.chunks_dir = self.output_dir / 'chunks'
        self.progress_file = self.output_dir / 'progress.json'

        # Create directories
        self.chunks_dir.mkdir(parents=True, exist_ok=True)

    def extract_metadata(self):
        """Extract PDF metadata."""
        with open(self.pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            metadata = {
                'total_pages': len(reader.pages),
                'title': None,
                'author': None,
            }

            if reader.metadata:
                metadata['title'] = reader.metadata.get('/Title', None)
                metadata['author'] = reader.metadata.get('/Author', None)

            return metadata

    def extract_page(self, reader, page_num):
        """Extract text from a single page."""
        try:
            page = reader.pages[page_num]
            text = page.extract_text()
            return text.strip()
        except Exception as e:
            print(f"Warning: Error extracting page {page_num + 1}: {e}")
            return ""

    def create_chunk(self, reader, start_page, end_page, chunk_num):
        """
        Extract and save a chunk of pages.

        Args:
            reader: PyPDF2 reader object
            start_page: Starting page number (0-indexed)
            end_page: Ending page number (0-indexed, inclusive)
            chunk_num: Chunk number for filename
        """
        chunk_text = []

        # Add header
        chunk_text.append(f"# Pages {start_page + 1}-{end_page + 1}")
        chunk_text.append(f"# Chunk {chunk_num}")
        chunk_text.append("=" * 80)
        chunk_text.append("")

        # Extract pages
        for page_num in range(start_page, end_page + 1):
            text = self.extract_page(reader, page_num)

            if text:
                chunk_text.append(f"[PAGE {page_num + 1}]")
                chunk_text.append(text)
                chunk_text.append("")
                chunk_text.append("-" * 80)
                chunk_text.append("")

        # Save chunk
        filename = f"chunk_{chunk_num:03d}_pages_{start_page + 1:03d}_{end_page + 1:03d}.txt"
        filepath = self.chunks_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(chunk_text))

        return {
            'chunk_num': chunk_num,
            'filename': filename,
            'start_page': start_page + 1,
            'end_page': end_page + 1,
            'page_count': end_page - start_page + 1,
            'translated': False
        }

    def extract_all(self, start_page=0):
        """
        Extract all pages from PDF into chunks.

        Args:
            start_page: Starting page number (0-indexed)
        """
        print(f"Opening PDF: {self.pdf_path}")

        with open(self.pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            total_pages = len(reader.pages)

            print(f"Total pages: {total_pages}")
            print(f"Chunk size: {self.chunk_size} pages")

            # Extract metadata
            metadata = self.extract_metadata()
            if metadata['title']:
                print(f"Title: {metadata['title']}")
            if metadata['author']:
                print(f"Author: {metadata['author']}")

            print(f"\nExtracting chunks...")
            print("=" * 80)

            chunks = []
            chunk_num = 1
            current_page = start_page

            while current_page < total_pages:
                end_page = min(current_page + self.chunk_size - 1, total_pages - 1)

                print(f"Chunk {chunk_num}: Pages {current_page + 1}-{end_page + 1}")

                chunk_info = self.create_chunk(reader, current_page, end_page, chunk_num)
                chunks.append(chunk_info)

                current_page = end_page + 1
                chunk_num += 1

            # Save progress
            progress = {
                'pdf_file': str(self.pdf_path),
                'metadata': metadata,
                'chunk_size': self.chunk_size,
                'total_chunks': len(chunks),
                'source_lang': self.source_lang,
                'source_lang_name': self.source_lang_name,
                'target_lang': self.target_lang,
                'target_lang_name': self.target_lang_name,
                'chunks': chunks
            }

            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)

            print("=" * 80)
            print(f"\n✓ Extraction complete!")
            print(f"  Total chunks created: {len(chunks)}")
            print(f"  Chunks directory: {self.chunks_dir}")
            print(f"  Progress file: {self.progress_file}")
            print(f"\nNext step: Use Claude Code to translate chunks from {self.source_lang_name} to {self.target_lang_name}")
            print(f'  Example: "translate chunk 1 from {self.source_lang_name} to {self.target_lang_name}"')
            print(f'  Or simply: "translate chunk 1"')


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Extract and chunk PDF text for translation'
    )
    parser.add_argument(
        'pdf_file',
        help='Path to PDF file'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Output directory (default: current directory)'
    )
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=20,
        help='Pages per chunk (default: 20)'
    )
    parser.add_argument(
        '--start-page',
        type=int,
        default=1,
        help='Starting page number (default: 1)'
    )
    parser.add_argument(
        '--source-lang',
        help='Source language code (e.g., en, fr). If not provided, will ask interactively.'
    )
    parser.add_argument(
        '--target-lang',
        help='Target language code (e.g., en, fr). If not provided, will ask interactively.'
    )
    parser.add_argument(
        '--non-interactive',
        action='store_true',
        help='Non-interactive mode (requires --source-lang and --target-lang)'
    )

    args = parser.parse_args()

    # Expand paths
    pdf_path = Path(args.pdf_file).expanduser()
    output_dir = Path(args.output_dir).expanduser()

    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    # Determine languages
    if args.non_interactive:
        if not args.source_lang or not args.target_lang:
            print("Error: --source-lang and --target-lang are required in non-interactive mode", file=sys.stderr)
            sys.exit(1)
        source_lang = args.source_lang
        target_lang = args.target_lang
        source_lang_name = LANGUAGES.get(source_lang, source_lang.capitalize())
        target_lang_name = LANGUAGES.get(target_lang, target_lang.capitalize())
    else:
        # Interactive language selection
        if args.source_lang:
            source_lang = args.source_lang
            source_lang_name = LANGUAGES.get(source_lang, source_lang.capitalize())
            print(f"Source language: {source_lang_name} ({source_lang})")
        else:
            source_lang, source_lang_name = ask_language_interactive("SELECT SOURCE LANGUAGE (language of the PDF)")

        if args.target_lang:
            target_lang = args.target_lang
            target_lang_name = LANGUAGES.get(target_lang, target_lang.capitalize())
            print(f"Target language: {target_lang_name} ({target_lang})")
        else:
            target_lang, target_lang_name = ask_language_interactive("SELECT TARGET LANGUAGE (desired translation)")

    # Display summary
    print("\n" + "=" * 80)
    print("TRANSLATION PROJECT SETUP")
    print("=" * 80)
    print(f"PDF file: {pdf_path.name}")
    print(f"Translation: {source_lang_name} → {target_lang_name}")
    print(f"Chunk size: {args.chunk_size} pages")
    print(f"Output directory: {output_dir}")
    print("=" * 80)

    # Create extractor and run
    extractor = PDFExtractor(
        pdf_path=pdf_path,
        output_dir=output_dir,
        chunk_size=args.chunk_size,
        source_lang=source_lang,
        target_lang=target_lang,
        source_lang_name=source_lang_name,
        target_lang_name=target_lang_name
    )

    extractor.extract_all(start_page=args.start_page - 1)


if __name__ == '__main__':
    main()
