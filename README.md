# benchStreamlit
This repo creates a streamlit app for creating and running an Arthur Bench test suite with the purpose of evaluating LLMs. 

#Start by installing the open source package Arthur Bench (https://github.com/arthur-ai/bench)https://github.com/arthur-ai/bench). Follow instructions for the local serving of results. 

#This repository also contains two sample datasets for evaluation purposes (News Articles and IPCC Climate Report). 

#To run, clone repo (or drop files) into the directory where you have installed arthur-bench ("streamlitBench.py" should be at the same level as the folders "tests", "docs", "examples", etc.)

#Modifications to streamlit.py - need to add your own openAI API key as environment variable (or at the top of the script). 

#Haven't included requirements.txt, just need to have arthur bench installed and ```pip install streamlit``` into your environment. 

