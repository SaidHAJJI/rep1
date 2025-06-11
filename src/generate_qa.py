import random

# Potentially import from src.process_textbook if needed in future development
# from src.process_textbook import load_text_files, segment_text, extract_keywords

def generate_factual_question(sentence: str, keyword: str) -> dict:
    """
    Generates a simple factual question about a keyword based on a sentence.

    Args:
        sentence: The input sentence (string).
        keyword: The keyword (string) present in the sentence.

    Returns:
        A dictionary {"question_text": "...", "answer_text": "..."}.
        Returns an empty dict if keyword not in sentence or generation fails.
    """
    if keyword.lower() not in sentence.lower():
        return {}

    # Simple templates - can be expanded significantly
    question_templates = [
        f"What is {keyword}?",
        f"What is the role of {keyword}?",
        f"What is known about {keyword} based on the text?",
        f"Can you describe {keyword}?",
        f"What does the text say about {keyword}?"
    ]

    # More specific templates if the keyword is at the beginning of the sentence
    if sentence.lower().startswith(keyword.lower()):
        question_templates.extend([
            f"What is stated about {keyword} in the sentence: '{sentence}'?",
            f"What are {keyword} responsible for, according to the text?", # Assumes plural keyword or use 'is'
            f"What does {keyword} do?"
        ])

    # Attempt to make slightly more targeted questions if possible (very basic)
    # This part is highly heuristic and would need proper NLP for robustness
    parts = sentence.split(keyword, 1)
    if len(parts) > 1 and parts[1].strip().startswith(("is ", "are ", "was ", "were ")):
        # e.g. "Mitochondria ARE responsible for..." -> "What ARE Mitochondria responsible for?"
        # e.g. "The nucleus IS the control center..." -> "What IS the nucleus?" (covered by generic)
        verb_phrase = parts[1].strip().split(" ", 2) # "are", "responsible", "for..."
        if len(verb_phrase) > 1 : # We have at least a verb and something after
            question_templates.append(f"What {verb_phrase[0]} {keyword} {verb_phrase[1] if len(verb_phrase) > 1 else ''}?")


    # Fallback if the keyword is not the subject or if more complex logic is needed
    # For "The nucleus contains the genetic material...", keyword "nucleus"
    # "What does the nucleus contain?" is a good question.
    # This requires more semantic understanding.
    # For now, we'll rely on the generic templates or simple structural ones.

    question = random.choice(question_templates)

    # A very simple approach for answer: use the original sentence.
    # More advanced: use the part of the sentence most relevant to the keyword.
    answer = sentence.strip()
    if not answer.endswith('.'): # Ensure answer ends with a period if it's a statement.
        answer += '.'

    return {"question_text": question, "answer_text": answer}


def generate_deductive_question(concept: str, principles_list: list[str]) -> dict:
    """
    Placeholder function to generate a deductive question.
    Deductive reasoning: Starts with a general principle, deduces specifics.
    Example: All birds have feathers (principle). A robin is a bird (observation).
             Therefore, a robin has feathers (deduction).
    """
    if not principles_list:
        principles_list = ["all X have property Y"]

    principle = random.choice(principles_list)

    # Template examples:
    # 1. "Given the principle that [principle], what can be logically concluded about [concept] if [concept] is an instance of X?"
    # 2. "If [principle] holds true, and [concept] is a specific case related to it, what must also be true about [concept]?"
    # 3. "Based on the general rule '[principle]', what specific characteristic can you deduce for [concept]?"

    question_text = f"Placeholder: Given the principle that '{principle}', what can be logically concluded about '{concept}'?"
    answer_text = f"Placeholder: Based on '{principle}', one can deduce that '{concept}' exhibits a characteristic consistent with this principle."

    return {"question_text": question_text, "answer_text": answer_text}


def generate_inductive_question(observations_list: list[str], potential_hypothesis: str) -> dict:
    """
    Placeholder function to generate an inductive question.
    Inductive reasoning: Starts with specific observations, infers a general principle/hypothesis.
    Example: Observation 1: Swan A is white. Observation 2: Swan B is white.
             Hypothesis: All swans are white. (This can be falsified by black swans)
    """
    if not observations_list:
        observations_list = ["specific observation A about X", "specific observation B about X"]

    observations_str = " and ".join(observations_list)

    # Template examples:
    # 1. "If one observes that [observation1] and [observation2], what general hypothesis about [related_topic/potential_hypothesis] could be proposed?"
    # 2. "Based on the following findings: [observations_str], what pattern or general rule might you infer regarding [potential_hypothesis]?"
    # 3. "What potential conclusion could be drawn about [potential_hypothesis] from these specific instances: [observations_str]?"

    question_text = f"Placeholder: If you observe that '{observations_str}', what might you conclude or hypothesize about '{potential_hypothesis}'?"
    answer_text = f"Placeholder: From '{observations_str}', one might hypothesize that '{potential_hypothesis}' is generally true, subject to further testing."

    return {"question_text": question_text, "answer_text": answer_text}


if __name__ == "__main__":
    print("--- Testing generate_factual_question ---")
    sentence1 = "Mitochondria are responsible for energy production in eukaryotic cells."
    keyword1 = "Mitochondria"
    qa1 = generate_factual_question(sentence1, keyword1)
    if qa1:
        print(f"  Sentence: \"{sentence1}\"")
        print(f"  Keyword: \"{keyword1}\"")
        print(f"  Question: {qa1['question_text']}")
        print(f"  Answer: {qa1['answer_text']}\n")

    sentence2 = "The nucleus contains the genetic material in the form of DNA."
    keyword2 = "nucleus"
    qa2 = generate_factual_question(sentence2, keyword2)
    if qa2:
        print(f"  Sentence: \"{sentence2}\"")
        print(f"  Keyword: \"{keyword2}\"")
        print(f"  Question: {qa2['question_text']}")
        print(f"  Answer: {qa2['answer_text']}\n")

    sentence3 = "Photosynthesis is the process by which green plants use sunlight."
    keyword3 = "Photosynthesis"
    qa3 = generate_factual_question(sentence3, keyword3)
    if qa3:
        print(f"  Sentence: \"{sentence3}\"")
        print(f"  Keyword: \"{keyword3}\"")
        print(f"  Question: {qa3['question_text']}")
        print(f"  Answer: {qa3['answer_text']}\n")

    print("\n--- Testing generate_deductive_question (Placeholder) ---")
    concept_deductive = "a newly discovered organism"
    principles_deductive = ["all living organisms are composed of cells (Cell Theory)"]
    qa_deductive = generate_deductive_question(concept_deductive, principles_deductive)
    print(f"  Question: {qa_deductive['question_text']}")
    print(f"  Answer: {qa_deductive['answer_text']}\n")

    print("\n--- Testing generate_inductive_question (Placeholder) ---")
    observations_inductive = ["microscopic entity A has a nucleus", "microscopic entity B has a nucleus and mitochondria"]
    hypothesis_inductive = "these entities are eukaryotic cells"
    qa_inductive = generate_inductive_question(observations_inductive, hypothesis_inductive)
    print(f"  Question: {qa_inductive['question_text']}")
    print(f"  Answer: {qa_inductive['answer_text']}\n")

    # Example of how one might integrate with process_textbook.py output (conceptual)
    print("\n--- Conceptual integration with process_textbook.py output ---")
    # mock_processed_data = {
    #     "chapter1_cells.txt": {
    #         "paragraphs": [
    #             ["The cell is the basic unit of life.", "All living organisms are composed of cells."],
    #             ["Cells have various organelles like the nucleus.", "The nucleus contains genetic material."]
    #         ],
    #         "keywords": [("cells", 5), ("nucleus", 4)]
    #     }
    # }
    # for chapter_name, data in mock_processed_data.items():
    #     print(f"Processing chapter: {chapter_name}")
    #     all_sentences_from_chapter = [sentence for para in data["paragraphs"] for sentence in para]
    #     chapter_keywords = [kw[0] for kw in data["keywords"]]
    #
    #     for sentence in all_sentences_from_chapter:
    #         for keyword in chapter_keywords:
    #             if keyword.lower() in sentence.lower():
    #                 # Ensure keyword is substantial enough for a question
    #                 if len(keyword) > 3:
    #                     factual_qa = generate_factual_question(sentence, keyword)
    #                     if factual_qa:
    #                         print(f"  Generated Q (factual): {factual_qa['question_text']}")
    #                         # Further processing: save to JSON, etc.
    #                         break # Process one keyword per sentence for this example
    print("Conceptual integration comments are in the script for future reference.")
