# AI-Augmented-DevSecOps-Platform

this is just text to undo the changes from the files
# Q: Tell me about a challenging problem you faced during a project and how you solved it. #
# Situation: #
While building a cloud-native DevSecOps platform using FastAPI microservices, Docker, PostgreSQL, GitHub Actions, and Kubernetes, I encountered an issue where my GitHub Actions CI pipeline was failing even though the application was working perfectly on my local machine.

# Task: #
My goal was to make the CI pipeline stable and ensure that automated tests could run successfully in both local and cloud environments without depending on Docker Compose-specific configurations.

# Action: #
I started by analyzing the GitHub Actions logs and compared the CI environment with my local setup. I discovered that the user-service was trying to connect to a PostgreSQL host named "db", which existed only inside the Docker Compose network. Since GitHub Actions did not have that service available, the tests failed during application startup.

To solve this, I introduced a dedicated testing mode using environment variables. I modified the application startup sequence to skip PostgreSQL initialization during test execution and configured the tests to use an isolated SQLite database instead. I then validated the changes by running tests locally and through GitHub Actions.

# Result: #
The CI pipeline became stable, all automated tests passed successfully, and the application could be tested independently of the production database environment. This improved the reliability of the pipeline and reinforced my understanding of environment isolation, automated testing, and systematic debugging in CI/CD workflows.
