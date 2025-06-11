# Web Application Design Notes - Cognitive AI Tutor

This document outlines design considerations for the Cognitive AI Tutor web application.

## User Interface (UI) and User Experience (UX) Overview

(This section can be expanded later with more detailed wireframes or mockups if needed.)

The application will feature two main interactive components:
1.  **AI Chat Interface**: Allows users to engage in a dialogue with the AI, ask questions, and explore life science topics.
2.  **Exercise System**: Presents users with various types of exercises (MCQ, True/False, Short Answer) to test their understanding and reasoning skills.

## User Progression and Feedback System (Conceptual)

This section details the conceptual framework for tracking user progress and providing feedback within the AI Tutor application. The goal is to create an adaptive and supportive learning environment.

### 1. User Progression Tracking

User progression will be tracked based on several factors. (Note: Actual implementation might start simple and become more complex).

*   **Concepts Covered**:
    *   The system could maintain a list of core life science concepts (e.g., derived from textbook structure or a predefined ontology).
    *   When a user interacts with the AI about a specific concept or successfully completes an exercise related to it, the concept can be marked as "interacted" or "mastered" at a basic level.
    *   *Storage Idea*: User-specific data, potentially in browser local storage for simple scenarios, or a backend database for persistent accounts.

*   **Exercises Completed**:
    *   Track which exercises the user has attempted and successfully completed.
    *   Store performance on exercises (e.g., first-try success, number of attempts).
    *   *Storage Idea*: Similar to concept tracking.

*   **Performance Scores (Optional - more advanced)**:
    *   Maintain scores for different concepts or skill types (e.g., factual recall, deductive reasoning, inductive reasoning).
    *   Scores could be updated based on exercise performance and potentially the AI's assessment of chat interactions.

*   **Learning Path (Adaptive - more advanced)**:
    *   Based on tracked progress, the system could suggest next concepts to explore or exercises to attempt.
    *   Difficulty of exercises could adapt to the user's performance.

### 2. Feedback Mechanisms

The system will provide feedback in various forms:

*   **Exercise Feedback**:
    *   **Immediate Correctness**: For MCQ and T/F questions, indicate if the answer was correct or incorrect.
    *   **Explanations**: Provide brief explanations for why an answer is correct or incorrect, especially for incorrect answers. This could link back to relevant concepts in the (future) digital textbook content or AI chat.
    *   **Short Answer Evaluation**:
        *   Initial feedback might be based on keyword matching or simple semantic similarity to a model answer.
        *   More advanced: The fine-tuned AI model itself could be used to evaluate the quality/correctness of short answers, providing more nuanced feedback.
    *   Reference: The backend `/submit_answer` endpoint currently provides basic feedback.

*   **Chat Interaction Feedback (AI-driven)**:
    *   The AI should be designed to:
        *   **Acknowledge understanding**: Confirm what the user is asking or stating.
        *   **Provide encouragement**: Use positive reinforcement.
        *   **Offer hints or scaffolding**: If the user is struggling with a concept during chat, the AI could offer simpler explanations or break down complex ideas.
        *   **Suggest related topics**: Based on the conversation, suggest further areas of exploration.
        *   **Identify misconceptions**: (Advanced goal) Attempt to gently correct misunderstandings expressed by the user.

*   **Progress Summary (Dashboard - Future Feature)**:
    *   A dedicated section where users can view their progress:
        *   Concepts they've engaged with.
        *   Exercises completed and their scores.
        *   Badges or milestones achieved (gamification element).

### 3. Data for Progression and Feedback

*   **Exercise Data**: The `difficulty_level` and `concepts_tested` fields in `evaluation_exercises.json` will be crucial.
*   **Q&A Corpus**: The `concepts`, `difficulty_level`, and `question_type` in `qa_corpus.json` can inform AI interactions and potentially link exercises to chat topics.
*   **Textbook Content**: (Future) Structured textbook content will be essential for the AI to refer to and for linking explanations.

### 4. Iterative Development

*   The progression and feedback system will be developed iteratively.
*   Initial versions will focus on basic exercise feedback and simple tracking.
*   More advanced features like adaptive learning paths and sophisticated AI-driven feedback in chat will be built incrementally.

This conceptual outline provides a starting point for designing a supportive and effective learning experience.
