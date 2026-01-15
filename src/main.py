import flet as ft
from llm_handler.llm_api import get_answer_from_ai


class ChatUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "DAGGAU AI"

        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20

        # Храним сообщения в структуре для будущего RAG-чата
        self.messages = []  # [{"role": "user" | "assistant", "content": str}]

        # Контейнер для сообщений
        self.chat_column = ft.Column(
            scroll=ft.ScrollMode.AUTO, expand=True, spacing=10, auto_scroll=True
        )
        # Приветственное сообщение от бота при запуске
        welcome_message = (
            "Привет! 👋 Я — DAGGAU AI, твой помощник по вопросам поступления и учёбы "
            "в Дагестанском государственном аграрном университете.\n\n"
            "Задавай любой вопрос — отвечу точно и по делу! 🚀"
        )

        self.messages.append({"role": "assistant", "content": welcome_message})
        self.add_message_to_ui("assistant", welcome_message)

        self.input_field = ft.TextField(
            expand=True,
            hint_text="Введите сообщение...",
            border_radius=30,
            on_submit=self.send_message,
        )

        self.send_button = ft.IconButton(
            icon=ft.Icons.SEND_ROUNDED,
            on_click=self.send_message,
            tooltip="Отправить",
        )

        self._build_layout()

    def _build_layout(self):
        # Заголовок

        title = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "DAGGAU AI",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Image(
                            src="images/logo.png",
                            error_content=ft.Text("🚫"),
                            width=40,
                            height=40,
                        ),
                    ],
                ),
                # ft.CupertinoSwitch(
                #     value=False,  # False = светлая тема
                #     # on_change=self.change_theme,
                #     thumb_icon=ft.Icons.WB_SUNNY_SHARP,
                #     # thumb_color=ft.Colors.WHITE,
                #     # active_track_color=ft.Colors.BLUE_600,
                #     # inactive_track_color=ft.Colors.GREY_400,
                #     # track_outline_color=ft.Colors.TRANSPARENT,
                #     scale=0.9,
                #     tooltip="Переключить тему",
                # ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=10,
        )

        # Контейнер с сообщениями
        self.messages_container = ft.Container(
            content=self.chat_column,
            expand=True,
            bgcolor=ft.Colors.GREY_100,
            border_radius=10,
            padding=10,
        )

        # Панель ввода
        input_row = ft.Row(
            controls=[self.input_field, self.send_button],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Основная колонка
        main_column = ft.Column(
            controls=[title, self.messages_container, input_row],
            expand=True,
            spacing=15,
        )

        self.page.add(main_column)

    def add_message_to_ui(self, role: str, content: str):
        """Добавляет сообщение в интерфейс в зависимости от роли"""
        if role == "user":
            alignment = ft.MainAxisAlignment.END
            bg_color = ft.Colors.BLUE_100
            text_color = ft.Colors.BLUE_900
            prefix = "Вы: "
            message_content = ft.Text(
                f"{prefix}{content}",
                color=text_color,
                selectable=True,
            )
            avatar = None
        else:  # assistant
            alignment = ft.MainAxisAlignment.START
            bg_color = ft.Colors.AMBER_100
            text_color = ft.Colors.BLACK_87
            prefix = ""
            # Markdown для бота
            message_content = ft.Markdown(
                f"{prefix}{content}",
                selectable=True,  # чтобы можно было копировать
                extension_set="commonmark",
            )
            # Иконка робота слева
            avatar = ft.CircleAvatar(
                content=ft.Icon(ft.Icons.SMART_TOY, color=ft.Colors.AMBER_800),
                bgcolor=ft.Colors.AMBER_200,
                radius=16,
            )

        message_bubble = ft.Container(
            content=ft.Row(
                controls=[
                    avatar if role == "assistant" else ft.Container(width=32),
                    ft.Container(
                        content=message_content,
                        bgcolor=bg_color,
                        padding=12,
                        border_radius=20,
                        expand=True,
                    ),
                    ft.Container(width=32) if role == "assistant" else ft.Container(),
                ],
                alignment=alignment,
            ),
            padding=ft.Padding.only(top=5, bottom=5),
        )

        self.chat_column.controls.append(message_bubble)
        self.page.update()

    def send_message(self, e):
        message = self.input_field.value.strip()
        if not message:
            return

        # 1. Добавляем сообщение пользователя
        self.messages.append({"role": "user", "content": message})
        self.add_message_to_ui("user", message)

        self.input_field.value = ""
        self.page.update()

        # 2. Запуск анимации загрузки
        self.add_loading_message()

        # 3. Запускаем LLM в фоне
        self.page.run_thread(self._get_ai_response)

    def _get_ai_response(self):
        bot_response = get_answer_from_ai(self.messages)
        self.remove_loading_message()
        self.messages.append({"role": "assistant", "content": bot_response})
        self.add_message_to_ui("assistant", bot_response)
        self.page.update()

    def add_loading_message(self):
        """Добавляет сообщение бота с анимацией загрузки"""
        self.loader = ft.ProgressRing(width=20, height=20, color=ft.Colors.BLUE)

        self.loading_bubble = ft.Container(
            content=ft.Row(
                controls=[
                    ft.CircleAvatar(
                        content=ft.Icon(ft.Icons.SMART_TOY, color=ft.Colors.AMBER_800),
                        bgcolor=ft.Colors.AMBER_200,
                        radius=16,
                    ),
                    ft.Container(
                        content=self.loader,
                        bgcolor=ft.Colors.AMBER_100,
                        padding=12,
                        border_radius=20,
                        width=50,
                        height=50,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=8,
            ),
            padding=ft.Padding.only(top=5, bottom=5),
        )

        # добавляем в колонку чата
        self.chat_column.controls.append(self.loading_bubble)
        self.page.update()

    def remove_loading_message(self):
        """Удаляет сообщение загрузки"""
        if (
            hasattr(self, "loading_bubble")
            and self.loading_bubble in self.chat_column.controls
        ):
            self.chat_column.controls.remove(self.loading_bubble)
            self.page.update()


def main(page: ft.Page):
    ChatUI(page)


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
