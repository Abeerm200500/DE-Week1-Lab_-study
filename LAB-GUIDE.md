# Data Engineering Lab Guide

Everything you need for every lab: the first-time setup, the cycle each lab follows, submitting, catching up, and
fixing common problems. Keep this page open during labs.

Two notes for every command on this page:

- **Mac:** write `python3.11` wherever it says `py -3.11`.
- **Run commands in Terminal.

## How the course works

- You work on **one repository all semester**. Each lab builds on the previous one, step by step, into a
  complete data pipeline for The Market.
- Every lab follows **the same cycle**: a new branch, the lab's work, a pull request.
- **A pull request is your submission.** Your instructor reviews it, grades it and merges it into `main`.

## The rules

| Rule | Why |
| --- | --- |
| **Never push to `main`.** Always work on a lab branch | `main` holds only reviewed, merged work |
| **Only your instructor/TA merges** your pull requests | Merging happens after grading |
| **Never commit `.env`** | It holds your passwords. If it ever appears in `git status`, stop and ask |
| **One branch per lab**, named `lab-02`, `lab-03`, ... | Each pull request then holds exactly one lab |
| **Pull request title:** `Lab 3 – Your Full Name` | So your instructor knows whose work it is |
| **Run one course environment at a time** | Two environments fight over the same ports |

## Part 1. First lab: set up once

Before this, complete the "Before Lab 2: Student Setup" checklist (Git, Docker Desktop, VS Code, Python 3.11).

1. **Accept the invitations.** GitHub emails you two invitations: one to the organization and one to your
   repository. Accept both (they also appear at https://github.com/DataEngineering-Fall).

2. **Start Docker Desktop.** Open it and wait until it shows **Engine running**.

3. **Clone your repository** into a simple folder that is **not** inside OneDrive, for example
   `C:\Users\<you>\labs`, then open it in VS Code:

   ```
   git clone https://github.com/DataEngineering-Fall/<your repository>.git
   cd <your repository>
   code .
   ```

   From now on, use the terminal inside VS Code.

4. **Set your name and email for this repository:**

   ```
   git config user.name "Your Full Name"
   git config user.email "the email of your GitHub account"
   ```

5. **Create your settings file.** Copy `.env.example` to `.env`:

   ```
   cp .env.example .env
   ```

   (In Command Prompt instead of VS Code's terminal: `copy .env.example .env`.)
   Open `.env` and replace each `change_me` with a password of your own, **letters and numbers only**.

   > **Important:** set your passwords **before** step 7. The databases save them the first time they start,
   > so changing `.env` afterwards has no effect (see Troubleshooting).

6. **Install the Python packages:**

   ```
   py -3.11 -m pip install -r requirements.txt
   ```

7. **Start the environment:**

   ```
   docker compose --profile core up -d
   ```

   The first start downloads the images and loads The Market's data, so it takes a few minutes.
   Then check that all four services are running:

   ```
   docker compose ps
   ```

8. **Run the check script.** Every line must say OK:

   ```
   py -3.11 scripts/check_env.py
   ```

9. **Look at the data in your browser:**
   - **pgAdmin** at http://localhost:5050: log in with `student@example.com` and your `PGADMIN_PASSWORD`.
     Open **Servers → The Market → market-db** and enter your `MARKET_DB_PASSWORD` once.
   - **mongo-express** at http://localhost:8081: open the `market` database, then `website_reviews`.

10. **Submit lab 2** with the cycle in Part 2, from step 3.

## Part 2. Every lab

### 1. Start from your latest `main`

Open your repository in VS Code, then:

```
git checkout main
git pull
```

`git pull` brings your merged work from GitHub to your laptop, so each lab starts from your last reviewed lab.
It should end with `Already up to date.` or a list of the files it updated.

### 2. Start the environment

Open Docker Desktop and wait for **Engine running**. If `requirements.txt` changed, install again first:
`py -3.11 -m pip install -r requirements.txt`. Then:

```
docker compose --profile core up -d
```

### 3. Create the lab's branch

```
git checkout -b lab-03
```

Git answers `Switched to a new branch 'lab-03'`. Check it any time:

```
git status
```

The first line must say `On branch lab-03` (VS Code also shows the branch name at the bottom left). From now on,
everything you commit is saved on `lab-03`, not on `main`.

**Missed the previous lab, or your work is broken?** Use Part 3 (Catch up) instead of this step.

### 4. Do the lab

Edit and run your files in VS Code. Save your progress with commits as you go, not only at the end:

```
git status                                # what changed? (.env must never appear here)
git add sql/lab3.sql                      # choose the files to save
git commit -m "Lab 3: revenue by branch"  # save a snapshot on your laptop
```

A good commit message says **what** you did in a few words: `Lab 3: find duplicate sales`, not `update`.

### 5. Push and open the pull request

```
git push -u origin lab-03
```

`git push` uploads your branch to GitHub. Your work is now online, but it is not submitted yet. To submit it,
open a **pull request**: a request to add your lab branch's work into `main`.

1. Open your repository on GitHub. Right after a push, a yellow bar appears: *"lab-03 had recent pushes"*.
   Click its green **Compare & pull request** button.
   (No yellow bar? Open the **Pull requests** tab and click **New pull request**.)
2. Check the two boxes at the top. They read: **base: `main`** ← **compare: `lab-03`**.
   - **compare** = where your work is (your lab branch)
   - **base** = where it should go (`main`)
3. Write the title: `Lab 3 – Your Full Name`.
4. Click **Create pull request**. That is your submission.

### 6. After submitting

- **Need to change something before the deadline?** Commit and `git push` again on the same branch. The open
  pull request updates by itself; don't open a second one. (Once it is merged, it can no longer change.)
- **Your instructor ** then merges it into `main`.
- **At the end of the lab**, stop the environment: `docker compose --profile core down` (your data is kept).

## Part 3. Missed a lab? Use the Catch up Branches

After each lab's deadline, your instructor publishes a starting point for the next lab in the course template: a
branch named `lab-NN-start` (for example `lab-04-start`). It holds everything you need at the start of that lab.

Do steps 1 and 2 of Part 2 as usual. Then, **instead of step 3**, start lab 4 from it:

```
git remote add template https://github.com/DataEngineering-Fall/themarket-template.git   # only the first time
git checkout -b lab-04
git fetch template
git checkout template/lab-04-start -- .
git commit -m "Lab 4: start from lab-04-start"
```

- `git remote add` saves the template's address under the name `template` (your own repository is `origin`).
- `git fetch template` downloads the template's branches without changing your files.
- `git checkout template/lab-04-start -- .` copies the starting files into your branch. Files with the same name
  are replaced by the starting version; your other files stay.

If the starting files changed `requirements.txt` or `docker-compose.yml`, run the commands of step 2 again.
Check with `git status` that you are `On branch lab-04`, then continue with steps 4 to 6 of Part 2 as usual.
In your pull request, mention that you started from `lab-04-start`.

**How the catch-up reaches `main`:** not directly (never push to `main`). The catch-up commit is part of your
`lab-04` branch, so it goes into `main` together with your lab 4 work when your instructor merges your pull
request. After that merge, `git pull` on `main` (step 1 of the next lab) brings it to your laptop, and you
continue normally.

## Commands you will use most

| Command | What it does |
| --- | --- |
| `git status` | Shows the branch you are on and what changed |
| `git checkout main` | Switches to the `main` branch |
| `git pull` | Brings the latest changes from GitHub |
| `git checkout -b lab-03` | Creates a new branch and switches to it |
| `git add <file>` | Chooses a file for the next commit |
| `git commit -m "..."` | Saves a snapshot on your laptop |
| `git push -u origin lab-03` | Sends the branch to GitHub (after the first time, `git push` is enough) |
| `git log --oneline` | Lists your commits |
| `git branch -a` | Lists your branches, and the ones on GitHub |
| `docker compose --profile core up -d` | Starts the environment |
| `docker compose --profile core down` | Stops it (data kept) |
| `docker compose --profile core down -v` | Stops it and deletes the databases; the next `up -d` rebuilds the original data |
| `docker compose ps` | Shows what's running |
| `docker compose logs <service>` | Shows a service's messages, to find errors |

## Troubleshooting

| Problem | Fix |
| --- | --- |
| "Cannot connect to the Docker daemon" or "docker: command not found" | Start Docker Desktop and wait for **Engine running** |
| `docker compose` says "no configuration file provided" | You're in the wrong folder. Use VS Code's terminal, which opens in your repository |
| "port is already allocated" | Another course environment is running. Stop it with `docker compose --profile core down` in its folder, or ask your instructor |
| "Password authentication failed" after changing `.env` | The databases kept your first passwords. Reset them: `docker compose --profile core down -v`, then `docker compose --profile core up -d` |
| pgAdmin shows no "The Market" group, or won't log in | `docker compose --profile core rm -s -f -v pgadmin`, then `docker compose --profile core up -d` |
| `git push` or `git clone` says "Repository not found" or "Permission denied" | Git is using another GitHub account saved on your laptop. Run `cmdkey /delete:git:https://github.com` (Windows), then try again and sign in with your course account |
| `.env` appears in `git status` | It was saved as `.env.txt`, or `.gitignore` is missing. Rename it to exactly `.env`; ask before committing anything |
| `git pull` says "untracked working tree files would be overwritten" | A file on your laptop has the same name as one coming from GitHub. Rename or delete your copy, then pull again |
| You committed on `main` by mistake | Don't push. Run `git branch lab-03` (keeps your work on a lab branch), `git reset --hard origin/main`, then `git checkout lab-03` |
| A path with spaces breaks a command | Put the path in quotes: `cd "C:\Users\me\My Labs"` |
| Anything else | Run `py -3.11 scripts/check_env.py` and send its output with a screenshot of the error |
