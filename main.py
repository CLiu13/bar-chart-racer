import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import datetime
from tkinter import *
from tkinter import font, filedialog
from tkinter import tix
from pandas import DataFrame

def main():

  window = tix.Tk()
  window.title("Bar Chart Racer")

  #titles
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
  bslide = Scale(window, from_=1, to=20, orient = 'horizontal')
  bslide.grid(row = 8, column=2, columnspan=2)
  bars_shown = bslide.get()


  #bslide.pack()
     
  # upload csv
  DEFAULT_FILENAME = "sample.csv"
  filename = StringVar()
  filename.set(DEFAULT_FILENAME)
  
  LABEL_WIDTH = 30 # characters
  file_label = Label(textvariable=filename, bg='white', width=LABEL_WIDTH,\
    wraplength=LABEL_WIDTH*font.Font(font='TkDefaultFont').measure(text="0"))
  file_label.grid(row=0, column=2, columnspan=2)

  select_csv_btn = Button(text="Select csv", command=lambda:\
    select_csv(window, filename))
  select_csv_btn.grid(row=1, column=2)

  reset_csv_btn = Button(text="Reset", command=lambda:\
    filename.set(DEFAULT_FILENAME)) 
  reset_csv_btn.grid(row=1, column=3)

  # plot button
  run_btn = Button(text="Plot", command=lambda:\
    animate_df(process_data(filename.get(), w.get(), bslide.get(), is_date.get(), date_format.get()),\
      chart_title.get(), y_axis.get(), x_axis.get(), bslide.get()))
  run_btn.grid(row=9, columnspan=3)

  window.mainloop()


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

  if is_date:
    df = df.reset_index()    
    df[index_col_name] =  df[index_col_name].apply(lambda x:\
      int(datetime.datetime.strptime(x, format_string).strftime("%Y%m%d")))
    df = df.set_index(index_col_name)

  # this only works right if the data is already sorted
  first_idx = df.index[0]
  last_idx = df.index[len(df) - 1]

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
  df = df.reset_index() # remove date as our index column
  new_idx = pd.Series(range(step, step * row_num + 1, step)) 
  df = df.set_index(new_idx)
  indices = range(new_idx[0], new_idx[len(new_idx) - 1] + 1)
  df = df.reindex(indices)
  df = df.interpolate()

  df = df.set_index(df.columns[0])

  return df

def animate_df(df, title, ylabel, xlabel, bars_shown):
  num_bars = len(df.columns)
  colors   = rand_colors(num_bars, min_val=0.5,    max_val=0.9)
   
  fig = plt.figure()

  def draw_graph(frame):
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

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

  graph_animation = animation.FuncAnimation(fig, draw_graph, range(len(df)), interval=500, repeat_delay=100)
  plt.show()

def rand_colors(num_colors, min_val=0, max_val=1):
    colors = []
    for i in range(num_colors):
      r = random.uniform(min_val, max_val)
      g = random.uniform(min_val, max_val)
      b = random.uniform(min_val, max_val)
      colors.append((r, g, b))
    return colors

main()
