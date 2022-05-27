
import numpy as np
import pandas as pd
import netCDF4 as nc


class OperationNetCDF():
	def __init__(self, NcFileName:str):
		self.NcFileName = NcFileName		# NetCDFのファイル名

	def read_file(self):
		""" ファイルの読み込み """
		self.NcData	= nc.Dataset(self.NcFileName, "r")
		
	def check_variable_keys(self, LogFileName:str=""):
		""" 変数名の確認（ログの出力） """
		self.read_file()
		
		# ログファイルに書き込み
		# ---------------------------------------
		if LogFileName == "":
			LogFileName	= self.NcFileName.replace(".nc", "_explanation.txt")
		OutFile	= open(LogFileName, "w", encoding="shift-jis")
		for key1 in self.NcData.variables.keys():
			if LogFileName != "":
				OutFile.write(f"------------  {key1}  --------------\n")
				OutFile.write(str(self.NcData[key1]))
				OutFile.write("\n\n\n")
		OutFile.close()

		# 画面出力
		# ---------------------------------------
		with open(LogFileName, "r") as file:
			print(file.read())

	def get_data_from_nc(self, VariableList:list=[]):
		"""
		変数データを取得して、配列を辞書型で返す
		Dic[VariableName]	= np.array()
		"""
		self.read_file()

		ReturnDic	= {}
		for var in VariableList:
			ReturnDic[var]	= np.array(self.NcData[var])
		return ReturnDic



class OperationPandas():
	def __init__(self, df1):
		self.df1	= df1		# 編集したいデータフレーム

	def Str2Numeric(self, Header:str):
		""" 文字列を含む配列から数値だけを抽出する """
		self.df1[Header] = pd.to_numeric(self.df1[Header], errors="coerce")

	def SaveDf(self):
		""" csvに保存する """
		self.df1.to_csv(self.df1)

	def ReturnDf(self):
		""" 処理が終わったデータフレームを返す """
		return self.df1

