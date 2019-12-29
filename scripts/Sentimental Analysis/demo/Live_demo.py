import plotly
import pandas as pd                 # for data frame
import plotly.plotly as py          # for plot
import plotly.graph_objs as go      # for table                      
import pickle                       # for data import
plotly.tools.set_credentials_file(username='hdchhabr', api_key='DnVjkDeQ7mBrKch58pFG') 
model_path = ""                     # directory path of models
file_path = ""                      # directory path of files


# In[29]:


# --------< predict labels for demo comments >--------
def predict(model_path, file_path):

    vectorizer_model = pickle.load(open(model_path +'vectorizer_model.sav', 'rb'))   # import trained vectorizer model
    sentimental_model = pickle.load(open(model_path +'sentimental_model.sav', 'rb'))   # import trained sentimental model

    df_demo = pd.read_csv(file_path + 'senti_analys_demo.csv')                       # import comments from csv for demo
    comment_demo = df_demo.Comment                                                   # selecting 'Comment' column 
    size_demo = len(comment_demo)

    sr_list = []
    for i in range(size_demo):
        sr_list.append(i+1)

    vectorized_comm = vectorizer_model.transform(comment_demo)                       # vectorize demo comments
    prediction_comm = sentimental_model.predict(vectorized_comm)                     # predict labels for demo comments 

    predict_table = go.Table(
              columnorder = [1,2,3],
              columnwidth = [20,400,80],
              header = dict(
                values = [['<b>No</b>'],['<b>Comment</b>'], ['<b>Label</b>']],       # header properties
                line = dict(color = '#506784'),
                fill = dict(color = '#6868FF'),
                align = ['center','center'],
                font = dict(color = 'white', size = 12),
                height = 40
              ),
              cells = dict(                                                          # columns properties 
                values = [sr_list,comment_demo, prediction_comm],
                line = dict(color = '#506784'),
                fill = dict(color = ['white','white',['#68B468' if val == 'positive' else '#FF6868' if val =='negative' else '#FFFF68' if val == 'neutral' else 'white' for val in prediction_comm]]),
                align = ['center','left', 'center'],
                font = dict(color = 'black', size = 12),
                height = 30
                ))

        # -------< plot table with comments and predicted labels >--------

    data = [predict_table]    
    py.plot(data, filename = "Sentimental_analysis_demo")


# In[30]:


if __name__ == "__main__":
    data = predict(model_path,file_path)   # predicting labels for comments in demo csv

