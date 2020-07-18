import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animate
import random

def main():
  
  # put input part here

  df = process_data('cases_by_country.csv')
  animate_df(df)

def process_data(file_name):
  df = pd.read_csv(file_name, index_col='Date')

  #####
  # this part is specific to parsing the dates in the covid data file
  df = df.fillna(value=0)

  is_date = True
  if is_date:
    format_string = "%d/%m/%Y"
    
    df['Date'].apply(lambda x: int(datetime.datetime.strptime(x, format_string).strftime("%Y%m%d")))
    print(df.index)

  df.set_index('Date')
  ######

  # this only works right if the data is already sorted
  first_idx = df.index[0]
  last_idx = df.index[len(df.index) - 1]

  # add one row for each year, this will not work
  # well for every dataset (room for improvement here)
  indices = range(first_idx, last_idx + 1)
  df = df.reindex(indices)
  df = df.interpolate()

  return df

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