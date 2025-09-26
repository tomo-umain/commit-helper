# commit-helper
helps you format commits + branches to the Jira WEBCHAN standard

## making branches
- the branch script will ask you for a `WEBCHAN ID` and guide you through the steps to ensure the formatting is always consistent.

<img width="751" height="153" alt="image" src="https://github.com/user-attachments/assets/9e934fc0-5c33-492d-a73c-c5ba7933eb39" />

## committing
- if you have run the branch script already and are not on develop, the commit script will read the `WEBCHAN ID` ✨ **automagically** ✨ from the branch name and guide you through the steps to ensure the commit name is always consistent.

<img width="651" height="129" alt="image" src="https://github.com/user-attachments/assets/78856158-11ee-4397-9c92-a54770bb3748" />

## aliases
- to avoid calling the Python files directly, I recommend adding these aliases to your terminal aliases, usually found in `~/.zshrc`. modify the script locations to suit you
```bash
alias cm="python3 ~/Documents/scripts/github.cm.py"
alias gcb="python3 ~/Documents/scripts/github.gcb.py"
```
