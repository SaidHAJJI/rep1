import os
import re
import string
from collections import Counter

# List of common English stop words
STOP_WORDS = [
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "should",
    "can", "could", "may", "might", "must", "am", "mr", "mrs", "ms", "dr",
    "and", "but", "or", "nor", "for", "so", "yet", "if", "else", "then",
    "when", "where", "why", "how", "what", "which", "who", "whom", "whose",
    "in", "on", "at", "by", "from", "to", "into", "onto", "with", "without",
    "about", "above", "below", "over", "under", "again", "further", "then",
    "once", "here", "there", "all", "any", "both", "each", "few", "more",
    "most", "other", "some", "such", "no", "not", "only", "own", "same",
    "so", "than", "too", "very", "s", "t", "just", "don", "should've",
    "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren", "couldn",
    "didn", "doesn", "hadn", "hasn", "haven", "isn", "ma", "mightn", "mustn",
    "needn", "shan", "shouldn", "wasn", "weren", "won", "wouldn", "of", "it",
    "this", "that", "its", "also", "etc"
]


def load_text_files(directory_path: str) -> dict[str, str]:
    """
    Reads all .txt files from the specified directory.

    Args:
        directory_path: The path to the directory containing .txt files.

    Returns:
        A dictionary where keys are filenames and values are the content of the files.
        Returns an empty dictionary if the directory is not found or no .txt files are present.
    """
    texts = {}
    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at {directory_path}")
        return texts

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(directory_path, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    texts[filename] = f.read()
            except Exception as e:
                print(f"Error reading file {filepath}: {e}")
    return texts

def segment_text(text_content: str) -> list[list[str]]:
    """
    Segments text content into paragraphs, and each paragraph into sentences.

    Args:
        text_content: The string content to segment.

    Returns:
        A list of paragraphs, where each paragraph is a list of sentences.
    """
    if not text_content:
        return []

    # Split into paragraphs. Preferring double newlines, then single if no double newlines found.
    # Using strip to remove empty paragraphs that might result from multiple newlines.
    if '\n\n' in text_content:
        paragraphs_raw = [p.strip() for p in text_content.split('\n\n') if p.strip()]
    else:
        paragraphs_raw = [p.strip() for p in text_content.split('\n') if p.strip()]

    segmented_paragraphs = []
    for para_text in paragraphs_raw:
        if not para_text:
            continue
        # Split sentences by '.', '?', '!'
        # This regex looks for a period, question mark, or exclamation mark,
        # possibly followed by quotes, and then by whitespace or end of string.
        # It's important to capture the delimiters as well if we want to keep them,
        # but for keyword extraction, they are usually removed.
        # Let's use a simpler split that removes them.
        sentences = re.split(r'[.?!]', para_text)
        # Filter out empty strings that may result from splitting and strip whitespace
        sentences = [s.strip() for s in sentences if s and s.strip()]
        if sentences:
            segmented_paragraphs.append(sentences)

    return segmented_paragraphs

def extract_keywords(list_of_paragraphs: list[list[str]], stop_words: list[str], top_n: int = 10) -> list[tuple[str, int]]:
    """
    Extracts top N keywords from a list of paragraphs (each paragraph being a list of sentences).

    Args:
        list_of_paragraphs: A list of paragraphs, where each paragraph is a list of sentences.
        stop_words: A list of stop words to ignore.
        top_n: The number of top keywords to return.

    Returns:
        A list of tuples, where each tuple contains a keyword and its frequency.
    """
    all_text = ""
    for paragraph in list_of_paragraphs:
        for sentence in paragraph:
            all_text += sentence + " " # Add space to separate sentences

    if not all_text.strip():
        return []

    # Convert to lowercase
    text_lower = all_text.lower()

    # Remove punctuation
    # Keep hyphenated words and alphanumeric like CO2
    # First, replace punctuation that should be space with space
    text_no_punct = re.sub(r'[,;:"\'(){}\[\]]', ' ', text_lower)
    # Then remove periods, question marks, exclamation marks that might be part of words or at end
    text_no_punct = re.sub(r'[.?!](?=\s|$)', '', text_no_punct)

    # Split into words (tokens)
    words = text_no_punct.split()

    # Filter out stop words and short words
    filtered_words = []
    for word in words:
        # Remove any remaining leading/trailing punctuation for the word itself
        cleaned_word = word.strip(string.punctuation)
        if cleaned_word not in stop_words:
            # Allow short words if they are alphanumeric (like 'co2') or all digits
            is_alphanum_short_word = any(char.isdigit() for char in cleaned_word) and any(char.isalpha() for char in cleaned_word)
            is_number = cleaned_word.isdigit()

            if len(cleaned_word) >= 3 or is_alphanum_short_word or is_number:
                filtered_words.append(cleaned_word)

    # Calculate frequency
    if not filtered_words:
        return []
    word_counts = Counter(filtered_words)

    return word_counts.most_common(top_n)

if __name__ == "__main__":
    textbooks_dir = "data/textbooks/"

    print(f"Loading text files from: {textbooks_dir}")
    textbook_data = load_text_files(textbooks_dir)

    if not textbook_data:
        print("No textbook data loaded. Exiting.")
    else:
        print(f"\nSuccessfully loaded {len(textbook_data)} file(s).\n")

        for filename, content in textbook_data.items():
            print(f"--- Processing: {filename} ---")

            if not content.strip():
                print("File is empty or contains only whitespace.")
                print("-" * 30)
                continue

            segmented_content = segment_text(content) # This is list_of_paragraphs

            num_paragraphs = len(segmented_content)
            num_sentences_total = sum(len(p) for p in segmented_content)
            print(f"Number of paragraphs: {num_paragraphs}, Total sentences: {num_sentences_total}")

            if segmented_content:
                # For brevity, just show first sentence of first paragraph
                # print("\nExample - First paragraph, first sentence:")
                # print(f"  '{segmented_content[0][0]}'")

                keywords = extract_keywords(segmented_content, STOP_WORDS, top_n=10)
                print("\nTop keywords:")
                if keywords:
                    for keyword, count in keywords:
                        print(f"  - {keyword}: {count}")
                else:
                    print("  No keywords extracted.")
            else:
                print("No content to extract keywords from.")
            print("-" * 30 + "\n")
