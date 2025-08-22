import os, json

from groq import Groq

SYSTEM_PROMPT = """
You are a Talent Acquisition Specialist. Rank the given users for job description based on skills, experience.

**Rules**
    - Always return response in ```json``` format . Example : {
        "job": {
            "id": << job_id >>,
            "title": "Junior Python Developer",
            "description": "We are looking for a motivated Python fresher to join our backend team. The candidate will work on web applications, REST APIs, and automation scripts.",
            "required_skills": [
                "Python",
                "Django",
                "REST API",
                "Git",
                "SQL",
                "Linux",
                "Nginx"
            ],
            "preferred_skills": [
                "Docker",
                "Celery",
                "Redis",
                "CI/CD",
                "PostgreSQL"
            ],
            "experience_required": 0,
            "education_required": [
                "Bachelor's in Computer Science",
                "Bachelor's in Information Technology",
                "B.Tech in Software Engineering"
            ],
            "employment_type": "full_time"
        },
        "candidates": [
            {
                "id": <<<id_here>>,
                "skills_matched": ["python", "django"],
                "rank": <<<< Rank of the user from give user list (positive integer in sequese based on user lis) >>>>,
                "description": "<<<< Mention the description here. Only add relevant description don't expose user id in this. Only prepare a proper description of ranking the user. >>>>
            }
        ]
    }
    - Only include the users in which atleast one skill is matched or any of details of user such as projects, summary matched with job description skills.
"""


class GroqLLM:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def send_message(self, messages):
        """
        Send data to Groq LLM and let llm decide the ranking.
        """

        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None
        )

        return completion.choices[0].message.content

    def prepare_ranking_prompt(self, job_data, users):
        return f"""
            This is **Job Description**
            jd = {job_data}

            users = {users}
        """
    
    def clean_response(self, content: str):
        """
        Remove ``` or ````json to clean llm response and prepare valid JSON.
        """
        return content.replace("```json", "").replace("```", "") if content else content
    
    def process_candidate_ranking(self, job_data, users):
        prompt = self.prepare_ranking_prompt(job_data, users)
        print("Prompt :", prompt)

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        print("Messages :", messages)
        llm_response = self.send_message(messages)
        print("LLM Response :", llm_response)

        cleaned_response = self.clean_response(llm_response)
        print("Cleaned  LLM response :", cleaned_response)

        return json.loads(cleaned_response)


grok_client = GroqLLM()