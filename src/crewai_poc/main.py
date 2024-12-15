#!/usr/bin/env python
import sys
import warnings

from crewai_poc.crew import CrewaiPoc

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'business_logic': """
The user needs an email address and an username to be created.

An user is distinguished from the others by his email address.

The username lenght cannot exceed 30 characters or less and can contain only alpha-numeric + “-” + “_” characters.

An user can be created, specifying an username and an email.

The user subscription process works as follows:

The user specify an email address.

The email address is verified by an external service.

A validation email is sent to the specified email address.

After clicking on the validation email, the user specify his username and his password.

The password must be stored in a password manager.

The user is created using the username and the email address.

The user authentication process required a strong password and the user’s email.
The user can be renamed, the email address can be modify, it must be validated before the modification apply.
The user can be deleted.
"""
    }
    CrewaiPoc().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CrewaiPoc().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewaiPoc().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CrewaiPoc().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
