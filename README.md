# Infix-aware Rule-based Stemming for the Rejang Language

## Description
This repository contains the official datasets and source code implementation for the research paper titled "Infix-aware rule-based stemming for the Rejang language". This project introduces a morphology-aware rule-based stemming framework designed specifically for the Rejang language—a low-resource regional language in Indonesia with an agglutinative structure. The system explicitly processes 18 morphological rules spanning prefixes, suffixes, confixes, and infixes using a linguistically motivated deletion-order strategy.

## Dataset Information
The repository includes the following dataset files used for system development, validation, and evaluation:
- `rejang_morphology_dataset.csv`: Contains 9,000 affixed words manually annotated with their structural affix category, pattern, ground truth base word, and Indonesian/English glosses.
- `rejang_document_evaluation.csv`: Contains 15 validated Rejang language text documents (~4,250 words) including folktales, conversations, and learning texts for document-level testing.
- `rejang_stemming_dataset_package.xlsx`: Complete evaluation package comprising data splits for baseline configuration, ablation studies, and error analysis.

## Code Information
- `stemmer.py`: The primary Python program implementing the modular 18 linguistic rules, regex-based string matching, the priority-based deletion sequence (Confix -> Prefix -> Infix -> Suffix), and hash table lexicon validation.

## Requirements
- Python 3.11 or higher
- Pandas (for handling the evaluation dataset)
- Openpyxl (required for loading the `.xlsx` dataset package)

To install dependencies:
```bash
pip install pandas openpyxl
```bash

from stemmer import RejangStemmer
   
stemmer = RejangStemmer()
print(stemmer.stem("temelak")) # Example input with infix

Wibowo, S. H., Handhayani, T. S., Wibowo, N. S. T., & Wibowo, C. S. T. (2026). Infix-aware rule-based stemming for the Rejang language. PeerJ Computer Science.

