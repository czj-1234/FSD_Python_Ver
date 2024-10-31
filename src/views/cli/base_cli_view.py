from typing import List, Any

from src.views.base_view import BaseView


class BaseCliView(BaseView):
    """Base class for CLI views providing common display functionality."""
    # 提供通用显示功能的CLI视图的基类。

    def display(self, data: Any = None):
        """Default display implementation."""
        # 默认显示实现。
        pass

    def display_header(self, title: str):
        """Display a header with title."""
        #默认显示实现。
        print(f"\n{title}")

    def display_error(self, message: str):
        """Display an error message."""
        print(f"Error: {message}")

    def display_success(self, message: str):
        """Display a success message."""
        print(f"Success: {message}")

    def display_menu(self, options: List[tuple]):
        """Display a menu with options."""
        # 显示带有选项的菜单。
        for code, description in options:
            print(f"({code}) {description}")

    def get_input(self, prompt: str) -> str:
        """Get user input with prompt."""
        # 使用提示符获取用户输入。
        return input(f"{prompt}: ").strip()

    def confirm_action(self, message: str) -> bool:
        """Get user confirmation."""
        # 获取用户确认。
        response = input(f"{message} (y/n): ").strip().lower()
        return response == 'y'

    def display_table(self, headers: List[str], rows: List[List[Any]], widths: List[int]):
        """Display data in tabular format."""
        # 以表格格式显示数据。
        header_format = " ".join("{:<" + str(w) + "}" for w in widths)
        print(header_format.format(*headers))
        print("-" * sum(widths))
        row_format = " ".join("{:<" + str(w) + "}" for w in widths)
        for row in rows:
            print(row_format.format(*row))
