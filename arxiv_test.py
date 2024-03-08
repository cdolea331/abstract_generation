import urllib, urllib.request
import arxiv
import time
import os
from py_pdf_parser.loaders import load_file
url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'
data = urllib.request.urlopen(url)
print(data.read().decode('utf-8'))
directories = ['./papers', './headless', './abstracts']
paper_limit=10


# paper = next(arxiv.Client().results(arxiv.Search(id_list=["2307.15802v1"])))
# # Download the PDF to the PWD with a default filename.
# paper.download_pdf()
# # Download the PDF to the PWD with a custom filename.
# paper.download_pdf(filename="downloaded-paper.pdf")
# # Download the PDF to a specified directory with a custom filename.
# paper.download_pdf(dirpath=".", filename="downloaded-paper.pdf")
# print(dir(paper))
# print(paper.summary)



big_slow_client = arxiv.Client(
  page_size = 10,
  delay_seconds = 10.0,
  num_retries = 5
)
paper_count = 0
# Prints 1000 titles before needing to make another request.
for result in big_slow_client.results(arxiv.Search(query="gender")):
	print(result.title)
	try:
		result.download_pdf(dirpath=".\\\\papers", filename=f"{result.title}.pdf")
	except:
		continue
	# time.sleep(1)
	abstract = result.summary
	abs_len = len(abstract)
	abs_chunk_size = 100
	abs_chunks = abs_len//abs_chunk_size
	abstract_file = open(f".\\\\abstracts\\\\{result.title}_abstract.txt", 'w', encoding="utf-8")
	abstract_file.write(abstract)
	headless_file = open(f".\\\\headless\\\\{result.title}_headless.txt", 'w', encoding="utf-8")
	document = load_file(f".\\\\papers\\\\{result.title}.pdf")
	elements = document.elements
	# print(len(elements))
	document_text = ""
	for i in range(len(elements)):
		text = document.elements[i].text()
		if text.lower() =="references":
			break
		if len(text) > 100:
			skip = "abstract" in text.lower()
			for j in range(abs_chunks):
				skip = skip if skip else abstract[j*abs_chunk_size:(j+1)*abs_chunk_size] in text
			if not skip:
				document_text += text
			else:
				print("chunk skipped")
	
	
	headless_file.write(document_text)
	paper_count += 1
	if paper_count > paper_limit:
		break


for directory in directories:
	files = os.listdir(directory)
	for file in files:
		full_path = directory + f"/{file}"
		file_stats = os.stat(full_path)
		size = file_stats.st_size
		if size < 500:
			os.remove(full_path)


