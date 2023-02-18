# VoidStars-JHU-Clue
VoidStars team project for JHU graduate software engineering course

# Setup
After cloning the repo, navigate to the project root in your terminal. Create a new python virtual environment in the project root called venv (the article in slack will explain how to do this). Then activate the environment and run pip install -r requirements.txt.

# Testing
When writing unit tests, create a separate file and follow the naming convention "test_[THING YOU ARE TESTING]". If you had a file called gameboard.py, your unit tests would go in test_gameboard.py. If you haven't worked with pytest it's incredibly straightforward, and the article linked in slack should explain everything. Remember that all your test functions need to start with the string "test_" in order for pytest to recognize them.
