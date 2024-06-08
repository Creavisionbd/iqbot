import flet as ft

def main(page):
    def slider_changed(e):
        t.value = e.control.value

    t = ft.Text()

    def get_rsi_slider_value(e):
        print(f"Slider value: {t.value}")

    bt = ft.TextButton("Click me", on_click=get_rsi_slider_value)

    page.add(
        ft.Text("Slider with 'on_change' event:"),
        ft.Slider(value=10, min=0, max=100, divisions=10, label="{value}%", on_change=slider_changed),
        t,
        bt
    )

ft.app(target=main)