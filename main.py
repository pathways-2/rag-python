import os
import warnings
from pathlib import Path
from dotenv import load_dotenv
from rag_chat import RAGChat
from cli_interface import CLIInterface, Config, Colors

warnings.filterwarnings("ignore", message="Pydantic serializer warnings")


def load_environment():
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        return True, "Environment variables loaded from .env file"
    else:
        return False, "No .env file found, using system environment variables"


def check_environment_variables():
    missing_vars = []
    for var in Config.ENV_VARS:
        if not os.environ.get(var):
            missing_vars.append(var)
    return missing_vars


def main():
    cli = CLIInterface(Config.APP_NAME)

    cli.clear_screen()
    cli.print_welcome_banner()

    env_loaded, env_message = load_environment()

    statuses = []
    statuses.append((env_loaded, env_message))

    missing_vars = check_environment_variables()
    if missing_vars:
        statuses.append((False, "Missing required environment variables"))
        cli.print_status_box(statuses)
        cli.print_environment_error(missing_vars)
        return
    else:
        statuses.append((True, "All environment variables configured"))

    try:
        rag = RAGChat(cli)
        statuses.append((True, "RAG Chat initialized successfully"))
        statuses.append((True, "Connected to Vectorize and OpenAI"))
        cli.print_status_box(statuses)

        cli.print_exit_instructions()

        while True:
            try:
                question = cli.get_user_input()

                if question.lower() in Config.QUIT_COMMANDS:
                    cli.print_goodbye()
                    break

                if not question:
                    cli.print_warning("Please enter a question")
                    continue

                answer = rag.chat(question)
                cli.print_answer(answer)

            except KeyboardInterrupt:
                cli.print_info("\nOperation cancelled")
                continue
            except Exception as e:
                cli.print_error(f"An error occurred: {e}")
                continue

    except Exception as e:
        statuses.append((False, f"Failed to initialize RAG Chat: {str(e)}"))
        cli.print_status_box(statuses)
        cli.print_error(f"Error: {e}")

        if missing_vars:
            cli.print_environment_error(missing_vars)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cli = CLIInterface()
        cli.print_info("\nApplication interrupted")
        cli.print_goodbye()
