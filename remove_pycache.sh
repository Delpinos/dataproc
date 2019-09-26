find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf &>/dev/null
git rm -f `git ls-files -i --exclude-from=.gitignore` &>/dev/null