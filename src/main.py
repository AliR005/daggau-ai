import flet as ft


class ChatUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "DAGGAU AI"

        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20

        # Храним сообщения в структуре для будущего RAG-чата
        self.messages = []  # [{"role": "user" | "assistant", "content": str}]

        # Контейнер для сообщений (Column вместо ListView)
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
                            src="data:image/jpeg;base64,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",
                            error_content=ft.Text("🚫"),
                            width=40,
                            height=40,
                        ),
                    ],
                ),
                ft.CupertinoSwitch(
                    value=False,  # False = светлая тема
                    # on_change=self.change_theme,
                    thumb_icon=ft.Icons.WB_SUNNY_SHARP,
                    # thumb_color=ft.Colors.WHITE,
                    # active_track_color=ft.Colors.BLUE_600,
                    # inactive_track_color=ft.Colors.GREY_400,
                    # track_outline_color=ft.Colors.TRANSPARENT,
                    scale=0.9,
                    tooltip="Переключить тему",
                ),
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
        else:  # assistant
            alignment = ft.MainAxisAlignment.START
            bg_color = ft.Colors.AMBER_100  # жёлтый фон для бота
            text_color = ft.Colors.BLACK_87
            prefix = ""

            # Иконка робота слева
            avatar = ft.CircleAvatar(
                content=ft.Icon(ft.Icons.SMART_TOY, color=ft.Colors.AMBER_800),
                bgcolor=ft.Colors.AMBER_200,
                radius=16,
            )

        message_bubble = ft.Container(
            content=ft.Row(
                controls=[
                    avatar
                    if role == "assistant"
                    else ft.Container(),  # аватар только у бота
                    ft.Container(
                        content=ft.Text(
                            f"{prefix}{content}",
                            color=text_color,
                        ),
                        bgcolor=bg_color,
                        padding=12,
                        border_radius=20,
                        expand=True,
                    ),
                    ft.Container(width=32)
                    if role == "assistant"
                    else ft.Container(),  # отступ под аватар
                ],
                alignment=alignment,
            ),
            padding=ft.Padding.only(top=5, bottom=5),
        )

        self.chat_column.controls.append(message_bubble)
        self.page.update()

    def send_message(self, e):
        """Обработчик отправки сообщения пользователем"""
        message = self.input_field.value.strip()
        if not message:
            return

        # Добавляем сообщение пользователя в историю и UI
        self.messages.append({"role": "user", "content": message})
        self.add_message_to_ui("user", message)

        # Очищаем поле ввода
        self.input_field.value = ""
        self.page.update()

        # Заглушка: ответ от бота
        bot_response = "Я получил ваше сообщение и обрабатываю его... Скоро отвечу точно по информации ДагГАУ! 🤖"
        self.messages.append({"role": "assistant", "content": bot_response})
        self.add_message_to_ui("assistant", bot_response)

        # Здесь в будущем будет вызов RAG + LLM

    def change_theme(self, e):
        pass


def main(page: ft.Page):
    ChatUI(page)


if __name__ == "__main__":
    ft.run(main)
