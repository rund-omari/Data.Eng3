# Data Preparation & Engineering for Machine Learning

**Instructor:** Rund Alomari  
**Course repository:** Lecture materials, practice datasets, assignments, and student submissions.

Welcome! This repository is our shared workspace for learning practical data preparation and engineering with Python, Pandas, and machine-learning-ready data.

## Repository structure

```text
.
├── lectures/                 # Instructor materials, notebooks and interactive lessons
│   ├── lecture_01/           # Introduction to Data Engineering for ML
│   └── lecture_02/           # Data Formats & Getting Started with Pandas
├── datasets/                 # Shared practice datasets (non-sensitive only)
├── assignments/              # Assignment instructions and deadlines
│   └── assignment_01/
├── students/                 # One folder per GitHub username
│   └── YOUR_GITHUB_USERNAME/
│       ├── assignment_01/
│       │   └── solution.ipynb
│       └── assignment_02/
├── templates/                # Example submission folder
├── resources/                # Additional references
├── .github/                  # Pull request template
├── .gitignore
├── CONTRIBUTING.md
└── requirements.txt
```

**Note:** Example student paths are illustrative. Create a folder using **your own exact GitHub username**.

## Getting started

1. Accept your GitHub repository invitation.
2. Clone the repository, and open the cloned folder in VS Code.
3. Activate your Python environment.
4. Install the libraries needed for the course:

```bash
python -m pip install -r requirements.txt
```

5. Study the materials in `lectures/`, and read each assignment's instructions in `assignments/`.
6. Submit your work under `students/YOUR_GITHUB_USERNAME/assignment_XX/`.

## How to submit an assignment

We practice a **branch + pull request** workflow. Do not push directly to `main`.

```bash
git switch main
git pull origin main
git switch -c assignment-01-YOUR_GITHUB_USERNAME

# Work only in students/YOUR_GITHUB_USERNAME/assignment_01/

git add students/YOUR_GITHUB_USERNAME/assignment_01/
git commit -m "Submit assignment 01 - YOUR_GITHUB_USERNAME"
git push -u origin assignment-01-YOUR_GITHUB_USERNAME
```

Open GitHub and create a **Pull Request** from your assignment branch into `main`.

Pull request title example: `Assignment 01 | YOUR_GITHUB_USERNAME`.

**Important:** Wait for the instructor's review before merging. A submitted Pull Request is your submission; it is not automatically approved or graded.

## Submission rules

- Submit only to your own student folder.
- Do not edit, delete, or move instructor materials or other students' work.
- Include your code or notebook and any required supporting files.
- Your code should run from top to bottom and include brief, clear explanations.
- Never commit passwords, API keys, `.env` files, or personal/customer data.
- Follow the assignment instructions and deadlines.

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the complete workflow and naming conventions.

## Lecture guide

| Lecture | Topic | Materials |
|---|---|---|
| 01 | Data Engineering for Machine Learning | `lectures/lecture_01/` |
| 02 | Data Formats & Getting Started with Pandas | `lectures/lecture_02/` |
| 03+ | More lessons will be added during the course | Coming soon |

## Need help?

Use the course communication channel or contact the instructor. When reporting an issue, include the lecture or assignment number and a clear description of the error (without exposing credentials).

---

**Prepared & Presented by Rund Alomari**  
SDK — *Touch Your Future*
