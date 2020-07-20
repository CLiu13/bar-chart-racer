  
 import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animate
import random
import datetime

def main():
  
  # put input part here

  # df = process_data('cases_by_country.csv', 100, True, "%d/%m/%Y")
  df = process_data('sample.csv', 1000)
  animate_df(df)

def process_data(file_name, num_frames, is_date=False, format_string="%m/%d/%Y"):
  df = pd.read_csv(file_name, index_col='Date')
  
  df = df.fillna(value=0)

  if is_date:
    df = df.reset_index()
    
    df['Date'] =  df['Date'].apply(lambda x: int(datetime.datetime.strptime(x, format_string).strftime("%Y%m%d")))
    print(df.index)
    df = df.set_index('Date')
    print(df.index)

  # this only works right if the data is already sorted
  first_idx = df.index[0]
  last_idx = df.index[len(df.index) - 1]

  # add one row for each year, this will not work
  # well for every dataset (room for improvement here)
  indices = range(first_idx, last_idx + 1)
  df = df.reindex(indices)
  df = df.interpolate()

  row_num = df.index.size
  print(row_num)

  if row_num < num_frames:
    df = expand_df(df, num_frames)
<<<<<<< HEAD
  else:
    df = condense_df(df, frame_num):

def condense_df(df, frame_num):
 
  dfempty = pd.DataFrame()

  for i in range(0, len(df) + 1, 2):
    print(df.iloc[i])
    dfempty = dfempty.append(df.iloc[i])
    
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

  df = df.set_index('Date')

  return df

=======

  return df

def expand_df(df, num_frames):
  step = num_frames // df.index.size

  # rescale - when number of rows is too small 
  df = df.reset_index() # remove date as our index column
  new_idx = pd.Series(range(step, num_frames + 1, step)) 
  df = df.set_index(new_idx)
  indices = range(new_idx[0], new_idx[len(new_idx) - 1] + 1)
  df = df.reindex(indices)
  df = df.interpolate()

  df = df.set_index('Date')

  return df

>>>>>>> d98283d4ae96251831ee16bd2cffd5846f4ec489

def animate_df(df):
  num_bars = len(df.iloc[0])
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

  animation = animate.FuncAnimation(fig, draw_graph, range(len(df)), interval=50, repeat_delay=100)

  plt.show()

def rand_colors(num_colors, min_val=0, max_val=1):
    # input validation
    if min_val < 0 or min_val > 1:
      min_val = 0
    if max_val < 0 or max_val > 1:
      max_val = 1
    if min_val > max_val:
      temp = min_val
      min_val = max_val
      max_val = temp
    
    colors = []
    for i in range(num_colors):
      r = random.uniform(min_val, max_val)
      g = random.uniform(min_val, max_val)
      b = random.uniform(min_val, max_val)
      colors.append((r, g, b))
    return colors

main()
© 2020 GitHub, Inc.
