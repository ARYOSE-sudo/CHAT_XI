from flet import *
from socket import *

# socket client
client = socket(AF_INET, SOCK_STREAM)
client.connect(('192.168.5.11', 8080))  # بدّل IP ديالك هنا

def main(page: Page):
    page.window.width = page.window.width  # مرونة العرض حسب الشاشة
    page.window.height = page.window.height  # مرونة الارتفاع حسب الشاشة
    page.window.top = 0
    page.window.left = 0
    page.window.title_bar_hidden = True

    messages = Column(scroll="auto")
    msg_field = TextField(
        hint_text="Votre message",
        border_color=colors.WHITE,
        bgcolor=colors.WHITE,
        border_radius=20,
        width=page.window.width * 0.75,  # مرونة مع العرض
        height=40,
        color="black"
    )

    def send_message(e):
        msg = msg_field.value.strip()
        if msg != "":
            try:
                # إرسال رسالة
                messages.controls.append(
                    Row(
                        alignment="end",
                        controls=[Container(
                            content=Text(msg, color="black", size=14),
                            bgcolor="#00FFFF",
                            padding=10,
                            border_radius=20,
                            margin=5
                        )]
                    )
                )
                client.send(msg.encode())
                msg_field.value = ""
                page.update()

                # استلام الرد من السيرفر
                data = client.recv(1024).decode()
                messages.controls.append(
                    Row(
                        alignment="start",
                        controls=[Container(
                            content=Text(data, color="white", size=14),
                            bgcolor="#222222",
                            padding=10,
                            border_radius=20,
                            margin=5
                        )]
                    )
                )
                page.update()
            except Exception as err:
                messages.controls.append(Text(f"❌ Erreur: {err}", color="red"))
                page.update()

    def chat(_):
        page.views.append(
            View(
                "/chat",
                bgcolor=colors.BLACK,
                controls=[
                    Stack([
                        Column(
                            controls=[
                                Container(
                                    content=messages,
                                    height=page.window.height * 0.75,  # مرونة مع ارتفاع الشاشة
                                    padding=10
                                ),
                                Container(
                                    width=page.window.width,
                                    height=60,
                                    bgcolor=colors.BLACK,
                                    content=Row(
                                        controls=[
                                            msg_field,
                                            IconButton(
                                                icon=icons.ARROW_UPWARD,
                                                icon_color="black",
                                                bgcolor="#8c03fc",
                                                on_click=send_message
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    ])
                ]
            )
        )
        page.update()

    def one_page(_):
        page.views.append(
            View(
                "/",
                bgcolor=colors.BLACK,
                padding=0,
                controls=[
                    Stack([
                        Image(
                            src="https://i.pinimg.com/736x/5c/b1/f7/5cb1f73d27ca03b747c94ee2f25b9351.jpg",
                            fit=ImageFit.COVER,
                            width=page.window.width,
                            height=page.window.height,
                        ),
                        ElevatedButton(
                            content=Text("ENTER", color="white", size=20, weight=FontWeight.W_500),
                            width=120,  # حجم زر أكبر لسهولة التفاعل
                            height=45,
                            bgcolor="#8c03fc",
                            style=ButtonStyle(
                                shape=ContinuousRectangleBorder(radius=10),
                                shadow_color="#00FFFF"
                            ),
                            top=page.window.height * 0.8,  # مرونة مع ارتفاع الشاشة
                            left=page.window.width * 0.65,  # مرونة مع عرض الشاشة
                            on_click=chat
                        )
                    ])
                ]
            )
        )
        page.update()

    page.on_route_change = one_page
    page.go("/")

app(target=main)
