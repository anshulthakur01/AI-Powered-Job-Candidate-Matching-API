# AI-Powered-Job-Candidate-Matching-API

Ai Powered REST APIs application , Used to Create, Retrieve, Update, Delete Jobs by Admins (HRs). Get AI-Powered recommendations of Top candidated who applied for that Job. Securely use of apis using JWT authentications for the protected routes.

### Pros :
- Admins can Create, Retrieve, Update, Delete Jobs.
- Candidates can Register and Modify their profile.
- Candidates can apply to the jobs.
- Admins can retrieve top candidates for specific job (Applied candidates only).

### Cons :
- Currently only handle small amount of users due to Context Window Limitations for the LLm. As LLm can take limited text. Currently not feasable for the large amount of users.


## Project setup :

### Access project from git :

Open terminal and run following commands step by step :
```bash
git clone https://github.com/anshulthakur01/AI-Powered-Job-Candidate-Matching-API.git
cd AI-Powered-Job-Candidate-Matching-API
```

### Create and activate virtual environment :

#### For Windows :
```bash
python -m venv venv     # Create virtualenv
\venv\Scripts\activate  # Activate venv
```

#### For Linux :
```bash
python3 -m venv venv     # Create virtualenv
source venv/bin/activate  # Activate venv
```


### Configuration :

Create a .env file in project root and add following or you can take refrence from .env_templarte also :

```bash
# App level secrets
SECRET_KEY="xxxxxxxxxx"
DEBUG="True" or "False"

# Groq LLM APi key
GROQ_API_KEY="<< YOUR GROQ API KEY >>"

# Postgres database configuration
DB_NAME="<< YOUR DATABASE NAME >>"
DB_USER="<< YOUR DATABASE USER >>"
DB_PASS="<< YOUR DATABASE PASSWORD >>"
DB_HOST="<< YOUR DATABASE HOST >>"
DB_PORT=5432
```


### Install requirements :

```bash
pip install -r requirements.txt
```

### Run project :

```bash
python manage.py runserver
```

### Starter guide :

- Collect and import the Postman collection inside the root directory named as "postman_collection.json" in Postman application and get started with APIs.
- Only those candidates will be ranked which have applied to that specific job in Candidate rank API.