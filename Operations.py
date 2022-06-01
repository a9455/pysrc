
import numpy as np
import pandas as pd
import netCDF4 as nc


class OperationNetCDF():
	def __init__(self, NcFileName:str):
		self.NcFileName = NcFileName		# NetCDFのファイル名

	# 読み込み関係
	# -------------------------------------
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


	# 書き込み関係
	# -------------------------------------
	def write_netCDF_file(self, DictionaryData={}):
		"""
		DictionaryDataを順番に格納していく
		DictionaryDataの作り方。⇒次元数とデータを設定する（以下は例）
		"Nx"		: ["axis", 1軸の次元数],
		"Ny"		: ["axis", 2軸の次元数],
		"Nz"		: ["axis", 3軸の次元数],
		"Element1"	: ["data", "dtype", ["Nx", "Ny"]		, Data1],
		"Element2"	: ["data", "dtype", ["Nx", "Ny", "Nz"]	, Data2],
		"""

		# ファイルの作成
		# ---------------------------
		NcData	= nc.Dataset(self.NcFileName, "w", format="NETCDF4")
		
		# 次元数の設定
		# ---------------------------
		for key in list(DictionaryData.keys()):
			tmp	= DictionaryData[key]
			if tmp[0] == "axis":
				NcData.createDimension(key, tmp[1])
		
		# データの設定
		# ---------------------------
		for key in list(DictionaryData.keys()):
			tmp	= DictionaryData[key]
			if tmp[0] == "data":
				tmpVar		= NcData.createVariable(key, tmp[1], tuple(tmp[2]), fill_value=-9999)
				tmpVar[:,:]	= tmp[3]

		NcData.close()



class OperationPandas():
	# 単一のデータフレームを編集
	# -----------------------------------------------------
	def load_df_from_df(self, df):
		""" 既に定義したデータフレームを選択する """
		self.df1	= df
	
	def load_df_from_filename(self, Filename:str, header=True, index_col=0):
		""" 新規ファイルを読み込む """
		self.df1	= pd.read_csv(Filename, header=header, index_col=index_col)

	def reset_header(self, NewHeader:list):
		""" ヘッダーの再定義 """
		self.df1.columns	= NewHeader

	def str_to_numeric(self, Header:str):
		""" 文字列を含む配列から数値だけを抽出する """
		self.df1[Header] = pd.to_numeric(self.df1[Header], errors="coerce")

	def str_to_numeric_all(self):
		""" すべての行に対して数値だけを抽出する """
		Header	= list(self.df1.columns)
		for head in Header:
			self.df1[head] = pd.to_numeric(self.df1[head], errors="coerce")
		self.df1.loc[:,:]	= np.array(self.df1, dtype=float)

	def save_df(self):
		""" csvに保存する """
		self.df1.to_csv(self.df1)

	def return_df(self):
		""" 処理が終わったデータフレームを返す """
		return self.df1



	# 複数のデータフレームを編集
	# -----------------------------------------------------
	def concat_df(self, FileNames:list, header=True, index_col=0, encoding="utf8"):
		""" csvを横に連結する """
		for filename in FileNames:
			if filename == FileNames[0]:
				df1	= pd.read_csv(filename, header=header, index_col=index_col, encoding=encoding)
			else:
				df2	= pd.read_csv(filename, header=header, index_col=index_col, encoding=encoding)
				df1	= pd.concat([df1, df2], axis=1)
		self.df1	= df1
		return df1









