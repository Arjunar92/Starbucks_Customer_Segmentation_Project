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
    portfolio  = portfolio.rename(columns= new_col_names_portfolio )
    
    
    #Create new column Offer name to assign a recogonizable identifyer for each of the 10 offers. 
    new_col = {'offer_name' : ['offer_1', 'offer_2','offer_3','offer_4',
                              'offer_5','offer_6','offer_7','offer_8','offer_9','offer_10' ]}
    portfolio['offer_name'] = pd.DataFrame(new_col)
    
    # One hot encode the 'offertype' column
    #offertype = pd.get_dummies(portfolio['offer_type'])
    
    # One hot encode the 'channels' columns
    mlb = MultiLabelBinarizer()
    mlb_fit = mlb.fit(portfolio['channels'])
    channels_df = pd.DataFrame(mlb_fit.transform(portfolio['channels']),columns=mlb_fit.classes_)
    
    #Drop the old 'channels'
    portfolio = portfolio.drop(columns=['channels'])
    
    #Replace the 'offertype' and 'channels' columns
    portfolio = pd.concat([portfolio, channels_df], axis=1)
    
    
    #Reorder the columns order
    portfolio = portfolio[[ 'offer_id','offer_name','offer_type' ,'offer_difficulty','offer_duration',
                           'offer_reward','email','mobile','social','web']]

    return portfolio





def clean_profile(profile = profile):

    '''
    INPUT:
    profile - (pandas dataframe), profile data
    
    OUTPUT:
    portfolio - (pandas dataframe), cleaned profile data

    
    Description:
    This function cleans the data and provides a DatFrame with cleaned profile data. 
    '''    
        
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
    #for i in binarizerobj.classes_:
      #  gender_integer_map[i] = binarizerobj.transform([i])[0,0]
        
        
    
    #Change datetype of bacame_member_on column
    profile['became_member_on'] = pd.to_datetime(profile['became_member_on'], format = '%Y%m%d')   
    #Encode the year values
    profile['membership_year'] = profile['became_member_on'].apply(lambda elem: elem.year)
    membership_year_df = pd.get_dummies(profile['membership_year'])
    
    
    #Group the Salary ranges
    sal_labels = ['Under $25K',' $25,000 - $49,999','$50,000 - $74,999','$75,000 - $99,999', '$100K']
    
    profile['customer_income_range'] = pd.cut(profile['customer_income'], 
                                                      bins=[1, 25000, 49999, 74999, 99999, 150000] , 
                                  labels=sal_labels, include_lowest=True)
    # Encode for Age ranges
    salrange_df = pd.get_dummies(profile['customer_income_range'])
    
    
    #Group the age ranges
    labels = ['GenZ(18–25)', 'Millennias(26-43)', 'GenXers(44-56)',
                            'Boomers(57-75)', 'Matures(76+)']
    profile['age_group'] = pd.cut(profile['age'], bins=[18, 26, 44, 57, 76, 101] , 
                                  labels=labels, include_lowest=True)
    
    # Encode for Age ranges
    agerange_df = pd.get_dummies(profile['age_group'])
    
    
    # Appened all the encoded variables to the main dataframe
    profile = pd.concat([profile,gender_df,
                         agerange_df,salrange_df,
                         membership_year_df], axis=1)

    
    # Drop depcreated columns
    profile_da = profile[['customer_id', 'gender','age',
            'age_group','customer_income','customer_income_range',
            'became_member_on','membership_year']]
    
    profile_m = profile[['customer_id','F','M','O',
            'GenZ(18–25)','Millennias(26-43)','GenXers(44-56)',
            'Boomers(57-75)','Matures(76+)',
            '$50,000 - $74,999','$75,000 - $99,999','$100K',
            2013, 2014, 2015, 2016, 2017, 2018]]

    return profile_da , profile_m
    


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



def offer_success(offers_portfolio, column):
    
    """
    This procedure is to create the following features:
    
    -Offer recieved count
    -Offer Viewed count/viewed rate
    -Offer complted count/completed rate
    
    For each of Offer type, Offer name, offer difficulty, offer durtion, offer reward
    
    INPUT: 
    - offers_portfolio: Offer_portfolio dataframe
    - column: column name for which the feature must be created. ed - offer_type, offer_name
    
    OUTPUT:
    - all_res: A list of dataframe
    
    """

    offer_name = offers_portfolio[column].unique()

    all_res = []
    for offer in offer_name:

        success = offers_portfolio[offers_portfolio[column] == offer].groupby(['customer_id']).agg({'received': 'sum' ,
                                                                                                          'viewed':'sum' ,
                                                                                                          'completed': 'sum'})
        offer_count= success.add_suffix('_count')
        col_name = list(offer_count.columns)
        offer_count['viewed_rate'] = offer_count[col_name[1]]/offer_count[col_name[0]]
        offer_count['completed_rate'] = offer_count[col_name[2]]/offer_count[col_name[1]]
        offer_count[offer_count['completed_rate']> 1] = 1
        offer_count = offer_count.add_prefix(column+'_'+str(offer)+'_')
        #offer_count.reset_index(inplace=True)

        all_res.append(offer_count)
    
    return all_res






def offer_success_channel(offers_portfolio):
    
    """
    This procedure is to create the following features:
    
    -Offer recieved count
    -Offer Viewed count/viewed rate
    -Offer complted count/completed rate
    
    For each of 'mobile','social','web','email' channels
    
    INPUT: 
    - offers_portfolio: Offer_portfolio dataframe
    - column: column name for which the feature must be created. eg - 'mobile','social','web','email' channels
    
    OUTPUT:
    - all_res: A list of dataframe
    
    """    
    all_res = []
    
    columns = ['mobile','social','web','email']
    for column in columns:
        success = offers_portfolio[(offers_portfolio[column] == 1) & 
                                   (offers_portfolio['offer_type'] != "informational")].groupby(['customer_id']).agg({'received': 'sum' ,'viewed':'sum' ,'completed': 'sum'})
        
        offer_count= success.add_suffix('_count')
        col_name = list(offer_count.columns)
        offer_count['viewed_rate'] = offer_count[col_name[1]]/offer_count[col_name[0]]
        offer_count['completed_rate'] = offer_count[col_name[2]]/offer_count[col_name[1]]
        offer_count[offer_count['completed_rate']> 1] = 1
        offer_count = offer_count.add_prefix(column+'_')
        #offer_count.reset_index(inplace=True)
        
        all_res.append(offer_count)
        
    return all_res



def plot_data(df,demo,groupby,palette,col_wrap,height,label_rotation):
    
    """
    This procedue is used to create aggregate measures per demographic group, and then plot those measures in rplot
    
    
    INPUT: 
    
    -Data input
    --df: input profile_offer dataframe with the measures to be aggrigated. 
    --demo: input profile_offer dataframe
    --groupby: input the domographic group you want to aggrigate for
    
    -Variables for Data visualization
    --palette: Input the No of color palatte for the bar plot
    --col_wrap: Input th enumber of column in the grid
    --height: Input the height of the plot
    --label_rotation: Input degrees to which X-axis labels need to be rotated.

    
    OUTPUT:
    - df: return dataframe with te aggregated measures and the plot
    
    """       
    
    
    df = df.join(demo[groupby])
    df = df.copy().reset_index()
    df = df.melt(id_vars=['customer_id', groupby],ignore_index = True)
    df = df.groupby([groupby, 'variable']).mean().reset_index()
    df = df[df['variable']!='index']
    starbucks = ["#008248", "#604c4c", "#eac784", "#f0cddb", "#6B9997"]
    
    sns.set_palette(sns.color_palette(starbucks,palette))
    g = sns.FacetGrid(df, col='variable', hue= groupby, col_wrap=col_wrap, height=height, sharey=False)
    g = g.map(plt.bar, groupby, 'value').set_titles("{col_name}")
    g.set_xticklabels(rotation = label_rotation)
    g.tight_layout()
    
    
    return df


def plot_data_overall(df,palette,label_rotation, order):
    
    
    """
    This procedue is used to create overall aggregate measures and then plot
    
    
    INPUT: 
    
    -Data input
    --df: input profile_offer dataframe with the measures to be aggrigated.
    
    -Variables for Data visualization
    --palette: Input the No of color palatte for the bar plot.
    --label_rotation: Input degrees to which X-axis labels need to be rotated.
    --order: input list of variables in the same order as how should appear in plot

    
    OUTPUT:
    - df: return dataframe with te aggregated measures and the plot
    
    """    
    
    df = df.copy().reset_index()
    df = df.melt(id_vars=['customer_id'],ignore_index = True)
    df = df.groupby(['variable']).mean().reset_index()
    df = df[df['variable']!='index']
    df
    starbucks = ["#008248", "#604c4c", "#eac784", "#f0cddb", "#6B9997"]
    plt.figure(figsize=(3, 3))
    g = sns.barplot(data=df, x="variable", y="value", order = order)
    g.set_xticklabels(g.get_xticklabels(), rotation=label_rotation)

    sns.set_palette(sns.color_palette(starbucks,palette))
    
    
    
    return df
        

