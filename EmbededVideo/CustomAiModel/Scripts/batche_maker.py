import os

from charging_bar import ChargingBar


def batch_creator(input_folder, output_folder, size):
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

	files = os.listdir(input_folder)
	batch_number = 0
	batchs = []
 
	bar = ChargingBar(len(files))
	bar.show()

	for i in range(0, len(files), size):
		batch = files[i:i+size]
		batch_folder = os.path.join(output_folder, f'batch_{batch_number}')
		if not os.path.exists(batch_folder):
			os.makedirs(batch_folder)
		for file in batch:
			src = os.path.join(input_folder, file)
			dst = os.path.join(batch_folder, file)
			os.rename(src, dst)
			bar.update()
		batch_number += 1
   


if __name__ == '__main__':
	input_foleder = "EmbededVideo/CustomAiModel/PreProcess/square_high_red"
	output_foleder = "EmbededVideo/CustomAiModel/PreProcess/batches"
	batch_creator(input_foleder,output_foleder, 100) 


