from analyzer import analyze_resume

sample_resume = """
Sarah Arshad
Computer Science Student

Skills:
Python, Java, JavaScript, React, MySQL, Firebase

Education:
BS Computer Science

Experience:
Software Development Intern

Projects:
AI Resume Evaluator
Interactive Sales Analytics Dashboard
Trail Tracking Android App
"""

print("Testing resume analysis...\n")

result = analyze_resume(sample_resume)

print("===== AI RESUME ANALYSIS =====\n")
print(result)