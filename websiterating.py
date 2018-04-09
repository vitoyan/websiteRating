import sys
import os
import util
import pathlib
import argparse 
import data_manager
import website_rating_model

logger = util.get_log('website_rating')


def main():
    parser = argparse.ArgumentParser(description='Websites Dynamic Rating')
    parser.add_argument('-b', '--basepath', help='The bath path to store the data set', type=str, required=False, default=str(path(pathlib.Path.home(), 'dataset')))
    parser.add_argument('-i', '--init', action='store_true', default=False, dest='boolean_switch', help='initail environment')
    parser.add_argument('-u', '--pages', action='store_true', default=False, dest='boolean_switch', help='prepare pages by url')
    parser.add_argument('-d', '--dataset', action='store_true', default=False, dest='boolean_switch', help='prepare dataset')
    parser.add_argument('-a', '--all', action='store_true', default=False, dest='boolean_switch', help='inital, prepare pages, prepare dataset')

    args = parser.parse_args()
    
    
    dm = data_manager.DataManager(base_path = args.b) 

    if args.i or args.a:
        logger.info("Initail Environment")             
        dm.init_environment()

    if args.u or args.a:
        logger.info("preparing websites pages by url")
        dm.prepare_websites_pages_by_url_files()

    if args.d or args.a:
        logger.info("preparing data set")
        dm.prepare_train_data()
        dm.prepare_valid_data()

    dm.load_categories_names()
    wrm = website_rating_model.WebsiteRatingModel(dm.train_path, dm.valid_path)
    wrm.load_data()
    wrm.train_model()
    wrm.SGDClassifier_trian_model()    

  
if __name__ == '__main__':
    main()    
    sys.exit(0)