# Article Generator

Interface to generate, publish and deploy article for your Hexo or Jekyll blog
Overview

This suite includes two main Python scripts: BlogPublisher, a GUI application for managing and publishing blog articles, and an auxiliary script for content generation and manipulation. The BlogPublisher script utilizes a dark-themed interface provided by CustomTkinter for setting up and generating blog content, while the auxiliary script offers backend support including content generation through OpenAI's API, article updating, and deployment.
Prerequisites

Before using these scripts, ensure you have the following installed:

    Python 3.x: The programming language used for both scripts.
    CustomTkinter: A library providing custom widgets for a better GUI experience in BlogPublisher.
    Requests: A library used for making API calls in the auxiliary script.
    PyYAML: A library used for YAML operations within the auxiliary script.

Additionally, you'll need an OpenAI API key for the content generation features.
Installation

    Install Python Dependencies: Run the following command to install the necessary Python libraries:

    bash

    pip install customtkinter requests pyyaml

    API Key Configuration: Insert your OpenAI API key into the API_KEY variable in the auxiliary script.

Usage
BlogPublisher Script

The BlogPublisher application is a graphical interface for setting up and managing your blog's content. Features include:

    Setting the blog directory and type (Hexo or Jekyll).
    Configuring categories, tags, and the number of articles.
    Generating article subjects and full articles.
    Publishing articles directly from the GUI.

To run the application, navigate to the script's directory in your terminal and execute:

bash

python BlogPublisher.py

Auxiliary Script

This script supports the main application and includes functions for:

    Cleaning and formatting titles.
    Generating content with OpenAI's API.
    Updating existing articles with new content, tags, and categories.
    Creating and publishing articles for Hexo or Jekyll blogs.

This script is utilized internally by the BlogPublisher but can also be modified for standalone use.
Contributing

Contributions to the project are welcome! You can contribute by:

    Reporting bugs
    Suggesting enhancements
    Submitting pull requests with new features or bug fixes

License

Specify your project's license here. If you haven't chosen a license yet, you can browse https://choosealicense.com/ to find one that suits your project.
Acknowledgments

    CustomTkinter for the GUI components.
    OpenAI for the content generation API.

For any questions or contributions, please open an issue or pull request on the project's repository.
