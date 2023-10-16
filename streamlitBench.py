#Imports

import streamlit as st
import pandas as pd
from arthur_bench.run.testsuite import TestSuite
import os
import subprocess

#from bench.arthur_bench.client import bench_client

#Set up: 
os.environ['OPENAI_API_KEY'] = 'YOUR OPENAI KEY HERE'

#Heading up top:
st.title("Using Arthur Bench with Streamlit")

#Image:
st.sidebar.image('arthurlogo.svg')

#Description
taskDescription = "Allow users to create and configure a test suite for evaluating LLMs."
st.subheader(taskDescription)
st.divider()

# Collect user input for the name of this test suite
testSuiteName = st.text_input("What would you like to call this test suite?")
st.divider()

#Create a dropdown for the selection of task type (maybe only one option at the moment)
taskLabel = "What type of task are you evaluating?"
taskOptions = ['Summarization']
taskType = st.selectbox(taskLabel,taskOptions, index = None, placeholder = "Select task type...", )
st.divider()

#Create a dropdown for the scoring method selection
methodLabel = "What scoring method would you like to use?"
methodOptions = ("summary_quality", "bertscore", "exact_match")
#methodOptions = ("summary_quality", "hallucination", "bertscore", "exact_match") #Hallucination check not available in local mode at the moment
scoringLink = 'https://bench.readthedocs.io/en/latest/scoring.html'
scoringMethod = st.selectbox(methodLabel, methodOptions, index = None, placeholder = "Select scoring method...", help = scoringLink)

#st.caption(scoringLink)
st.divider()

#Create a dropdown for the dataset selection
datasetLabel = "What dataset would you like to use to evaluate your candidates?"
datasetOptions = ("IPCC Climate Change Report (2022)", "News Articles")
dataset = st.selectbox(datasetLabel, datasetOptions, index = None, placeholder = "Select dataset...")
st.divider()

#Initialize some of the objects that will be created
refDataset = None
candidateDataset = None

#A function for creating a test suite based on the user's selections
def readTestSuiteData(dataset, scoringMethod):
    if dataset == "IPCC Climate Change Report (2022)":
        refDataset = pd.read_csv("BenchStreamlit/climateSummaries.csv")
        #candidateDataset = pd.read_csv("BenchStreamlit/climateCandidate.csv")
    elif dataset == "News Articles":
        refDataset = pd.read_csv('BenchStreamlit/NewsSummaryInputsRef.csv')
        #candidateDataset = pd.read_csv('BenchStreamlit/candidateNewsSummaries.csv')

    if scoringMethod == "summary_quality" or "bertscore" or "exact_match": 
        streamlitSuite = TestSuite(
        testSuiteName,
        scoringMethod,
        reference_data = refDataset,
        input_column = "input_text",
        reference_column = "reference_outputs")

    elif scoringMethod == "hallucination": 
        streamlitSuite = TestSuite(
        testSuiteName,
        scoringMethod,
        reference_data = refDataset,
        input_column = "input_text")
    
    st.text('Test Suite Successfully Created')
    st.text(streamlitSuite)
    return streamlitSuite


# Have user click a button to create the test_suite. Button is a callback for the function which creates test suite
createTestSuiteButton = st.button("Create test suite", on_click = readTestSuiteData, args = (dataset, scoringMethod), type='primary')
st.divider()

# The section below pertains to providing candidate responses for running the test suite that was created in the previous step. 
st.subheader("Run your test suite with candidate responses")
st.divider()

runName = st.text_input('What would you like to call this test run?')

#Load candidate summaries
uploaded_file = st.file_uploader('Upload Candidate Responses')
st.divider()

#Function for running test suite
def runTestSuite(runName, streamlitSuite, candidateDataset):
    streamlitSuite.run(runName, candidate_data = candidateDataset, candidate_column = 'candidate_output')
    subprocess.run('bench')
    #st.text(result.stdout)

#Allow user to upload file containing candidate responses, then run the test suite on those responses.
if uploaded_file is not None:
#read csv
    candidateDataset=pd.read_csv(uploaded_file)
    st.dataframe(data = candidateDataset)

    streamlitSuite = TestSuite(
    testSuiteName,
    scoringMethod,
    reference_data = refDataset,
    input_column = "input_text",
    reference_column = "reference_outputs")
    
    st.button('Create test run', on_click = runTestSuite, args = (runName, streamlitSuite, candidateDataset))
    #streamlitSuite.run(runName, candidateDataset)




