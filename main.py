import os
import warnings
from pathlib import Path
from dotenv import load_dotenv
from rag_chat import RAGChat
from cli_interface import CLIInterface, Config, Colors
from rag_source_base import RAGSourceType, RAGSourceBase
from vectorize_wrapper import VectorizeWrapper
from pinecone_wrapper import PineconeWrapper

# This is just to suppress warnings in our terminal
warnings.filterwarnings("ignore", message="Pydantic serializer warnings")

RAG_SOURCE = RAGSourceType.VECTORIZE


def load_environment():
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        return True, "Environment variables loaded from .env file"
    else:
        return False, "No .env file found, using system environment variables"


def get_rag_source() -> tuple[RAGSourceBase | None, list[str]]:
    """
    Create and return the appropriate RAG source based on configuration.
    Returns tuple of (rag_source, required_env_vars)
    """
    if RAG_SOURCE == RAGSourceType.NONE:
        return None, []
    elif RAG_SOURCE == RAGSourceType.VECTORIZE:
        wrapper = VectorizeWrapper()
        return wrapper, wrapper.get_required_env_vars()
    elif RAG_SOURCE == RAGSourceType.PINECONE:
        wrapper = PineconeWrapper()
        return wrapper, wrapper.get_required_env_vars()
    else:
        raise ValueError(f"Unknown RAG source type: {RAG_SOURCE}")


def check_environment_variables(rag_source_vars: list[str]) -> list[str]:
    missing_vars = []

    core_vars = ["OPENAI_API_KEY"]
    for var in core_vars:
        if not os.environ.get(var):
            missing_vars.append(var)

    for var in rag_source_vars:
        if not os.environ.get(var):
            missing_vars.append(var)

    return missing_vars


def main():
    app_name_suffix = {
        RAGSourceType.NONE: "",
        RAGSourceType.VECTORIZE: " with Vectorize",
        RAGSourceType.PINECONE: " with Pinecone"
    }
    app_name = Config.APP_NAME + app_name_suffix.get(RAG_SOURCE, "")
    cli = CLIInterface(app_name)

    cli.clear_screen()
    cli.print_welcome_banner()

    env_loaded, env_message = load_environment()

    statuses = []
    statuses.append((env_loaded, env_message))

    try:
        rag_source_instance, required_vars = get_rag_source()
    except Exception as e:
        statuses.append((False, f"Failed to initialize RAG source: {str(e)}"))
        cli.print_status_box(statuses)
        return

    missing_vars = check_environment_variables(required_vars)
    if missing_vars:
        statuses.append((False, "Missing required environment variables"))
        cli.print_status_box(statuses)
        cli.print_environment_error(missing_vars)
        return
    else:
        statuses.append((True, "All environment variables configured"))

    try:
        rag = RAGChat(cli, rag_source=rag_source_instance)
        statuses.append((True, "RAG Chat initialized successfully"))

        if RAG_SOURCE == RAGSourceType.VECTORIZE:
            statuses.append((True, "Connected to Vectorize and OpenAI"))
        elif RAG_SOURCE == RAGSourceType.PINECONE:
            statuses.append((True, "Connected to Pinecone and OpenAI"))
        else:
            statuses.append((True, "Connected to OpenAI"))

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
