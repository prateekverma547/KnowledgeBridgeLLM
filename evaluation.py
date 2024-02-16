from langchain_community.chat_models import ChatOpenAI
from langchain.chains import QAGenerationChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from data_preprocessor import DataPreprocessor
from langchain_community.document_loaders import DataFrameLoader
from langchain.chains import RetrievalQA
from query import QueryEngine
from langchain.evaluation.qa import QAEvalChain
import csv
import os

preprocess_data = DataPreprocessor()
data = preprocess_data.preprocess_data()
loader = DataFrameLoader(data, page_content_column="sentence")
documents = loader.load()

all_doc=[]
# qa_dataset = []
# split_docs=[]
# predictions=[]

llm = ChatOpenAI(
        model_name='gpt-3.5-turbo-16k',
        )

def split_texts():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=430,
        chunk_overlap=20,
        length_function=len,
    )
    split_doc = text_splitter.split_documents(documents)
    print("0")
    return split_doc


# Testing data Q and A generation on x documents
def test_data_generation(x):
    print("1")
    all_doc=split_texts()
    print("1.1")
    print("1.2")
    chain = QAGenerationChain.from_llm(llm)
    print("1.3")
    finaldoc=[]
    for i in all_doc[0:x]:
        finaldoc.append(i.page_content)
    print(finaldoc)
    qa_data=chain.batch(finaldoc, config={"max_concurrency": 5})
    print("1.4")
    qa_dataset = [l['questions'][0] for l in qa_data]
    print("2")
    return qa_dataset

def genrating_predition_on_test(qa_dataset):

    # Loading chain which we are using for our Q&A BOT
    print("2")
    QE=QueryEngine()
    chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=QE.get_retriver(),
            chain_type_kwargs={"prompt": QE.prompt()},
            input_key="question"
        )
    predictions = chain.apply(qa_dataset)
    print("3")
    return predictions


def evaluation_of_prediction(qa_dataset,predictions):
    print("4")

    qaeval_chain = QAEvalChain.from_llm(llm)
    graded_outputs = qaeval_chain.evaluate(qa_dataset, 
                                     predictions, 
                                     question_key="question",
                                     answer_key="answer",
                                     prediction_key="result")
    print("5")
    return graded_outputs

def proces_result(test_result,prediction):
    print("6")
    merged_dataset = []
    print(prediction[0],test_result[0])
    for item1, item2 in zip(prediction, test_result):
        merged_item = {
            'Question': item1['question'],
            'Answer': item1['answer'],
            'Prediction': item1['result'],
            'Outcome': 1 if item2['results'] == 'CORRECT' else 0
        }
        merged_dataset.append(merged_item)
    print("7")
    save_to_csv(merged_dataset,"testOutcome.csv")

def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Question', 'Answer', 'Prediction', 'Outcome']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in data:
            writer.writerow(item)

def score_showcase(filename):
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        merged_dataset = list(reader)

        total_positive = sum(1 for item in merged_dataset if item['Outcome'] == '1')
        total_negative = sum(1 for item in merged_dataset if item['Outcome'] == '0')
        total_entries = len(merged_dataset)
        positive_percentage = (total_positive / total_entries) * 100
        negative_percentage = (total_negative / total_entries) * 100

        print("Total Positive Outcomes:", total_positive)
        print("Total Negative Outcomes:", total_negative)
        print("Positive Outcome Percentage: {:.2f}%".format(positive_percentage))
        print("Negative Outcome Percentage: {:.2f}%".format(negative_percentage))



###############################

#Lets test the model on 60 data set
filename = 'testOutcome.csv'
if os.path.exists(filename):
    score_showcase(filename)
else:
    print("File does not exist.")
    datasetcount=100
    qa_data=test_data_generation(datasetcount)
    predicted_data=genrating_predition_on_test(qa_data)
    result=evaluation_of_prediction(qa_data,predicted_data)
    proces_result(result,predicted_data)
    score_showcase(filename)
