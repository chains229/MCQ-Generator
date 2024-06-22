from typing import List

class Question:
    def __init__(self, answerText:str, questionText: str = '', distractors: List[str] = []):
        self.answerText = answerText
        self.questionText = questionText
        self.distractors = distractors
    def __str__(self):
        return f"Question: {self.questionText}\nAnswer: {self.answerText}\nDistractors: {', '.join(self.distractors)}"
