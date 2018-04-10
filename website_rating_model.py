import util

import os
import pathlib
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

logger = util.get_log('website_rating_model')

class WebsiteRatingModel:
    def __init__(self, trian_container, valid_container):
        if trian_container:
            self.trian_container = trian_container
        else:
            self.trian_container = os.path.join(str(pathlib.Path.home()), 'train')
            
        if valid_container:
            self.valid_container = valid_container
        else:
            self.valid_container = os.path.join(str(pathlib.Path.home()), 'valid')
        self.classifier = SGDClassifier
        self.parameter_for_clf = {'loss' : 'hinge', 
                                  'penalty' : 'l2',
                                  'alpha' : 1e-3, 
                                  'random_state' : 42,
                                  'max_iter' : 5, 
                                  'tol' : None}
        self.models = {}
     
    def load_data(self):
        self.train_data = load_files(self.trian_container)
        self.valid_data = load_files(self.valid_container)
    
    def train_model(self, classifier = '', parameter_for_clf = '', parameter_for_pip = ''):
        if not classifier:
            classifier = self.classifier 

        if not parameter_for_clf:
            parameter_for_clf = self.parameter_for_clf
        
        website_clf = Pipeline([('vect', CountVectorizer()),
                                     ('tdidf', TfidfTransformer()),
                                     ('clf', classifier(**parameter_for_clf))])
        if parameter_for_pip:
            website_clf = GridSearchCV(website_clf, parameter_for_pip, n_jobs=-1)
        
        website_clf = website_clf.fit(self.train_data.data, self.train_data.target)

        # predict on train set
        train_predicted = website_clf.predict(self.train_data.data)
        
        result_metrics = metrics.classification_report(self.train_data.target, train_predicted,
                                                    target_names=self.train_data.target_names)
        
        logger.info('mertics on train set \n {}'.format(result_metrics))

        # predict on valid set        
        valid_predicted = website_clf.predict(self.valid_data.data)
        
        result_metrics = metrics.classification_report(self.valid_data.target, valid_predicted,
                                                    target_names=self.valid_data.target_names)
        
        logger.info('mertics on valid set \n {}'.format(result_metrics))

        # store the model
        return website_clf
    
    def SGDClassifier_train_model(self, parameter_for_clf = '', parameter_for_pip = ''):
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
        model = self.train_model(SGDClassifier, parameter_for_clf, parameter_for_pip)

        self.models['sgd'] = model


    def MultinomialNB_train_model(self, parameter_for_clf = '', parameter_for_pip = ''):
        if not parameter_for_clf:
            parameter_for_clf = {'fit_prior' : 'false'}

        if not parameter_for_pip:
            parameter_for_pip = {'tdidf__use_idf': (True, False),
                                 'clf__fit_prior': (True, False)}            
        model = self.train_model(MultinomialNB, parameter_for_clf, parameter_for_pip)

        self.models['mnb'] = model


    def BernoulliNB_train_model(self, parameter_for_clf = '', parameter_for_pip = ''):
        if not parameter_for_clf:
            parameter_for_clf = {'fit_prior' : 'false'}

        if not parameter_for_pip:
            parameter_for_pip = {'tdidf__use_idf': (True, False),
                                 'clf__fit_prior': (True, False)}            
        model = self.train_model(BernoulliNB, parameter_for_clf, parameter_for_pip)

        self.models['bnb'] = model

    def SVC_train_model(self, parameter_for_clf = '', parameter_for_pip = ''):
        if not parameter_for_clf:
            parameter_for_clf = {'C' : 1.0,
                                'kernel': 'rbf'}

        if not parameter_for_pip:
            parameter_for_pip = {'tdidf__use_idf': (True, False),
                                 'clf__C': (0.1, 1.0, 10),
                                 'clf__kernel':('linear','poly','rbf','sigmoid')}            
        model = self.train_model(SVC, parameter_for_clf, parameter_for_pip)

        self.models['svc'] = model

    def DecisionTreeClassifier_train_model(self, parameter_for_clf = '', parameter_for_pip = ''):
        if not parameter_for_clf:
            parameter_for_clf = {'splitter':'best',
                                 'max_features ':None,
                                 'max_depth':None,
                                 'max_leaf_node':None
                              }

        if not parameter_for_pip:
            parameter_for_pip = {'tdidf__use_idf': (True, False),
                                 'clf__splitter': ('best','random'),
                                 'clf__max_features':('auto','sqrt','log2',None),
                                 'clf__max_depth':(None, 10),
                                 'clf__max_leaf_node':(None, 64,128)
                                 }            
        model = self.train_model(DecisionTreeClassifier, parameter_for_clf, parameter_for_pip)

        self.models['dtc'] = model


    