def calculate_score(questions, user_answers):
    score = 0
    for i, q in enumerate(questions):
        if user_answers[i] == q["answer"]:
            score += 1
    return score


def get_feedback(score, total):
    percentage = (score / total) * 100
    
    if percentage >= 80:
        return "Excellent 🔥"
    elif percentage >= 60:
        return "Good 👍"
    elif percentage >= 40:
        return "Average 🙂"
    else:
        return "Needs Improvement ⚠️"


def get_result_summary(questions, user_answers):
    result = []
    
    for i, q in enumerate(questions):
        if user_answers[i] == q["answer"]:
            result.append((q["question"], "Correct"))
        else:
            result.append((q["question"], f"Wrong (Ans: {q['answer']})"))
    
    return result