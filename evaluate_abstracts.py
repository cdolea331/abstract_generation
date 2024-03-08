import utils
from utils import getResponse, llm_judge
import openai
import os
import csv

record_file = open("results.csv", 'w', encoding="utf-8", newline="")
writer = csv.writer(record_file)
system_message = """You generate abstracts based on research papers you are given. Reply only with the abstract for the paper."""
context_limit = 7000
writer.writerow(["Paper title", "abstract", "generated_abstract", "score"])

utils.init()
utils.model_selection = "gpt-3.5-turbo"

papers_to_test = os.listdir("./papers/")

papers = []

for paper in papers_to_test:
	name = paper[:-4]
	abstract_lines = open(f"./abstracts/{name}_abstract.txt", encoding="utf-8").readlines()
	abstract = ""
	for line in abstract_lines:
		abstract += line

	headless_lines = open(f"./headless/{name}_headless.txt", encoding="utf-8").readlines()
	headless = ""
	for line in headless_lines:
		headless += line
	# print(headless)
	# headless.strip('\n')
	papers.append({"title": name, "headless": headless[:7000], "abstract" : abstract})

for paper in papers:
	messages = [{"role":"system", "content": system_message}, {"role": "user", "content": paper["headless"]}]
	generated_abstract = getResponse(messages)
	grade = llm_judge(generated_abstract, paper["abstract"])
	print(grade)
	writer.writerow([paper['title'], paper['abstract'], generated_abstract, str(grade)])
	

