import sys
import os
import util
import data_manager
import website_rating_model

logger = util.get_log('website_rating')


def main(base_path):
    dm = data_manager.DataManager(base_path = base_path, 
                     pages_folder_path = os.path.join(base_path, 'pages'), 
                     train_path = os.path.join(base_path, 'train'), 
                     valid_path = os.path.join(base_path, 'valid'),
                     urls_folder_path = os.path.join(base_path, 'urls'))
    #dm.init_environment()
    #dm.prepare_websites_pages_by_url_files()
    #dm.prepare_train_data()    
    #dm.prepare_valid_data()
    dm.load_categories_names()
    wrm = website_rating_model.WebsiteRatingModel(os.path.join(base_path, 'train'), 
                                                 os.path.join(base_path, 'valid'))
    wrm.load_data()
    wrm.train_model()
    wrm.SGDClassifier_trian_model()    

  
if __name__ == '__main__':
    base_path = r'C:\Users\vitoy\Documents\dr'
    main(base_path)    
    sys.exit(0)