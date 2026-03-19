# Microsoft Learn Transcript Extractor

This is a lightweight Python tool that converts Microsoft Learn lesson pages into clean text transcripts for offline study. The script downloads lesson pages, removes navigation and UI elements, and extracts only the educational content.

---

## Features

- Download Microsoft Learn lesson pages
- Extract readable lesson text
- Remove UI elements (reading time, feedback blocks, navigation)
- Save transcripts as `.txt` files
- Combine multiple lessons into a single module transcript

---

## Installation

Clone the repository:

```bash
git clone https://github.com/giulianodileo/microsoft-learn-transcriber.git
cd microsoft-learn-transcriber
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the script:

```bash
python learn_transcript_extractor.py
```

Paste lesson URLs when prompted:

```
URL: https://learn.microsoft.com/...lesson1
URL: https://learn.microsoft.com/...lesson2
URL:
```

Press **Enter on an empty line** to start processing.

---

## Output

The script creates two folders:

```
downloaded_HTMLs/
clean_transcripts/
```

Example:

```
clean_transcripts/
├─ describe-cloud-compute_4-describe-shared-responsibility-model.txt
├─ describe-cloud-compute_6-describe-consumption-based-model.txt
└─ module_transcript.txt
```

---

## Why this tool?

Microsoft Learn pages contain navigation, UI components, and interactive elements that make copying content difficult.

This tool extracts **only the lesson text**, producing clean study notes.

---

## Disclaimer

This project is an independent study tool and is not affiliated with or endorsed by Microsoft.

All Microsoft Learn content remains the property of Microsoft.
Users are responsible for complying with Microsoft's terms of service.

---

## License

MIT License
