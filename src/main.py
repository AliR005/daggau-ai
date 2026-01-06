import flet as ft


def main(page: ft.Page):
    page.title = "DAGGAU AI"
    page.theme_mode = ft.ThemeMode.LIGHT

    chat = ft.Column(scroll=ft.ScrollMode.AUTO)
    new_message = ft.TextField(expand=True)

    messages = []

    def send_click(e):
        user_text = new_message.value.strip()
        if not user_text:
            return

        # 1. сохраняем сообщение пользователя
        messages.append({"role": "user", "content": user_text})

        # 2. отображаем в UI
        chat.controls.append(ft.Text(f"User: {user_text}"))

        new_message.value = ""

        # ---- здесь позже будет RAG + LLM ----
        bot_answer = "Ответ бота (заглушка)"

        messages.append({"role": "assistant", "content": bot_answer})
        chat.controls.append(ft.Text(f"AI: {bot_answer}"))

        page.update()

    page.add(
        chat,
        ft.Row(
            controls=[
                new_message,
                ft.Button("Send", on_click=send_click),
            ]
        ),
    )


ft.run(main)
