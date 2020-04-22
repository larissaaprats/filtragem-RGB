from os import path
from PIL import Image, ImageEnhance, ImageOps
import numpy as np

class Editor():
	img = None
	img_formato = None
	img_local = None
	img_nome = None
	img_ext = None

	def resetar(self):
		self.img = None
		self.img_formato = None
		self.img_local = None
		self.img_nome = None
		self.img_ext = None

	def carregar_imagem(self, imagem):
		try:
			self.img = Image.open(imagem)
			self.img_formato = self.img.format
			self.img_local = path.dirname(path.realpath(imagem))
			self.img_nome, self.img_ext = path.splitext(path.basename(imagem))
			print('Imagem carregada!')
			return True
		except:
			print('Falha ao carregar imagem.')
			return False

	def red_filter (self):
		M = np.array(self.img)
		np.save ("imagem.npy", np.array, allow_pickle=True, fix_imports=True )
		M [:,:,1] = 0
		M [:,:,2] = 0
		self.img = Image.fromarray (M, "RGB")

	def green_filter (self):
		M = np.array(self.img)
		np.save ("imagem.npy", np.array, allow_pickle=True, fix_imports=True )
		M [:,:,0] = 0
		M [:,:,2] = 0
		self.img = Image.fromarray (M, "RGB")

	def blue_filter (self):
		M = np.array(self.img)
		np.save ("imagem.npy", np.array, allow_pickle=True, fix_imports=True )
		M [:,:,0] = 0
		M [:,:,1] = 0
		self.img = Image.fromarray (M, "RGB")

	def remover_cor_imagem(self):
		conversor = ImageEnhance.Color(self.img)
		self.img = conversor.enhance(0)

	def ajuste (self):
		conversor = ImageEnhance.Brightness(self.img) 
		self.img = conversor.enhance(3)
		
	def salvar(self, local, nome_imagem):
		ln = local + '/' + nome_imagem + self.img_ext
		self.img.save(ln, self.img_formato)
		self.resetar()


ed = Editor()