import time
import openai
import re
import os
from openai import OpenAI
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)


system_messages = {'normal': "You are taking a test. Provide your answers by responding only with the number of the appropriate answer for the presented question",
'researcher': "Act as a researcher with an IQ of 180 that is an expert at problem solving, common sense reasoning, and strategy. You are taking a test. Provide your answers by responding only with the number of the appropriate answer for the presented question,",
'persona': "You are taking a test. Act as the persona provided and provide your answers by responding only with the number of the appropriate answer for the presented question",
'roundtable_admin_initial': "You are taking a test. Provide your answers by responding with the number of the appropriate answer for the presented question as well as your reasoning for choosing it.",
'roundtable_expert': "You are {}, also referred to as {}.\n You are assisting the administrator in taking a test by offering useful critique and information. Provide feedback on the most recent answer given by the administrator, as well as their reasoning and offer suggested changes if you think the answer is incorrected, as well as your reasoning why. Pay attention to the feedback of any other experts and correct any incorrect information or suggestions. ((Be succinct and only suggest answers that are provided by the question. Do not provide overly long feedback. Do not exceed 1500 characters in your response))",
'roundtable_admin_revisor': "You are taking a test. Revise the previous answer according to the feedback provided by the experts you are collaborating with. ((You are not allowed to change the answers to the question, only the choice of answer you make.))",
'roundtable_admin_decider': "You are taking a test. Decide the best answer given the feedback and revisions that have been made. ((Provide your answers by responding only with the number of the appropriate answer for the presented question.))",
'roundtable_creator':"""You are an expert at creating useful personas. You create detailed personas of useful experts for answering the questions you are given.
	((When you return the personas, be sure to seperate them with a sequence of two newlines, followed by 5 dashes, followed by two newlines. For example:
	Persona description 1

	-----

	Persona description 2))
	""",
'clean_dataset': "nothing",
'judge': """You are a test proctor. You will recieve a question, response and correct answer and you should respond with a number from 0 through 9 that rates how well the response captures the main points of the correct answer where 1 is not at all and 9 is completely.
The following is an example:
Question: What is the meaning of life?
Correct answer: Generally one should seek to improve the world around them by being a good steward of nature and improving the lives of other people.
Response: People should take care of their environment and do their best to help each other

Grade: 9

Another example with the same question follows:
Question: What is the meaning of life?
Correct answer: Generally one should seek to improve the world around them by being a good steward of nature and improving the lives of other people.
Response: People should be good to each other

Grade: 6

Another example with the same question follows:
Question: What is the meaning of life?
Correct answer: Generally one should seek to improve the world around them by being a good steward of nature and improving the lives of other people.
Response: Doing what makes you feel good

Grade: 3

Another example with the same question follows:
Question: What is the meaning of life?
Correct answer: Generally one should seek to improve the world around them by being a good steward of nature and improving the lives of other people.
Response: Breaking rocks

Grade: 0

(((Your responses should always be formatted by two newlines, then the string 'Grade:' followed by the number grade for the given response. Respond with nothing other than what was just detailed.)))""",
'normal_long': "You are taking a test. Provide your answers by responding with one to two sentences.",
'researcher_long': "Act as a researcher with an IQ of 180 that is an expert at problem solving, common sense reasoning, and strategy. You are taking a test. Provide your answers by responding with one to two sentences.",
'persona_long': "You are taking a test. Act as the persona provided and provide your answers by responding with one to two sentences.",
'roundtable_admin_initial_long': "You are taking a test. Provide your answers by responding with one to two sentences as well as separately providing your reasoning for your answer.",
'roundtable_expert_long': "You are {}, also referred to as {}.\n You are assisting the administrator in taking a test by offering useful critique and information. Provide feedback on the most recent answer given by the administrator, as well as their reasoning and offer suggested changes if you think the answer is incorrected, as well as your reasoning why. Pay attention to the feedback of any other experts and correct any incorrect information or suggestions. ((Be succinct. Do not provide overly long feedback. Do not exceed 1500 characters in your response))",
'roundtable_admin_revisor_long': "You are taking a test. Revise the previous answer according to the feedback provided by the experts you are collaborating with.",
'roundtable_admin_decider_long': "You are taking a test. Decide the best answer given the feedback and revisions that have been made. ((Provide your answers by responding with one to two sentences.))",}

def init():
	global model_selection
	model_selection = ""


def getResponse(messages, model="gpt-3.5-turbo"):
	successful_response = False
	current_time = 2
	time_max = 60
	tries = 0
	if model == "gpt-3.5-turbo":
		#global model_selection defined in LLM_eval.py
		model = model_selection
	while not successful_response:
		try:
			response = client.chat.completions.create(

				model=model,
				messages=messages
			)
			successful_response = True
		except Exception as e:
			print(e)
			print("Retrying after time: {}".format(current_time))
			print(messages)
			time.sleep(current_time)

			current_time **= 2
			current_time = min(current_time, time_max)
			tries += 1
			if tries > 4:
				print("Max tries exceeded")
				sys.exit()
	# time.sleep(4)
	# print(response.choices[0].message.content)
	return response.choices[0].message.content[:4000]

def llm_judge(response, answer):
	messages = messages =[
				{"role": "system", "content": system_messages['judge']},
				{"role": "user", "content": """Correct Answer:{}


				Response:{}""".format(answer, response)}
			]

	judge_response = getResponse(messages, model="gpt-4")

	return judge_response