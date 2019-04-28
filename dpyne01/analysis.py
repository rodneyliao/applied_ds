from io_hw import io_hw
import pandas as pd
import matplotlib.pyplot as pyplot
import matplotlib.cm as cm
import numpy as np
import math

def analysis():
	obese, drink, inactive, fastfood = read_data()
	fig = pyplot.figure()
	plot(obese, drink, 1, fig)
	plot(obese, inactive, 2, fig)
	plot(obese, fastfood, 3, fig)
	drink_corr = correlation(obese, drink)
	inactive_corr = correlation(obese, inactive)
	fastfood_corr = correlation(obese, fastfood)
	highest_corr = max([drink_corr, inactive_corr, fastfood_corr], key=abs)
	zip_corr = [("Drink Correlation", drink_corr), 
				("Inactivity Correlation", inactive_corr), 
				("Fast Food Correlation", fastfood_corr)]
	highest_corr_name = [x for (x, y) in zip_corr if highest_corr==y]
	print(highest_corr_name[0] + ": " + str(highest_corr))
	pyplot.show()
	#plot_all(obese, drink, inactive, fastfood)





def read_data():
	df, head_df = io_hw('data.csv')
	obese = df.iloc[:, 3].tolist()
	drink = df.iloc[:, 4].tolist()
	inactive = df.iloc[:, 5].tolist()
	fastfood = df.iloc[:, 6].tolist()
	return obese, drink, inactive, fastfood

def plot_all(obese, drink, inactive, fastfood):
	ziplist = zip(obese, drink, inactive, fastfood)
	o_clean = [x for (x, y, z, w) in ziplist if not math.isnan(w)]
	ziplist = zip(obese, drink, inactive, fastfood)
	d_clean = [y for (x, y, z, w) in ziplist if not math.isnan(w)]
	ziplist = zip(obese, drink, inactive, fastfood)
	i_clean = [z for (x, y, z, w) in ziplist if not math.isnan(w)]
	ziplist = zip(obese, drink, inactive, fastfood)
	f_clean = [w for (x, y, z, w) in ziplist if not math.isnan(w)]

	df_dict = {"Obesity": obese, "Binge Drinking": drink, "Inactivity": inactive, "Fast Food Proximity": fastfood}
	df = pd.DataFrame(df_dict)
	fig = pyplot.figure()
	ax = fig.add_subplot(111)
	cmap = cm.get_cmap('jet', 30)
	cax = ax.imshow(df.corr(), interpolation = "nearest", cmap = cmap)
	ax.grid(True)
	pyplot.title('Correlation Between Test Variables and Obesity')
	labels = ["", "Obesity", "", "Binge Drinking", "", "Inactivity", "", "Fast Food", ""]
	ax.set_xticklabels(labels)
	ax.set_yticklabels(labels)
	fig.colorbar(cax)
	pyplot.show()
	

def plot(x_init, y_init, index, fig):
	fig.add_subplot(3, 1, index)
	x, y = clean(x_init, y_init)
	curr_plot = pyplot.scatter(x, y)


def correlation(x_init, y_init):
	x, y = clean(x_init, y_init)
	x_np = np.array(x)
	y_np = np.array(y)
	return np.corrcoef(x_np, y_np)[0][1]

def clean(x_init, y_init):
	ziplist = zip(x_init, y_init)
	x_clean = [x for (x, y) in ziplist if not math.isnan(y)]
	ziplist = zip(x_init, y_init)
	y_clean = [y for (x, y) in ziplist if not math.isnan(y)]
	return x_clean, y_clean


analysis()
