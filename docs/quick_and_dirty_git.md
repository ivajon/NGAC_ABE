# quick and dirty git

Contains a quick and dirty guide to git.  This is not meant to be a complete guide, but rather a quick reference for the most common commands.

### Create a branch

```bash
git branch <branch_name>                # Create branch
git checkout <branch_name>              # Switch to branch
git checkout -b <branch_name>           # 2for1 switcheroo
git branch -a                           # List all branches
git branch -r                           # List remote branches
git branch -d <branch_name>             # Delete branch,locally
git push origin --delete <branch_name>  # Delete branch, remotely
```

## Github specific

### Create a pull request

Go to [github](https://github.com/ivario123/NGAC_ABE/pulls) and click on `New pull request`.  Select the branch you want to merge into master and click `Create pull request`.  Add a description, assign the pull request to the scrum master and assign reviewers. When the pull request is approved, the scrum master merges the pull request.

### Finding things to work on

Go to [github](https://github.com/ivario123/NGAC_ABE/issues) and look through the issue list.  Assign yourself to an issue and create a branch for it.

### If you are stuck

Go to [github](https://github.com/ivario123/NGAC_ABE/issues) find the issue you are working on and write comments there. If you are stuck, ask for help in the discord server.

## Doing reviews

A review should be exhaustive and should cover the following:

- Does the code do what it is supposed to do?
- Does it follow the standards?
- Is the code readable?
- Is the code documented? (every public function should have a docstring)
- Is the code tested? (every major function should have a unit test)
- Is the code efficient? (no unnecessary loops, no unnecessary memory allocations, etc.)

Note that pointing these things out is just a way to help the author improve the code quality.  It is not a way to make the author feel bad.
