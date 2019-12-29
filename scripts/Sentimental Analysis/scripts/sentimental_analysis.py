import time                                                   # for time 
import pandas as pd                                           # for data frames
import numpy as np                                            # for arrays 
import pickle                                                 # for dumping data
from sklearn.feature_extraction.text import TfidfVectorizer   # for document-term matrix
from sklearn import svm                                       # for Singular Vector Machine 
from sklearn.metrics import classification_report             # for F-measure or accuracy of model
from sklearn.model_selection import cross_val_score           # for cross-validation score



def senti_analys():
    
    train_data = pd.read_csv("../data/train_data.csv")                      # training data
    test_data = pd.read_csv("../data/test_data.csv")                        # testing data

    # --------< generating training and testing data vectors >--------
    vectorizer = TfidfVectorizer(min_df = 5,                        # only words with frequency >5 
                                 max_df = 0.8,                      # only words under 80% frequency 
                                 sublinear_tf = True)               # sublinear tf scaling, i.e. replacing tf with 1 + log(tf)
    train_vectors = vectorizer.fit_transform(train_data['Comment']) # vectorized training data
    test_vectors = vectorizer.transform(test_data['Comment'])       # vectorized testing data     

    # --------< Perform classification with SVM, linear kernel >--------
    classifier_model = svm.SVC(kernel='linear', C=1)
    t_start = time.time()

    # --------< training SVM model >--------
    trained_model = classifier_model.fit(train_vectors, train_data['Label'])
    t_trained = time.time()

    # --------< Testing SVM model >--------
    prediction_model = trained_model.predict(test_vectors)
    t_predicted = time.time()

    # --------< calculating training and testing duration >--------
    training_time = t_trained-t_start
    predicting_time = t_predicted-t_trained

    # --------< generating report >--------
    report = classification_report(test_data['Label'], prediction_model, output_dict=True)
    fmeasure_pos = report['positive']['f1-score']
    fmeasure_neg = report['negative']['f1-score']
    fmeasure_neut = report['neutral']['f1-score']

    # --------< displaying report >--------
    print("Training time: %fs; Prediction time: %fs" % (training_time, predicting_time))
    print("F-measure for positive: ", fmeasure_pos)
    print("F-measure for negative: ", fmeasure_neg)
    print("F-measure for neutral: ", fmeasure_neut)

    # --------< writing report >--------
    report = open("SVM_model_report.txt","w") 
    report.write("Training time: %f secs; Prediction time: %f secs" % (training_time, predicting_time))
    report.write("\nF-measure for positive: %f" % fmeasure_pos)
    report.write("\nF-measure for negative: %f" % fmeasure_neg)
    report.write("\nF-measure for neutral: %f" % fmeasure_neut)
    report.close() 
   
    # --------< storing the trained Sentimental and Vectorizer Model >--------
    pickle.dump(trained_model, open('sentimental_model.sav', 'wb'))
    pickle.dump(vectorizer,open('vectorizer_model.sav','wb'))
    
    # --------< writing predicted values to .csv file >--------
    a = {'Comment' : test_data['Comment'], 'Label': test_data['Label'], 'Category' : test_data['Category'], 'Prediction' : prediction_model}
    result_df = pd.DataFrame(a)
    result_df.to_csv('prediction.csv', encoding='utf-8', index=False)


if __name__ == "__main__":
    
    senti_analys()   # build the Sentimental Analysis Model, check accuracy and store the trained model


