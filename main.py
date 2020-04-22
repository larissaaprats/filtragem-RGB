from kivy import Config
Config.set('graphics', 'multisamples', '0')
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
import kivy
from io import BytesIO
from editor import ed
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition


Builder.load_file ('kvlang.kv')

class Geral():
	def mudar_tela(self, nome_tela, tipo_transicao='Slide', direcao='left'):
		if (tipo_transicao == 'Slide'):
			self.manager.transition = SlideTransition()
		else:
			self.manager.transition = NoTransition()
		self.manager.transition.direction = direcao
		self.manager.current = nome_tela

class TelaInicial(Screen, Geral):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Window.bind(on_dropfile=self.soltou)

	def alterar_mensagem(self, texto):
		lb = self.ids.mensagem
		lb.text = texto

	def soltou(self, window, caminho_arquivo):
		ca = caminho_arquivo.decode('utf-8')

		if (ed.carregar_imagem(ca) == False):
			self.alterar_mensagem('[b]Imagem Inválida[/b] tente novamente')
		else:
			tela_edicao = self.manager.get_screen('tela_edicao')
			tela_edicao.exibir_imagem()
			self.mudar_tela('tela_edicao')

class TelaEdicao(Screen, Geral):
	def exibir_imagem(self):
		area_imagem = self.ids.area_imagem
		area_imagem.clear_widgets()

		img_buffer = BytesIO()
		ed.img.save(img_buffer, format=ed.img_formato)
		img_buffer.seek(0)

		co = CoreImage(img_buffer, ext=ed.img_formato.lower())
		textura = co.texture

		img_buffer.close()

		img = Image()
		img.texture = textura

		area_imagem.add_widget(img)

	def bt_vermelho(self):
		ed.red_filter()
		ed.remover_cor_imagem()
		ed.ajuste()
		self.exibir_imagem()

	def bt_verde(self):
		ed.green_filter()
		ed.remover_cor_imagem()
		ed.ajuste()
		self.exibir_imagem()

	def bt_azul(self):
		ed.blue_filter()
		ed.remover_cor_imagem()
		ed.ajuste()
		self.exibir_imagem()

	def bt_cancelar(self):
		tela_inicial = self.manager.get_screen('tela_inicial')
		tela_inicial.alterar_mensagem('[b]Procure uma imagem[/b] e arraste ela aqui')
		self.mudar_tela('tela_inicial', 'No')
		ed.resetar()

	def bt_salvar(self):
		ed.salvar(ed.img_local, ed.img_nome + '_editada')
		ed.resetar()

sm = ScreenManager()
sm.add_widget(TelaInicial(name='tela_inicial'))
sm.add_widget(TelaEdicao(name='tela_edicao'))

class Programa(App):
	title = ' Editor de Imagens - Camadas RGB '
	def build(self):
		return sm

if __name__ == '__main__':
	Programa().run()