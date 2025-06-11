# rep1
rep. num. 1

## Project: Cognitive Adolescent IA - Life Sciences

This project aims to develop an AI simulating the cognitive abilities of a 14-year-old (8th grade) American student specializing in life sciences.

### Phase 1: Data Preparation (Completed Initial Setup)

*   **Objective**: To create, structure, and document the dataset required for training and evaluating the AI.
*   **Key Artifacts**:
    *   `data/textbooks/`: Placeholder for processed textbook content. (See `data/textbooks/chapter*.txt` for samples).
    *   `data/qa_corpus/`: JSON-formatted question-answer pairs for training. (See `data/qa_corpus/sample_qa_pairs.json`).
    *   `data/evaluation_exercises/`: JSON-formatted exercises for evaluation. (See `data/evaluation_exercises/sample_evaluation_exercises.json`).
    *   `src/process_textbook.py`: Script for text processing.
    *   `src/generate_qa.py`: Script for generating Q&A pairs.
    *   `src/generate_exercises.py`: Script for generating exercises.
    *   `data/README.md`: Detailed documentation for the dataset.

### Phase 2: Model Fine-tuning (Initial Setup Completed)

*   **Objective**: To establish the foundational scripts, configurations, and documentation for fine-tuning the Llama 2 7B model.
*   **Key Artifacts**:
    *   `notebooks/fine_tuning/Llama2_Finetuning_Setup.ipynb`: A conceptual guide for setting up the Colab Pro+ environment, including model and tokenizer loading.
    *   `configs/model_configs/llama2_7b_config.json`: Placeholder configuration for the Llama 2 7B model parameters.
    *   `scripts/fine_tuning/train.py`: An outline of the Python script for the fine-tuning process, including argument parsing, data loading placeholders, PEFT/LoRA setup, and `SFTTrainer` integration.
    *   `docs/fine_tuning/README.md`: Comprehensive documentation detailing the hyperparameter optimization strategy, model evaluation metrics, and the overall validation process for fine-tuning.

### (Upcoming) Phase 3: Web Application Development

*   Details to be added.

### (Upcoming) Phase 4: Evaluation and Validation

*   Details to be added.
