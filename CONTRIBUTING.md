# Student Submission Guide

This is a shared course repository. Treat other people's work and instructor materials with care.

## Rules

1. Work only inside `students/YOUR_GITHUB_USERNAME/`.
2. For each assignment, create a dedicated subfolder named `assignment_01`, `assignment_02`, and so on.
3. Use short, meaningful filenames such as `solution.ipynb`, `answers.py`, or `reflection.md`.
4. Do not modify `lectures/`, `datasets/`, `assignments/`, `.github/`, or other students' folders.
5. Never upload `.env` secrets, tokens, credentials, or sensitive real-world data.
6. Submit through a separate branch and Pull Request. Do **not** merge your own submission into `main` unless the instructor explicitly asks.
7. Put the assignment number and GitHub username in the Pull Request title.
8. Respond to review comments on your Pull Request. Make corrections on the same branch when asked.

## Example workflow

```bash
git switch main
git pull origin main
git switch -c assignment-01-YOUR_GITHUB_USERNAME
# Add/edit files in students/YOUR_GITHUB_USERNAME/assignment_01/
git add students/YOUR_GITHUB_USERNAME/assignment_01/
git commit -m "Assignment 01 submission"
git push -u origin assignment-01-YOUR_GITHUB_USERNAME
```

Then open a Pull Request targeting `main` on GitHub.

**Repository permissions warning:** Folders are an organizational convention, not a GitHub permission boundary. Students with write access to a shared repository may technically be able to change other folders or branches. Instructor review and protected-branch settings (where available) are recommended.

**Privacy warning:** Other collaborators may be able to see work in branches and Pull Requests, even before it is graded. For private individual submissions, separate student repositories are safer.
