import openai
import os
from utils.nlp_analysis import analyze_text

# Set your OpenAI API key here or use environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-...your-key...")
openai.api_key = OPENAI_API_KEY

class AIInterviewer:
    def __init__(self, context=None):
        self.context = context or "You are an AI interviewer. Ask relevant questions and evaluate answers."
        self.questions = []
        self.answers = []
        self.scores = []

    def generate_question(self, previous_answer=None):
        prompt = self.context
        if previous_answer:
            prompt += f"\nCandidate's previous answer: {previous_answer}\nAsk the next question."
        else:
            prompt += "\nStart the interview. Ask the first question."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        question = response.choices[0].message['content'].strip()
        self.questions.append(question)
        return question

    def evaluate_answer(self, question, answer):
        # Use LLM to evaluate answer
        prompt = f"Question: {question}\nAnswer: {answer}\nEvaluate the answer for accuracy, completeness, and confidence. Give a score out of 10 and a short explanation."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        evaluation = response.choices[0].message['content'].strip()
        # Extract score (simple parsing)
        score = None
        for line in evaluation.splitlines():
            if "score" in line.lower():
                try:
                    score = float([s for s in line.split() if s.replace('.', '', 1).isdigit()][0])
                    break
                except Exception:
                    continue
        if score is None:
            score = 5.0  # default if not found
        self.answers.append(answer)
        self.scores.append(score)
        return {"evaluation": evaluation, "score": score}

    def make_decision(self):
        avg_score = sum(self.scores) / len(self.scores) if self.scores else 0
        return "Pass" if avg_score >= 6.0 else "Fail"

# Example usage:
# interviewer = AIInterviewer()
# q = interviewer.generate_question()
# result = interviewer.evaluate_answer(q, "My answer...")
# decision = interviewer.make_decision()

