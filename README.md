# Planck DT

Minimal GitHub-ready and Vercel-ready repository for **Planck DT**.

## Structure

```text
planck-dt/
├─ api/
│  └─ simulate.py
├─ core/
│  ├─ __init__.py
│  └─ planck_dt.py
├─ index.html
├─ app.js
├─ styles.css
├─ requirements.txt
├─ vercel.json
└─ .gitignore
```

## Local quick test

```bash
python -c "from core.planck_dt import run_summary; print(run_summary())"
```

## GitHub

```bash
git init
git add .
git commit -m "Initial Planck DT prototype"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/planck-dt.git
git push -u origin main
```

## Vercel

Import the repo into Vercel and deploy.
The API endpoint will be available at:

```text
/api/simulate
```
