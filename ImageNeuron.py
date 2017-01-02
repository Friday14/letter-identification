from PIL import Image
import json

class ImageNeuron:
	signal_scaled = [] # Масштабированные сигналы
	signal_scaled_sum = 0
	matrix_input = [] # Матрица пикселей
	access_limit = 5880 # минимальный лимит допуска истины
	com_number = 99 # количество связей(аксонов) 
	weight = 0 # Вес сигнала

	def __init__(self):
		template_matrix = [ [0 for i2 in range(0,self.com_number)] for i in range(0,self.com_number)] 

		f = open('./data.json', 'r+')
		data = f.read()
		if data != '':
			data = json.loads(data)	
		if data == '':
			f.write(json.dumps(template_matrix))
			data = template_matrix
		self.signal_scaled = template_matrix
		self.weight = data
		# print(self.weight)
		f.close()


	def saveWight(self):
		weight = json.dumps(self.weight)
		f = open('./data.json','w')
		f.write(weight)
		print('Сохранено')

	def inputImage(self, file):
		size = 105, 105
		img = Image.open(file)
		img.thumbnail(size)
		L,H = img.size
		pixels = [ [0 for i2 in range(0,self.com_number)] for i in range(0,self.com_number)] 
		for x in range(0, 99):
			for y in range(0, 99):
				if L <= x or H <= y: 
					r = 0
				else:
					r, g, b= img.getpixel( (x,y) )
					S = r + g + b
					if (S > (((255 + 110) // 2) * 3)):
						r = 0
						# r, g, b = 0, 255, 255
					else:
						r = 1
					# r, g, b = 1, 0, 0
				# img.putpixel( (x,y), (r,g,b) )
				pixels[x][y] = r
		img.show()
		self.matrix_input = pixels
		# print(self.matrix_input)
		self.adapter()


	#Масташбирование
	def adapter(self):
		for x in range(0, self.com_number):
			for y in range(0, self.com_number):
				self.signal_scaled[x][y] = self.matrix_input[x][y] * self.weight[x][y]

		for x in range(0, self.com_number):
			for y in range(0, self.com_number):
				self.signal_scaled_sum += self.signal_scaled[x][y]


	def getResult(self):
		return self.signal_scaled_sum >= self.access_limit

	def training(self, response):
		if response == 'y': 
			return True
		
		if self.getResult():
			self.decrementWeb()
		else:
			# print('t', self.getResult())
			self.incrementWeb()
		self.signal_scaled_sum = 0
		
	def decrementWeb(self):
		# print('--')
		for x in range(0, self.com_number):
			for y in range(0, self.com_number):
				self.weight[x][y] -= self.matrix_input[x][y] 
				
	def incrementWeb(self):
		print('++')
		for x in range(0, self.com_number):
			for y in range(0, self.com_number):
				self.weight[x][y] += self.matrix_input[x][y] 
				
	def createGist(self):
		img = Image.open('./template.jpg')
		for x in range(0,90):
			for y in range(0,90):
				rgb = (0,0,0)
				if(self.weight[x][y] > 5):
					rgb = (0,0,0)
				elif(self.weight[x][y] > 1):
					rgb = (50,50,50)
				else:
					rgb = (255,255,255)
				img.putpixel( (x,y), rgb )
		img.save('./output.jpg')
		