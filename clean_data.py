import pandas as pd
import numpy as np
import math
#import json


from sklearn.preprocessing import LabelBinarizer, MultiLabelBinarizer
import seaborn as sns #For Data visualization

#%matplotlib inline

# read in the json files
portfolio = pd.read_json('data/portfolio.json', orient='records', lines=True)
profile = pd.read_json('data/profile.json', orient='records', lines=True)
transcript = pd.read_json('data/transcript.json', orient='records', lines=True)



from datetime import datetime
from sklearn.preprocessing import LabelBinarizer, MultiLabelBinarizer



def rename_cols(df, new_col_names):
    """
    INPUT
    ----------
    df: input dataframe for renaming columns
    new_col_names: define new column name for each column
    
    OUTPUT
    -------
    df: output data frame with renamed column names
       
    """

    df= df.rename(columns = new_col_names)
    return df



def clean_portfolio(portfolio=portfolio):
    '''
    INPUT:
    portfolio - (pandas dataframe), portfolio data
    
    OUTPUT:
    portfolio - (pandas dataframe), cleaned portfolio data

    
    Description:
    This function cleans the dat and provides a DatFrame with Offer ID and other data about the offer. 
    '''    
    new_col_names_portfolio = {'difficulty':'offer_difficulty' , 'id':'offer_id', 
                 'duration':'offer_duration', 'reward': 'offer_reward'}
    portfolio  = rename_cols(portfolio, new_col_names_portfolio )
    
    # One hot encode the 'offertype' column
    offertype = pd.get_dummies(portfolio['offer_type'])
    
    # One hot encode the 'channels' columns
    mlb = MultiLabelBinarizer()
    mlb_fit = mlb.fit(portfolio['channels'])
    channels_df = pd.DataFrame(mlb_fit.transform(portfolio['channels']),columns=mlb_fit.classes_)
    
    #Drop the old 'channels' and 'offer_type' columns
    #portfolio = portfolio.drop(columns=['channels', 'offer_type'])
    
    #Replace the 'offertype' and 'channels' columns
    portfolio = pd.concat([portfolio, offertype, channels_df], axis=1)
    
    
    #Reorder the columns order
    #portfolio = portfolio[[ 'offer_id','offer_difficulty','offer_duration','offer_reward','bogo','discount',
    #                        'informational','email','mobile','social','web']]

    return portfolio





def clean_profile(profile = profile):
    
    #rename profile columns
    new_col_profile = {'id':'customer_id' , 'income':'customer_income'}
    profile = rename_cols(profile, new_col_profile )
    
    #Removed those with no income data
    profile = profile[profile['customer_income'].notnull()]
    
    
    #Removed customer with unspecified Gender
    #profile = profile[profile['gender'] != 'O']
    profile = profile.reset_index(drop=True)
    
    #binarizerobj = LabelBinarizer()
    gender_df = pd.get_dummies(profile['gender'])
    
    #gender_integer_map = {}
   # for i in binarizerobj.classes_:
        #gender_integer_map[i] = binarizerobj.transform([i])[0,0]''''
        
        
    
    #Change datetype of bacame_member_on column
    profile['became_member_on'] = pd.to_datetime(profile['became_member_on'], format = '%Y%m%d')   
    #Encode the year values
    profile['membership_year'] = profile['became_member_on'].apply(lambda elem: elem.year)
    membership_year_df = pd.get_dummies(profile['membership_year'])
    
    
    #Group the age ranges
    labels = ['GenZ(18–25)', 'Millennias(26-43)', 'GenXers(44-56)',
                            'Boomers(57-75)', 'Matures(76+)']
    profile['age_group'] = pd.cut(profile['age'], bins=[18, 26, 44, 57, 76, 101] , 
                                  labels=labels, include_lowest=True)
    
    # Encode for Age ranges
    agerange_df = pd.get_dummies(profile['age_group'])
    
    
    # Appened all the encoded variables to the main dataframe
    profile = pd.concat([profile,
                         agerange_df,
                         membership_year_df, gender_df], axis=1)

    
    # Drop depcreated columns
    '''profile = profile.drop(columns=['age',
                                    'age_group',
                                    'became_member_on',
                                    'membership_year'])'''
    return profile
    


def clean_transcript(transcript =transcript):
    
    # Rename Transcript columns
    new_col_transcript = {'person': 'customer_id' , 'offerid' : 'offer_id' }
    transcript = rename_cols(transcript, new_col_transcript)

    
    # Remove customer id's that are not in the customer profile DataFrame
    select_data = transcript['customer_id'].isin(profile['id'])
    transcript = transcript[select_data]
    
    # Convert from hours to days
    transcript['time'] = transcript['time'] // 24   
    
    # Change'person' column name to 'customer_id'
    transcript = transcript.rename(columns={'time': 'time_in_days'})
    
    transcript['offer_id'] =\
        transcript['value'].apply(lambda elem: list(elem.values())[0])
    
    #Create seperate Dataframes for Offers and Transactions
    
    #1.Create Dataframe for Transactions
    transactions = transcript[transcript['event']=='transaction'].drop(['value'], axis =1)
    transactions = transactions.rename(columns={'offer_id': 'amount'})
    
    
    # One hot encode customer offer events
    transcript = transcript[transcript['event'].isin(['offer received' , 
                                                      'offer completed', 'offer viewed' ])].drop(['value'], axis =1)
    event_df = pd.get_dummies(transcript['event'])
    
    #2.Create Dataframe for offers

    offers = pd.concat([transcript,event_df], axis =1)
    offers  = offers.rename(columns={'offer completed': 'completed','offer received':'received' , 'offer viewed': 'viewed'})
    #offers = offers[['offer_id','customer_id', 'time_in_days', 'completed',
           #'received', 'viewed']]
    
    return offers,transactions 

