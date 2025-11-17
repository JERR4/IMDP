from collections import defaultdict
import random as rd
import simpy
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

OKHO = True   # флаг визуализации модели
mainpanel = tk.Tk()
# код заглушки вместо инфопанели для эксперимента


def dummyPanel():
    global bus_log, sellers, scanners

    class BusLog:
        def __init__(self):
            pass

        def next_bus(self, minutes):
            pass

        def bus_arrived(self, people):
            pass

    class Sellers:
        def __init__(self):
            pass

        def add_to_line(self, seller_number):
            pass

        def remove_from_line(self, seller_number):
            pass

    class Scanners:
        def __init__(self):
            pass

        def add_to_line(self, seller_number):
            pass

        def remove_from_line(self, seller_number):
            pass

    bus_log = BusLog()
    sellers = Sellers()
    scanners = Scanners()

# -------------------------
#  UI/ANIMATION
# -------------------------


def infoPanel():
    global bus_log, sellers, scanners, clockinfo, mainpanel

    mainpanel.title("Nash Sim Proc")
    mainpanel.config(bg="#fff")
    top_frame = tk.Frame(mainpanel)
    top_frame.pack(side=tk.TOP, expand=False)
    canvas = tk.Canvas(mainpanel, width=1200, height=450, bg="white")
    f = plt.Figure(figsize=(2, 2), dpi=72)
    a3 = f.add_subplot(221)
    a3.plot()
    a1 = f.add_subplot(222)
    a1.plot()
    a4 = f.add_subplot(223)
    a4.plot()
    a2 = f.add_subplot(224)
    a2.plot()

    data_plot = FigureCanvasTkAgg(f, master=mainpanel)
    data_plot.get_tk_widget().config(height=400)
    data_plot.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    canvas.pack(side=tk.TOP, expand=False)

    class QueueGraphics:
        text_height = 30

        def __init__(self, icon, icon_width, queue_name, num_lines, canvas, x_top, y_top):
            self.icon_file = icon + ".gif"
            self.icon_width = icon_width
            self.queue_name = queue_name
            self.num_lines = num_lines
            self.canvas = canvas
            self.x_top = x_top
            self.y_top = y_top
            dataimg = "R0v"
            if icon == "group":
                dataimg = "R0lGODlhGAAYAHAAACH/C0ltYWdlTWFnaWNrDWdhbW1hPTAuNDU0NTUAIfkEAAAAAAAsAAAAABgAGACHAAAAAAAzAABmAACZAADMAAD/ACsAACszACtmACuZACvMACv/AFUAAFUzAFVmAFWZAFXMAFX/AIAAAIAzAIBmAICZAIDMAID/AKoAAKozAKpmAKqZAKrMAKr/ANUAANUzANVmANWZANXMANX/AP8AAP8zAP9mAP+ZAP/MAP//MwAAMwAzMwBmMwCZMwDMMwD/MysAMyszMytmMyuZMyvMMyv/M1UAM1UzM1VmM1WZM1XMM1X/M4AAM4AzM4BmM4CZM4DMM4D/M6oAM6ozM6pmM6qZM6rMM6r/M9UAM9UzM9VmM9WZM9XMM9X/M/8AM/8zM/9mM/+ZM//MM///ZgAAZgAzZgBmZgCZZgDMZgD/ZisAZiszZitmZiuZZivMZiv/ZlUAZlUzZlVmZlWZZlXMZlX/ZoAAZoAzZoBmZoCZZoDMZoD/ZqoAZqozZqpmZqqZZqrMZqr/ZtUAZtUzZtVmZtWZZtXMZtX/Zv8AZv8zZv9mZv+ZZv/MZv//mQAAmQAzmQBmmQCZmQDMmQD/mSsAmSszmStmmSuZmSvMmSv/mVUAmVUzmVVmmVWZmVXMmVX/mYAAmYAzmYBmmYCZmYDMmYD/maoAmaozmapmmaqZmarMmar/mdUAmdUzmdVmmdWZmdXMmdX/mf8Amf8zmf9mmf+Zmf/Mmf//zAAAzAAzzABmzACZzADMzAD/zCsAzCszzCtmzCuZzCvMzCv/zFUAzFUzzFVmzFWZzFXMzFX/zIAAzIAzzIBmzICZzIDMzID/zKoAzKozzKpmzKqZzKrMzKr/zNUAzNUzzNVmzNWZzNXMzNX/zP8AzP8zzP9mzP+ZzP/MzP///wAA/wAz/wBm/wCZ/wDM/wD//ysA/ysz/ytm/yuZ/yvM/yv//1UA/1Uz/1Vm/1WZ/1XM/1X//4AA/4Az/4Bm/4CZ/4DM/4D//6oA/6oz/6pm/6qZ/6rM/6r//9UA/9Uz/9Vm/9WZ/9XM/9X///8A//8z//9m//+Z///M////AAAAAAAAAAAAAAAACPsA9wkcSLCgwYMIEypcuJBTM4cCiSmTKFAZPHXwlBnM1CwTMU6ZJmYKKWafGHUWYxgUk0lgM5Yl9ym7QezGQBzDCoqZJHASzIg3lMXQuG9oQTQAJqExMBIAmkkxxAjFMelGDGIEM8VAI4YrVK5cb8DkKiboQJZZY1a0SRAHVoFP0xIUWjAMUZMtB2ZSu48Y36Jv8codSJegWbh8997NdLiv0Ypc2N7waRTNikxcWhLbWnDmvno095lF0xLtXoOFpUKTapJn3JoGYYPGWrl0y9OdVYrGynqnYNxzbSpTXXtfXOAEY0Q1KmY5Vq3N0RxUNhHaQIl3sTPczp1hQAA7"
            if icon == "person":
                dataimg = "R0lGODlhGAAYAHA9ACH5BAAAAAAALAAAAAAYABgAhwAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwArZgArmQArzAAr/wBVAABVMwBVZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCqmQCqzACq/wDVAADVMwDVZgDVmQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/zMrADMrMzMrZjMrmTMrzDMr/zNVADNVMzNVZjNVmTNVzDNV/zOAADOAMzOAZjOAmTOAzDOA/zOqADOqMzOqZjOqmTOqzDOq/zPVADPVMzPVZjPVmTPVzDPV/zP/ADP/MzP/ZjP/mTP/zDP//2YAAGYAM2YAZmYAmWYAzGYA/2YrAGYrM2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZVzGZV/2aAAGaAM2aAZmaAmWaAzGaA/2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmWbVzGbV/2b/AGb/M2b/Zmb/mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krAJkrM5krZpkrmZkrzJkr/5lVAJlVM5lVZplVmZlVzJlV/5mAAJmAM5mAZpmAmZmAzJmA/5mqAJmqM5mqZpmqmZmqzJmq/5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswAmcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxVM8xVZsxVmcxVzMxV/8yAAMyAM8yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zVAMzVM8zVZszVmczVzMzV/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8rM/8rZv8rmf8rzP8r//9VAP9VM/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+qM/+qZv+qmf+qzP+q///VAP/VM//VZv/Vmf/VzP/V////AP//M///Zv//mf//zP///wAAAAAAAAAAAAAAAAiLAPcJHEiwoMGDCBMqXMiwYCZiyhoenIRGDJqIEgcqs2iRWMaB9SpKEpPp48BMk0jWMykw2jBNGE0qk4QGjaSSJjOJETNmZ0yJkzIoGULkYk4xQzQMEfOz4cihaNI0ZZipYkVGUxcSE5PGIk6TFDuy3KdTUhp6Y4lVTDN238abbfdR1BRX38q4eDMGBAA7"
            self.image = tk.PhotoImage(data=dataimg)
            self.icons = defaultdict(lambda: [])
            for i in range(num_lines):
                canvas.create_text(
                    x_top, y_top + (i * self.text_height), anchor=tk.NW, text=f"{queue_name} {i+1}")
            self.canvas.update()

        def add_to_line(self, service_number):
            count = len(self.icons[service_number])
            x = self.x_top + 62 + (count * self.icon_width)
            y = self.y_top + ((service_number - 1) * self.text_height) - 8
            self.icons[service_number].append(
                self.canvas.create_image(x, y, anchor=tk.NW, image=self.image))
            self.canvas.update()

        def remove_from_line(self, service_number):
            if len(self.icons[service_number]) == 0:
                return
            to_del = self.icons[service_number].pop()
            self.canvas.delete(to_del)
            self.canvas.update()

    def Sellers(canvas, x_top, y_top):
        return QueueGraphics("group", 24, "Касса", SELLER_LINES, canvas, x_top, y_top)

    def Scanners(canvas, x_top, y_top):
        return QueueGraphics("person", 17, "Контроль", SCANNER_LINES, canvas, x_top, y_top)

    class BusLog:
        TEXT_HEIGHT = 24

        def __init__(self, canvas, x_top, y_top):
            self.canvas = canvas
            self.x_top = x_top
            self.y_top = y_top
            self.bus_count = 0

        def next_bus(self, minutes):
            x = self.x_top
            y = self.y_top + (self.bus_count * self.TEXT_HEIGHT)
            self.canvas.create_text(
                x, y, anchor=tk.NW, text=f"Прибытие через {round(minutes, 1)} мин")
            self.canvas.update()

        def bus_arrived(self, people):
            x = self.x_top + 150
            y = self.y_top + (self.bus_count * self.TEXT_HEIGHT)
            self.canvas.create_text(
                x, y, anchor=tk.NW, text=f"Привез {people} чел", fill="blue")
            self.bus_count += 1
            self.canvas.update()

    class ClockData:
        def __init__(self, canvas, x1, y1, x2, y2, time):
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.tot_q_list = {}
            self.canvas = canvas
            self.train = canvas.create_rectangle(
                self.x1, self.y1, self.x2, self.y2, fill="lavender")
            self.options = {"font": "Arial 10", "fill": "red",
                            "activefill": "blue", "anchor": "nw"}
            self.time = canvas.create_text(
                self.x1 + 10, self.y1 + 10, text=f"ВРЕМЯ = {round(time, 1)}m", **self.options)
            self.seller_wait = canvas.create_text(
                self.x1 + 10, self.y1 + 30, text="сред.ожидание в кассу = ", **self.options)
            self.scan_wait = canvas.create_text(
                self.x1 + 10, self.y1 + 50, text="сред.ожидание на контроле= ", **self.options)
            self.seller_count = canvas.create_text(
                self.x1 + 10, self.y1 + 70, text="очереди в кассу: суммарно=", **self.options)
            self.scan_count = canvas.create_text(
                self.x1 + 10, self.y1 + 90, text=">>>", **self.options)
            self.canvas.update()

        def tick(self, time):
          # метод обновления данных по вызову из процесса clockTablo
            for z in [self.time, self.seller_wait, self.scan_wait, self.seller_count, self.scan_count]:
                self.canvas.delete(z)

            # подготовка суммарной информации по очередям
            self.seller_que_str = ''
            self. total_queues = 0
            for i in range(SELLER_LINES):
                self.seller_que_str += str(i + 1) + 'K>>' + \
                    str(seller_queues[i][int(time)]) + ' '
                self.total_queues += seller_queues[i][int(time)]
            self.tot_q_list[int(time)] = self.total_queues
            self.total_queues = max(list(self.tot_q_list.values()))

            # вывод на канвас текста состояния характеристик процесса
            self.time = canvas.create_text(self.x1 + 10, self.y1 + 10,
                                           text=f"ВРЕМЯ ::: {round(time, 1)} мин :::", **self.options)
            self.seller_wait = canvas.create_text(self.x1 + 10, self.y1 + 30,
                                                  text=f"сред.ожидание в кассу = {avg_wait(seller_waits)}м", **self.options)
            self.scan_wait = canvas.create_text(self.x1 + 10, self.y1 + 50,
                                                text=f"сред.ожидание на контроле= {avg_wait(scan_waits)}м", **self.options)
            self.seller_count = canvas.create_text(self.x1 + 10, self.y1 + 70,
                                                   text=f"очереди в кассу: суммарно(макс)= {self.total_queues}", **self.options)
            self.scan_count = canvas.create_text(
                self.x1 + 10, self.y1 + 90, text=self.seller_que_str[::-1], **self.options)
            a1.cla()
            a1.set_xlabel("время (мин)")
            a1.set_ylabel("сред.ожидание в кассу")
            a1.plot(seller_waits.keys(), [
                    sum(waits) / len(waits) for (t, waits) in seller_waits.items()])

            a2.cla()
            a2.set_xlabel("время (мин)")
            a2.set_ylabel("сред.ожидание на контроле")
            a2.plot(scan_waits.keys(), [sum(waits) / len(waits)
                    for (t, waits) in scan_waits.items()])

            a3.cla()
            a3.set_xlabel("время")
            a3.set_ylabel("прибытие")
            a3.bar(arrivals.keys(), arrivals.values(), color='salmon')

            a4.cla()
            a4.set_xlabel("время (мин)")
            a4.set_ylabel("общая очередь в кассу")
            a4.step(self.tot_q_list.keys(), self.tot_q_list.values())

            data_plot.draw()
            self.canvas.update()

    bus_log = BusLog(canvas, 842, 20)
    sellers = Sellers(canvas, 428, 20)
    scanners = Scanners(canvas, 42, 20)
    clockinfo = ClockData(canvas, 56, 284, 345, 421, 0)


# ----------------------------
# Параметры конфигурации модели CONFIGURATION
# ----------------------------

seller_lines, scanner_lines = [], []
bus_log, sellers, scanners, clockinfo = 0, 0, 0, 0

BUS_ARRIVAL_MEAN = 3
BUS_OCCUPANCY_MEAN = 80
BUS_OCCUPANCY_STD = 15

PURCHASE_RATIO_MEAN = 0.5
PURCHASE_GROUP_SIZE_MEAN = 2.5
PURCHASE_GROUP_SIZE_STD = 0.50

TIME_TO_WALK_TO_SELLERS_MEAN = 1
TIME_TO_WALK_TO_SELLERS_STD = 0.25
TIME_TO_WALK_TO_SCANNERS_MEAN = 0.5
TIME_TO_WALK_TO_SCANNERS_STD = 0.1

SELLER_LINES = 6
SELLERS_PER_LINE = 1
SELLER_MEAN = 1
SELLER_STD = 0.2

SCANNER_LINES = 7
SCANNERS_PER_LINE = 2
SCANNER_MEAN = 0.4
SCANNER_STD = 0.1
# предварительно запишем времена прибытия автобусов и кол-во пассажиров
# чтобы точно управлять случайностью
rd.seed(4210)

# -------------------------
#  ANALYTICAL GLOBALS
# списки и словари для аналитики
event_log = []
arrivals = defaultdict(lambda: 0)
seller_waits = defaultdict(lambda: [])
scan_waits = defaultdict(lambda: [])
seller_queues = {v: [] for v in range(SELLER_LINES)}

# методы и функции


def avg_wait(raw_waits):
    waits = [w for i in raw_waits.values() for w in i]
    return round(sum(waits) / len(waits), 1) if len(waits) > 0 else 0


def register_bus_arrival(time, bus_id, people_created):
    arrivals[int(time)] += len(people_created)
    if OKHO:
        print(
            f"Автобус {bus_id+1} приехал в {round(time, 2)} с {len(people_created)} чел")


def register_group_moving_from_bus_to_seller(people, walk_begin, walk_end, seller_line, queue_begin, queue_end, sale_begin, sale_end):
    wait = queue_end - queue_begin
    service_time = sale_end - sale_begin
    seller_waits[int(queue_end)].append(wait)
    if OKHO:
        print(
            f"Группа клиентов {len(people)} чел ждала {round(wait,2)} мин в очереди_{seller_line}, обслужилась за {round(service_time,2)} мин")


def register_visitor_moving_to_scanner(person, walk_begin, walk_end, scanner_line, queue_begin, queue_end, scan_begin, scan_end):
    wait = queue_end - queue_begin
    service_time = scan_end - scan_begin
    scan_waits[int(queue_end)].append(wait)
    if OKHO:
        print(
            f"Клиент на контроле ждал {round(wait,2)} м в очереди_{scanner_line}, обслуживался {round(service_time,2)} м")


ARRIVALS = [rd.expovariate(1 / BUS_ARRIVAL_MEAN) for _ in range(22)]
ON_BOARD = [abs(int(rd.gauss(BUS_OCCUPANCY_MEAN, BUS_OCCUPANCY_STD)))
            for _ in range(22)]
ARRIVAL_ORIGIN = ARRIVALS.copy()  # сохраним оригинальные списки для
ON_BOARD_ORIGIN = ON_BOARD.copy()  # повторного использования в эксперименте


# -------------------------
#  SIMULATION процессы модели
# -------------------------


def pick_shortest(lines):
    """
        определяем самую короткую очередь к ресурсам модели -
        функция возвращает кортеж, где 0й элемент - SimPy resource,
        а 1й элемент - номер ресурса (начиная с 1, а не с 0) //
        номер очереди выбирается случайно после перемешивания shuffle, чтобы не всегда начинать с 1ой
    """
    shuffled = list(zip(range(len(lines)), lines)
                    )  # list of tuples (i, line)
    rd.shuffle(shuffled)
    shortest = shuffled[0][0]
    for i, line in shuffled:
        if len(line.queue) < len(lines[shortest].queue):
            shortest = i
            break
    return (lines[shortest], shortest + 1)

# специальная функция для сбора данных


def clockTablo(env):
    global clockinfo
    while True:
        yield env.timeout(0.1)
        clockinfo.tick(env.now)


def monitor(ev):
    global seller_queues, seller_lines
    while True:
       # запомним текущую длину очередей
        for i in range(len(seller_lines)):
            seller_queues[i].append(len(seller_lines[i].queue))
        yield ev.timeout(1.0)


def bus_arrival(env, seller_lines, scanner_lines):
    """
      моделируем приезд автобуса через BUS_ARRIVAL_MEAN минут,
      который привозит BUS_OCCUPANCY_MEAN людей
      это первое событие в модели, от которого срабатывают другие события
    """
    # уникальные ID для автобуса и людей нужны для последующей визуализации
    next_bus_id = 0
    next_person_id = 0
    while True:
        next_bus = ARRIVALS.pop()
        on_board = ON_BOARD.pop()

        # ждать следующий автобус
        bus_log.next_bus(next_bus)
        yield env.timeout(next_bus)
        bus_log.bus_arrived(on_board)

        # автобус прибыл, определяем Id для прибывших клиентов для записи в логи
        clientIDs = list(range(next_person_id, next_person_id + on_board))
        register_bus_arrival(env.now, next_bus_id, clientIDs)
        next_person_id += on_board
        next_bus_id += 1
        while len(clientIDs) > 0:
            group_size = min(round(abs(rd.gauss(
                PURCHASE_GROUP_SIZE_MEAN, PURCHASE_GROUP_SIZE_STD))), len(clientIDs))
            # получить последние элементы из группы
            people_processed = clientIDs[-group_size:]
            # оставить id тем кто еще остался
            clientIDs = clientIDs[:-group_size]

            # определяем через Random - надо купить билет или сразу идти на контроль
            if rd.random() > PURCHASE_RATIO_MEAN:
                env.process(scanning_customer(env, people_processed, scanner_lines,
                            TIME_TO_WALK_TO_SELLERS_MEAN + TIME_TO_WALK_TO_SCANNERS_MEAN,
                            TIME_TO_WALK_TO_SELLERS_STD + TIME_TO_WALK_TO_SCANNERS_STD))
            else:
                env.process(purchasing_customer(
                    env, people_processed, seller_lines, scanner_lines))


def purchasing_customer(env, people_processed, seller_lines, scanner_lines):
    """
      моделируем приход клиентов в кассу, клиент тратит -
       время TIME_TO_WALK_TO_SELLERS_MEAN на подход к кассе от автобуса
       время SELLER_MEAN на обслуживание в кассе
    """
    # подойти к кассе
    walk_begin = env.now
    yield env.timeout(abs(rd.gauss(TIME_TO_WALK_TO_SELLERS_MEAN, TIME_TO_WALK_TO_SELLERS_STD)))
    walk_end = env.now
    # встать в очередь
    queue_begin = env.now
    # клиент всегда выбирает самую короткую очередь
    seller_line = pick_shortest(seller_lines)
    # ждем начала обслуживания
    with seller_line[0].request() as req:
        # подождать в очереди
        sellers.add_to_line(seller_line[1])
        yield req
        sellers.remove_from_line(seller_line[1])
        # обслуживание началось
        queue_end = env.now
        # купить билеты
        sale_begin = env.now
        yield env.timeout(rd.gauss(SELLER_MEAN, SELLER_STD))
        # билеты куплены
        sale_end = env.now
        register_group_moving_from_bus_to_seller(
            people_processed, walk_begin, walk_end, seller_line[1], queue_begin, queue_end, sale_begin, sale_end)
        # начать процесс контроля билета
        env.process(scanning_customer(env, people_processed, scanner_lines,
                                      TIME_TO_WALK_TO_SCANNERS_MEAN, TIME_TO_WALK_TO_SCANNERS_STD))


def scanning_customer(env, people_processed, scanner_lines, walk_duration, walk_std):
    """
      моделируем приход клиентов на контроль билетов, клиент тратит -
        время walk_duration на подход к контролю,
        время SCANNER_MEAN на обслуживание на контроле
    """
    # подойти к контролеру
    walk_begin = env.now
    yield env.timeout(abs(rd.gauss(walk_duration, walk_std)))
    walk_end = env.now
    # встать в очередь
    queue_begin = env.now
    # клиент всегда выбирает самую короткую очередь
    scanner_line = pick_shortest(scanner_lines)
    with scanner_line[0].request() as req:
        # подождать в очереди
        yield req
        queue_end = env.now
        # контроль билета у каждого клиента
        for person in people_processed:
            scan_begin = env.now
            yield env.timeout(abs(rd.gauss(SCANNER_MEAN, SCANNER_STD)))
            # контроль билетов пройден
            scan_end = env.now
            register_visitor_moving_to_scanner(
                person, walk_begin, walk_end, scanner_line[1], queue_begin, queue_end, scan_begin, scan_end)


# основная функция для запуска модели


def model_env():
    global seller_lines, scanner_lines, OKHO
    env = simpy.Environment()
    seller_lines = [simpy.Resource(env, capacity=SELLERS_PER_LINE)
                    for _ in range(SELLER_LINES)]
    scanner_lines = [simpy.Resource(
        env, capacity=SCANNERS_PER_LINE) for _ in range(SCANNER_LINES)]
    env.process(bus_arrival(env, seller_lines, scanner_lines))
    env.process(monitor(env))

    if OKHO:
        infoPanel()
        env.process(clockTablo(env))
    else:
        dummyPanel()
    env.run(until=45)
    if OKHO:
        mainpanel.mainloop()


def main(variant=0):
    global OKHO
    # простой запуск модели
    if variant == 1:
        OKHO = True   # выводить окно визуализации процесса!
        model_env()
    elif variant == 2:
        OKHO = False   # не выводить окно визуализации процесса!
        mainpanel.destroy()
        stat_experimentA()
    else:
        print("старт main(1) или main(2)")


def stat_experimentA():
    global ARRIVALS, ARRIVAL_ORIGIN, ON_BOARD, ON_BOARD_ORIGIN, OKHO
    global SELLER_LINES, SCANNER_LINES, seller_waits, scan_waits, seller_queues

    # эксперимент 1
    Level = 4  # кол-во уровней фактора
    numReplica = 11  # кол-во реплик на каждом уровне
    print("_Запуск эксперимента_")
    # _1_
    experiment_ds = {o: [] for o in range(Level)}
    # создадим словарь списков результатов моделирования
    for f in range(Level):
        SELLER_LINES = 4 + f
        SCANNER_LINES = 6
        print(f'_уровень ++ {f+1} ++ SELLER_LINES= {SELLER_LINES}')
        for i in range(numReplica):
            # восстановление нач.значений
            ARRIVALS = ARRIVAL_ORIGIN.copy()
            ON_BOARD = ON_BOARD_ORIGIN.copy()
            # сброс списков статистики
            arrivals = defaultdict(lambda: 0)
            seller_waits = defaultdict(lambda: [])
            scan_waits = defaultdict(lambda: [])
            seller_queues = {v: [] for v in range(SELLER_LINES)}
            #
            rd.seed(7321 + i * numReplica + f)  # установка нового случ.зерна
            model_env()  # запуск модели
            print(f'+ {f+1} + реплика_{i+1} +')
            experiment_ds[f].append(
                avg_wait(seller_waits) + avg_wait(scan_waits))
           # сохраняем результат прогона
    print(experiment_ds)
    # _2_
    print('\n_Сводная описательная статистика_\n')
    print('фактор SELLER_LINES принимал значения  [4,5,6,7]')

    from scipy import stats
    import math
    # подготовим коллекцию для сохранения результатов эксперимента
    statDescript = {'N': [0] * Level, 'smm': [0] * Level, 'sm': [0] * Level,
                    'sv': [0] * Level, 'ss': [0] * Level, 'sk': [0] * Level,
                    'D_KS': [0] * Level, 'pval_KS': [0] * Level}
    for z in range(Level):
        nn, (smin, smax), smn, sv, ss, sk = stats.describe(experiment_ds[z])
        statDescript['N'][z] = nn     # размер выборки
        statDescript['smm'][z] = (smin, smax)
        statDescript['sm'][z] = smn   # среднее выборочное
        statDescript['sv'][z] = sv    # дисперсия выборки
        statDescript['ss'][z] = ss    # skew/скос
        statDescript['sk'][z] = sk    # kurtosis/эксцесс
        print(
            f'Датасет{z}::{nn}: среднее= {round(smn,3)} | дисперсия= {round(sv,3)} | min={round(smin,3)} | max={round(smax,3)}')
        # нормализуем датасет перед тестом на нормальность
        zx = (experiment_ds[z] - smn) / math.sqrt(sv)
        # тест Колмогорова-Смирнова на нормальность распределения
        dks, pval = stats.kstest(zx, 'norm')
        print(
            f'Датасет{z}: KS-статистика: D={round(dks,4)} |  p-value= {round(pval,3)}')
        statDescript['D_KS'][z] = dks
        statDescript['pval_KS'][z] = pval

    print(statDescript)
    # _3_
    print("\n_Расчет однофакторного дисперсионного анализа ANOVA (alpha=0.05)\n")

    F, pval = stats.f_oneway(
        experiment_ds[0], experiment_ds[1], experiment_ds[2], experiment_ds[3])
    print(f' значение критерия F: {round(F,4)} |  p-value: {round(pval,4)}')


main(1)
