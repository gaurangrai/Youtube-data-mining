
# -------------------------- importing necessary modules --------------------------

import csv                                    # writing results to .csv file
import re                                     # regular expression
import pandas as pd                           # for data frames
import matplotlib.pyplot as plt               # for plots
import numpy as np                            # for maths
plt.style.use('ggplot')                       # for plots
# set jupyter's max row display
pd.set_option('display.max_row', 1000)
# set jupyter's max column width to 50
pd.set_option('display.max_columns', 50)
csv_filepath = "../../csv_files/"                             # directory path to .csv files
files = ["comments_tech.csv","comments_comedy.csv","comments_news.csv","comments_TV.csv"]   # list of files to be analyzed for profanity
txt_filepath = "text_files/"


# In[ ]:


# -------------------------- retrieving set of bad words --------------------------
def get_set(filepath): 
    with open(filepath) as fp:
        set_words = set([])
        for line in fp:
            s = line.strip()
            set_words.add(s[:len(s)-2])
    set_words.remove('')
    return set_words
    
# -------------------------- filtering stopwords from comments --------------------------
def filter_words(inputlist,stopwords_inp_file):
    filter_comment = []                             # initializing list to store filtered comment
    for i in inputlist:
        if i not in stopwords_inp_file:             # removing words in reviews that are stopwords
            filter_comment.append(i)
    return filter_comment                           # returning length of filtered comment


# In[ ]:


# -------------------------- reading comments from .csv file and finding profane words --------------------------

def find_profanity(filepath,filename,set_filter_stopwords,badwords):
    my_csv = pd.read_csv(filepath, na_filter=True, keep_default_na=False)   # importing comments from .csv file 
    column = my_csv.text                                                    # storing data only from 'text' column of the .csv file
    
    with open('results_' + filename, 'w+', newline='') as outputfile:  # opening required files to read and write
        results_write = csv.writer(outputfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        results_write.writerows([["Comments","Profine_words", "No_words_per_comment","No_filtered_words", "Is_profine", "Avg_profine_per_comment", "Avg_profine_per_filter_comment", "No_profane_words"]])   # writing column headers
        count = 0
        for line in column:                                               # reading all comments one by one
            count = count + 1
            if line:                                                      # if comment is not blank
                line = re.sub(r'[^\w\s\*]','',line, flags=re.MULTILINE)   # filtering out non-words, 
                line = re.sub(r'\n\s+', ' ', line, flags=re.MULTILINE)    # filtering out newline characters and tab spaces

            word_list = line.split(' ')
            filt_word_list = filter_words(word_list,set_filter_stopwords) # total words in comments after filtering stopwords
            res = []
            for word in filt_word_list:
                if word in badwords:
                    res.append(word)
            if res:
                avg_prof_comm = len(res)/len(word_list)       # average profane words in comment 
                total_profane_words = len(res)
                isProfane = 1
                str_res = ', '.join(res)
            else:
                avg_prof_comm = 0                             # average profane words in comment 
                total_profane_words = 0
                isProfane = 0
                str_res = ""

            if len(filt_word_list) == 0:                      # if whole comment is filtered out
                avg_prof_filt_comm = 0
            else:
                avg_prof_filt_comm = len(res)/len(filt_word_list)  # average profane words in filtered comment

            results_write.writerows([[                         # writing results to .csv file
                                        line,                  # original comment
                                        str_res,               # string of profane words
                                        len(word_list),        # total length of comment (before filter)
                                        len(filt_word_list),   # total length of comment (after filter) 
                                        isProfane,             # Is comment profane? - '1':'Yes' and '0':'No'
                                        avg_prof_comm,         # average profanity (before filter)
                                        avg_prof_filt_comm,    # average profanity (after filter)
                                        total_profane_words    # number of profane words
            ]])


# -------------------------- reading comments from .csv file and finding profane words --------------------------    

def plot():
    # --------------< reading result csv files and storing No_profane_words in data frame >--------------------
    csv_news = pd.read_csv('results_comments_news.csv')
    csv_tv = pd.read_csv('results_comments_TV.csv')
    csv_comedy = pd.read_csv('results_comments_comedy.csv')
    csv_tech = pd.read_csv('results_comments_tech.csv')
    profane_news = csv_news.No_profane_words
    profane_tv = csv_tv.No_profane_words
    profane_comedy = csv_comedy.No_profane_words
    profane_tech = csv_tech.No_profane_words

    # --------------< calculating profanity in each category >--------------------
    percent_news = profane_news.sum(axis = 0, skipna = True)/300
    percent_tv = profane_tv.sum(axis = 0, skipna = True)/300
    percent_comedy = profane_comedy.sum(axis = 0, skipna = True)/300
    percent_tech = profane_tech.sum(axis = 0, skipna = True)/300
    print("Percent profanity in News : " + str(percent_news))
    print("Percent profanity in TV shows : " + str(percent_tv))
    print("Percent profanity in Comedy : " + str(percent_comedy))
    print("Percent profanity in Tech : " + str(percent_tech))
    
    # --------------< Plotting bar graph >--------------------
    df = pd.DataFrame({
    'Category':['News', 'TV Shows', 'Comedy', 'Technology'],
    'Percentages':[percent_news, percent_tv, percent_comedy, percent_tech],
    })

    ax = df.plot(kind='bar', figsize=(12,9), rot = 0, fontsize=13, x='Category',y='Percentages', legend = False);
    ax.set_alpha(0.75)
    ax.set_title("Percentage profanity per category\n", fontsize=18)
    ax.set_xlabel("categories", fontsize=16);
    ax.set_ylabel("% profanity", fontsize=16);
    ax.set_yticks([0,2,4,6,8,10,12])
    for p in ax.patches: 
            ax.annotate(np.round(p.get_height(),decimals=2), (p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=13)
    
    plt.savefig("profanity_analysis.png")
    plt.show(block=True)



if __name__ == "__main__":
    
    set_filter_stopwords = set([])
    stopwords_inp_file = open(txt_filepath + 'stop.txt','r')                  # importing stopwords from .txt file
    lst_stopwords = stopwords_inp_file.readlines()                            # list of stopwords
    for wrd in lst_stopwords:
        set_filter_stopwords.add(re.sub(r"\n", '', wrd, flags=re.MULTILINE))  # removing newline characters from each stopword
    stopwords_inp_file.close()
    badwords = get_set(txt_filepath + 'badwords.txt')                         # retrieving set of bad/profane words
    
    # --------< Calculating profanity for various categories >--------
    for filename in files:
        find_profanity(csv_filepath+filename, filename, set_filter_stopwords, badwords)
        print('Profanity for ' + filename + ' completed!')
    
    print('\n----- Profanity percentages per category -----')
    plot()

