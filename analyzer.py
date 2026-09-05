import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY was not found.")


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=api_key
)


def is_resume(resume_text):
    """
    Check whether the uploaded document appears to be a resume/CV.
    Returns True if it is a resume, otherwise False.
    """

    validation_prompt = f"""
You are a strict document classifier.

Your ONLY task is to determine whether the provided document is a
professional resume/CV.

A resume/CV normally contains several career-related elements such as:
- Candidate/contact information
- Education
- Work experience
- Internships
- Skills
- Projects
- Certifications
- Professional summary/objective
- Achievements

IMPORTANT RULES:
- A certificate is NOT a resume.
- A course completion certificate is NOT a resume.
- An academic assignment is NOT a resume.
- A transcript is NOT a resume.
- An invoice or receipt is NOT a resume.
- A cover letter by itself is NOT a resume.
- A random document is NOT a resume.
- Do not classify a document as a resume simply because it contains a person's name.
- Do not classify a document as a resume simply because it contains career-related words.
- A short resume is still a resume if it clearly represents a person's CV/resume.
- Base your decision ONLY on the provided text.
- Do not guess missing information.

Return EXACTLY one of these two values:

VALID
INVALID

Document:
{resume_text}
"""

    response = llm.invoke(validation_prompt)

    result = response.content.strip().upper()

    if result.startswith("VALID"):
        return True

    if result.startswith("INVALID"):
        return False
  
    # If the model returns an unexpected response,
    # reject the document rather than analyzing it.
    return False


def analyze_resume(resume_text):
    """
    Analyze a document that has already been validated as a resume.
    """

    prompt = f"""
You are an AI resume evaluator.

The document below has already been validated as a resume/CV.

Analyze ONLY information explicitly present in the resume.

STRICT ANTI-HALLUCINATION RULES:
- Never invent names, companies, dates, degrees, GPAs, job titles,
  achievements, metrics, skills, technologies, URLs, or other facts.
- Never assume information that is not explicitly present.
- If information is missing, say "Not provided in the resume."
- Do not recommend a skill as if the candidate already has that skill.
- Do not create fake achievements, projects, experience, numbers,
  technologies, qualifications, or certifications.
- Do not infer that the candidate knows a technology merely because
  another technology or concept is mentioned.
- Recommendations must be based on actual weaknesses in the resume.
- If you suggest adding something that is not currently present,
  clearly describe it as a recommendation, NOT as existing candidate
  information.
- Do not fabricate examples containing candidate-specific information.

Provide the analysis using these sections:

1. Overall Assessment
Give a brief assessment of the resume's current quality based only
on the actual resume.

2. Skills Identified
List ONLY skills, technologies, tools, languages, or competencies
explicitly mentioned in the resume.

3. Strengths
Identify genuine strengths supported by the resume.

4. Areas for Improvement
Identify specific weaknesses or areas that could be improved.
Do not invent missing facts.

5. Resume Structure & Formatting
Evaluate structure, organization, readability, and formatting based
only on what can reasonably be determined from the resume text.

6. ATS & Readability
Identify potential ATS and readability issues based on the actual
resume content.
Do not claim that something is missing unless it is actually absent.

7. Missing or Weak Sections
Identify sections that are missing or insufficiently detailed.

8. Actionable Recommendations
Give practical recommendations for improving the resume.

IMPORTANT:
When recommending something that is not currently present, phrase it
as a recommendation.

For example:
"Consider adding a professional summary if appropriate."

Do NOT write:
"The candidate should add their Python skills."

unless Python is actually present in the resume.

Do not provide fake candidate-specific examples.

Keep the response organized, professional, and concise.

RESUME:
{resume_text}
"""

    response = llm.invoke(prompt)

    return response.content