# Infix-aware Rule-based Stemming for the Rejang Language

## Description
This repository contains the official datasets and source code implementation for the research paper titled "Infix-aware rule-based stemming for the Rejang language". This project introduces a morphology-aware rule-based stemming framework designed specifically for the Rejang language a low-resource regional language in Indonesia with an agglutinative structure. The system explicitly processes 18 morphological rules spanning prefixes, suffixes, confixes, and infixes using a linguistically motivated deletion-order strategy.

## Dataset Information
This repository includes a manually created and verified Rejang language morphology dataset, consisting of:
**Word-level dataset:** 9,000 affix words spread across prefixes, suffixes, infixes, and confixes (`rejang_morphology_dataset_3.csv`).
**Document-level dataset:** 15 Rejang language text documents containing approximately 4,250 words representing real-world regional contexts (`rejang_document_evaluation_3.csv`).
**Lexicon:** A digital dictionary consisting of 6,983 Rejang basic root words used for validation during the stemming process, securely compiled inside `rejang_stemming_dataset_package_3.xlsx`.

## Code Information
The computational model is entirely rule-based and consists of 18 morphological rules derived from word formation patterns in the Rejang language. The architecture components include text normalization, affix detection, deletion-order sequence processing, rule-based stemming, and lexicon validation via a hash table lookup.

## Usage Instruction
1.  Clone this repository to your local machine:
git clone [https://github.com/sastiahendriwibowo-web/Infix-aware-rule-based-stemming-for-the-Rejang-language-.git](https://github.com/sastiahendriwibowo-web/Infix-aware-rule-based-stemming-for-the-Rejang-language-.git)
2.  Run the main Python script to open the evaluation and testing GUI:
python stemmer-2.py
3.  Lexicon & Dataset Validation:
The script automatically attempts to load default text configurations. To evaluate the latest version 3 data packages, use the built-in GUI interactive utility buttons **"Buka Dataset Baru"** to load `rejang_morphology_dataset_3.csv` and **"Buka Lexicon Baru"** to load your target validation dictionary.

## Requirements
*   Python 3.11 or higher
*   Standard Python modules: `re`, `time`, `csv`, `os`, and `tkinter`
*   *Note for Linux users:* If the GUI fails to launch, ensure Tkinter is installed via your package manager (e.g., `sudo apt-get install python3-tk`).
*   No external deep learning libraries or GPU acceleration are required, making the script lightweight and highly efficient.

## Methodology
The framework follows a sequential pipeline to process the input text:
1.  Text Normalization: Converting text to lowercase and filtering out non-alphabetic symbols.
2.  Deletion Order Algorithm: Affixes are checked and removed sequentially in a strict priority order: Confix → Prefix → Infix → Suffix.
3.  Lexicon Validation: After each morphological removal step, the system verifies the intermediate word against the 6,983 root words dictionary. The process stops immediately once a valid stem is identified, preventing overstemming and structural degradation. 

## Citations
If you use this dataset or code framework in your research, please cite the primary publication:
Wibowo, S. H., Handhayani, T. S., Wibowo, N. S. T., & Wibowo, C. S. T. (2026). Infix-aware rule-based stemming for the Rejang language. PeerJ Computer Science (Submitted).

## License & Contribution Guidelines
License: This project is licensed under the MIT License.
Contributions: Contributions to expand the morphological rules (especially concerning complex affixation/infixes) or lexicon coverage are welcome. Please open an issue or submit a pull request for any suggested enhancements on our GitHub repository.


