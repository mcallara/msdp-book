% Sections
% - Software Development Life Cycle  
% - Continuous integration  
% - Continuous delivery  
% - Continuous deployment  
% - GitHub Actions CI/CD Tutorial for Beginners [Crash Course]  

# 5.1 CI/CD pipelines with GitHub

## The DevOps Cycle

The DevOps cycle is a set of practices that combines software development (Dev) and IT operations (Ops). The goal is to shorten the software development life cycle (SDLC) and provide continuous delivery with high software quality.

The 8 phases of the [DevOps cycle](https://marvel-b1-cdn.bc0a.com/f00000000236551/dt-cdn.net/wp-content/uploads/2021/07/13429_ILL_DevOpsLoop.png) are:
- Plan
- Code
- Build
- Test
- Release
- Deploy
- Operate
- Monitor

To implement DevOps, development teams apply different best practices. An important one is CI/CD, which stands for continuous integration and continuous delivery or deployment.

## Continuous Integration (CI)

Continuous Integration encourages developers to integrate their changes into a main branch frequently. Each push is automatically built and tested, reducing integration issues and allowing teams to develop cohesive software more rapidly.

## Continuous Delivery and Deployment

Continuous Delivery extends CI by ensuring that your software can be released to your customers at any moment. It involves automatically deploying all changes to a testing or staging environment after the build stage.

Continuous Deployment takes this a step further by automatically deploying every change that passes through the pipeline to production, eliminating manual steps in the deployment process.

## How does GitHub Actions CI/CD work?

GitHub allows us to define a workflow in our repository by creating a file named `.github/workflows/ci.yml` (or any name) in the `.github/workflows` directory. A workflow is a set of jobs that are executed in stages every time a developer pushes a change to the repository or opens a pull request. Each job runs in a fresh virtual environment provided by GitHub called a runner. For example, we can define a job that runs tests, and another job that deploys the project to a server.

Furthermore, GitHub Actions provides a set of predefined environment variables that we can use in our scripts to access information about the repository, the workflow, and the runner. These variables are available in the environment where the job is executed and allow us to define conditional logic in our scripts. For example, we can define a job that only runs when a specific branch is pushed to the repository.

## Getting Started with GitHub Actions

To get started with GitHub Actions, we will now create our first workflow in a new repository. We will use the GitHub web interface to create a new repository named `my-package` that will only contain a README file, and then we will define a simple workflow in a `.github/workflows/ci.yml` file.

Go to the [GitHub website](https://github.com/) and sign in with your account. Then, click on the "New" button to create a new repository. Name your project "First Pipeline" and click on the "Create repository" button. This will create a new repository in GitHub containing only a README file.

Let's now add a workflow file to the repository. This file will define a workflow with three jobs. To do this, click on "Add file" > "Create new file" in the repository, name the file `.github/workflows/ci.yml`, and paste the following content into the file. Then, commit the changes.

```yaml
# filepath: .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build the project
        run: |
          echo "Building the project..."
          echo "Hello, ${{ github.actor }}!"

  test:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: echo "Running tests..."

  deploy:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          echo "This job deploys something from the ${{ github.ref_name }} branch."
```

```{admonition} What to notice
:class: hint
- The `on` keyword defines the events that trigger the workflow. In this example, the workflow runs on pushes and pull requests to the `main` branch.
- The workflow defines three jobs: `build`, `test`, and `deploy`. Each job runs in a fresh GitHub-hosted runner.
- The `steps` section defines the commands that the job will execute. The `actions/checkout` step checks out the repository code.
- The `${{ github.actor }}` and `${{ github.ref_name }}` are GitHub Actions environment variables.
```

To inspect the workflow, click on the "Actions" tab in the repository. You will see the workflow running with the three jobs. You can inspect the logs of each job by clicking on the job name.

```{admonition} What to notice
:class: hint
- In the logs of each job, you will see the output of the commands that the job executed. You will also see the values of the predefined variables that we used in the commands.
```

To gain a better understanding of what is going on in each job, let's add some commands to the steps that will show us more information about the environment where the job is executed. For example, we can add commands to show the list of files in the current directory, the output of the `git config --list` command, and the current working directory. We can also add a command to create a new file in the current directory and then show the list of files again. To do this, edit the `.github/workflows/ci.yml` file and add the following content:

```yaml
# filepath: .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build the project
        run: |
          echo "Building the project..."
          echo "Hello, ${{ github.actor }}!"
          git config --list
          git log --oneline
          git status
          pwd
          ls -a
          touch test-file.txt
          ls -a

  test:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          echo "Running tests..."
          git config --list
          git log --oneline
          git status
          pwd
          ls -a
          touch test-file2.txt
          ls -a

  deploy:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          echo "This job deploys something from the ${{ github.ref_name }} branch."
          git config --list
          git log --oneline
          git status
          pwd
          ls -a
          echo $GITHUB_REPOSITORY
          echo $GITHUB_WORKSPACE
          echo $GITHUB_REF_NAME
```

```{admonition} What to notice
:class: hint
- In the logs of each job, you will see the output of the commands that the job executed. You will also see the values of the predefined variables that we used in the commands.
- The GitHub Actions runner checks out the commit in a detached HEAD state, so `git status` will show that state.
- Files created in one job are not available in the next job, as each job runs in a fresh environment.
```

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Continuous integration vs delivery vs deployment.](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment)