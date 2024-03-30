import tools
import tkinter as tk
import random
from tkinter import filedialog
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from angle_calculate import angle_compare
from distance_calculate import dist_compare
from datetime import datetime, timedelta


def browse_file(entry):
    file = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file)


def show(act: str):
    if act == "no_file_error":
        alert = "请先选择输入文件！"
    elif act == "no_result_error":
        alert = "请先进行校核计算！"
    elif act == "rename_finished":
        alert = "已对筛选观测重设编号！"
    elif act == "retiming_finished":
        alert = "已对筛选观测重设时间戳！"
    else:
        alert = "错误"
    error_window = tk.Toplevel(root)
    error_window.title("注意")
    error_label = tk.Label(error_window, text=alert, padx=20, pady=20)
    error_label.pack()
    error_window.geometry("200x100")
    error_window.geometry("+%d+%d" % (root.winfo_rootx() + root.winfo_width() / 2
                                      - error_window.winfo_reqwidth() / 2,
                                      root.winfo_rooty() + root.winfo_height() / 2
                                      - error_window.winfo_reqheight() / 2))
    close_button = ttk.Button(error_window, text="确定", command=error_window.destroy)
    close_button.pack()


def dist_check(level=2):
    if not rtk_trans_entry.get() or not ts_entry.get():
        show("no_file_error")
    else:
        dist_pairs, dist_errors = dist_compare(rtk_trans_entry.get(), ts_entry.get(), selection.get())
        dist_pairs = tools.output_format(dist_pairs)
        dist_result_text.delete(1.0, tk.END)
        dist_pairs = '按边长校核最优观测点号： \n' + dist_pairs
        dist_result_text.insert(0.0, dist_pairs)

        dist_errors = tools.errors_format(dist_errors,"dist")
        dist_errors_text.delete(1.0, tk.END)
        dist_errors = dist_errors
        dist_errors_text.insert(0.0, dist_errors)


def angle_check(level):
    if not rtk_trans_entry.get() or not ts_entry.get():
        show("no_file_error")
    else:
        angle_pairs, angle_errors = angle_compare(rtk_trans_entry.get(), ts_entry.get())
        angle_pairs = tools.output_format(angle_pairs)
        angle_result_text.delete(1.0, tk.END)
        angle_pairs = '按角度校核最优观测点号： \n' + angle_pairs
        angle_result_text.insert(0.0, angle_pairs)

        angle_errors = tools.errors_format(angle_errors,"angel")
        angle_errors_text.delete(1.0, tk.END)
        angle_errors = angle_errors
        angle_errors_text.insert(0.0, angle_errors)


def re_number(rule, level=2):
    if not rtk_org_entry.get() and rtk_trans_entry.get():
        show("no_file_error")
    else:
        rtk_org = rtk_org_entry.get()
        rtk_trans = rtk_trans_entry.get()
        dist_result = dist_result_text.get(1.0, tk.END)
        angle_result = angle_result_text.get(1.0, tk.END)
        if rule == 'dist':
            tools.rtk_rename(rtk_org, dist_result, level)
            tools.rtk_rename(rtk_trans, dist_result, level)
            show("rename_finished")
        elif rule == 'angel':
            tools.rtk_rename(rtk_org, angle_result, level)
            tools.rtk_rename(rtk_trans, angle_result, level)
            show("rename_finished")
        else:
            show(" ")


def re_number_pop(level):
    rtk_org = rtk_org_entry.get()
    rtk_trans = rtk_trans_entry.get()
    ts_org = ts_entry.get()
    if not rtk_org and not rtk_trans and not ts_org:
        show("no_file_error")
    elif not dist_result_text.get("1.0", "end-1c"):
        show("no_result_error")
    else:
        rename_window = tk.Toplevel(root)
        rename_window.title("重设编号")

        selected_var = tk.StringVar()
        selected_var.set(" ")
        option1 = tk.Radiobutton(rename_window,
                                 text="按边长校核结果重设编号",
                                 variable=selected_var,
                                 value="dist")
        option2 = tk.Radiobutton(rename_window,
                                 text="按角度校核结果重设编号",
                                 variable=selected_var,
                                 value="angel")

        option1.pack(padx=10, pady=10, anchor=tk.N)
        option2.pack(padx=10, pady=10, anchor=tk.N)

        confirm_button = ttk.Button(rename_window,
                                    text="确定",
                                    command=lambda: re_number(selected_var.get(), level))
        confirm_button.pack(padx=10, anchor=tk.S)
        rename_window.geometry("250x150+%d+%d" % (root.winfo_rootx() + root.winfo_width() / 2 -
                                                  rename_window.winfo_reqwidth() / 2,
                                                  root.winfo_rooty() + root.winfo_height() / 2 -
                                                  rename_window.winfo_reqheight() / 2))


def re_time_pop(level):
    rtk_org = rtk_org_entry.get()
    if not rtk_org:
        show("no_file_error")
    else:
        retiming_window = tk.Toplevel(root)
        retiming_window.title("重设时间戳")
        hint_label = tk.Label(retiming_window, text='设置观测开始时间：', anchor="w")
        hint_label.pack(padx=10)
        date_frame = tk.Frame(retiming_window)
        date_frame.pack(padx=5, pady=5)
        year_text = tk.Text(date_frame, width=5, height=1, font=("Times New Roman", 12))
        year_label = tk.Label(date_frame, text="年", anchor="w")
        month_text = tk.Text(date_frame, width=2, height=1, font=("Times New Roman", 12))
        month_label = tk.Label(date_frame, text="月", anchor="w")
        day_text = tk.Text(date_frame, width=2, height=1, font=("Times New Roman", 12))
        day_label = tk.Label(date_frame, text="日", anchor="w")
        hour_text = tk.Text(date_frame, width=2, height=1, font=("Times New Roman", 12))
        hour_label = tk.Label(date_frame, text="时", anchor="w")
        minute_text = tk.Text(date_frame, width=2, height=1, font=("Times New Roman", 12))
        minute_label = tk.Label(date_frame, text="分", anchor="w")
        second_text = tk.Text(date_frame, width=2, height=1, font=("Times New Roman", 12))
        second_label = tk.Label(date_frame, text="秒", anchor="w")
        year_text.pack(side="left", padx=5, pady=5, anchor="w")
        year_label.pack(side="left", padx=5, pady=5)
        month_text.pack(side="left", padx=5, pady=5, anchor="w")
        month_label.pack(side="left", padx=5, pady=5)
        day_text.pack(side="left", padx=5, pady=5, anchor="w")
        day_label.pack(side="left", padx=5, pady=5)
        hour_text.pack(side="left", padx=5, pady=5, anchor="w")
        hour_label.pack(side="left", padx=5, pady=5)
        minute_text.pack(side="left", padx=5, pady=5, anchor="w")
        minute_label.pack(side="left", padx=5, pady=5)
        second_text.pack(side="left", padx=5, pady=5, anchor="w")
        second_label.pack(side="left", padx=5, pady=5)
        confirm_button = ttk.Button(retiming_window,
                                    text="确定",
                                    command=lambda: re_timing(rtk_org, level,
                                                              [year_text.get(0.0, tk.END),
                                                               month_text.get(0.0, tk.END),
                                                               day_text.get(0.0, tk.END),
                                                               hour_text.get(0.0, tk.END),
                                                               minute_text.get(0.0, tk.END),
                                                               second_text.get(0.0, tk.END)]))
        confirm_button.pack(padx=10, anchor=tk.S)
        retiming_window.geometry("500x100+%d+%d" % (root.winfo_rootx() + root.winfo_width() / 2 -
                                                    retiming_window.winfo_reqwidth() / 2,
                                                    root.winfo_rooty() + root.winfo_height() / 2 -
                                                    retiming_window.winfo_reqheight() / 2))


def re_timing(rtk_path, level, start_time):
    if '\n' not in start_time and int(start_time[0]) > 1900:
        t = ' '.join(start_time).replace('\n', '')
        t = datetime.strptime(t, '%Y %m %d %H %M %S')
        new_rtk_path = rtk_path.replace('.txt', '') + '_new.txt'
        new_time_path = rtk_path.replace('.txt', '') + '_new_time.txt'
        time_list = []
        new_records = []
        with open(new_rtk_path, 'r', encoding='utf-8-sig') as rtk:
            rtk_records = rtk.readlines()
        rtk_records = rtk_records[1:]
        p_number = int(len(rtk_records) / (level * 2))
        for i in range(p_number):
            time_stick = time_gene(t)
            time_list += time_stick
            t = t + timedelta(minutes=random.randint(10, 20))
        for r in rtk_records:
            idx = rtk_records.index(r)
            r = r.split(' ')
            r = ' '.join(r[:-4])
            new_time = datetime.strftime(time_list[idx], "%H:%M:%S %d %m月 %Y")
            r += ' ' + new_time
            new_records.append(r)
        with open(new_time_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(new_records))
        show("retiming_finished")


def time_gene(t, level=4):
    new_t = []
    if level == 4:
        t1 = t
        t2 = t1 + timedelta(minutes=1, seconds=random.randint(1, 60))
        t3 = t2 + timedelta(hours=1, seconds=random.randint(1, 60))
        t4 = t3 + timedelta(minutes=1, seconds=random.randint(1, 60))
        new_t = t1, t2, t3, t4
    if level == 6:
        t1 = t
        t2 = t1 + timedelta(minutes=1, seconds=random.randint(1, 60))
        t3 = t2 + timedelta(minutes=1, seconds=random.randint(1, 60))
        t4 = t3 + timedelta(hours=1, seconds=random.randint(1, 60))
        t5 = t4 + timedelta(minutes=1, seconds=random.randint(1, 60))
        t6 = t5 + timedelta(minutes=1, seconds=random.randint(1, 60))
        new_t = t1, t2, t3, t4, t5, t6
    return new_t


# 创建主窗口
root = tk.Tk()
root.title('RTK-全站仪观测数据校核')
root.configure(bg="#F8F8FF")
# 使用ttk模块创建主题按钮样式
style = ttk.Style()

# 创建Frame
rtk_org_frame = tk.Frame(root, bg="#F8F8FF")
rtk_file_frame = tk.Frame(root, bg="#F8F8FF")
ts_file_frame = tk.Frame(root, bg="#F8F8FF")
radio_frame = tk.Frame(root)
button_frame = tk.Frame(root, bg="#F8F8FF")
dist_frame = tk.Frame(root, bg="#F8F8FF")
angle_frame = tk.Frame(root, bg="#F8F8FF")

# 创建标签、输入框和按钮
rtk_org_label = tk.Label(rtk_org_frame, text="RTK原始观测文件:", bg="#F8F8FF")
rtk_org_entry = tk.Entry(rtk_org_frame)
rtk_org_button = ttk.Button(rtk_org_frame, text="浏览", command=lambda: browse_file(rtk_org_entry))

rtk_label = tk.Label(rtk_file_frame, text="RTK转换观测文件:", bg="#F8F8FF")
rtk_trans_entry = tk.Entry(rtk_file_frame)
rtk_browse_button = ttk.Button(rtk_file_frame, text="浏览", command=lambda: browse_file(rtk_trans_entry))

ts_label = tk.Label(ts_file_frame, text="全站仪观测文件:", bg="#F8F8FF")
ts_entry = tk.Entry(ts_file_frame)
ts_browse_button = ttk.Button(ts_file_frame, text="浏览", command=lambda: browse_file(ts_entry))

selection = tk.IntVar()
selection.set(2)
radio_label = tk.Label(radio_frame, text="控制等级:")
radio1 = tk.Radiobutton(radio_frame, text="图根", variable=selection, value=2)
radio2 = tk.Radiobutton(radio_frame, text="三级", variable=selection, value=3)
dist_cal_button = ttk.Button(button_frame, text="按边长校核", command=lambda: dist_check(selection.get()))
angle_cal_button = ttk.Button(button_frame, text="按夹角校核", command=lambda: angle_check(selection.get()))
renumber_button = ttk.Button(button_frame, text="重设编号", command=lambda: re_number_pop(selection.get()))
# retime_button = ttk.Button(button_frame, text="重设时间戳", command=lambda: re_time_pop(selection.get()))

# 创建结果显示的文本框
dist_result_label = tk.Label(dist_frame, text="边长校核结果:", bg="#F8F8FF", anchor="w")
dist_result_text = ScrolledText(dist_frame, width=40, height=10, font=("Times New Roman", 12))

dist_errors_label = tk.Label(dist_frame, text="边长校核误差（米）", bg="#F8F8FF", anchor="w")
dist_errors_text = ScrolledText(dist_frame, width=40, height=10, font=("Times New Roman", 12))

angle_errors_label = tk.Label(angle_frame, text="角度校核误差（度分秒）:", bg="#F8F8FF", anchor="w")
angle_errors_text = ScrolledText(angle_frame, width=40, height=10, font=("Times New Roman", 12))

angle_result_label = tk.Label(angle_frame, text="角度校核结果:", bg="#F8F8FF", anchor="w")
angle_result_text = ScrolledText(angle_frame, width=40, height=10, font=("Times New Roman", 12))

# 布局
rtk_org_frame.pack(fill="x", padx=5, pady=5)
rtk_org_label.pack(side="left", padx=5, pady=5, anchor="w")
rtk_org_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")
rtk_org_button.pack(side="left", padx=5, pady=5)

rtk_file_frame.pack(fill="x", padx=5, pady=5)
rtk_label.pack(side="left", padx=5, pady=5, anchor="w")
rtk_trans_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")
rtk_browse_button.pack(side="left", padx=5, pady=5)

ts_file_frame.pack(fill="x", padx=5, pady=5)
ts_label.pack(side="left", padx=5, pady=5, anchor="w")
ts_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")
ts_browse_button.pack(side="left", padx=5, pady=5)

radio_frame.pack(fill="x", padx=5, pady=5)
radio_label.pack(side="left", padx=5, pady=5)
radio1.pack(side="left", padx=5, pady=5)
radio2.pack(side="left", padx=5, pady=5)
button_frame.pack(padx=10, pady=5)
dist_cal_button.pack(side="left", padx=5)
angle_cal_button.pack(side="left", padx=5)
renumber_button.pack(side="left", padx=5)


# 存放点号选取结果
dist_frame.pack(side="left", padx=5, expand=True)
dist_result_label.pack(side="top", anchor="w")
dist_result_text.pack(side="top", fill="x")
dist_errors_label.pack(side="top", anchor="w")
dist_errors_text.pack(side="top", fill="x")

angle_frame.pack(side="left", padx=5, expand=True)
angle_result_label.pack(side="top", anchor="w")
angle_result_text.pack(side="top", fill="x")

angle_errors_label.pack(side="top", anchor="w")
angle_errors_text.pack(side="top", fill="x")

root.geometry("700x700+700+200")
root.mainloop()
