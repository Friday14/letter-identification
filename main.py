import ImageNeuron
import GridNeuron

images = [
'./img/az/B1.jpg',
'./img/az/B2.jpg',
]

neuron = ImageNeuron.ImageNeuron()
for i in range(0,2):
	neuron.inputImage(images[i])
	result = neuron.getResult()
	# print(neuron.matrix_input)
	print(images[i])
	print('Результат: ' + str(result))
	isYes = input('Верно? (y/n)')
	neuron.training(isYes)
	# print(neuron.signal_scaled_sum)

neuron.createGist()

if input('Сохранить результаты? (y/n)') == 'y':
	neuron.saveWight()

