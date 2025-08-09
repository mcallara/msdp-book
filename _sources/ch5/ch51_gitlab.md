% Sections
% - Software Development Life Cycle  (https://about.gitlab.com/platform/)  
% - Continuous integration  
% - Continuous delivery  
% - Continuous deployment  
% - GitLab CI/CD GitLab CI CD Tutorial for Beginners [Crash Course]  

# 5.1 CI/CD pipelines with Gitlab

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

To implement DevOps, development teams apply different best practices. An important one, is CI/CD which stands for continuos integration and continuos delivery or deployment.

## Continuous Integration (CI)

Continuous Integration encourages developers to integrate their changes into a main branch frequently. Each push is automatically built and tested, reducing integration issues and allowing teams to develop cohesive software more rapidly.

## Continuous Delivery and Deployment

The key difference between **Continuous Delivery** and **Continuous Deployment** lies in the final step of the software release process:

### Continuous Delivery (CD)
- **Automated pipeline with manual release**: The code is automatically built, tested, and prepared for deployment, but the actual release to production requires **manual approval/intervention**
- **Production-ready code**: Every change that passes the automated tests is ready to be deployed to production at any time
- **Human gate**: There's a human decision point before production deployment
- **Risk mitigation**: Allows for final business/stakeholder review before going live

### Continuous Deployment (CD)
- **Fully automated pipeline**: Every change that passes all automated tests is **automatically deployed to production** without human intervention
- **No manual gates**: No human approval step - if tests pass, it goes live immediately
- **Higher automation**: Requires more comprehensive automated testing and monitoring
- **Faster feedback**: Changes reach users immediately after passing tests

**Visually**

```
Continuous Delivery:
Code → Build → Test → Stage → [Manual Approval] → Production

Continuous Deployment:
Code → Build → Test → Stage → Production (automatic)
```

### When to Use Which?
- **Continuous Delivery**: Better for applications where you need business approval, regulatory compliance, or coordinated releases
- **Continuous Deployment**: Ideal for applications where rapid iteration is crucial and you have robust automated testing and monitoring in place

Both practices require strong automated testing, but Continuous Deployment demands even more confidence in your automated quality gates since there's no human safety net before production.

## How does GitLab CI/CD work?

Gitlab allow us to define a pipeline in our repository by creating a file named `.gitlab-ci.yml` in the root of the repository. A pipeline is a set of jobs that are executed in stages everytime a developer pushes a change to the repository. Each job is a script that runs in a separate docker container on a machine that GitLab provides for us named a runner. For example, we can define a job that runs tests, and another job that deploys the project to a server.

Furthermore, GitLab provides a set of predefined variables that we can use in our scripts to access information about the repository, the pipeline, and the runner. These variables are available in the environment where the job is executed and allow us to define conditional logic in our scripts. This means that we can define different behaviors for our jobs based on the values of these variables. For example, we can define a job that only runs when a specific branch is pushed to the repository.

## Getting Started with GitLab CI/CD

To get started with GitLab CI/CD, we will now create our first pipeline in a new repository. We will use the GitLab web interface to create a new repository named `my-package` that will only contain a README file, and then we will define a simple pipeline in a `.gitlab-ci.yml` file.

Go to the [GitLab website](https://gitlab.com/) and sign in with your account. Then, click on the "New project" button and select "Create blank project". Name your project "First Pipeline" and click on the "Create project" button. This will create a new repository in GitLab containing only a README file.

Let's now add a `.gitlab-ci.yml` file to the repository. This file will define a pipeline with three jobs. To do this, click on the "Create new file" button in the repository and name the file `.gitlab-ci.yml`. Then, paste the following content into the file and click on the "Commit changes" button.

```{code-block} yaml
stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  script:
    - echo "Building the project..."
    - echo "Hello, $GITLAB_USER_LOGIN!"

test_job:
  stage: test
  script:
    - echo "Running tests..."

deploy_job:
  stage: deploy
  script:
    - echo "Deploying to production..."
    - echo "This job deploys something from the $CI_COMMIT_BRANCH branch."
```

```{admonition} What to notice
:class: hint
- The `stages` keyword defines the stages of the pipeline. In this example, we have three stages: `build`, `test`, and `deploy`.
- Each stage contains a job. A job is a script that runs in a separate docker container on a machine that GitLab provides for us named a runner. In this example, we have three jobs: `build_job`, `test_job`, and `deploy_job`.
- The `script` keyword defines the commands that the job will execute. In this example, each job runs a set of commands to demonstrate how to access the predefined variables in the environment where the job is executed.
```

To inspect the pipeline, click on the "Build" button in the repository and then click on the "Pipelines". You will see the pipeline running with the three stages. You can inspect the logs of each job by clicking first on the stage and then on the job.

```{admonition} What to notice
:class: hint
- In the logs of each job, you will see the output of the commands that the job executed. You will also see the values of the predefined variables that we used in the commands.
```

To gain a better understanding of what is going on in each job, let's add some commands to the scripts that will show us more information about the environment where the job is executed. For example, we can add commands to show the list of files in the current directory, the output of the `git config --list` command. We can also add a command to create a new file in the current directory and then show the list of files again. To do this, edit the `.gitlab-ci.yml` file and add the following content:

```{code-block} yaml
stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  script:
    - echo "Building the project..."
    - echo "Hello, $GITLAB_USER_LOGIN!"
    - git config --list
    - git log
    - git status
    - pwd
    - ls -a
    - touch test-file.txt
    - ls -a

test_job:
  stage: test
  script:
    - echo "Running tests..."
    - git config --list
    - git log
    - git status
    - pwd
    - ls -a
    - touch test-file2.txt
    - ls -a

deploy_job:
  stage: deploy
  script:
    - echo "Deploying to production..."
    - echo "This job deploys something from the $CI_COMMIT_BRANCH branch."
    - git config --list
    - git log
    - git status
    - pwd
    - ls -a
    - echo $CI_PROJECT_ID
    - echo $CI_PROJECT_NAME
    - echo $CI_PROJECT_DIR
    - echo $CI_COMMIT_REF_NAME
```

```{admonition} What to notice
:class: hint
- In the logs of each job, you will see the output of the commands that the job executed. You will also see the values of the predefined variables that we used in the commands.
- The Gitlab pipeline checks out the commit in the runner's environment producing a detached HEAD state. This means that the runner is in a state where it is not on any branch. This is why the `git status` command shows that the runner is in a detached HEAD state.
- Files that are created in a job are not persisted to the next job. This means that the `test-file.txt` and `test-file2.txt` files that we created in the `build_job` and `test_job` jobs are not available in the `deploy_job` job.
```

## References

- [Continuous integration vs delivery vs deployment.](https://www.atlassian.com/continuous-delivery/principles/continuous-integration-vs-delivery-vs-deployment)