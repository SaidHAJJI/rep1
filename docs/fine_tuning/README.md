# Fine-tuning Llama 2 7B for Life Sciences: Hyperparameter Optimization and Validation Strategy

This document outlines the strategy for fine-tuning the Llama 2 7B model on our custom life sciences dataset, focusing on hyperparameter optimization and model validation.

## 1. Key Hyperparameters for Fine-tuning

The following hyperparameters are critical for the fine-tuning process using PEFT/LoRA and SFTTrainer. Initial values will be based on common practices and adapted based on experimentation.

### Training Arguments (`transformers.TrainingArguments`):
-   **`output_dir`**: Directory to save model checkpoints and logs.
-   **`num_train_epochs`**: Number of training epochs (e.g., 1-5).
-   **`per_device_train_batch_size`**: Batch size per GPU (e.g., 1, 2, 4).
-   **`gradient_accumulation_steps`**: Number of steps to accumulate gradients before an optimizer update (e.g., 1, 2, 4, 8). Effective batch size = `per_device_train_batch_size` * `num_gpus` * `gradient_accumulation_steps`.
-   **`learning_rate`**: Initial learning rate (e.g., 2e-5, 5e-5, 2e-4 for AdamW).
-   **`lr_scheduler_type`**: Learning rate scheduler (e.g., "cosine", "linear").
-   **`warmup_steps`**: Number of warmup steps for the learning rate scheduler (e.g., 0, 100, 500).
-   **`weight_decay`**: Weight decay for regularization (e.g., 0.0, 0.01).
-   **`optim`**: Optimizer to use (e.g., "adamw_torch", "paged_adamw_8bit" for 4-bit models).
-   **`fp16` / `bf16`**: Whether to use mixed-precision training (True/False). `bf16` is preferred on A100s.
-   **`logging_steps`**: Log metrics every X steps.
-   **`save_steps`**: Save a checkpoint every X steps.
-   **`evaluation_strategy`**: "steps" or "epoch" if an eval dataset is used during training.

### LoRA Configuration (`peft.LoraConfig`):
-   **`r`**: Rank of the LoRA matrices (e.g., 8, 16, 32, 64). Higher `r` means more trainable parameters.
-   **`lora_alpha`**: LoRA scaling factor (e.g., 16, 32, 64). Often set to `r` or `2*r`.
-   **`lora_dropout`**: Dropout probability for LoRA layers (e.g., 0.05, 0.1).
-   **`target_modules`**: Modules to apply LoRA to (e.g., `['q_proj', 'v_proj']` or more comprehensive lists for Llama 2).
-   **`bias`**: Bias type for LoRA layers (e.g., "none", "all", "lora_only").

### SFTTrainer Specifics:
-   **`max_seq_length`**: Maximum sequence length for packing (e.g., 512, 1024, 2048).
-   **`packing`**: Whether to pack multiple short examples into one sequence (True/False). Improves training efficiency.
-   **`dataset_text_field`**: Name of the field in the dataset that SFTTrainer should use as the source of text data.

## 2. Hyperparameter Optimization Strategy

A systematic approach will be taken for hyperparameter optimization:

1.  **Establish a Baseline**: Start with commonly recommended hyperparameters for Llama 2 and LoRA fine-tuning.
2.  **Iterative Tuning**:
    *   Tune one or a small set of hyperparameters at a time.
    *   Prioritize tuning `learning_rate`, `batch_size` (effective), LoRA `r` and `lora_alpha`.
    *   Monitor training loss closely.
3.  **Automated Sweeps (Optional/Future)**:
    *   Consider using tools like Weights & Biases Sweeps or Optuna for more systematic exploration of the hyperparameter space if time and resources permit.
4.  **Resource Constraints**: Optimization will be mindful of Colab Pro+ resource limits (GPU memory, training time). This might favor smaller batch sizes with gradient accumulation and potentially smaller LoRA ranks (`r`).

## 3. Model Evaluation Metrics

The performance of the fine-tuned model will be assessed using a combination of metrics:

1.  **Training Metrics**:
    *   **Loss (Cross-Entropy)**: Primary indicator during training, monitored on both training and (if used) a validation split. A decreasing validation loss that's close to training loss is ideal.
    *   **Perplexity**: Measure of how well the model predicts the dataset. Lower is better.
2.  **Performance on Custom Evaluation Exercises**:
    *   The exercises developed in `data/evaluation_exercises/` will be used to assess:
        *   **Accuracy**: For multiple-choice, true/false questions.
        *   **Conceptual Understanding**: For short answer questions (qualitative review, potentially aided by LLM-as-judge or semantic similarity to reference answers).
        *   **Reasoning Skills**: Performance on questions designed to test inductive and deductive reasoning.
3.  **Qualitative Review**:
    *   Manual inspection of model outputs for coherence, factual accuracy (in the context of 8th-grade science), and appropriate tone.
    *   Assessment of whether the AI exhibits curiosity or asks clarifying questions (a more advanced goal).

## 4. Model Validation Process

1.  **Dataset Split**:
    *   The custom dataset (Q&A pairs, textbook excerpts) will be split into:
        *   **Training Set**: Used for model fine-tuning.
        *   **Validation Set**: Used during training to monitor for overfitting and for hyperparameter tuning.
        *   **Test Set**: Held-out set, used for final model evaluation after fine-tuning and hyperparameter selection. The `data/evaluation_exercises/` will serve as a core component of the test set.
2.  **Validation During Training**:
    *   If a validation split of the training data is available, `TrainingArguments.evaluation_strategy` will be set to "steps" or "epoch" to compute validation loss and perplexity periodically. This helps in early stopping or adjusting learning rates.
3.  **Post-Training Evaluation**:
    *   The best performing model checkpoint (based on validation metrics) will be thoroughly evaluated on the dedicated test set (`data/evaluation_exercises/` and potentially a held-out portion of the Q&A corpus).
    *   This evaluation will cover all defined metrics (accuracy, reasoning, qualitative aspects).
4.  **Benchmarking (Future Consideration)**:
    *   Compare performance against the base Llama 2 7B model (zero-shot or few-shot on the eval tasks).
    *   If other relevant middle school science benchmarks exist, consider evaluating against them.

This structured approach to hyperparameter tuning and validation will help ensure the development of a robust and effective cognitive AI model.
