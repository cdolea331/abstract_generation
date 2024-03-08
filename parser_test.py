from py_pdf_parser.loaders import load_file
from py_pdf_parser.visualise import visualise
import time


output = open("downloaded_text.txt", 'w', encoding='utf-8')
document = load_file("papers/A Causal Inference Method for Reducing Gender Bias in Word Embedding Relations.pdf")
print(dir(document.elements[0]))
print(document.elements[0].text())
elements = document.elements
document_text = ""
for i in range(len(elements)):
	print(i)
	text = document.elements[i].text()
	if len(text) > 150:
		print(text)
		document_text += text + "\n"
	if text.lower() =="references":
		break
	time.sleep(.1)
# visualise(document)
output.write(document_text)
