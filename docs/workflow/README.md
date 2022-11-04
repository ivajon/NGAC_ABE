# Workflow
This file contains the workflow for the project.  The workflow is as follows:


## Sprint preparation
- Create a project for every sprint ( One person does this )
- Create an issue for every story and subtask in the sprint
- Assign the issue with priority and estimate

## Sprint
- Self-assign issues that you want to work on ( typically two people per issue )
- Create branches for every issue that you are working on
- Commit often.
- When you are done with an issue, create a pull request a review from at least one other person and assign the pull request to the current scrum master.
- When the pull request is approved, repo owner ( or scrum master if it works ) merges the pull request and deletes the branch. 

### If a pull request is merged
When a new pull request is merged all branches should be rebased onto the master to avoid conflicts.  This can be done by running the following command:

```bash
git checkout master     # Make sure you are on the master branch
git pull                # Get the latest changes
git checkout <branch>   # Switch to the branch you want to rebase
git rebase master       # Rebase the branch onto master
```

### Other things to keep in mind to reduce our headaches
- Commit messages should be descriptive and should contain a short description of the thing they are adding. For example, adding a function to parse a tree structure to a string should have a commit message like `Added function to parse tree to string`.  This makes it easier to find the commit that introduced a bug.



