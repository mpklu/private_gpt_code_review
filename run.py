import fire
import subprocess
import os
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.messages import ChatMessage
from langchain_community.llms import Ollama
from prompts import code_review_instructions

llm_model = Ollama(model="mistral")

# llama3 model does not strictly follow the review instructions
# It's not be as engaging in conversational dialogue as Mistral
# llm_model = Ollama(model="llama3")
gitlab_token = os.getenv("GITLAB_TOKEN")
gitlab_server = os.getenv("GITLAB_SERVER")


def prompt_template():
    template = code_review_instructions

    human_template = "Review the code diff: {content}"

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            ("human", human_template),
        ]
    )
    return chat_prompt


def review_code_diff(processed_code):
    chat_prompt = prompt_template()
    messages = chat_prompt.format_messages(content=processed_code)
    result = llm_model.invoke(messages)
    print(result)


def get_git_diff(repo_path):
    # Store the current working directory
    current_dir = os.getcwd()

    try:
        # Change to the specified git repository directory
        os.chdir(repo_path)

        # Run 'git diff' command and capture the output
        command = "git diff -U20 && git diff --cached -U20"
        git_diff_output = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )

        # Check if 'git diff' command was successful
        if git_diff_output.returncode == 0:
            # Return the git diff output
            return git_diff_output.stdout
        else:
            # Print error message if 'git diff' command failed
            print("Error: Failed to retrieve git diff.")
            return None
    except FileNotFoundError:
        print("Error: Specified directory is not a valid git repository.")
        return None
    finally:
        # Change back to the original working directory
        os.chdir(current_dir)


def review_local(repo_path):
    # Get the git diff content for the local repository
    diff_content = get_git_diff(repo_path)
    # print("git diff:")
    # print(diff_content)

    review_code_diff(diff_content)


def get_gitlab_diff(project_id, commit_sha):
    # Define the GitLab API URL
    gitlab_api_url = f"{gitlab_server}/api/v4/projects/{project_id}/repository/commits/{commit_sha}/diff"
    return ""


def review_gitlab(project_id: int, commit_sha: str):
    # Get the git diff content for the GitLab repository
    diff_content = get_gitlab_diff(project_id, commit_sha)

    print("git diff:")
    print(diff_content)


if __name__ == "__main__":
    fire.Fire(
        {
            "local": review_local,
            "gitlab": review_gitlab,
        }
    )
