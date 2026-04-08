from .menu import run_main_menu


def main() -> None:
    run_main_menu([
        {"name": "Player 1", "score": 10000},
        {"name": "Player 2", "score": 9000},
        {"name": "Player 3", "score": 8000},
        {"name": "Player 4", "score": 7000},
        {"name": "Player 5", "score": 6000},
        {"name": "Player 6", "score": 5000},
        {"name": "Player 7", "score": 4000},
        {"name": "Player 8", "score": 4000},
        {"name": "Player 9", "score": 3000},
        {"name": "Player 10", "score": 2000},
    ])


if __name__ == "__main__":
    main()
