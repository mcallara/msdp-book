---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 5.3 Packaging
```{code-cell} python
:tags: [remove-input]
import os
os.chdir('../home')
```

%TODO: 
%Packaging (https://packaging.python.org/en/latest/flow/ , https://python-poetry.org/docs/libraries/ )
%Distribution package
%What is a distribution package
%Build with poetry
%Python Package Index (PyPI)
%Upload to the package distribution service, publishing with poetry.


Create Gitlab account
Create Repo
Create Access Token, Api and Developer
Look for Project ID

poetry build
poetry config repositories.gitlab https://gitlab.com/api/v4/projects/55040597/packages/pypi --local
poetry publish --repository gitlab -u mcallara -p YOURTOKEN
