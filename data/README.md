# Dataset Sources

## Overview
This dataset consists of 5 automotive and laptop product manuals in PDF format,
used as the knowledge base for the RAG (Retrieval-Augmented Generation) chatbot.

---

## PDF Files

| File Name | Brand | Source URL | Type |
|-----------|-------|-----------|------|
| fortuner_2025_mannual.pdf | Toyota Fortuner 2025 | https://www.toyotabharat.com/q-service/owners-manual/ | Owner's Manual |
| innova-crysta2024_mannual.pdf | Toyota Innova Crysta 2024 | https://www.toyotabharat.com/q-service/owners-manual/ | Owner's Manual |
| dell_mannual_Inspiron_153000.pdf | Dell Inspiron 15 3000 | https://www.dell.com/support/manuals/en-in/inspiron-15-3565-laptop/inspiron-15-3565-setup-specifications/set-up-your-computer | Setup & Specifications Manual |
| hp_mannual.pdf | HP Laptop | https://h10032.www1.hp.com/ctg/Manual/c05633409.pdf | User Guide |
| lennova_mannual.pdf | Lenovo ThinkPad X250 | https://download.lenovo.com/pccbbs/mobiles_pdf/x250_ug_en.pdf | User Guide |

---

## Dataset Stats

- **Total PDFs:** 5
- **Categories:** Automotive (2), Laptops/PCs (3)
- **Brands covered:** Toyota, Dell, HP, Lenovo
- **Estimated total pages:** 500+

---

## Usage

These PDFs are stored locally in `data/raw/` and are excluded from version control
via `.gitignore` due to file size and copyright.

The ingestion pipeline (`src/ingest.py`) loads, chunks, and embeds these documents
into a FAISS vector index stored at `data/faiss_index/`.

---

## Notes

- PDFs are public domain / publicly available from official manufacturer websites
- All sources are official brand documentation
- Do NOT commit raw PDFs to GitHub
