# Multilingual PDF Translation System

A semi-automated PDF translation system using Claude Code as the translation engine. Supports **any language pair** with an interactive CLI interface.

## ✨ Features

- 🌍 **Multilingual Support** - Translate between any language pair (English ↔ French, Spanish → German, etc.)
- 💬 **Interactive CLI** - Simple question-and-answer interface for configuration
- 💰 **No API costs** - Uses Claude Code session
- 📚 **High-quality translation** - Literary-quality output preserving style and context
- 📊 **Progress tracking** - Resume capability for large documents
- 📄 **Multiple output formats** - Markdown and HTML
- 🔄 **Reusable** - Works with any PDF document

## 🚀 Quick Start

### 1. Extract PDF and Configure Languages

```bash
python3 extract_pdf.py "path/to/your.pdf"
```

The tool will interactively ask you:
- **Source language** (the language of your PDF)
- **Target language** (desired translation language)
- **Chunk size** (optional, defaults to 20 pages)

**Example interaction:**
```
================================================================================
SELECT SOURCE LANGUAGE (language of the PDF)
================================================================================

Available languages:
   1. en  - English
   2. fr  - Français
   3. es  - Español
   4. de  - Deutsch
   5. it  - Italiano
   ...

Enter number (1-16): 1
✓ Selected: English (en)

================================================================================
SELECT TARGET LANGUAGE (desired translation)
================================================================================
...
Enter number (1-16): 2
✓ Selected: Français (fr)
```

**Non-interactive mode** (for scripts):
```bash
python3 extract_pdf.py "book.pdf" --source-lang en --target-lang fr --non-interactive
```

### 2. Check Translation Status

```bash
python3 translate_helper.py --status
```

Shows:
- Language pair
- Total pages and chunks
- Progress percentage
- List of translated/pending chunks

### 3. Translate Chunks Automatically

**Fully automatic translation with Claude Code:**

```bash
python3 auto_translate.py
```

This shows you a simple command to copy-paste. Then just tell Claude Code:

```
"Translate all remaining chunks from English to Français automatically"
```

Claude Code will automatically:
- Read each chunk
- Translate it
- Save to translations/
- Continue with the next one
- Report progress

**Alternative - Manual chunk by chunk:**

```bash
python3 translate_helper.py --next
```

Then tell Claude Code: `"Translate this chunk and save it"`

### 4. Assemble Final Output

```bash
# Create both Markdown and HTML
python3 assemble_output.py

# Just Markdown
python3 assemble_output.py --format markdown

# Check status without assembling
python3 assemble_output.py --status
```

Output files are saved to the `output/` directory with language-specific naming.

## 📁 Project Structure

```
your-project/
├── extract_pdf.py           # Extract and configure translation project
├── translate_helper.py      # Translation workflow helper
├── assemble_output.py       # Assemble final output
├── chunks/                  # Extracted source text (auto-created)
├── translations/            # Translated chunks (auto-created)
├── output/                  # Final combined output (auto-created)
└── progress.json            # Project configuration & progress
```

## 🌍 Supported Languages

The interactive CLI supports:

- **English** (en)
- **Français** (fr)
- **Español** (es)
- **Deutsch** (de)
- **Italiano** (it)
- **Português** (pt)
- **Русский** (ru)
- **中文** (zh)
- **日本語** (ja)
- **한국어** (ko)
- **العربية** (ar)
- **हिन्दी** (hi)
- **Nederlands** (nl)
- **Polski** (pl)
- **Svenska** (sv)
- **Türkçe** (tr)
- **Other** - Custom language input

## 📖 Usage Examples

### Example 1: English → French

```bash
python3 extract_pdf.py "english-book.pdf"
# Select: 1 (English) → 2 (Français)

python3 translate_helper.py --next
# Claude translates chunk to French

python3 assemble_output.py
# Creates: english-book_fr.md
```

### Example 2: Spanish → German

```bash
python3 extract_pdf.py "libro-español.pdf" --source-lang es --target-lang de
python3 translate_helper.py --next
# ... translate chunks ...
python3 assemble_output.py
```

### Example 3: Using Custom Language

```bash
python3 extract_pdf.py "vietnamese-doc.pdf"
# Select "other" for source
# Enter: vi (Vietnamese)
# Enter: Tiếng Việt
```

## 🛠️ Advanced Options

### extract_pdf.py

```bash
# Custom chunk size (smaller for complex texts)
python3 extract_pdf.py "book.pdf" --chunk-size 10

# Start from specific page
python3 extract_pdf.py "book.pdf" --start-page 50

# Custom output directory
python3 extract_pdf.py "book.pdf" --output-dir ~/my-translation

# Non-interactive (for automation)
python3 extract_pdf.py "book.pdf" --source-lang en --target-lang fr --non-interactive
```

### translate_helper.py

```bash
# Show overall progress
python3 translate_helper.py --status

# Show next untranslated chunk
python3 translate_helper.py --next

# Show specific chunk
python3 translate_helper.py --chunk 5

# Custom project directory
python3 translate_helper.py --project-dir ~/my-project --next
```

### assemble_output.py

```bash
# Create all formats (default)
python3 assemble_output.py

# Markdown only
python3 assemble_output.py --format markdown

# HTML only
python3 assemble_output.py --format html

# Check status
python3 assemble_output.py --status
```

## 📋 Workflow Script

The included `translate.sh` provides shortcuts:

```bash
./translate.sh status    # Show progress
./translate.sh next      # Show next chunk
./translate.sh chunk 5   # Show chunk 5
./translate.sh assemble  # Create final output
```

## 💡 Translation Quality Tips

### For Best Results

1. **Review periodically** - Check translations every few chunks
2. **Provide context** - Mention document type (technical, literary, legal, etc.)
3. **Consistency** - Let Claude know about terminology preferences
4. **Adjust as needed** - Request retranslation if quality varies

### Example Claude Instructions

```
"This is a technical manual about aviation. Please maintain formal tone
and preserve technical terminology."

"This is a literary novel. Focus on preserving the author's voice and
emotional tone while adapting cultural references for French readers."

"Retranslate chunk 3 with more formal language"
```

## 🔧 Requirements

- Python 3.6+
- PyPDF2 (auto-installed)
- markdown (optional, for HTML output)

Install optional dependencies:
```bash
pip3 install markdown
```

## 📚 Use Cases

- **Books & Novels** - Literary translation with style preservation
- **Academic Papers** - Technical translation maintaining precision
- **Legal Documents** - Formal translation with consistent terminology
- **Technical Manuals** - Accurate translation of specialized content
- **Business Documents** - Professional translation
- **Articles & Reports** - Any multi-page PDF content

## 🎯 Common Translation Pairs

Popular language combinations:
- 🇬🇧 English ↔ 🇫🇷 French
- 🇬🇧 English ↔ 🇪🇸 Spanish
- 🇬🇧 English ↔ 🇩🇪 German
- 🇬🇧 English ↔ 🇯🇵 Japanese
- 🇫🇷 French ↔ 🇪🇸 Spanish
- 🇷🇺 Russian ↔ 🇬🇧 English
- 🇨🇳 Chinese ↔ 🇬🇧 English

## 🐛 Troubleshooting

### Chunk file not found
```bash
# Re-run extraction
python3 extract_pdf.py "your.pdf"
```

### Language configuration incorrect
```bash
# Delete progress.json and re-extract
rm progress.json
python3 extract_pdf.py "your.pdf"
```

### Translation quality issues
```
Tell Claude: "Please provide more context about document type and
adjust translation style accordingly"
```

### Want to retranslate
```
"Retranslate chunk 3 with a different approach"
```

## 📊 Output Formats

### Markdown
- Clean, readable format
- Preserved structure and headings
- Page number references
- Easy to edit or convert further

### HTML
- Styled web version
- Beautiful typography
- Dark/light mode support
- Print-friendly CSS
- Responsive design

## 🔄 Resume Capability

The system automatically tracks progress in `progress.json`:

```bash
# After a break, just continue
python3 translate_helper.py --next

# Check what's left
python3 translate_helper.py --status
```

## 📜 License

MIT License - Feel free to use and modify

## 🤝 Credits

Co-Authored by gvmfhy & Claude Sonnet 4.5 (Anthropic)

Built as a flexible, multilingual tool for translating any PDF document between any language pair using Claude Code.

---

**Ready to start?**

```bash
python3 extract_pdf.py "your-document.pdf"
```
