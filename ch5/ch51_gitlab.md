% Sections
% - Software Development Life Cycle  (https://about.gitlab.com/platform/)  
% - Continuous integration  
% - Continuous delivery  
% - Continuous deployment  
% - GitLab CI/CD GitLab CI CD Tutorial for Beginners [Crash Course]  

# 5.1 Software Development Life Cycle 

This chapter introduces the core concepts of the Software Development Life Cycle (SDLC), focusing on Continuous Integration (CI), Continuous Delivery (CD), and Continuous Deployment. We'll explore how GitLab's CI/CD platform can facilitate these practices, enhancing the efficiency and reliability of software development processes.

## Understanding the SDLC

The SDLC outlines the phases involved in developing software, aiming to produce high-quality software in a cost-effective and timely manner. It encompasses everything from initial planning and analysis through maintenance and eventual retirement of the system. GitLab supports the SDLC by providing tools for project management, source code management, and automated CI/CD processes.

### Continuous Integration (CI)

Continuous Integration encourages developers to integrate their changes into a main branch frequently. Each push is automatically built and tested, reducing integration issues and allowing teams to develop cohesive software more rapidly.

#### GitLab CI Essentials

GitLab CI, integrated within the GitLab platform, automates the process of software integration by executing predefined scripts. These scripts can build the project, run tests, and perform many other tasks based on the project's needs.

- **Features of GitLab CI** include:
    - **Automated testing**: Automatically runs your tests.
    - **Merge requests integration**: Allows easy viewing of CI statuses directly from merge requests.
    - **Parallel execution**: Enables splitting your build into multiple jobs that can run simultaneously.

### Continuous Delivery and Deployment

Continuous Delivery extends CI by ensuring that your software can be released to your customers at any moment. It involves automatically deploying all changes to a testing or staging environment after the build stage.

Continuous Deployment takes this a step further by automatically deploying every change that passes through the pipeline to production, eliminating manual steps in the deployment process.

#### Implementing CD with GitLab

GitLab facilitates Continuous Delivery and Deployment by allowing developers to define specific jobs and environments in the `.gitlab-ci.yml` file. This includes automatic deployment to environments like staging or production, with controls for manual gates or fully automated workflows.

## Getting Started with GitLab CI/CD

To leverage GitLab CI/CD, you'll need familiarity with YAML and a GitLab account. Here's a basic overview to kickstart your CI/CD journey:

1. **Create a `.gitlab-ci.yml` file** in your project's root directory. This file defines your CI/CD pipeline in GitLab.

2. **Define pipeline stages**: Common stages include `build`, `test`, and `deploy`, each containing specific jobs.

3. **Configure jobs**: Jobs define the actions to be performed at each stage, such as scripts to execute.

4. **Utilize GitLab Runners**: Runners execute your jobs. You can use GitLab's shared runners or set up your own.

5. **Monitor your pipeline**: After pushing changes to a repository with a `.gitlab-ci.yml` file, GitLab automatically initiates and runs your pipeline. You can track its progress and review job logs within the GitLab interface.

### Sample `.gitlab-ci.yml` Configuration

```yaml
stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  script:
    - echo "Building the project..."

test_job:
  stage: test
  script:
    - echo "Running tests..."

deploy_job:
  stage: deploy
  script:
    - echo "Deploying to production..."
```

This simple pipeline configuration demonstrates defining stages and jobs within a GitLab CI/CD pipeline.
