import sys
import os
import util
import argparse 
import data_manager
import website_rating_model

logger = util.get_log('website_rating')


def main():
    parser = argparse.ArgumentParser(description='Websites Dynamic Rating')
    parser.add_argument('-b', '--basepath', help='The base path to store the data set', type=str, required=False, default=str(os.path.join(os.path.expanduser('~'), 'dataset')), dest ='basepath')
    parser.add_argument('-i', '--init', action='store_true', default=False, dest='init', help='initail environment')
    parser.add_argument('-u', '--pages', action='store_true', default=False, dest='pages', help='prepare pages by url')
    parser.add_argument('-d', '--dataset', action='store_true', default=False, dest='dataset', help='prepare dataset')
    parser.add_argument('-a', '--all', action='store_true', default=False, dest='all', help='inital, prepare pages, prepare dataset')
    parser.add_argument('-t', '--train', help='The base path to store the data set', type=str, required=False, default='SGD', dest ='train')
    parser.add_argument('-T', '--trainall', action='store_true', default=False, dest='trainall', help='train all data with all methods')


    args = parser.parse_args()
    
    
    dm = data_manager.DataManager(base_path = args.basepath) 

    if args.init or args.all:
        logger.info("Initail Environment")             
        dm.init_environment()

    if args.pages or args.all:
        logger.info("preparing websites pages by url")
        dm.prepare_websites_pages_by_url_files()

    if args.dataset or args.all:
        logger.info("preparing data set")
        dm.prepare_train_data()
        dm.prepare_valid_data()

    dm.load_categories_names()
    wrm = website_rating_model.WebsiteRatingModel(dm.train_path, dm.valid_path)
    wrm.load_data()

    if args.train.upper() == 'SGD' or args.trainall:
        logger.info('training with SGD')
        wrm.SGDClassifier_train_model()  

    if args.train.upper() == 'MNB' or args.trainall:
        logger.info('training with MNB')
        wrm.MultinomialNB_train_model()

    if args.train.upper() == 'BNB' or args.trainall:
        logger.info('training with BNB')
        wrm.BernoulliNB_train_model()

    if args.train.upper() == 'SVC' or args.trainall:
        logger.info('training with SVC')
        wrm.SVC_train_model()  

  
if __name__ == '__main__':
    main()    
    sys.exit(0)
