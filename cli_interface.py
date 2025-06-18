import os
import sys
import time
import threading
from typing import Optional, List, Any
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


class LoadingAnimation:
    def __init__(self, message: str, color: str = Colors.CYAN):
        self.message = message
        self.color = color
        self.is_running = False
        self.thread = None
        self.frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.current_frame = 0

    def _animate(self):
        while self.is_running:
            frame = self.frames[self.current_frame]
            sys.stdout.write(
                f'\r{self.color}{frame} {self.message}{Colors.RESET}')
            sys.stdout.flush()
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            time.sleep(0.1)

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write('\r' + ' ' * (len(self.message) + 4) + '\r')
        sys.stdout.flush()


class CLIInterface:
    def __init__(self, app_name: str = "RAG Chat"):
        self.app_name = app_name
        self.terminal_width = self._get_terminal_width()
        self.current_loading = None

    def _get_terminal_width(self) -> int:
        try:
            return os.get_terminal_size().columns
        except:
            return 80

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_welcome_banner(self):
        banner_text = f"Welcome to {self.app_name}"
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

    def start_loading(self, message: str):
        self.current_loading = LoadingAnimation(message)
        self.current_loading.start()

    def stop_loading(self):
        if self.current_loading:
            self.current_loading.stop()
            self.current_loading = None

    def print_retrieving(self, query: str):
        print(
            f"\n{Colors.CYAN}{Icons.DOT} Retrieving documents for: {Colors.WHITE}\"{query}\"{Colors.RESET}")
        self.start_loading("Searching knowledge base...")

    def print_documents_with_snippets(self, documents: List[Any]):
        self.stop_loading()

        if not documents:
            print(f"{Colors.YELLOW}{Icons.DOT} No documents found{Colors.RESET}")
            return

        count = len(documents)
        print(f"\n{Colors.GREEN}{Icons.CHECK} Found {count} relevant document{'s' if count != 1 else ''}{Colors.RESET}")

        print(f"\n{Colors.GRAY}{'─' * 60}{Colors.RESET}")

        for i, doc in enumerate(documents[:5], 1):
            snippet = ""
            source = ""
            score = ""

            if hasattr(doc, 'text') and doc.text:
                snippet = doc.text[:120].strip()
                if len(doc.text) > 120:
                    snippet += "..."
            elif isinstance(doc, dict) and 'text' in doc:
                snippet = doc['text'][:120].strip()
                if len(doc['text']) > 120:
                    snippet += "..."

            if hasattr(doc, 'source_display_name') and doc.source_display_name:
                source = doc.source_display_name
            elif isinstance(doc, dict) and 'source_display_name' in doc:
                source = doc['source_display_name']

            if hasattr(doc, 'relevancy') and doc.relevancy:
                score = f"{doc.relevancy:.2f}"
            elif isinstance(doc, dict) and 'relevancy' in doc:
                score = f"{doc['relevancy']:.2f}"

            print(f"{Colors.BLUE}{Colors.BOLD}[{i}]{Colors.RESET} ", end='')

            if source:
                print(f"{Colors.GREEN}{source}{Colors.RESET}", end='')

            if score:
                print(f" {Colors.GRAY}(relevance: {score}){Colors.RESET}")
            else:
                print()

            if snippet:
                print(f"    {Colors.DIM}{snippet}{Colors.RESET}")

            if i < min(5, count):
                print(f"{Colors.GRAY}{'─' * 60}{Colors.RESET}")

        print()

    def print_generating(self):
        self.start_loading("Generating answer...")

    def print_answer(self, answer: str):
        self.stop_loading()
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
