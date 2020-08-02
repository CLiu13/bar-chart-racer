import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import datetime
import traceback
from tkinter import *
from pandas import DataFrame
from tkinter import tix, filedialog, font, messagebox, colorchooser

# determine whether to print caught exceptions
DEBUG = True

def main():

  # allows us to handle exceptions thrown by tkinter
  Tk.report_callback_exception = show_error

  window = tix.Tk()
  window.title("Bar Chart Racer")

  def show_entry_fields():
    print("Chart title: %s\nY-axis label: %s\nX-axis label: %s\nBar Number: %s" % (chart_title.get(), y_axis.get(), x_axis.get(), bslide.get()))
    chart_title.delete(0, END)
    y_axis.delete(0, END)
    x_axis.delete(0, END)

  Label(window, text="Chart title").grid(row=2, column=1)
  Label(window, text="Y-axis label").grid(row=3, column=1)
  Label(window, text="X-axis label").grid(row=4, column=1)

  chart_title = Entry(window)
  chart_title.insert(10, "Animated Bar Racer Chart")
  y_axis = Entry(window)
  y_axis.insert(10, "Categories")
  x_axis = Entry(window)
  x_axis.insert(10, "Amount")

  chart_title.grid(row=2, column=2)
  y_axis.grid(row=3, column=2)
  x_axis.grid(row=4, column=2)

  Button(window, text='Show', command=show_entry_fields).grid(row=4, column=3, sticky=W, pady=4)

  # enable/disable parse dates
  is_date = BooleanVar()
  date_checkbox = Checkbutton(window, text="Parse time column as date, " +\
    "using format string below", wraplength=150, variable=is_date,\
    justify=LEFT, onvalue=True, offvalue=False)
  date_checkbox.grid(row=5, column=2)

  date_format = Entry(window)
  date_format.grid(row=6, column=2)
  
  date_info = tix.Balloon(window)
  date_info.bind_widget(date_format, balloonmsg="Use %m for month, " +\
    "%d for day, %Y for year. For example, 12/31/1999 would have the format" +\
    " string %m/%d/%Y")

  #slider frame
  Label(window, text="Frame count").grid(row=7, column=1)
  w = Scale(window, from_=10, to=1000, orient='horizontal')
  w.grid(row=7, column=2, columnspan=2)

 # slider bars
  Label(window, text ="Number of bars").grid(row=8, column=1)
  bslide = Scale(window, from_=1, to=len(df), orient = 'horizontal')
  bslide.grid(row = 8, column=2, columnspan=2)

  # upload csv
  DEFAULT_FILENAME = "sample.csv"
  filename = StringVar()
  filename.set(DEFAULT_FILENAME)

  # characters
  LABEL_WIDTH = 30
  file_label = Label(textvariable=filename, bg='white', width=LABEL_WIDTH,\
    wraplength=LABEL_WIDTH*font.Font(font='TkDefaultFont').measure(text="0"))
  file_label.grid(row=0, column=2, columnspan=2)

  select_csv_btn = Button(text="Select csv", command=lambda:\
    select_csv(window, filename))
  select_csv_btn.grid(row=1, column=2)

  reset_csv_btn = Button(text="Reset", command=lambda:\
    filename.set(DEFAULT_FILENAME)) 
  reset_csv_btn.grid(row=1, column=3)
  
  global graph_animation

  # ensure that the variable is defined
  graph_animation = None

  # save button
  save_btn = Button(window, text="Save as", command=lambda: save_animation(window))
  save_btn.grid(row=10, column=3)
  
  # color chooser 
  has_custom_color = BooleanVar()
  color_checkbox = Checkbutton(window, text="Use custom color", variable=has_custom_color,\
    onvalue=True, offvalue=False)
  color_checkbox.grid(row=9, column=1)

  hex_color = StringVar()
  def mcolor(): 
    hex_color.set(colorchooser.askcolor()[1])
    color_label = Label(text='your chosen color', bg=hex_color.get()).grid(row=9, column=3)
  button = Button(text="Choose color", width = 30, command= mcolor)
  button.grid(row=9, column=2)
  
  # plot button
  run_btn = Button(text="Plot", command=lambda:\

    animate_df(process_data(filename.get(), w.get(), bslide.get(), is_date.get(), date_format.get()),\
      chart_title.get(), y_axis.get(), x_axis.get(), bslide.get(), has_custom_color.get(), hex_color.get()))
  run_btn.grid(row=10, columnspan=2)

  window.mainloop()

def show_error(*args):
  if DEBUG:
    traceback.print_exc()
  messagebox.showerror("An error occurred", "Please try again.")
  
def run_animation(filename, num_frames, is_date, format_string,\
  chart_title, y_label, x_label, has_custom_color, hex_color):
  
  dataframe = process_data(filename, num_frames, is_date, format_string)
  if dataframe is not None:
    animation_successful = animate_df(dataframe, chart_title, y_label, x_label,\
      has_custom_color, hex_color)
    if not animation_successful:
      messagebox.showerror("Unable to create animation", "There was an issue " +\
        "while creating your animation. Please try again.")
  else:
    messagebox.showerror("Unable to process your data", "Check that your " +\
      "file is in the correct format. The first column should be the time - " +\
      "either an integer or a date (you must provide the format of the date " +\
      "for it to be processed correctly). The top row should contain your " +\
      "category names.")


def select_csv(window, filename_var):
  selected_filename = filedialog.askopenfilename(parent=window,\
    title="Choose your data", filetypes=[("csv files", ".csv")])

  # only set if file was selected
  if selected_filename:
    filename_var.set(selected_filename)



def process_data(file_name, num_frames, bars_shown, is_date=False, format_string="%m/%d/%Y"):
  df = pd.read_csv(file_name)
  index_col_name = df.columns[0]
  df = df.set_index(index_col_name)

  
  df = df.fillna(value=0)

def save_animation(window):
  if not graph_animation:
    messagebox.showwarning("No animation", "You cannot save until " +\
      "you have run the animation.")
  else:
    try:
      filename = filedialog.asksaveasfilename(parent=window,\
        title="Choose save location", filetypes=[("gif", ".gif"), ("mp4", ".mp4")],\
          defaultextension=".gif")
      writer = 'ffmpeg'
      if filename:
        if filename.endswith('gif'):
          writer = animation.PillowWriter()
        elif not filename.endswith('mp4'):
          filename += ".gif"
        graph_animation.save(filename, writer=writer)
    except:
      messagebox.showerror("Unable to save animation", "There was an issue " +\
        "saving your animation. Make sure you entered a valid filename and " +\
        "that the animation you want to save is still running.")
      if DEBUG:
        traceback.print_exc()


def process_data(file_name, num_frames, is_date=False, format_string="%m/%d/%Y"):
  try:
    df = pd.read_csv(file_name)
    index_col_name = df.columns[0]
    df = df.set_index(index_col_name)
    
    df = df.fillna(value=0)


    if is_date:
      df = df.reset_index()
      df[index_col_name] = df[index_col_name].apply(lambda x:\
        int(datetime.datetime.strptime(x, format_string).strftime("%Y%m%d")))
      df = df.set_index(index_col_name)
      
    # this only works right if the data is already sorted
    first_idx = df.index[0]
    last_idx = df.index[len(df.index) - 1]

    # add one row for each year, this will not work
    # well for every dataset (room for improvement here)
    indices = range(first_idx, last_idx + 1)
    df = df.reindex(indices)
    df = df.interpolate()

    row_num = df.index.size

    if row_num < num_frames:
      df = expand_df(df, num_frames)
    elif row_num > num_frames:
      df = condense_df(df, num_frames)

    return df
  except:
    if DEBUG:
      traceback.print_exc()

def condense_df(df, num_frames):
  row_num = df.index.size
  step = round(row_num / num_frames)

  dfempty = pd.DataFrame()
  for i in range(0, len(df) + 1, step):
    dfempty = dfempty.append(df.iloc[i])

  return dfempty

def expand_df(df, num_frames):
  row_num = df.index.size
  step = round(num_frames / row_num)

  # rescale - when number of rows is too small
  # remove date as our index column
  df = df.reset_index()
  new_idx = pd.Series(range(step, step * row_num + 1, step)) 
  df = df.set_index(new_idx)
  indices = range(new_idx[0], new_idx[len(new_idx) - 1] + 1)
  df = df.reindex(indices)
  df = df.interpolate()

  df = df.set_index(df.columns[0])

  return df

def animate_df(df, title, ylabel, xlabel, bars_shown, has_custom_color, color_hex):
  try:
    num_bars = len(df.columns)

    if not has_custom_color:
      colors = rand_colors(num_bars, min_val=0.5,    max_val=0.9)

    max_bar = df.max().max()
    min_bar = df.min().min()

    x_max = max_bar + (max_bar - min_bar) * 0.05
    x_min = min_bar - (max_bar - min_bar) * 0.01

    fig, ax = plt.subplots()
  
  num_bars = len(df.columns)
  colors   = rand_colors(num_bars, min_val=0.5,    max_val=0.9)
   
  fig = plt.figure()

  def draw_graph(frame):
    plt.cla()
    ax = plt.axes(label=str(frame))
    length = len(df)
    my_list =[]
    categories = []
    new_colors = []

    series        = df.iloc[frame] #selects ith row
    rank          = series.rank(method = 'first', ascending=0)

    for i in range(1,bars_shown+1):
      for j in range(len(series)):
        if rank[j] == i:
          my_list.append(series[j])
          categories.append(series.index[j])
          new_colors.append(colors[j])
    
    values = my_list # x-axis
   
    max_bar = df.max().max()
    min_bar = df.min().min()

    x_max = max_bar + (max_bar - min_bar) * 0.05
    x_min = min_bar - (max_bar - min_bar) * 0.01

       
    ax.set_xlim(left=x_min, right=x_max)
    ax.barh(range(bars_shown+1,1,-1), values, tick_label=categories, color=new_colors)

    if has_custom_color:
      ax.barh(rank, values, tick_label=categories, color=color_hex)
     else:
      ax.barh(rank, values, tick_label=categories, color=colors)

     plt.title(title)
     plt.ylabel(ylabel)
     plt.xlabel(xlabel)

    global graph_animation
    graph_animation = animation.FuncAnimation(fig, draw_graph, range(len(df)), interval=50, repeat_delay=100)
 
    plt.show()
    
    return True

  except:
    if DEBUG:
      traceback.print_exc()
    return False


def rand_colors(num_colors, min_val=0, max_val=1):
    colors = []
    for i in range(num_colors):
      r = random.uniform(min_val, max_val)
      g = random.uniform(min_val, max_val)
      b = random.uniform(min_val, max_val)
      colors.append((r, g, b))
    return colors

main()
