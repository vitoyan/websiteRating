import util

import os
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import SGDClassifier

logger = util.get_log('website_rating_model')

class WebsiteRatingModel:
    def __init__(self, trian_container, valid_container):
        if trian_container:
            self.trian_container = trian_container
        else:
            self.trian_container = os.path.join(os.getcwd(), 'train')
            
        if valid_container:
            self.valid_container = valid_container
        else:
            self.valid_container = os.path.join(os.getcwd(), 'valid')
        self.classifier = SGDClassifier
        self.parameter_for_clf = {'loss' : 'hinge', 
                                  'penalty' : 'l2',
                                  'alpha' : 1e-3, 
                                  'random_state' : 42,
                                  'max_iter' : 5, 
                                  'tol' : None}
     
    def load_data(self):
        self.train_data = load_files(self.trian_container)
        self.valid_data = load_files(self.valid_container)
    
    def train_model(self, classifier = '', parameter_for_clf = '', parameter_for_pip = ''):
        if classifier:
            self.classifier = classifier
        if parameter_for_clf:
            self.parameter_for_clf = parameter_for_clf
        
        self.website_clf = Pipeline([('vect', CountVectorizer()),
                                     ('tdidf', TfidfTransformer()),
                                     ('clf', self.classifier(**self.parameter_for_clf))])
        if parameter_for_pip:
            self.website_clf = GridSearchCV(self.website_clf, parameter_for_pip, n_jobs=-1)
        
        self.website_clf = self.website_clf.fit(self.train_data.data, self.train_data.target)
        
        valid_predicted = self.website_clf.predict(self.valid_data.data)
        
        result_metrics = metrics.classification_report(self.valid_data.target, valid_predicted,
                                                    target_names=self.valid_data.target_names)
        
        logger.info('{}'.format(result_metrics))
        print('{}'.format(result_metrics))
    
    def SGDClassifier_trian_model(self, parameter_for_clf = '', parameter_for_pip = ''):
        if not parameter_for_clf:
            parameter_for_clf = {'loss' : 'hinge', 
                                  'penalty' : 'l2',
                                  'alpha' : 1e-3, 
                                  'random_state' : 42,
                                  'max_iter' : 5, 
                                  'tol' : None}

        if not parameter_for_pip:
            parameter_for_pip = {'tdidf__use_idf': (True, False),
                                 'clf__alpha': (1e-2, 1e-4)}            
        self.train_model(SGDClassifier, parameter_for_clf, parameter_for_pip)
    
    