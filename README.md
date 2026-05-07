# quick-note

## "A notes and tasks app with authentication to save your quick notes add task!"


## App overview--
  - Add, update and delete notes 
  - Add, update and delete tasks with checkbox toggle
  - User authentication (register, login, logout)
  - Each user sees only their own notes and tasks
  - After logout 
 ## Built using ---
  - Python (Flask)
  - SQLite (Flask-SQLAlchemy)
  - HTML, CSS, JavaScript

## How to Install and Run


  1. Clone the repo--
      git clone https://github.com/taaiiioo/quick-note.git


  3. Create a virtual environment (optional but recommended)--
      python -m venv .venv
      source .venv/bin/activate


  4. Install dependencies with -- 
      pip install -r requirements.txt


  5. Run the app with --
      python server.py


  6. It will open in browser--
      http://127.0.0.1:5000

# Note--
  - A .env file with a secret key will be automatically created on first run.
  - To delete all data, delete the instance/notes.db file and restart the app.
