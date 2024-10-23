import sys
from pathlib import Path


def setup_environment():
    """Set up the environment for the application."""
    # Add project root to Python path
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # Database file will be created in project root
    return project_root  # 直接返回项目根目录


def main():
    """Main entry point for the Flet GUI application."""
    try:
        import flet as ft
        from src.views.flet_ui.app_view import AppView
        from src.models.database import Database

        database_file = setup_environment()
        Database.DEFAULT_PATH = str(database_file)  # Set the database path

        def app_view(page: ft.Page):
            app = AppView(page)
            app.initialize()

        ft.app(target=app_view)
        return 0

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())