import pandas as pd
import numpy as np
import scipy.stats
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
class rcbd():
	def __init__(self, file_name, alpha=0.05):
		dataset = pd.read_csv(file_name)
		data = dataset.iloc[:,1:].values
		data = data.astype(np.float)
		self.no_of_treatments = np.size(data, 1)
		self.blocks = np.size(data, 0)
		sum = np.sum(data)
		bias = sum*sum/(self.no_of_treatments*self.blocks)
		self.ss_total = np.sum(np.square(data))-bias
		self.ss_treatments = np.sum(np.square(np.sum(data, axis=0)))/self.blocks-bias
		self.ss_blocks = np.sum(np.square(np.sum(data, axis=1)))/self.no_of_treatments-bias
		self.ss_error = self.ss_total - self.ss_treatments-self.ss_blocks
		self.df_total = self.no_of_treatments*self.blocks-1
		self.df_treatments = self.no_of_treatments - 1
		self.df_blocks = self.blocks - 1
		self.df_error = self.df_total - self.df_treatments - self.df_blocks
		self.ms_treatments = self.ss_treatments/self.df_treatments
		self.ms_blocks = self.ss_blocks/self.df_blocks
		self.ms_error = self.ss_error/self.df_error
		self.F_treatments = self.ms_treatments/self.ms_error
		self.F_blocks = self.ms_blocks/self.ms_error
		self.p_value_treatments = 1-scipy.stats.f.cdf(self.F_treatments, dfn=self.df_treatments, dfd=self.df_error)
		self.p_value_blocks = 1-scipy.stats.f.cdf(self.F_blocks, dfn=self.df_blocks, dfd=self.df_error)
		self.x = PrettyTable()
		self.x.set_style(MSWORD_FRIENDLY)
		self.x.field_names = ["Source of Variation", "Sum of squares", "Degrees of Freedom", "Mean Square", "F", "p value"]
		self.x.float_format["Sum of squares"] = ' 10.2'
		self.x.float_format["Mean Square"] = ' 10.2'
		self.x.float_format["F"] = ' 10.2'
		self.x.float_format["p value"] = ' 10.4'
		self.x.add_row(["Treatments", self.ss_treatments, self.df_treatments, self.ms_treatments, self.F_treatments, self.p_value_treatments])
		self.x.add_row(["Blocks", self.ss_blocks, self.df_blocks, self.ms_blocks, self.F_blocks, self.p_value_blocks])
		self.x.add_row(["Error", self.ss_error, self.df_error, self.ms_error, " ", " "])
		self.x.add_row(["Total", self.ss_total, self.df_total, " ", " ", " "])
	def print(self):
		print(self.x)
	def export(self):
		with open('result.csv', 'w') as csvFile:
			csvFile.write(self.x.get_string())
