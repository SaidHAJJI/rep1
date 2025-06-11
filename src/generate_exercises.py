import random
import uuid

# Placeholder for concepts that could be used as distractors or for negation
DISTRACTOR_CONCEPTS = ["the cell wall", "vacuoles", "flagella", "RNA", "anaerobic respiration", "carbon monoxide"]

def _negate_statement(true_statement: str, concepts_tested: list = None) -> str:
    """
    Tries to minimally alter a true statement to make it false.
    This is very basic and needs more sophisticated NLP for robust negation.
    """
    words = true_statement.split()
    negated_statement = ""

    if "is" in words:
        idx = words.index("is")
        words.insert(idx + 1, "not")
        negated_statement = " ".join(words)
    elif "are" in words:
        idx = words.index("are")
        words.insert(idx + 1, "not")
        negated_statement = " ".join(words)
    elif "does" in words: # e.g. "The nucleus does contain DNA"
        idx = words.index("does")
        words.insert(idx + 1, "not") # "The nucleus does not contain DNA"
        negated_statement = " ".join(words)
    elif "do" in words:
        idx = words.index("do")
        words.insert(idx + 1, "not")
        negated_statement = " ".join(words)
    elif len(words) > 3: # Fallback: replace a key word
        replaceable_word_idx = -1
        if concepts_tested: # Try to replace a known concept
            for i, word in enumerate(words):
                # Avoid replacing very common words or articles if they sneak into concepts
                if word in concepts_tested and word.lower() not in ["the", "a", "an", "of"] and len(word) > 2:
                    replaceable_word_idx = i
                    break

        if replaceable_word_idx == -1: # Try to find a capitalized word (potential noun) not at start
            for i, word in enumerate(words):
                if word.istitle() and i > 0:
                    replaceable_word_idx = i
                    break

        if replaceable_word_idx == -1 and len(words) > 2 : # Last resort, replace a word (e.g. second word)
            replaceable_word_idx = 1 if words[0].lower() == "the" and len(words) > 1 else 0


        if replaceable_word_idx != -1:
            original_word = words[replaceable_word_idx]
            distractor = random.choice(DISTRACTOR_CONCEPTS)
            # Ensure distractor is not too similar to original or already in statement
            loop_count = 0
            while (distractor == original_word or distractor in true_statement) and loop_count < len(DISTRACTOR_CONCEPTS) * 2:
                distractor = random.choice(DISTRACTOR_CONCEPTS)
                loop_count +=1

            words[replaceable_word_idx] = distractor
            negated_statement = " ".join(words)
        else: # Default if no other negation worked
            negated_statement = f"It is not true that: {true_statement}"
    else: # Default for very short statements
        negated_statement = f"It is not true that: {true_statement}"

    return negated_statement


def create_true_false_exercise_from_statement(
    true_statement: str,
    present_as_true_question: bool,
    concepts_tested: list = None,
    source_ref: str = "unknown"
) -> dict:
    """
    Creates a true/false exercise from a true factual statement.

    Args:
        true_statement: The TRUE factual statement (string).
        present_as_true_question: If True, the question will be the true_statement and answer is "True".
                                 If False, the statement will be negated, and answer is "False".
        concepts_tested: List of concepts tested.
        source_ref: Source reference for the statement.

    Returns:
        A dictionary representing a true/false exercise.
    """
    if present_as_true_question:
        question_prompt = true_statement
        correct_answer = "True"
        rubric_note = f"The statement '{true_statement}' is presented as true."
    else:
        question_prompt = _negate_statement(true_statement, concepts_tested)
        correct_answer = "False"
        rubric_note = f"The original true statement was: '{true_statement}'. It was negated for this question."

    # Ensure the prompt ends with a punctuation mark if it doesn't have one.
    if not question_prompt.endswith(('.', '?', '!')):
        question_prompt += "."

    return {
        "exercise_id": f"ex_tf_{uuid.uuid4().hex[:6]}",
        "source_material_type": "statement_based",
        "source_reference": source_ref,
        "concepts_tested": concepts_tested if concepts_tested else [true_statement.split()[0]], # Fallback concept
        "exercise_type": "true_false",
        "difficulty_level": "easy", # Default, can be adjusted
        "question_prompt": question_prompt,
        "options": None,
        "correct_answer": correct_answer,
        "rubric_notes": rubric_note
    }


def create_multiple_choice_exercise(main_concept: str, correct_statement: str, list_of_distractors: list[str], source_ref: str = "unknown_source") -> dict:
    """
    Placeholder function to generate a multiple-choice exercise.

    Args:
        main_concept: The primary concept the question is about.
        correct_statement: The statement that forms the basis of the correct answer.
        list_of_distractors: A list of distractor statements or concepts.
        source_ref: Source reference for the exercise.

    Returns:
        A dictionary representing a multiple-choice exercise with placeholder options.
    """
    # How one might generate distractors:
    # 1. Semantic Similarity: Find concepts related to 'main_concept' but distinct (e.g., for 'mitochondria', distractors could be 'chloroplast', 'ribosome', 'nucleus').
    # 2. Negation/Alteration: Create plausible but incorrect variations of the 'correct_statement'.
    #    - E.g., If correct is "Mitochondria produce ATP", a distractor could be "Mitochondria store genetic material."
    # 3. Common Misconceptions: Use known common misunderstandings related to the 'main_concept'.
    # 4. Incorrect Definitions: Provide wrong definitions for the 'main_concept'.

    options = [
        {"option_text": correct_statement, "is_correct": True},
        {"option_text": f"Placeholder distractor A for {main_concept}: {list_of_distractors[0] if list_of_distractors else 'Distractor 1'}", "is_correct": False},
        {"option_text": f"Placeholder distractor B for {main_concept}: {list_of_distractors[1] if len(list_of_distractors) > 1 else 'Distractor 2'}", "is_correct": False},
        {"option_text": f"Placeholder distractor C for {main_concept}: {list_of_distractors[2] if len(list_of_distractors) > 2 else 'Distractor 3'}", "is_correct": False},
    ]
    random.shuffle(options) # Shuffle options so correct answer isn't always first

    return {
        "exercise_id": f"ex_mc_{uuid.uuid4().hex[:6]}",
        "source_material_type": "concept_based",
        "source_reference": source_ref,
        "concepts_tested": [main_concept],
        "exercise_type": "multiple_choice",
        "difficulty_level": "medium", # Default
        "question_prompt": f"Placeholder: Which of the following statements about '{main_concept}' is correct?",
        "options": options,
        "correct_answer": None, # Correctness is in the options
        "rubric_notes": "Student should identify the correct statement about the main concept."
    }


def create_short_answer_exercise(concept_to_explain: str, source_ref: str = "unknown_source", context: str = "") -> dict:
    """
    Placeholder function to generate a short_answer exercise.

    Args:
        concept_to_explain: The concept that needs explanation.
        source_ref: Source reference for the exercise.
        context: Optional context for the explanation.

    Returns:
        A dictionary representing a short_answer exercise with a placeholder question.
    """
    # How a short answer question could be framed:
    # 1. Direct Explanation: "Explain the role of [concept_to_explain] in [context]."
    # 2. Comparison: "Compare and contrast [concept_to_explain] with [another_concept]."
    # 3. Significance: "Why is [concept_to_explain] important for [larger_process/system]?"
    # 4. Process Description: "Describe the process of [concept_to_explain]."

    question_context_addon = f" in the context of {context}" if context else ""

    return {
        "exercise_id": f"ex_sa_{uuid.uuid4().hex[:6]}",
        "source_material_type": "concept_based",
        "source_reference": source_ref,
        "concepts_tested": [concept_to_explain],
        "exercise_type": "short_answer",
        "difficulty_level": "medium", # Default
        "question_prompt": f"Placeholder: Explain the concept of '{concept_to_explain}'{question_context_addon}.",
        "options": None,
        "correct_answer": f"Placeholder: A comprehensive explanation of '{concept_to_explain}' focusing on its key aspects and role{question_context_addon}.",
        "rubric_notes": "Answer should clearly define the concept, list its main characteristics/functions, and provide relevant examples if applicable."
    }


if __name__ == "__main__":
    print("--- Testing create_true_false_exercise_from_statement ---")
    true_statement_1 = "Mitochondria are responsible for energy production."
    concepts_1 = ["Mitochondria", "energy production"]
    # Test Case 1: Presenting a true statement as a "True" question
    tf_exercise_true_q = create_true_false_exercise_from_statement(true_statement_1, True, concepts_1, "chapter1_cells.txt")
    print(f"  Example (True statement presented as True question):")
    print(f"    ID: {tf_exercise_true_q['exercise_id']}")
    print(f"    Question: {tf_exercise_true_q['question_prompt']}")
    print(f"    Correct Answer: {tf_exercise_true_q['correct_answer']}")
    print(f"    Rubric: {tf_exercise_true_q['rubric_notes']}\n")

    # Test Case 2: Presenting a true statement as a "False" question (negated)
    true_statement_2 = "Chloroplasts are found in plant cells."
    concepts_2 = ["Chloroplasts", "plant cells"]
    tf_exercise_false_q = create_true_false_exercise_from_statement(true_statement_2, False, concepts_2, "chapter2_photosynthesis.txt")
    print(f"  Example (True statement presented as False question - negated):")
    print(f"    ID: {tf_exercise_false_q['exercise_id']}")
    print(f"    Question: {tf_exercise_false_q['question_prompt']}")
    print(f"    Correct Answer: {tf_exercise_false_q['correct_answer']}")
    print(f"    Rubric: {tf_exercise_false_q['rubric_notes']}\n")

    # Test Case 3: Another example of negation, different sentence structure
    true_statement_3 = "Photosynthesis uses carbon dioxide and water."
    concepts_3 = ["Photosynthesis", "carbon dioxide", "water"]
    tf_exercise_false_q_2 = create_true_false_exercise_from_statement(true_statement_3, False, concepts_3, "chapter2_photosynthesis.txt")
    print(f"  Example (True statement with 'uses' presented as False question - negated):")
    print(f"    ID: {tf_exercise_false_q_2['exercise_id']}")
    print(f"    Question: {tf_exercise_false_q_2['question_prompt']}") # Expect negation, e.g. word replacement or "It is not true..."
    print(f"    Correct Answer: {tf_exercise_false_q_2['correct_answer']}")
    print(f"    Rubric: {tf_exercise_false_q_2['rubric_notes']}\n")

    print("\n--- Testing create_multiple_choice_exercise (Placeholder) ---")
    mc_concept = "Cell Nucleus"
    mc_correct_statement = "The cell nucleus contains the cell's genetic material (DNA)."
    mc_distractors = ["The nucleus is the primary site of protein synthesis.", "The nucleus is responsible for energy production.", "The nucleus is only found in prokaryotic cells."]
    mc_exercise = create_multiple_choice_exercise(mc_concept, mc_correct_statement, mc_distractors, "chapter1_cells.txt")
    print(f"  ID: {mc_exercise['exercise_id']}")
    print(f"  Question: {mc_exercise['question_prompt']}")
    # print(f"  Options: {mc_exercise['options']}") # Output can be long
    print(f"  One option example: {mc_exercise['options'][0]['option_text']} (Correct: {mc_exercise['options'][0]['is_correct']})")
    print(f"  Rubric: {mc_exercise['rubric_notes']}\n")


    print("\n--- Testing create_short_answer_exercise (Placeholder) ---")
    sa_concept = "Photosynthesis"
    sa_context = "plant biology"
    sa_exercise = create_short_answer_exercise(sa_concept, "chapter2_photosynthesis.txt", sa_context)
    print(f"  ID: {sa_exercise['exercise_id']}")
    print(f"  Question: {sa_exercise['question_prompt']}")
    print(f"  Correct Answer Hint: {sa_exercise['correct_answer']}")
    print(f"  Rubric: {sa_exercise['rubric_notes']}\n")

    print("Conceptual integration notes:")
    print("To integrate with process_textbook.py:")
    print("- Sentences from segmented_content could be used as input for create_true_false_exercise_from_statement.")
    print("- Keywords from extract_keywords could be used as 'main_concept' for MCQs or 'concept_to_explain' for short answers.")
    print("- Q&A pairs from generate_qa.py could also feed into exercise generation, e.g., a factual answer could become a true statement.")
