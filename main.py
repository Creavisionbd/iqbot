import flet as ft
from iqoptionapi.stable_api import IQ_Option
import shutil
from flet import *
import json
import pickle
import time
import math
import sys
with open('requirements.txt', 'r') as file:
    function_code = file.read()
exec(function_code)

result = MyContainer()
print(result)
import os
# Add the directory containing the file to the Python path
strategy_path = os.path.abspath("C:/tradebakery")
print(f"Adding {strategy_path} to sys.path")
sys.path.append(strategy_path)
total_win=0
total_loss=0
# Now you can try to import the Mycontainer class from the strategy module
try:
    from strategy import MyContainer
    from strategy import trade_strategy_logic
    from strategy import trade_strategy
    print("Import successful")
except ImportError as e:
    from strategy1 import MyContainer
    from strategy1 import trade_strategy_logic
    from strategy1 import trade_strategy
    print(f"ImportError: {e}")
def main(page: ft.Page):
    # Create the 3 containers
    global keep_running
    keep_running = False
    container=result
    page.window_height = 600,
    page.window_width = 1000,
    page.window_min_width, page.window_max_width = 1000,1000
    page.window_min_height, page.window_max_height = 600,600
    page.window_resizable = False
    page.theme_mode = ft.ThemeMode.DARK # window is not resizable
    page.update(),
    
    
    def close_banner(e):
        page.banner.open = False
        page.update()

    banner= ft.Banner(
        bgcolor=ft.colors.BLACK,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.BLACK, size=40),
        content=ft.Text(
            "Oops, there were some errors while trying to delete the file. What would you like me to do?",color=ft.colors.WHITE
        ),
        actions=[
            
            ft.TextButton("Cancel", on_click=close_banner),
        ],
    )
    page.banner=banner
    def audio_play():
        audio = ft.Audio(src="alarm.wav", autoplay=True)
        page.overlay.append(audio)
    
    def show_banner_click(e):
        page.banner.open = True
        page.update()
    acc_balance=ft.Row(
        controls=[
                ft.Text(
                    "Balance",
                    size=20,
                    font_family="Montserrat",
                    weight=ft.FontWeight.W_900,
                    text_align=ft.TextAlign.CENTER,
                    color="#FFFFFF"
                ),
                ft.Text(
                    "223",
                    size=18,
                    font_family="Platypi",
                    weight=ft.FontWeight.W_900,
                    text_align=ft.TextAlign.CENTER,
                    color="#FFFFFF"
                ),
        ],
        height=50,
        width=150,
        
    )
    
    #  file upload
    youlocation_file =ft.Text(""),

	# CREATE FUNCTION OPEN FILE
    	# CREATE FUNCTION OPEN FILE
    def dialog_picker(e:FilePickerResultEvent):
        directory = "C:/tradebakery"
        if os.path.exists(directory):
            print("Directory already exists")
            for x in e.files:
                shutil.copy(x.name,f"C:/tradebakery/strategy.py")
                page.update()
            global trade_strategy
            from strategy1 import trade_strategy
            open_dlg_modal_restart(e)
            time.sleep(10)
            e.page.window_destroy()
        else:
            os.makedirs(directory)
            print("Directory created successfully")
            for x in e.files:
                shutil.copy(x.name,f"C:/tradebakery/strategy.py")
                page.update()
            global trade_strategy
            from strategy1 import trade_strategy
            open_dlg_modal_restart(e)
            time.sleep(10)
            e.page.window_destroy()
            
    Mypick=FilePicker(on_result=dialog_picker)
    page.overlay.append(Mypick)
    # Login Function
    ab=ft.Column(
            [   
                ft.TextField(label="Your Email",color="#FFFFFF"),
                ft.TextField(label="Your Password",color="#FFFFFF")
            ],
            height=200,
            width=250
        )
    restart=ft.Container(bgcolor=ft.colors.BLACK,content=ft.Column(
        [
            ft.Container( alignment=ft.alignment.center,content=ft.Image("rotating.gif",height=150,width=150)),
            ft.Text(
                "         We are updating, please run app again after restart",
                size=14,
                font_family="Montserrat",
                weight=ft.FontWeight.W_900,
                # text_align=ft.TextAlign.CENTER,
                color="#d9113a"
            ),
        ],
        ft.MainAxisAlignment.CENTER,
        
        ),
        height=250,
        width=450,
        alignment=ft.alignment.center,

    )
    def close_dlg(e):
        dlg_modal.open = False
        page.update()
    def close_dlg_dance(e):
        dlg_modal_dance.open = False
        page.update()
    def close_restart(e):
        dlg_modal_restart.open = False
        page.update()
    def close_dlg_backtesting(e):
        dlg_modal_backtesting.open = False
        page.update()
    def close_dlg_backtesting_report(e):
        dlg_modal_backtesting_report.open=False
        page.update()
    def login(e):
        email=ab.controls[0].value
        password=ab.controls[1].value
        print(dropdown)
        global I_want_money
        open_dlg_modal_dance(e)
        I_want_money=IQ_Option(email,password)
        I_want_money.connect()#connect to iqoption
        if I_want_money.connect()[0]==True:
            bal=I_want_money.get_balance()
            print(acc_balance.controls[1].value)
            acc_balance.controls[1].value=int(bal)
            close_dlg_dance(e)
            dlg_modal.open = False
            page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm",color="#FFFFFF"),
        content=ab,
        actions=[
            ft.ElevatedButton(text="Login",color=ft.colors.WHITE,on_click=login),
            ft.ElevatedButton(text="Close",color=ft.colors.WHITE,on_click=close_dlg),
            
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor=ft.colors.BLACK87,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
    dlg_modal_restart = ft.AlertDialog(
        modal=True,
        title=ft.Text("We are restarting App",color="#FFFFFF"),
        content=restart,
        actions=[
            
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor=ft.colors.BLACK,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
    dlg_modal_dance = ft.AlertDialog(
        modal=True,
        title=ft.Text("Loading.....",color="#FFFFFF"),
        content=ft.Row(
            [
                ft.Image("loading.gif"),
                # ft.Audio(
                #     src="kala.mp3", autoplay=True
                # )
            ]
        ),
        actions=[
           
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor=ft.colors.BLACK,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
    dlg_modal_backtesting= ft.AlertDialog(
        modal=True,
        title=ft.Text("Backing.....",color="#d9113a"),
        actions=[
            ft.Text(""),
            ft.ElevatedButton(text="Close",color=ft.colors.WHITE,on_click=close_dlg_backtesting,bgcolor="#d9113a"),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        bgcolor=ft.colors.BLACK87,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
    dlg_modal_backtesting_report= ft.AlertDialog(
        modal=True,
        title=ft.Text("Loading.....",color="#FFFFFF"),
        actions=[
            ft.Text(""),
            ft.ElevatedButton(text="Close",color=ft.colors.WHITE,on_click=close_dlg_backtesting_report),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        bgcolor=ft.colors.BLACK87,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    
    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()
    def open_dlg_modal_restart(e):
        page.dialog = dlg_modal_restart
        dlg_modal_restart.open = True
        page.update()
    def open_dlg_modal_dance(e):
        page.dialog = dlg_modal_dance
        dlg_modal_dance.open = True
        page.update()
    def open_dlg_modal_backtesting(e):
        page.dialog = dlg_modal_backtesting
        dlg_modal_backtesting.open = True
        page.update()
    def open_dlg_modal_backtesting_report(e):
        page.dialog = dlg_modal_backtesting_report
        dlg_modal_backtesting_report.open = True
        page.update()
    def trade(e):
        print(trade_multi.controls[1].value)
        print(trade_amount.value)
        print(trade_time.controls[1].value)
        print(account_type.content.content.controls[0].value)
        trade_times=1
        amount=int(trade_amount.value)
        bal=int(I_want_money.get_balance())
        win=win_control.content.content.content.controls[4].value
        target=bal+int(win)
        loss=win_control.content.content.content.controls[5].value
        Stop_loss=bal-int(loss)
        print(bal,target,Stop_loss)
        switch_signal=container2.content.controls[0].value
        print(switch_signal)
        global keep_running
        keep_running = True
        while keep_running:
            rslt=trade_strategy(I_want_money,amount,trade_times,switch_signal)
            if rslt!=None:
                signal.controls[0].content.content.controls[0].value=rslt[0]
                if rslt[1]=="call":
                    signal.controls[0].content.content.controls[1].content.src="up-arrow.png"
                    audio_play()
                    t_end = time.time() + 60 * 1.2
                    start_time = time.time()
                    while time.time() < t_end:
                        elapsed_time = time.time() - start_time
                        signal.controls[0].content.content.controls[2].value="Time Spent: "+str(int(elapsed_time))+"sec"
                        page.update()

                else:
                    signal.controls[0].content.content.controls[1].content.src="down.png"
                    audio_play()
                    t_end = time.time() + 60 * 1.2
                    start_time = time.time()
                    while time.time() < t_end:
                        elapsed_time = time.time() - start_time
                        signal.controls[0].content.content.controls[2].value="Time Spent: "+str(int(elapsed_time))+"sec"
                        page.update()
                  
                page.update()
           
            bal=int(I_want_money.get_balance())
            if bal > target or bal<Stop_loss:
                break
         

    def stop(e):
        global keep_running
        keep_running = False
    def marketplace(e):
        # print(signal.controls[0].content.content.controls)
        container=MyContainer()
        print(container.get_bollinger_band_period_value())
       

    normal_radius = 50
    hover_radius = 60
    normal_title_style = ft.TextStyle(
    size=12, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
    )
    hover_title_style = ft.TextStyle(
    size=12,
    color=ft.colors.WHITE,
    weight=ft.FontWeight.BOLD,
    shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
    )
    

    def on_chart_event(e: ft.PieChartEvent):
        for idx, section in enumerate(chart.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        chart.update()
    def on_chart_event_timezone(e: ft.PieChartEvent):
        for idx, section in enumerate(chart_timezone.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        chart_timezone.update()

    chart=ft.PieChart(
            sections=[
            ft.PieChartSection(
            40,
            title="40%",
            title_style=normal_title_style,
            color=ft.colors.BLUE,
            radius=normal_radius,
            ),
                    ft.PieChartSection(
            40,
            title="40%",
            title_style=normal_title_style,
            color="#d9113a",
            radius=normal_radius,
            ),
                    ft.PieChartSection(
            40,
            title="40%",
            title_style=normal_title_style,
            color="#fecf00",
            radius=normal_radius,
            ),                             
            ],
            sections_space=0,
            center_space_radius=40,
            on_chart_event=on_chart_event,
            expand=True,
        )
    chart_timezone=ft.PieChart(
            sections=[
            ft.PieChartSection(
            40,
            title="40%",
            title_style=normal_title_style,
            color=ft.colors.BLUE,
            radius=normal_radius,
            ),
                    ft.PieChartSection(
            40,
            title="40%",
            title_style=normal_title_style,
            color="#d9113a",
            radius=normal_radius,
            ),
                    ft.PieChartSection(
            40,
            title="40%",
            title_style=normal_title_style,
            color="#fecf00",
            radius=normal_radius,
            ),                             
            ],
            sections_space=0,
            center_space_radius=40,
            on_chart_event=on_chart_event_timezone,
            expand=True,
        )
    report_summary=ft.Card(
                        height=180,
                        width=300,
                        color="#3d3d3d",
                        content=ft.Column(
                            [   
                                ft.Container(content=ft.Row(
                                    [
                                    ft.Image("win.png",width=20,height=20),
                                    ft.Text(
                                        "you just won 34 dollar",
                                        size=10,
                                        font_family="Platypi",
                                        weight=ft.FontWeight.W_900,
                                        text_align=ft.TextAlign.CENTER,
                                        color="#FFFFFF"
                                    ),
                                    ],
                                    
                                ),
                                padding=ft.padding.all(10)
                                ),
                                 ft.Container(content=ft.Row(
                                    [
                                    ft.Image("time.png",width=20,height=20),
                                    ft.Text(
                                        "you just won 34 dollar",
                                        size=10,
                                        font_family="Platypi",
                                        weight=ft.FontWeight.W_900,
                                        text_align=ft.TextAlign.CENTER,
                                        color="#FFFFFF"
                                    ),
                                    ],
                                    
                                ),
                                padding=ft.padding.all(10)
                                ),
                                 ft.Container(content=ft.Row(
                                    [
                                    ft.Image("zone.png",width=20,height=20),
                                    ft.Text(
                                        "you just won 34 dollar",
                                        size=10,
                                        font_family="Platypi",
                                        weight=ft.FontWeight.W_900,
                                        text_align=ft.TextAlign.CENTER,
                                        color="#FFFFFF"
                                    ),
                                    ],
                                    
                                ),
                                padding=ft.padding.all(10)
                                )
                                
                            ]
                        )
                       
                )

    backtecting_report=ft.Container(
            height=700,
            width=800,
            content=ft.Column(
                [   
                    ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Container(
                                height=190,
                                width=370,
                                content=ft.Column(
                                [
                                ft.Text("                    Win Lose Rate",color="#FFFFFF"),
                                
                                ft.BarChart(
                                    bar_groups=[
                                        ft.BarChartGroup(
                                            x=0,
                                            bar_rods=[
                                            ft.BarChartRod(
                                                from_y=0,
                                                to_y=100,
                                                width=40,
                                                color=ft.colors.BLUE,
                                                tooltip="Lose",
                                                border_radius=10,
                        
                                            ),
                                            ],
                                        ),
                                        ft.BarChartGroup(
                                            x=1,
                                            bar_rods=[
                                            ft.BarChartRod(
                                                from_y=0,
                                                to_y=100,
                                                width=40,
                                                color="#d9113a",
                                                tooltip="Lose",
                                                border_radius=10,
                                            ),
                                            ],
                                        ),
                                    
                                    ],
                                    # border=ft.border.all(1, ft.colors.GREY_400),
                                    
                                    bottom_axis=ft.ChartAxis(
                                        labels=[
                                            ft.ChartAxisLabel(
                                                value=0, label=ft.Container(ft.Text("Win"), padding=10)
                                            ),
                                            ft.ChartAxisLabel(
                                                value=1, label=ft.Container(ft.Text("Lose"), padding=10)
                                            ),

                                        ],
                                        labels_size=40,
                                    ),
                                
                                    tooltip_bgcolor=ft.colors.WHITE,
                                    
                                    max_y=110,
                                    interactive=True,
                                    expand=True,
                                )],ft.MainAxisAlignment.CENTER
                                )
                            ),
                            ]
                        ),
                        ft.Container(
                            height=190,
                            width=370,
                            content=ft.Column(
                                [
                                    ft.Text("                             Win in Timezone",color="#FFFFFF"),
                                    ft.Text(""),
                                    chart
                                ],
                                ft.MainAxisAlignment.CENTER
                            )
                        )
                    ]
                    
                    ),
                    ft.Text(""),
                    ft.Row(
                    [
                        ft.Container(
                            height=190,
                            width=370,
                            content=report_summary
                            
                        ),
                        ft.Container(
                            height=190,
                            width=370,
                            content=ft.Column(
                                [
                                    ft.Text("                             Best Timezone",color="#FFFFFF"),
                                    ft.Text(""),
                                    chart_timezone
                                ],
                                ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        )
                    ]
                    )
                ]
            )
            )
    
    back_test_loading=ft.Container(
                height=600,
                width=800,
                bgcolor=ft.colors.BLACK,
                content=ft.Row((
                    [ft.Image(src="technology.gif",height=300,width=400),
                      ft.Text(
                        "I am doing....",
                        size=15,
                        font_family="Montserrat",
                        weight=ft.FontWeight.W_900,
                        text_align=ft.TextAlign.CENTER,
                        color="#d9113a"
                    ),
                    ]
                ))
            )

    def back_test(e):
        dlg_modal_backtesting.content=back_test_loading
        open_dlg_modal_backtesting(e)
        print(dlg_modal_backtesting.title.value)
       
        
        if I_want_money.connect()[0]==True:
            result=trade_strategy_logic(I_want_money)
            print(result)
            print((result[0]/(result[0]+result[1]))*100)
            if result !=None:
                # dlg_modal_backtesting_report.title.value="Backed"
                print("okay again")
                dlg_modal_backtesting_report.content=backtecting_report
                backtecting_report.content.controls[0].controls[0].controls[0].content.controls[1].bar_groups[0].bar_rods[0].to_y=(result[0]/(result[0]+result[1]))*100
                backtecting_report.content.controls[0].controls[0].controls[0].content.controls[1].bar_groups[0].bar_rods[0].tooltip=str(int((result[0]/(result[0]+result[1]))*100))+str("%")
                backtecting_report.content.controls[0].controls[0].controls[0].content.controls[1].bar_groups[1].bar_rods[0].to_y=(result[1]/(result[0]+result[1]))*100
                backtecting_report.content.controls[0].controls[0].controls[0].content.controls[1].bar_groups[1].bar_rods[0].tooltip=str(int((result[1]/(result[0]+result[1]))*100))+str("%")
                chart.sections[0].value=result[2]
                chart.sections[0].title="new york session"+str(result[2])
                chart.sections[1].value=result[3]
                chart.sections[1].title="London session"+str(result[3])
                chart.sections[2].value=result[4]
                chart.sections[2].title="Asian session"+str(result[4])
                chart_timezone.sections[0].value=result[0]
                chart_timezone.sections[0].title="5m Trade"+str(result[0])
                chart_timezone.sections[1].value=result[5]
                chart_timezone.sections[1].title="3m Trade"+str(result[5])
                chart_timezone.sections[2].value=result[6]
                chart_timezone.sections[2].title="3m Trade"+str(result[6])
                report_summary.content.controls[0].content.controls[1].value="You won "+str(result[0])+" and lose "+str(result[1])+" trade"
                report_summary.content.controls[1].content.controls[1].value=str(result[0])+" win in 5min trade "+str(result[5])+" win in 3min trade\n"+str(result[6])+" win in 1min trade"
                report_summary.content.controls[2].content.controls[1].value="Newyork session "+str(result[2])+" London session ]\n"+str(result[3])+" Asian session "+str(result[4])
                open_dlg_modal_backtesting_report(e)
                page.update()
                    
        else:
            dlg_modal_backtesting.title.value="Please Login"
            page.update()

    def signal_trade(e):
        print(signal.controls[0].content.n)
            

       
    container1=ft.Container(
                    height=550,
                    width=280,
                    bgcolor="#fecf00",
                    border_radius=ft.border_radius.all(10),
                    # bgcolor=ft.colors.AMBER,
                    padding=ft.padding.all(10),
                    content=ft.Column(controls=[
                    ElevatedButton("Back Testing",
                                   on_click=back_test,bgcolor="#d9113a",color="#ffffff"
                                       
                                            ),
                    ft.Container(
                            height=400,
                            width=280,
                            content=container
                    ),
                    ft.Container(
                        content=ft.Row([
                            ElevatedButton("Insert file",
                                on_click=lambda _: Mypick.pick_files(),bgcolor="#d9113a",color="#ffffff"
                            ),
                            ElevatedButton("Marketplace",
                                on_click=marketplace,bgcolor="#d9113a",color="#ffffff"
                            ),
                            ],
                            ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ),
                ]
            ),
    )
    
    signal=ft.Row(
            [ft.Card(
                height=170,
                width=160,
                color="#d9113a",
                content=ft.Container(alignment=ft.alignment.center,content=ft.Column(
                    [
                        ft.Text(
                            "EURUSD",
                            size=20,
                            font_family="Platypi",
                            weight=ft.FontWeight.W_900,
                            text_align=ft.TextAlign.CENTER,
                            color="#FFFFFF"
                        ),
                        ft.Container(content=ft.Image(src='up-arrow.png',width=30,height=30),
                                     padding=ft.padding.only(left=27)
                                     ),
                        
                        ft.Text(
                            "Remaining.",
                            size=10,
                            font_family="Platypi",
                            weight=ft.FontWeight.W_900,
                            text_align=ft.TextAlign.CENTER,
                            color="#FFFFFF"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,    
                ))
                )],

        )
    label=ft.Text("dfdfd"),
    win_control=ft.Container(content=ft.Card(
        height=280,
        width=160,
        color="#281e1c",
        content=ft.Container(alignment=ft.alignment.center,content=ft.Column(
            [
                ft.Checkbox(label="London Session", value=False,active_color="#d9113a",overlay_color="#d9113a"),
                ft.Checkbox(label="New York Session", value=False,active_color="#d9113a"),
                ft.Checkbox(label="Asian Session", value=False,active_color="#d9113a"),
                ft.Container(alignment=ft.alignment.center,content=ft.Text(
                    "Take Profit Take Loss",
                    size=8,
                    font_family="Platypi",
                    weight=ft.FontWeight.W_900,
                    text_align=ft.TextAlign.CENTER,
                    color="#FFFFFF"
                )),
                ft.Slider(min=0, max=100, label="{value}",divisions=10, thumb_color="#d9113a",active_color="#d9113a",inactive_color="#d9113a"),
                ft.Slider(min=0, max=100, divisions=10, label="{value}",thumb_color="#d9113a",active_color="#d9113a",inactive_color="#d9113a"),
            ],
            
            alignment=ft.MainAxisAlignment.CENTER,
        ))
    ))
 
    container2 = ft.Container(
                    height=600,
                    width=220,
                    # bgcolor=ft.colors.AMBER,
                    content=ft.Column(
                        [
                            ft.Switch(
                                label="Signal or Trade",
                                value=True,
                                thumb_color={ft.MaterialState.SELECTED: "#d9113a"},
                                track_color="#161a1c",
                                focus_color="#161a1c",
                            ),
                            ft.Text(""),
                            
                            signal,
                            win_control  
                        ]
                    )
                )

    container3=ft.Container(
                    height=600,
                    width=280,
                    # bgcolor=ft.colors.AMBER,
                    padding=ft.padding.all(10),
                    
                    content=ft.Column(controls=[
                    ft.Container(
                            height=450,
                            width=280,
                            # bgcolor=ft.colors.WHITE
                            ),
                            ft.Container(
                            content=ft.ElevatedButton(text="Centered Button"),
                            margin=ft.margin.all(30)
                            ),
                        ]),
    )
    def account_change(e):
        try:
            I_want_money.change_balance("REAL")
        except:
            show_banner_click(e)
    account_type=ft.Container(
                    height=60,
                    width=450,
                    # bgcolor=ft.colors.WHITE,
                    padding=ft.padding.all(10),
                    content=ft.Container(
                        content=ft.Row(
                        [
                            ft.Switch(
                            label="Real or Demo Account",
                            value=False,
                            thumb_color={ft.MaterialState.SELECTED: "#d9113a"},
                            track_color="#161a1c",
                            focus_color="#161a1c",
                            on_change=account_change
                            ),
                            ft.ElevatedButton(text="LogIn account",color=ft.colors.WHITE, on_click=open_dlg_modal,bgcolor="#d9113a"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                                
                ),
        )
    subscription=ft.Card(
                    height=180,
                    width=450,
                    # color="#3d3d3d",
                    
                    content=ft.Container(
                        gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=Alignment(0.8, 1),
                colors=[
                    "#ffc40e",
                    "#e02a38",
                    "#fe7513",
    
                    "#ffac0e",
                   
                ],
                tile_mode=ft.GradientTileMode.MIRROR,
                rotation=math.pi / 3,
            ),
            border_radius=20,
                        content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Image(
                                            src="favicon.png",
                                            height=90,
                                            width=90,
                                            border_radius=35
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text(
                                                "You have only 7days",
                                                size=12,
                                                font_family="Montserrat",
                                                weight=ft.FontWeight.W_900,
                                                text_align=ft.TextAlign.CENTER,
                                                color="#FFFFFF"
                                                ),
                                                ft.Text(
                                                    "Get your subscription",
                                                    size=18,
                                                    font_family="Montserrat",
                                                    weight=ft.FontWeight.W_900,
                                                    text_align=ft.TextAlign.CENTER,
                                                    color="#FFFFFF"
                                                    ),
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                )
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        "39 dollars/month",
                                        size=18,
                                        font_family="Platypi",
                                        weight=ft.FontWeight.W_900,
                                        text_align=ft.TextAlign.CENTER,
                                        color="FFFFFF"
                                        ),
                                        ft.ElevatedButton(text="Subcription",bgcolor="d9113a",color="#FFFFFF"),

                                ],
                                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    )
                ),
            )
    
    trade_amount=ft.TextField(
                    height=50,
                    width=170,
                    border_color="#d9113a",
                    label="Trade Amount" 
                )
    trade_multi=ft.Row(
                [
                    ft.Container(
                    height=50,
                    width=170,
                    border_radius=10,
                    # bgcolor=ft.colors.AMBER_100,
                    content=ft.Switch(
                            label="Multiplier",
                            value=True,
                            thumb_color={ft.MaterialState.SELECTED: "#d9113a"},
                            track_color="#161a1c",
                            focus_color="#161a1c",
                        ),
                    ),
                      
                    # bgcolor=ft.colors.AMBER_100,
                    ft.TextField(
                        label="Multiplier step",
                        border_color="#d9113a",
                        height=50,
                        width=170,
                    )
                                                        
                                
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )                                                        
    trade_time=ft.Column(
        [
            ft.Text("Select Trade time"),
            ft.Slider(min=5, max=100, divisions=25, label='Trade Time',thumb_color="#d9113a",active_color="#d9113a",inactive_color="#d9113a")
        ]
    )
    trade_trigger=ft.Row(
                    [
                        ft.ElevatedButton(text="stop",color=ft.colors.WHITE,on_click=stop,bgcolor="#d9113a"),
                        ft.ElevatedButton(text="Bake Trade",color=ft.colors.WHITE,on_click=trade,bgcolor="#d9113a"),    
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
                        
    trade_magic=ft.Container(
        height=190,
        width=450,
        content=ft.Column(
            [
                ft.Container(
                    height=60,
                    width=450,
                    content=ft.Container(
                        content=
                        ft.Row(
                            [
                                acc_balance,
                                trade_amount,       
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    )
                ),
                trade_multi,
                trade_time,
                
            ]
        )
    )

   
    middle_info=ft.Container(
                    height=600,
                    width=500,
                    # bgcolor=ft.colors.AMBER,
                    padding=ft.padding.all(10),
                    content=ft.Column(
                        [
                            account_type,
                            subscription,
                            trade_magic,
                            ft.Text(""),
                            trade_trigger
                        ]
                    )
                )

    # Create a row to hold the 3 containers
    row = ft.Row(
        controls=[container1, middle_info,container2],
        spacing=10,
    )

    # Add the row to the page
    page.add(row)

ft.app(target=main,assets_dir="assets")