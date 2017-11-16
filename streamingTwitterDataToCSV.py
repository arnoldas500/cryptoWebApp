from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
#import MySQLdb                                                                                                                                         
import time
import datetime
from datetime import timezone
import json
import pandas as pd
import textblob
'''                                                                                                                                                     
EX DATA:                                                                                                                                                
{"created_at":"Tue Oct 31 19:34:20 +0000 2017","id":925445854005284866,"id_str":"925445854005284866","text":"I wonder what kind of money are pumbing #B\
itcoinGold right now. \n\n#bitcoin" ...                                                                                                                 
'''


#        replace mysql.server with "localhost" if you are running via your own server!                                                                  
#                        server       MySQL usernameMySQL pass  Database name.                                                                          
#conn = MySQLdb.connect("mysql.server","beginneraccount","cookies","beginneraccount$tutorial")                                                          

#c = conn.cursor()                                                                                                                                      

'''                                                                                                                                                     
# Convert created_at to datetimes                                                                                                                       
df['created_at'] = pd.to_datetime(df['created_at'])                                                                                                     
'''


#consumer key, consumer secret, access token, access secret.                                                                                            
consumer_key = 'E3xLP2DJVCojAuRc4dsIQhOhH'
consumer_secret = '46e1t5l5uZDUY3WfuNf0NwzsNVdPnJS7qtVjVc6HKwxfH0BYX4'

access_token = '398425873-SL80lXVpCqZN8zTTNWSz6pBWRdy1CwzdWQlRrBEu'
access_token_secret = 'FAmHxrdwJfnrcjRVKvuxVRpoQfezjS7npTc6dH20EfwAq'

dataList = []
cols = ["Date", "Tweet", "Polarity", "Subjectivity"]
class listener(StreamListener):

    def on_data(self, data):
        try:
            #print(data)                                                                                                                                
            #full tweet                                                                                                                                 
            #tweet = data.split(',"text":"')[1].split('","source')[0] #give us the right side of the split [1] and then the left side [0]               
            #print(tweet)                                                                                                                               
            #saving the current tweet with unix timestamp                                                                                               
            #saveCur = str(time.time())+':::'+tweet                                                                                                     
            #print(saveCur)                                                                                                                             
            #dataList = []                                                                                                                              
            allData = json.loads(data)

            #remove new lines in file                                                                                                                   
            #allData.rstrip()                                                                                                                           

            tweet = allData["text"]
            date = allData["created_at"]
            blob = textblob.TextBlob(tweet).sentiment
            polarity = int(round(blob.polarity))
            subj = blob.subjectivity
            #print(date+tweet)                                                                                                                          
            #print("polarity is : "+ str(polarity))                                                                                                     
            #The polarity score is a float within the range [-1.0, 1.0] 1 is pos and -1 is neg                                                          
#The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.                                        
            dataList.append([date, tweet, polarity, subj])
            #list(filter((0).__ne__,dataList))                                                                                                          
            #print(dataList)                                                                                                                            
            #print(list)                                                                                                                                
            df = pd.DataFrame(dataList, columns=cols)
            #formating datetime from bla to bla                                                                                                         
            #datetime.datetime.strptime(df["created_at"], '%a %b %d %H:%M:%S %z %Y').replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%\
d %H:%M:%S')                                                                                                                                            
            if not df.empty:
                df["Date"] = pd.to_datetime(df["Date"], format="%a %b %d %H:%M:%S +0000 %Y")
                #pd.to_datetime(df['Date'])                                                                                                             

            #dropping duplicated timestamps                                                                                                             
            #df_clean = df.drop_duplicates(subset=['Date'],keep='last')                                                                                 

            #removing rows with polarity values of zero                                                                                                 
            df_clean = df[df.Polarity != 0]
            '''                                                                                                                                         
            #uncomment if want to remove subjective tweets                                                                                              
            df = df[df.Subjectivity != 1]                                                                                                               
            '''

            #finding the running sum of sentiment for each day                                                                                          
            df2 = df_clean.set_index('Date')
            df2['PolarityDailySum'] = df2.groupby(pd.TimeGrouper('D'))['Polarity'].cumsum()
            df2['SubjectivityDailySum'] = df2.groupby(pd.TimeGrouper('D'))['Subjectivity'].cumsum()

            #removing new line character from file                                                                                                      
            df2 = df2.replace('\n',' ', regex=True)

            #reset the index                                                                                                                            
            df2 = df2.reset_index()
            #saving df to csv file                                                                                                                      
            print(df2.head())
            #dropping duplicated timestamps                                                                                                             
            df_clean = df.drop_duplicates(subset=['Date'],keep='last')
            df2.to_csv('bitcoinSentimentClean.csv', mode='w+') #later add if codition chceking if not empty then append mode='a'                        

            #stream.filter(track=[t], stall_warnings=True)                                                                                              
            #df = data                                                                                                                                  
            #print(df.head())                                                                                                                           
        #saving to a file                                                                                                                               
            #savef = open('twitterBitcoin.csv','a')                                                                                                     
            #savef.write(dataList)                                                                                                                      
        #add new line                                                                                                                                   
            #savef.write('\n')                                                                                                                          
            #savef.close()                                                                                                                              

        #added to catch base exception, thread exception and                                                                                            
        except (IncompleteRead, BaseException, SocketError, ProtocolError, Exception) as e:
            print("failed ondata,",str(e))
            time.sleep(25)
            #clear the last thrown exception                                                                                                            
            sys.exc_clear()

        #saving to a database                                                                                                                           
        '''                                                                                                                                             
        all_data = json.loads(data)                                                                                                                     
                                                                                                                                                        
        tweet = all_data["text"]                                                                                                                        
                                                                                                                                                        
        username = all_data["user"]["screen_name"]                                                                                                      
                                                                                                                                                        
        c.execute("INSERT INTO taula (time, username, tweet) VALUES (%s,%s,%s)",                                                                        
            (time.time(), username, tweet))                                                                                                             
                                                                                                                                                        
        conn.commit()                               
         print((username,tweet))                                                                                                                         
        '''
        return True

    def on_error(self, status):
        print(status)
        if status == 420:
            return False

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["bitcoin"], stall_warnings=True, async=True)
