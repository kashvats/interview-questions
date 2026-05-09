# Technical Interview Mastery Registry

A production-grade, high-fidelity technical interview registry covering 880+ questions across 15 engineering domains. 

## 🚀 Live Demo
The registry is hosted on GitHub Pages: **[Link to your GitHub Pages URL once deployed]**

## 📂 Project Structure
- `*.json`: The source of truth for all interview questions, categorized by master-domains.
- `generate_html.py`: A Python script that compiles the JSON data into a rich, interactive `index.html` dashboard.
- `index.html`: The generated static dashboard featuring:
  - **Study Mode**: Full visibility for learning.
  - **Test Mode**: Blurred answers for self-assessment.
  - **Search & Filter**: Real-time filtering across 880+ items.
  - **Mastery Tracking**: LocalStorage-based persistence of your progress.

## 🛠️ How to Update
1. Modify or add questions in the relevant `.json` files.
2. Run the generator:
   ```bash
   python generate_html.py
   ```
3. Commit and push the changes to GitHub.

## 🤖 Automated Deployment
This repository is configured with GitHub Actions. Any push to the `main` branch will automatically:
1. Run `generate_html.py`.
2. Deploy the updated `index.html` to GitHub Pages.
