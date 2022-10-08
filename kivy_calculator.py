from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang.builder import Builder

kv = """
#:import hex kivy.utils.get_color_from_hex
<MainWidget> :
	buttons : buttons.__self__
	past : past.__self__
	calculation : calculation.__self__
	
	orientation : "vertical"
	spacing : dp(3)
	
	canvas.before :
		Color :
			rgba : hex("BDBFBF")
		Rectangle :
			pos : self.pos
			size : self.size
	
	Label :
		id : past
		text : "Last Data"
		size_hint : 1 , 0.1
	
	TextInput :
		id : calculation
		readonly : True
		halign : "right"
		valign : "bottom"
		font_size : sp(20)
		size_hint : 1 , 0.2
	
	GridLayout :
		cols : 4
		spacing : dp(2)
		padding : dp(2)
		id : buttons
		
	
"""

class MainWidget(BoxLayout) :
	textButtons = "1 2 3 + 4 5 6 - 7 8 9 * C 0 S /".split()
	def __init__(self , **kwargs) :
		super(MainWidget , self).__init__(**kwargs)
		
		for text in self.textButtons :
			widget = Button(
				text = text 
			)
			widget.bind(
				on_press = self.callback
			)
			self.ids["buttons"].add_widget( widget )
		
	def callback(self , obj : object) :
		
		self.ids["calculation"].font_size = "20sp"
		if self.ids["calculation"].text.startswith("Error Calculation") :
			self.ids["calculation"].text = ""
		if obj.text.isdigit() :
			self.ids["calculation"].text += obj.text
		if obj.text in "+ - * /".split() :
			if len(self.ids["calculation"].text) != 0 and self.ids["calculation"].text[-1] not in "+ - * /".split() :
				self.ids["calculation"].text += obj.text
		if obj.text == "C" :
			self.ids["calculation"].text = self.ids["calculation"].text[:-1]
		if obj.text == "S" :
			try :
				result = eval(self.ids["calculation"].text)
			except Exception as e:
				self.ids["calculation"].font_size = "40sp"
				self.ids["calculation"].text = "Error Calculation"
			else :
				self.ids["past"].text = str(result)
				self.ids["calculation"].text = str(result)
		
Builder.load_string(kv)
class CalcApp(App) :
	def build(self):
		return MainWidget()
CalcApp().run()