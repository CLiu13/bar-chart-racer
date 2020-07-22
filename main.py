import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import datetime
from tkinter import Tk, filedialog, Label, Button, Entry, StringVar, font

def main():
  window = Tk()
  window.title("Bar Chart Racer")

  # upload csv
  DEFAULT_FILENAME = "sample.csv"
  filename = StringVar()
  filename.set(DEFAULT_FILENAME)
  
  LABEL_WIDTH = 30 # characters
  file_label = Label(textvariable=filename, bg='white', width=LABEL_WIDTH,\
    wraplength=LABEL_WIDTH*font.Font(font='TkDefaultFont').measure(text="0"))
  file_label.grid(row=0, column=1, columnspan=2)

  select_csv_btn = Button(text="select csv", command=lambda: select_csv(window, filename))
  select_csv_btn.grid(row=1, column=1)

  reset_csv_btn = Button(text="reset", command=lambda: filename.set(DEFAULT_FILENAME)) 
  reset_csv_btn.grid(row=1, column=2)

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
 
  dfempty = pd.DataFrame()

  for i in range(0, len(df) + 1, 2):
    print(df.iloc[i])
    dfempty = dfempty.append(df.iloc[i])
    
  print(dfempty)
  return dfempty

def expand_df(df, num_frames):
  step = num_frames // df.index.size

  # rescale - when number of rows is too small 
  df = df.reset_index() # remove date as our index column
  new_idx = pd.Series(range(step, num_frames + 1, step)) 
  df = df.set_index(new_idx)
  indices = range(new_idx[0], new_idx[len(new_idx) - 1] + 1)
  df = df.reindex(indices)
  df = df.interpolate()

  df = df.set_index(df.columns[0])

  return df

def animate_df(df):
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
    plt.title('Animated Bar Racer Chart')

    plt.ylabel('Categories')
    plt.xlabel('Amount')

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