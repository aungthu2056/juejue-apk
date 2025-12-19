def mmk(n):
    try:
        return f"{int(n):,}"
    except:
        return "0"
import json
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.core.window import Window

Window.fullscreen = True

# ---------------------- Base Page ----------------------
class PageBase(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root_layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        with self.canvas.before:
            Color(0.0, 0.25, 0.18, 1)
            self.bg = RoundedRectangle(size=self.size, pos=self.pos, radius=[0])
        self.bind(size=self.update_bg, pos=self.update_bg)
        self.add_widget(self.root_layout)

    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def add_page_switcher(self):
        switcher = BoxLayout(size_hint_y=None, height=160, spacing=30, padding=[5,5,5,5])
        for txt, page in [("HOME","page1"),("LEDGER","page2"),("PROFIT","page3"),("SETTING","page4")]:
            btn = Button(
                text=txt,
                font_size=48,
                size_hint=(1,1),
                background_normal='',
                background_color=(1,1,1,1),
                color=(0,0.5,0,1),
            )
            with btn.canvas.before:
                Color(1,1,1,1)
                btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[20])
            btn.bind(pos=lambda inst, val: setattr(btn.rect,'pos',val),
                     size=lambda inst, val: setattr(btn.rect,'size',val))
            btn.bind(on_press=lambda x,p=page: setattr(self.manager,'current',p))
            switcher.add_widget(btn)
        self.root_layout.add_widget(Widget(size_hint_y=None, height=25))
        self.root_layout.add_widget(switcher)

# ---------------------- Page1 ----------------------
class Page1(PageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Header
        self.root_layout.add_widget(Widget(size_hint_y=None, height=10))
        self.root_layout.add_widget(Label(
            text="JUE JUE",
            font_size=140,
            size_hint_y=None,
            height=250,
            color=(1,1,1,1)
        ))
        self.root_layout.add_widget(Label(
            text="Profit Details",
            font_size=100,
            size_hint_y=None,
            height=180,
            color=(1,1,1,1)
        ))
        self.root_layout.add_widget(Widget(size_hint_y=None, height=40))

        # Grid for input fields
        grid = GridLayout(cols=2, spacing=30, size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        def create_label(text, font_size=48, text_color=(1,1,1,1), bg_color=(0,0,0,1)):
            container = BoxLayout(size_hint_y=None, height=120, padding=[5,5,5,5])
            with container.canvas.before:
                Color(*bg_color)
                container.rect = RoundedRectangle(pos=container.pos, size=container.size, radius=[20])
            container.bind(pos=lambda inst, val: setattr(container.rect,'pos',val),
                           size=lambda inst, val: setattr(container.rect,'size',val))
            lbl = Label(text=text, font_size=font_size, color=text_color, halign='center', valign='middle', text_size=(Window.width-100,None))
            container.add_widget(lbl)
            return container

        def create_input(hint, numeric=False, font_size=48, fg_color=(1,1,1,1), bg_color=(0,0,0,1)):
            return TextInput(hint_text=hint, font_size=font_size, size_hint_y=None, height=130,
                             background_color=bg_color, foreground_color=fg_color, halign='center',
                             input_filter='int' if numeric else None)

        # Inputs
        self.date_input = create_input("14-12-2025", font_size=52, fg_color=(1,1,1,1), bg_color=(0,0,0,1))
        self.item_input = create_input("Item name", fg_color=(1,1,1,1), bg_color=(0,0,0,1))
        self.per_bag_input = create_input("Qty per bag", True, fg_color=(1,1,1,1), bg_color=(0,0,0,1))
        self.bag_input = create_input("Bag count", True, fg_color=(1,1,1,1), bg_color=(0,0,0,1))
        self.total_pack_lbl = Label(text="0", font_size=52, size_hint_y=None, height=130, color=(1,1,1,1))
        self.unit_price_input = create_input("Unit price MMK", True, fg_color=(1,1,1,1), bg_color=(0,0,0,1))
        self.car_fee_input = create_input("Car fee MMK", True, fg_color=(1,1,1,1), bg_color=(0,0,0,1))
        self.total_amount_lbl = Label(text="0 MMK", font_size=56, size_hint_y=None, height=140, color=(1,1,1,1))

        fields = [
            ("Date", self.date_input),
            ("Item", self.item_input),
            ("Qty per bag", self.per_bag_input),
            ("Bag count", self.bag_input),
            ("Total pack", self.total_pack_lbl),
            ("Unit price", self.unit_price_input),
            ("Car fee", self.car_fee_input),
            ("Total amount", self.total_amount_lbl)
        ]

        for label, widget in fields:
            grid.add_widget(create_label(label))
            container = BoxLayout(size_hint_y=None, height=widget.height, padding=[5,5,5,5])
            with container.canvas.before:
                Color(0,0,0,1)
                container.rect = RoundedRectangle(pos=container.pos, size=container.size, radius=[20])
            container.bind(pos=lambda inst, val: setattr(container.rect,'pos',val),
                           size=lambda inst, val: setattr(container.rect,'size',val))
            container.add_widget(widget)
            grid.add_widget(container)

        # Buttons
        calc_btn = Button(text="CALCULATE", font_size=52, size_hint_y=None, height=150, background_color=(0,0.6,0.35,1), color=(1,1,1,1))
        calc_btn.bind(on_press=self.calculate)
        save_btn = Button(text="SAVE & NEXT", font_size=52, size_hint_y=None, height=150, background_color=(0,0.6,0.35,1), color=(1,1,1,1))
        save_btn.bind(on_press=self.save_and_next)

        grid.add_widget(calc_btn)
        grid.add_widget(save_btn)

        self.root_layout.add_widget(grid)
        self.root_layout.add_widget(Widget(size_hint_y=None, height=40))
        self.add_page_switcher()

    def calculate(self, instance):
        try:
            per_bag=int(self.per_bag_input.text or 0)
            bag=int(self.bag_input.text or 0)
            unit=int(self.unit_price_input.text or 0)
            car=int(self.car_fee_input.text or 0)
            total_pack = per_bag * bag
            total_money = total_pack * unit + car
            self.total_pack_lbl.color=(1,1,1,1)
            self.total_pack_lbl.text = str(total_pack)
            self.total_amount_lbl.color=(1,1,1,1)
            self.total_amount_lbl.text = f"{total_money} MMK"
        except:
            self.total_pack_lbl.text="0"
            self.total_amount_lbl.text="0 MMK"

    def save_and_next(self, instance):
        self.calculate(instance)
        entry={
            "date":self.date_input.text,
            "item":self.item_input.text,
            "total_pack":self.total_pack_lbl.text,
            "car_fee":self.car_fee_input.text,
            "total_money":self.total_amount_lbl.text
        }
        self.manager.get_screen('page2').entries.append(entry)
        self.manager.get_screen('page2').update_entries()
        # Clear inputs
        self.item_input.text=""
        self.per_bag_input.text=""
        self.bag_input.text=""
        self.unit_price_input.text=""
        self.car_fee_input.text=""
        self.total_pack_lbl.text="0"
        self.total_amount_lbl.text="0 MMK"
        self.manager.current='page2'

# ---------------------- Page2 ----------------------
class Page2(PageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)

        self.ledger_file = os.path.join(self.data_dir, "ledger.json")
        self.kpay_file = os.path.join(self.data_dir, "kpay.json")

        self.entries = self.load_json(self.ledger_file)
        self.kpay_entries = self.load_json(self.kpay_file)

        # -------- TITLE --------
        self.root_layout.add_widget(Label(
            text="LEDGER",
            font_size=72,
            size_hint_y=None,
            height=120,
            color=(1,1,1,1)
        ))

        # -------- LEDGER --------
        self.root_layout.add_widget(self.make_section_title("Ledger Records"))

        self.ledger_grid = GridLayout(
            cols=5,
            spacing=10,
            size_hint_y=None,
            row_default_height=80
        )
        self.ledger_grid.bind(minimum_height=self.ledger_grid.setter("height"))

        ledger_scroll = ScrollView(size_hint=(1, 0.45))
        ledger_scroll.add_widget(self.ledger_grid)
        self.root_layout.add_widget(ledger_scroll)

        # -------- KPAY INPUT --------
        self.root_layout.add_widget(self.make_section_title("K-Pay Payments"))

        kpay_box = BoxLayout(size_hint_y=None, height=90, spacing=10)

        self.kpay_date = TextInput(hint_text="Date", font_size=36)
        self.kpay_amount = TextInput(
            hint_text="Amount MMK", font_size=36, input_filter="int"
        )

        add_kpay_btn = Button(
            text="ADD", font_size=36, background_color=(0,0.6,0.35,1)
        )
        add_kpay_btn.bind(on_press=self.add_kpay)

        kpay_box.add_widget(self.kpay_date)
        kpay_box.add_widget(self.kpay_amount)
        kpay_box.add_widget(add_kpay_btn)
        self.root_layout.add_widget(kpay_box)

        # -------- KPAY TABLE --------
        self.kpay_grid = GridLayout(
            cols=2,
            spacing=10,
            size_hint_y=None,
            row_default_height=70
        )
        self.kpay_grid.bind(minimum_height=self.kpay_grid.setter("height"))

        kpay_scroll = ScrollView(size_hint=(1, 0.25))
        kpay_scroll.add_widget(self.kpay_grid)
        self.root_layout.add_widget(kpay_scroll)

        # -------- TOTAL --------
        self.total_label = Label(
            text="",
            font_size=44,
            size_hint_y=None,
            height=120,
            color=(1,1,1,1)
        )
        self.root_layout.add_widget(self.total_label)

        self.add_page_switcher()
        self.refresh_all()

    # ================= UTIL =================
    def make_section_title(self, text):
        return Label(text=text, font_size=48, size_hint_y=None, height=80, color=(1,1,1,1))

    def load_json(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_json(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def mmk(self, n):
        try:
            return f"{int(n):,}"
        except:
            return "0"

    # ================= LEDGER =================
    def update_entries(self):
        self.save_json(self.ledger_file, self.entries)
        self.refresh_all()
        self.refresh_linked_pages()

    def draw_ledger(self):
        self.ledger_grid.clear_widgets()

        headers = ["Date", "Item", "Pack", "Car Fee", "Total"]
        for h in headers:
            self.ledger_grid.add_widget(
                Label(text=h, font_size=36, bold=True, color=(1,1,1,1))
            )

        for idx, e in enumerate(self.entries[::-1]):
            real_index = len(self.entries) - 1 - idx

            def bind_edit(widget, index):
                widget.bind(on_touch_down=lambda w, t, i=index:
                            self.edit_ledger(i) if w.collide_point(*t.pos) else None)

            widgets = [
                Label(text=e["date"], font_size=32, color=(1,1,1,1)),
                Label(text=e["item"], font_size=32, color=(1,1,1,1)),
                Label(text=self.mmk(e["total_pack"]), font_size=32, color=(1,1,1,1)),
                Label(text=self.mmk(e["car_fee"]), font_size=32, color=(1,1,1,1)),
                Label(
                    text=f"{self.mmk(e['total_money'].replace(' MMK',''))} MMK",
                    font_size=32, color=(1,1,1,1)
                )
            ]

            for w in widgets:
                bind_edit(w, real_index)
                self.ledger_grid.add_widget(w)

    def edit_ledger(self, index):
        from kivy.uix.popup import Popup

        e = self.entries[index]
        box = BoxLayout(orientation="vertical", spacing=10, padding=10)

        date = TextInput(text=e["date"], font_size=32)
        item = TextInput(text=e["item"], font_size=32)
        pack = TextInput(text=e["total_pack"], input_filter="int", font_size=32)
        car = TextInput(text=e["car_fee"], input_filter="int", font_size=32)
        total = TextInput(
            text=e["total_money"].replace(" MMK",""),
            input_filter="int",
            font_size=32
        )

        update_btn = Button(text="UPDATE", font_size=32, background_color=(0,0.6,0.35,1))
        delete_btn = Button(text="DELETE", font_size=32, background_color=(0.8,0.2,0.2,1))

        for w in [date,item,pack,car,total,update_btn,delete_btn]:
            box.add_widget(w)

        popup = Popup(title="Edit Ledger", content=box, size_hint=(0.9,0.9))
        popup.open()

        def update_entry(instance):
            self.entries[index] = {
                "date": date.text,
                "item": item.text,
                "total_pack": pack.text,
                "car_fee": car.text,
                "total_money": f"{total.text} MMK"
            }
            self.update_entries()
            popup.dismiss()

        def delete_entry(instance):
            self.entries.pop(index)
            self.update_entries()
            popup.dismiss()

        update_btn.bind(on_press=update_entry)
        delete_btn.bind(on_press=delete_entry)

    # ================= KPAY =================
    def add_kpay(self, instance):
        if not self.kpay_date.text or not self.kpay_amount.text:
            return

        self.kpay_entries.append({
            "date": self.kpay_date.text,
            "amount": int(self.kpay_amount.text)
        })
        self.kpay_date.text = ""
        self.kpay_amount.text = ""

        self.save_json(self.kpay_file, self.kpay_entries)
        self.refresh_all()
        self.refresh_linked_pages()

    def draw_kpay(self):
        self.kpay_grid.clear_widgets()

        self.kpay_grid.add_widget(Label(text="Date", font_size=34, bold=True,color=(1,1,1,1)))
        self.kpay_grid.add_widget(Label(text="Amount", font_size=34, bold=True,color=(1,1,1,1)))

        for idx, k in enumerate(self.kpay_entries[::-1]):
            real_index = len(self.kpay_entries) - 1 - idx

            date_lbl = Label(text=k["date"], font_size=30,color=(1,1,1,1))
            amt_lbl = Label(text=f"{self.mmk(k['amount'])} MMK", font_size=30,color=(1,1,1,1))

            date_lbl.bind(on_touch_down=lambda w,t,i=real_index:
                          self.edit_kpay(i) if w.collide_point(*t.pos) else None)
            amt_lbl.bind(on_touch_down=lambda w,t,i=real_index:
                         self.edit_kpay(i) if w.collide_point(*t.pos) else None)

            self.kpay_grid.add_widget(date_lbl)
            self.kpay_grid.add_widget(amt_lbl)

    def edit_kpay(self, index):
        from kivy.uix.popup import Popup

        k = self.kpay_entries[index]
        box = BoxLayout(orientation="vertical", spacing=10, padding=10)

        date = TextInput(text=k["date"], font_size=32)
        amount = TextInput(text=str(k["amount"]), input_filter="int", font_size=32)

        update_btn = Button(text="UPDATE", font_size=32, background_color=(0,0.6,0.35,1))
        delete_btn = Button(text="DELETE", font_size=32, background_color=(0.8,0.2,0.2,1))

        for w in [date,amount,update_btn,delete_btn]:
            box.add_widget(w)

        popup = Popup(title="Edit KPay", content=box, size_hint=(0.8,0.6))
        popup.open()

        def update_k(instance):
            self.kpay_entries[index] = {
                "date": date.text,
                "amount": int(amount.text)
            }
            self.save_json(self.kpay_file, self.kpay_entries)
            self.refresh_all()
            self.refresh_linked_pages()
            popup.dismiss()

        def delete_k(instance):
            self.kpay_entries.pop(index)
            self.save_json(self.kpay_file, self.kpay_entries)
            self.refresh_all()
            self.refresh_linked_pages()
            popup.dismiss()

        update_btn.bind(on_press=update_k)
        delete_btn.bind(on_press=delete_k)

    # ================= TOTAL =================
    def refresh_all(self):
        self.draw_ledger()
        self.draw_kpay()

        ledger_total = sum(int(e["total_money"].replace(" MMK","")) for e in self.entries)
        kpay_total = sum(k["amount"] for k in self.kpay_entries)
        balance = ledger_total - kpay_total

        self.total_label.text = (
            f"Ledger Total : {self.mmk(ledger_total)} MMK\n"
            f"K-Pay Total : {self.mmk(kpay_total)} MMK\n"
            f"Balance : {self.mmk(balance)} MMK"
        )

    # ================= AUTO REFRESH =================
    def refresh_linked_pages(self):
        if not self.manager:
            return
        self.manager.get_screen("page3").draw_table()
        self.manager.get_screen("page4").update_monthly_profit()
# ---------------------- Page3 ----------------------
class Page3(PageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ---------- DATA ----------
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        self.profit_file = os.path.join(self.data_dir, "profit.json")
        self.sales = self.load_profit()

        # ---------- TITLE ----------
        self.root_layout.add_widget(Label(
            text="PROFIT",
            font_size=70,
            size_hint_y=None,
            height=120,
            color=(1,1,1,1)
        ))

        # ---------- INPUT ----------
        input_box = BoxLayout(size_hint_y=None, height=90, spacing=10)

        self.date_input = TextInput(
            hint_text="Date (DD-MM-YYYY)",
            multiline=False,
            font_size=34
        )

        self.price_input = TextInput(
            hint_text="Price per pack (MMK)",
            multiline=False,
            font_size=34,
            input_filter="int"
        )

        add_btn = Button(
            text="ADD",
            font_size=34,
            background_color=(0,0.6,0.35,1)
        )
        add_btn.bind(on_press=self.add_sale)

        input_box.add_widget(self.date_input)
        input_box.add_widget(self.price_input)
        input_box.add_widget(add_btn)
        self.root_layout.add_widget(input_box)

        # ---------- TABLE ----------
        self.grid = GridLayout(
            cols=7,
            size_hint_y=None,
            row_default_height=70,
            spacing=2
        )
        self.grid.bind(minimum_height=self.grid.setter("height"))

        scroll = ScrollView(size_hint=(1,1))
        scroll.add_widget(self.grid)
        self.root_layout.add_widget(scroll)

        self.add_page_switcher()
        self.draw_table()

    # ---------- LOAD / SAVE ----------
    def load_profit(self):
        if os.path.exists(self.profit_file):
            with open(self.profit_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_profit(self):
        with open(self.profit_file, "w", encoding="utf-8") as f:
            json.dump(self.sales, f, ensure_ascii=False, indent=2)

    # ---------- CELL ----------
    def cell(self, text, width, bold=False):
        box = BoxLayout(size_hint_x=None, width=width)
        lbl = Label(
            text=text,
            font_size=30,
            bold=bold,
            halign="center",
            valign="middle",
            color=(1,1,1,1),
            text_size=(width-10,None)
        )
        box.add_widget(lbl)
        return box

    # ---------- DRAW TABLE ----------
    def draw_table(self):
        self.grid.clear_widgets()

        headers = [
            ("Date",160),
            ("Pack",100),
            ("Price",140),
            ("Sales",160),
            ("Cost",160),
            ("Car",120),
            ("Profit",160)
        ]
        for h,w in headers:
            self.grid.add_widget(self.cell(h,w,True))

        for idx, s in enumerate(self.sales[::-1]):
            real_index = len(self.sales) - 1 - idx

            cells = [
                (s["date"],160),
                (str(s["pack"]),100),
                (f"{s['price']:,}",140),
                (f"{s['sales']:,}",160),
                (f"{s['cost']:,}",160),
                (f"{s['car']:,}",120),
                (f"{s['profit']:,}",160)
            ]

            for text, width in cells:
                lbl = Label(
                    text=text,
                    font_size=30,
                    color=(1,1,1,1),
                    size_hint_x=None,
                    width=width,
                    halign="center",
                    valign="middle"
                )
                lbl.bind(
                    on_touch_down=lambda w,t,i=real_index:
                    self.edit_sale(i) if w.collide_point(*t.pos) else None
                )
                self.grid.add_widget(lbl)

    # ---------- ADD SALE ----------
    def add_sale(self, instance):
        if not self.date_input.text or not self.price_input.text:
            return

        date = self.date_input.text
        price = int(self.price_input.text)

        page2 = self.manager.get_screen("page2")

        pack = cost = car = 0
        for e in page2.entries:
            if e["date"] == date:
                pack += int(e["total_pack"])
                car += int(e.get("car_fee",0) or 0)
                cost += int(e["total_money"].replace(" MMK",""))

        if pack == 0:
            return

        sales = pack * price
        profit = sales - cost

        self.sales.append({
            "date": date,
            "pack": pack,
            "price": price,
            "sales": sales,
            "cost": cost,
            "car": car,
            "profit": profit
        })

        self.save_profit()
        self.draw_table()
        self.refresh_page4()

        self.date_input.text = ""
        self.price_input.text = ""

    # ---------- EDIT SALE ----------
    def edit_sale(self, index):
        from kivy.uix.popup import Popup

        s = self.sales[index]
        box = BoxLayout(orientation="vertical", spacing=10, padding=10)

        date = TextInput(text=s["date"], font_size=32)
        price = TextInput(text=str(s["price"]), input_filter="int", font_size=32)

        update_btn = Button(text="UPDATE", font_size=32, background_color=(0,0.6,0.35,1))
        delete_btn = Button(text="DELETE", font_size=32, background_color=(0.8,0.2,0.2,1))

        box.add_widget(date)
        box.add_widget(price)
        box.add_widget(update_btn)
        box.add_widget(delete_btn)

        popup = Popup(title="Edit Sale", content=box, size_hint=(0.8,0.6))
        popup.open()

        def update_sale(instance):
            page2 = self.manager.get_screen("page2")

            pack = cost = car = 0
            for e in page2.entries:
                if e["date"] == date.text:
                    pack += int(e["total_pack"])
                    car += int(e.get("car_fee",0) or 0)
                    cost += int(e["total_money"].replace(" MMK",""))

            if pack == 0:
                popup.dismiss()
                return

            price_val = int(price.text)
            sales = pack * price_val
            profit = sales - cost

            self.sales[index] = {
                "date": date.text,
                "pack": pack,
                "price": price_val,
                "sales": sales,
                "cost": cost,
                "car": car,
                "profit": profit
            }

            self.save_profit()
            self.draw_table()
            self.refresh_page4()
            popup.dismiss()

        def delete_sale(instance):
            self.sales.pop(index)
            self.save_profit()
            self.draw_table()
            self.refresh_page4()
            popup.dismiss()

        update_btn.bind(on_press=update_sale)
        delete_btn.bind(on_press=delete_sale)

    # ---------- REFRESH PAGE 4 ----------
    def refresh_page4(self):
        if self.manager:
            self.manager.get_screen("page4").update_monthly_profit()
# ---------------------- Page4 ----------------------
class Page4(PageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ---------- TITLE ----------
        self.root_layout.add_widget(Label(
            text="MONTHLY PROFIT",
            font_size=60,
            size_hint_y=None,
            height=120,
            color=(1,1,1,1)
        ))

        # ---------- TABLE ----------
        self.grid = GridLayout(
            cols=2,
            size_hint_y=None,
            row_default_height=70,
            spacing=2
        )
        self.grid.bind(minimum_height=self.grid.setter("height"))

        scroll = ScrollView(size_hint=(1,1))
        scroll.add_widget(self.grid)
        self.root_layout.add_widget(scroll)

        self.add_page_switcher()

        # first load
        self.update_monthly_profit()

    # ---------- AUTO REFRESH WHEN ENTER ----------
    def on_pre_enter(self):
        self.update_monthly_profit()

    # ---------- CELL ----------
    def cell(self, text, bold=False):
        return Label(
            text=text,
            font_size=32 if not bold else 34,
            bold=bold,
            color=(1,1,1,1),
            halign="center",
            valign="middle"
        )

    # ---------- UPDATE MONTHLY PROFIT ----------
    def update_monthly_profit(self):
        self.grid.clear_widgets()

        # header
        self.grid.add_widget(self.cell("Month", True))
        self.grid.add_widget(self.cell("Profit (MMK)", True))

        profit_file = os.path.join("data", "profit.json")
        if not os.path.exists(profit_file):
            return

        with open(profit_file, "r", encoding="utf-8") as f:
            sales = json.load(f)

        monthly = {}
        for s in sales:
            # expected date format: DD-MM-YYYY
            month = s["date"][-7:]  # MM-YYYY
            monthly.setdefault(month, 0)
            monthly[month] += int(s["profit"])

        for m in sorted(monthly.keys(), reverse=True):
            self.grid.add_widget(self.cell(m))
            self.grid.add_widget(self.cell(f"{monthly[m]:,}"))
# ---------------------- App ----------------------
class JueJueApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Page1(name='page1'))
        sm.add_widget(Page2(name='page2'))
        sm.add_widget(Page3(name='page3'))
        sm.add_widget(Page4(name='page4'))
        return sm

if __name__=="__main__":
    JueJueApp().run()