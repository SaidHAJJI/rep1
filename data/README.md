# Dataset for 8th-Grade Life Science AI Simulation

## 1. Dataset Overview

This dataset is being developed to train and evaluate an Artificial Intelligence (AI) system designed to simulate the learning processes and cognitive abilities of an 8th-grade American life science student. The primary goal is to create an AI that can engage in reasoning (deductive and inductive) and demonstrate progressive learning based on the provided educational materials.

The dataset will encompass textbook content, question-answer pairs for dialogue simulation, and evaluation exercises to assess the AI's understanding and reasoning capabilities.

## 2. Directory Structure

The `data/` directory is organized as follows to manage the different components of the dataset:

*   **`data/textbooks/`**:
    *   **Purpose**: This directory holds the raw and processed content from life science textbooks or Open Educational Resources (OER) suitable for the 8th-grade level. Initially, it contains sample `.txt` files.
    *   **Format**: Primarily plain text (`.txt`) files. These files can be raw chapter dumps or pre-processed versions (e.g., segmented into paragraphs and sentences by scripts like `src/process_textbook.py`). Each file typically represents a chapter or a distinct section of a textbook.

*   **`data/qa_corpus/`**:
    *   **Purpose**: This directory contains a corpus of question-and-answer (Q&A) pairs. These are intended for training dialogue capabilities and for assessing the AI's ability to answer questions based on the textbook content.
    *   **Format**: JSON (`.json` files, e.g., `sample_qa_pairs.json`). Each Q&A pair in the JSON array includes fields such as:
        *   `id`: A unique identifier for the Q&A pair (e.g., "qa_001").
        *   `source_chapter`: The filename of the textbook chapter it relates to (e.g., "chapter1_cells.txt").
        *   `concepts`: A list of keywords or concepts from the chapter that this Q&A pair covers.
        *   `question_type`: Type of question (e.g., "deductive", "inductive", "factual_recall").
        *   `difficulty_level`: A numerical or descriptive level (e.g., 1-5, or "easy", "medium", "hard").
        *   `question_text`: The text of the question.
        *   `answer_text`: The text of the answer.
        *   `context_snippet` (optional): A short snippet from the textbook that provides context.

*   **`data/evaluation_exercises/`**:
    *   **Purpose**: This directory stores materials designed to evaluate the AI's understanding of concepts and its reasoning skills. These exercises are more formal assessment tools compared to the Q&A corpus.
    *   **Format**: JSON (`.json` files, e.g., `sample_evaluation_exercises.json`). Each exercise object includes fields such as:
        *   `exercise_id`: A unique identifier for the exercise (e.g., "ex_mc_001").
        *   `source_material_type`: Indicates if it's based on "textbook_chapter", "qa_concept", etc.
        *   `source_reference`: Specific reference (e.g., "chapter1_cells.txt", "qa_001_concept_cell_theory").
        *   `concepts_tested`: A list of keywords or concepts the exercise evaluates.
        *   `exercise_type`: Type of exercise (e.g., "multiple_choice", "true_false", "short_answer", "matching").
        *   `difficulty_level`: (e.g., 1-5, or "easy", "medium", "hard").
        *   `question_prompt`: The main prompt or question for the exercise.
        *   `options` (for multiple_choice/matching): A list of options, where each option for multiple choice might be `{"option_text": "...", "is_correct": true/false}`.
        *   `correct_answer` (for true_false, short_answer): The specific correct answer.
        *   `rubric_notes` (optional): Notes on how to score the exercise.

## 3. Data Generation and Processing Scripts

The following Python scripts, located in the `src/` directory, are involved in the generation and processing of this dataset:

*   **`src/process_textbook.py`**:
    *   Responsible for reading raw textbook files (e.g., from `data/textbooks/`).
    *   Segments the text into paragraphs and sentences.
    *   Extracts keywords from the content to identify key concepts.

*   **`src/generate_qa.py`**:
    *   Aims to generate question-answer pairs based on the processed textbook content from `process_textbook.py`.
    *   Includes functions to create factual questions and placeholders for generating more complex deductive and inductive questions.

*   **`src/generate_exercises.py`**:
    *   Designed to create evaluation exercises (like true/false, multiple-choice, short answer) using textbook content, extracted concepts, or existing Q&A pairs.
    *   Contains functions to structure these exercises according to the defined JSON format.

## 4. Content Details & Examples

*   **`qa_corpus`**:
    *   For detailed structure and examples, please refer to the `data/qa_corpus/sample_qa_pairs.json` file.
    *   The corpus aims to include a variety of question types, focusing on:
        *   **Factual Recall**: Testing direct knowledge from the text.
        *   **Deductive Reasoning**: Requiring the AI to apply general principles to specific cases.
        *   **Inductive Reasoning**: Requiring the AI to infer general principles from specific observations.

*   **`evaluation_exercises`**:
    *   For detailed structure and examples, please refer to the `data/evaluation_exercises/sample_evaluation_exercises.json` file.
    *   A range of exercise types are planned to assess different facets of understanding:
        *   Multiple-Choice Questions (MCQ)
        *   True/False (T/F) statements
        *   Short Answer questions requiring explanations or definitions.
        *   (Potentially) Matching exercises.

## 5. Planned Validation Strategy

To ensure the quality, relevance, and effectiveness of this dataset, an ideal validation process would involve the following (note: this describes a plan, not current execution):

*   **Expert Review**:
    *   The entire dataset (textbook excerpts, Q&A pairs, evaluation exercises) would be reviewed by middle school science educators and subject matter experts in life sciences.

*   **Criteria for Review**:
    *   **Accuracy**: Scientific correctness of all content, answers, and explanations.
    *   **Age-Appropriateness**: Language complexity, examples, and cognitive demands suitable for an 8th-grade student.
    *   **Clarity**: Unambiguous wording in questions, answers, prompts, and options.
    *   **Reasoning Assessment**: Effectiveness of Q&A and exercises in genuinely promoting and assessing deductive and inductive reasoning skills, not just rote memorization.
    *   **Curriculum Alignment**: Consistency with typical US middle school life science curricula and learning objectives.
    *   **Concept Coverage**: Adequate representation of core life science concepts expected at the 8th-grade level.
    *   **Variety and Balance**: A good mix of question/exercise types, difficulty levels, and concepts covered.

*   **Iterative Refinement**:
    *   The dataset would be iteratively updated and improved based on the feedback received from the expert review process. This includes correcting errors, rephrasing questions, adjusting difficulty, and ensuring better alignment with educational goals.

## 6. Current Status & Limitations

*   **Sample Data**: The current content within `data/textbooks/`, `data/qa_corpus/`, and `data/evaluation_exercises/` consists of **sample/dummy data**. This data has been created primarily to establish the directory structure, define data formats (JSON schemas), and to provide illustrative examples for the initial development of data processing and generation scripts.
*   **Future Tasks**:
    *   **Actual Data Collection**: Populating the `data/textbooks/` directory with comprehensive content from real 8th-grade life science textbooks or OER is a significant next step.
    *   **Large-Scale Generation**: The Q&A corpus and evaluation exercises will need to be generated at a much larger scale using the developed scripts, once substantial textbook content is available.
    *   **Validation Implementation**: The planned validation strategy needs to be implemented once a more substantial dataset is compiled.

This README will be updated as the dataset evolves.
