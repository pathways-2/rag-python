import os
import sys
from typing import Optional, List
from pathlib import Path


class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

    BG_DARK = '\033[48;5;235m'
    BG_DARKER = '\033[48;5;233m'


class Icons:
    CHECK = '✓'
    CROSS = '✗'
    ARROW = '➤'
    DOT = '•'
    STAR = '✭'


class CLIInterface:
    def __init__(self, app_name: str = "RAG Chat"):
        self.app_name = app_name
        self.terminal_width = self._get_terminal_width()

    def _get_terminal_width(self) -> int:
        try:
            return os.get_terminal_size().columns
        except:
            return 80

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_welcome_banner(self):
        banner_text = f"Welcome to {self.app_name} with Vectorize and OpenAI"
        padding = 4
        box_width = len(banner_text) + (padding * 2)

        print(f"\n{Colors.CYAN}{'═' * box_width}{Colors.RESET}")
        print(f"{Colors.CYAN}║{Colors.RESET}{Colors.YELLOW}{' ' * padding}{banner_text}{' ' * padding}{Colors.CYAN}║{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * box_width}{Colors.RESET}\n")

    def print_success(self, message: str):
        print(f"{Colors.GREEN}{Icons.CHECK}{Colors.RESET} {message}")

    def print_error(self, message: str):
        print(f"{Colors.RED}{Icons.CROSS}{Colors.RESET} {message}")

    def print_info(self, message: str):
        print(f"{Colors.CYAN}{Icons.DOT}{Colors.RESET} {message}")

    def print_warning(self, message: str):
        print(f"{Colors.YELLOW}⚠{Colors.RESET}  {message}")

    def print_section_header(self, title: str):
        print(f"\n{Colors.BLUE}{Colors.BOLD}{title}{Colors.RESET}")
        print(f"{Colors.GRAY}{'─' * len(title)}{Colors.RESET}")

    def print_box(self, title: str, items: List[str], color: str = Colors.CYAN):
        max_length = max(len(title), max(len(item)
                         for item in items if items)) + 4

        print(f"\n{color}╭{'─' * (max_length + 2)}╮{Colors.RESET}")
        print(f"{color}│{Colors.RESET} {Colors.BOLD}{title.ljust(max_length)}{Colors.RESET} {color}│{Colors.RESET}")
        print(f"{color}├{'─' * (max_length + 2)}┤{Colors.RESET}")

        for item in items:
            print(
                f"{color}│{Colors.RESET} {item.ljust(max_length)} {color}│{Colors.RESET}")

        print(f"{color}╰{'─' * (max_length + 2)}╯{Colors.RESET}")

    def print_status_box(self, statuses: List[tuple]):
        max_length = max(len(status[1]) for status in statuses) + 10

        print(f"\n{Colors.GRAY}┌{'─' * (max_length + 2)}┐{Colors.RESET}")

        for success, message in statuses:
            icon = f"{Colors.GREEN}{Icons.CHECK}{Colors.RESET}" if success else f"{Colors.RED}{Icons.CROSS}{Colors.RESET}"
            print(
                f"{Colors.GRAY}│{Colors.RESET} {icon} {message.ljust(max_length - 2)} {Colors.GRAY}│{Colors.RESET}")

        print(f"{Colors.GRAY}└{'─' * (max_length + 2)}┘{Colors.RESET}")

    def get_user_input(self, prompt: str = "Your question") -> str:
        print(
            f"\n{Colors.CYAN}{Icons.ARROW}{Colors.RESET} {Colors.BOLD}{prompt}:{Colors.RESET} ", end='')
        return input().strip()

    def print_separator(self, char: str = "─", color: str = Colors.GRAY):
        print(f"{color}{char * self.terminal_width}{Colors.RESET}")

    def print_thinking(self):
        print(f"\n{Colors.YELLOW}{Icons.DOT} Thinking...{Colors.RESET}")

    def print_retrieving(self, query: str):
        print(
            f"\n{Colors.CYAN}{Icons.DOT} Retrieving documents for: {Colors.WHITE}\"{query}\"{Colors.RESET}")

    def print_document_count(self, count: int):
        if count > 0:
            print(
                f"{Colors.GREEN}{Icons.CHECK} Found {count} relevant document{'s' if count != 1 else ''}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}{Icons.DOT} No documents found{Colors.RESET}")

    def print_generating(self):
        print(f"{Colors.CYAN}{Icons.DOT} Generating answer...{Colors.RESET}")

    def print_answer(self, answer: str):
        print(f"\n{Colors.GREEN}{Colors.BOLD}Answer:{Colors.RESET}")
        print(f"{Colors.GRAY}{'─' * 50}{Colors.RESET}")
        print(f"{answer}")
        print(f"{Colors.GRAY}{'─' * 50}{Colors.RESET}")

    def print_exit_instructions(self):
        print(
            f"\n{Colors.GRAY}Type 'quit' or 'exit' to end the session{Colors.RESET}")
        print(f"{Colors.GRAY}Press Ctrl+C to cancel current operation{Colors.RESET}")

    def print_goodbye(self):
        print(
            f"\n{Colors.CYAN}{Icons.STAR} Thank you for using {self.app_name}!{Colors.RESET}")
        print(f"{Colors.GRAY}Goodbye!{Colors.RESET}\n")

    def print_environment_error(self, missing_vars: List[str]):
        self.print_error("Missing required environment variables")
        self.print_box("Required Environment Variables", [
            f"{Colors.RED}{Icons.CROSS}{Colors.RESET} {var}" for var in missing_vars
        ], color=Colors.RED)
        print(
            f"\n{Colors.YELLOW}Please set these variables in your .env file{Colors.RESET}")


class Config:
    APP_NAME = "RAG Chat"
    DEFAULT_NUM_RESULTS = 5
    ENV_VARS = [
        "OPENAI_API_KEY",
        "VECTORIZE_PIPELINE_ACCESS_TOKEN",
        "VECTORIZE_ORGANIZATION_ID",
        "VECTORIZE_PIPELINE_ID"
    ]

    QUIT_COMMANDS = ['quit', 'exit', 'q']

    SYSTEM_PROMPT = (
        "You are a helpful assistant that answers questions based on the provided context. "
        "If the context doesn't contain relevant information, say so."
    )

    USER_PROMPT_TEMPLATE = (
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Please provide a comprehensive answer based on the context above."
    )
