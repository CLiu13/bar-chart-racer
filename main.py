import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import datetime
from tkinter import *
from tkinter import font, filedialog

def main():
  window = Tk()
  window.title("Bar Chart Racer")
  
  #titles
  def show_entry_fields():
    print("Chart title: %s\nY-axis label: %s\nX-axis label: %s" % (chart_title.get(), y_axis.get(), x_axis.get()))
    chart_title.delete(0, END)
    y_axis.delete(0, END)
    x_axis.delete(0, END)

  Label(window, text="Chart title").grid(row=2)
  Label(window, text="Y-axis label").grid(row=3)
  Label(window, text="X-axis label").grid(row=4)

  chart_title = Entry(window)
  chart_title.insert(10, "Animated Bar Racer Chart")
  y_axis = Entry(window)
  y_axis.insert(10, "Amount")
  x_axis = Entry(window)
  x_axis.insert(10, "Categories")

  chart_title.grid(row=2, column=1)
  y_axis.grid(row=3, column=1)
  x_axis.grid(row=4, column=1)
        
  Button(window, text='Show', command=show_entry_fields).grid(row=4, column=2, sticky=W, pady=4)
  
  #slider
  Label(window, text="Frame count").grid(row=5, column=0)
  w = Scale(window, from_=10, to=1000, orient='horizontal')
  w.grid(row=5, column=1, columnspan=2)
   
  # upload csv
  DEFAULT_FILENAME = "sample.csv"
  filename = StringVar()
  filename.set(DEFAULT_FILENAME)
  
  LABEL_WIDTH = 30 # characters
  file_label = Label(textvariable=filename, bg='white', width=LABEL_WIDTH,\
    wraplength=LABEL_WIDTH*font.Font(font='TkDefaultFont').measure(text="0"))
  file_label.grid(row=0, column=1, columnspan=2)

  select_csv_btn = Button(text="Select csv", command=lambda:\
    select_csv(window, filename))
  select_csv_btn.grid(row=1, column=1)

  reset_csv_btn = Button(text="Reset", command=lambda:\
    filename.set(DEFAULT_FILENAME)) 
  reset_csv_btn.grid(row=1, column=2, sticky=W, pady=4)

  # run button
  run_btn = Button(text="Plot", command=lambda:\
    animate_df(process_data(filename.get(), w.get()), chart_title.get(), y_axis.get(), x_axis.get()))
  run_btn.grid(row=10, columnspan=2)

  window.mainloop()

def select_csv(window, filename_var):
  selected_filename = filedialog.askopenfilename(parent=window,\
    title="Choose your data", filetypes=[("csv files", ".csv")])
  
  # only set if file was selected
  if selected_filename:
    filename_var.set(selected_filename)

def process_data(file_name, num_frames, is_date=False, format_string="%m/%d/%Y"):
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

def animate_df(df, title, ylabel, xlabel):
  num_bars = len(df.columns)
  colors   = rand_colors(num_bars, min_val=0.5,    max_val=0.9)

  max_bar = df.max().max()
  min_bar = df.min().min()

  x_max = max_bar + (max_bar - min_bar) * 0.05
  x_min = min_bar - (max_bar - min_bar) * 0.01
  
  fig = plt.figure()
  
  # note - maybe we could make this a function outside of this one?
  def draw_graph(frame):
    ax = plt.axes(label=str(frame))
    
    series        = df.iloc[frame] #selects ith row
    rank          = series.rank(method='first')
    # to do: only show certain max number of bars
    categories    = series.index
    values        = series.array # y-axis
    
    ax.set_xlim(left=x_min, right=x_max)
    ax.barh(rank, values, tick_label=categories, color=colors)
    plt.title(title)

    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

  graph_animation = animation.FuncAnimation(fig, draw_graph, range(len(df)), interval=50, repeat_delay=100)

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
