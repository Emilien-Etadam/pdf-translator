# Quick Start Guide - Multilingual PDF Translation

Get started translating PDFs between any language pair in 3 steps.

## Step 1: Extract PDF & Configure Languages

```bash
python3 extract_pdf.py "your-document.pdf"
```

**Interactive prompts will ask:**

1. **Source language** - Language of your PDF
2. **Target language** - Desired translation language

**Example:**
```
Select source language:
  1. en  - English
  2. fr  - Français
  ...
Enter number: 1

Select target language:
  1. en  - English
  2. fr  - Français
  ...
Enter number: 2
```

**Result:**
- Creates `chunks/` directory with text segments
- Creates `progress.json` with configuration
- Ready for translation!

## Step 2: Translate Automatically

```bash
python3 auto_translate.py
```

**That's it!** Claude Code automatically detects and translates all chunks!

Like AUTOCLAUDE, it will:
- ✅ Read each chunk
- ✅ Translate it
- ✅ Save the result
- ✅ Continue with next chunk
- ✅ Report progress

## Step 3: Assemble Final Output

```bash
python3 assemble_output.py
```

**Result:**
- Creates `output/your-document_[lang].md` (Markdown)
- Creates `output/your-document_[lang].html` (HTML)
- Complete translated document!

## That's It!

### Check Progress Anytime

```bash
python3 translate_helper.py --status
```

### Resume After Break

```bash
python3 translate_helper.py --next
```

The system remembers where you left off!

---

## Common Language Pairs

### English → French
```bash
python3 extract_pdf.py "book.pdf"
# Select: 1 (English) → 2 (Français)
```

### Spanish → English
```bash
python3 extract_pdf.py "libro.pdf" --source-lang es --target-lang en
```

### German → French
```bash
python3 extract_pdf.py "buch.pdf" --source-lang de --target-lang fr
```

---

## Quick Commands Reference

| Action | Command |
|--------|---------|
| Extract PDF | `python3 extract_pdf.py "file.pdf"` |
| Check status | `python3 translate_helper.py --status` |
| Show next chunk | `python3 translate_helper.py --next` |
| Show specific chunk | `python3 translate_helper.py --chunk 5` |
| Assemble final output | `python3 assemble_output.py` |
| Check assembly status | `python3 assemble_output.py --status` |

---

## Example Translation Session

```
You: "python3 extract_pdf.py 'mybook.pdf'"
System: [Asks for source/target languages]
You: [Select English → French]

You: "python3 translate_helper.py --next"
System: [Shows chunk 1 content]

You (to Claude): "Translate this chunk and save it"
Claude: [Translates and saves to translations/]

You: "Translate the next 3 chunks"
Claude: [Translates chunks 2, 3, 4]

[Take a break - progress is saved]

You: "python3 translate_helper.py --status"
System: [Shows 4/10 chunks done]

You (to Claude): "Continue translating"
Claude: [Picks up from chunk 5]

[When all done]
You: "python3 assemble_output.py"
System: [Creates final translated document]
```

---

## Need Help?

See full documentation in [README.md](README.md)

**Common issues:**
- PDF not found? Check file path
- Want to restart? Delete `progress.json` and re-run step 1
- Translation quality? Provide context to Claude about document type
