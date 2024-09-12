# Project Title

A little documentation on setting up a python virtual environment

## Installation 

Clone the repository to your local machine:

```bash
git clone git@github.com:G0oCe/timetable_bot.git
```
## Setting Up a Python Virtual Environment

Before you can start working on this project, you'll need to set up a Python virtual environment. This helps to keep dependencies used by different projects separate by creating isolated Python environments for them.

Here's how to set it up:

1. Navigate to the project directory:


```bash
cd \path\to\timetable_bot
```

2. Create the virtual environment:

On Windows, run:

```bash
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt

```

On Unix or MacOS, run:

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

3. Once the virtual environment is activated, the name of your virtual environment will appear on left side of terminal. This will let you know that the virtual environment is currently active. 

In the terminal, you should see something similar to:

```bash
(env) C:\path\to\timetable_bot
```

Now you can install necessary packages in this environment which are required for your project.

## Usage/Examples

N/A soon


[MIT](https://choosealicense.com/licenses/mit/)
