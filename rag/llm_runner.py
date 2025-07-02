# rag/llm_runner.py

from llama_cpp import Llama


class LLMRunner:
    def __init__(self, model_path: str):
        self.model = Llama(model_path=model_path, n_ctx=2048, n_threads=4)

    def generate_answer(self, prompt: str) -> str:
        response = self.model(prompt=prompt, max_tokens=512, stop=["\n\n", "User:", "Question:"], echo=False)
        return response["choices"][0]["text"].strip()
