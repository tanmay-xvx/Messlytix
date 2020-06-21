#!/usr/bin/env python
# coding: utf-8

# In[118]:


import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import pickle
from sklearn import linear_model


# In[119]:


df=pd.read_csv('veggieprices.csv')


# In[120]:


df.head()


# In[121]:


df['year'] = pd.DatetimeIndex(df['Date']).year


# In[122]:


df.head()


# In[123]:


df['Price']=df['Price'].replace(0,np.nan)
#dataset['datesk']=dataset['datesk'].replace(0,np.nan)
#dataset['Item Name']=dataset['Item Name'].replace(0,np.nan)
df.dropna(inplace=True)


# In[124]:


df.head()


# In[125]:


df.describe()


# In[126]:


df.info()


# In[127]:


i=['Spring Onion','Potato(M)','Raddish','Coconut (M)','Ginger','Cabbage','Capsicum','Beans','Brinjal (W)']
dff=df.loc[df['Item_Name'].isin(i)]
dff.head()


# In[130]:


dff['month'] = pd.to_datetime(dff.Date).apply(lambda x: x.month)
dff['day'] = pd.to_datetime(dff.Date).apply(lambda x: x.day)
dff['dayname'] = pd.to_datetime(dff.Date).apply(lambda x: x.day_name())
dff


# In[131]:


X=dff.drop('Price',axis=1)
X=dff.drop('Date',axis=1)
X=dff.drop('Datesk',axis=1)
Y=dff['Price']


# In[132]:


X=dff.drop('Date',axis=1)
X


# In[135]:


X=dff.drop('Datesk',axis=1)
X=X.drop('Date',axis=1)
X=X.drop('Price',axis=1)
X


# In[107]:


import seaborn as sns
sns.distplot(dff['Price']);


# In[136]:


#veggies to text
def convert_to_int(word):
    word_dict = {'Spring Onion':1, 'Potato(M)':2, 'Raddish':3, 'Coconut (M)':4, 'Ginger':5, 'Cabbage': 6, 'Capsicum':7,'Beans':8,'Brinjal (W)':9,0:0}
    return word_dict[word]

X['Item_Name'] = X['Item_Name'].apply(lambda x : convert_to_int(x))


# In[137]:


#For days

def convert_to_int(word):
    word_dict = {'Monday':1, 'Tuesday':2, 'Wednesday':3, 'Thursday':4, 'Friday':5, 'Saturday': 6, 'Sunday':7,0:0}
    return word_dict[word]

X['dayname'] = X['dayname'].apply(lambda x : convert_to_int(x))


# In[138]:


X.head()


# In[181]:


#Training using Random Forest

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state = 2)


# In[182]:


from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

acc1 = regressor.score(X_test, y_test)
print(acc1)


# In[165]:


predicted= regressor.predict(X_test)
x_test1=np.array(X_test)
y_test1=np.array(y_test)


# In[166]:


#Comparing predicitons with actual results
for w in range(1000):
    print(y_test1[w],' ',x_test1[w])
    print("{:.2f}".format(predicted[w]))
    print()


# In[172]:


import datetime 
import calendar 


#word_dict = {'Spring Onion':1, 'Potato(M)':2, 'Raddish':3, 'Coconut (M)':4, 'Ginger':5, 'Cabbage': 6, 'Capsicum':7,'Beans':8,'Brinjal (W)':9,0:0}

def wordd():
    if new_Item_Name=='Spring Onion':
        Item=1
    elif new_Item_Name=='Potato(M)':
        Item=2
    elif new_Item_Name=='Raddish':
        Item=3
    elif new_Item_Name=='Coconut (M)':
        Item=4
    elif new_Item_Name=='Ginger':
        Item=5   
    elif new_Item_Name=='Cabbage':
        Item=6
    elif new_Item_Name=='Capsicum':
        Item=7
    elif new_Item_Name=='Beans':
        Item=8
    elif new_Item_Name=='Brinjal (W)': 
        Item=9
    else:
        print('Please enter correct choice')
        


def inputt():
    

    datee = datetime.datetime.strptime(new_date, "%d-%m-%Y")


    new_month=datee.month


    new_year=datee.year


    new_day=datee.day
    



# In[194]:


new_date=input('Enter Date :')

def month():
    
    datee = datetime.datetime.strptime(new_date, "%d-%m-%Y")


    return datee.month

def year():
    
    datee = datetime.datetime.strptime(new_date, "%d-%m-%Y")
    return datee.year

def day():
    datee = datetime.datetime.strptime(new_date, "%d-%m-%Y")
    return datee.day
    

new_Item_Name=input('Enter Food Item :')
def wordd():
    if new_Item_Name=='Spring Onion':
        return 1
    elif new_Item_Name=='Potato(M)':
        return 2
    elif new_Item_Name=='Raddish':
        return 3
    elif new_Item_Name=='Coconut (M)':
        return 4
    elif new_Item_Name=='Ginger':
        return 5   
    elif new_Item_Name=='Cabbage':
        return 6
    elif new_Item_Name=='Capsicum':
        return 7
    elif new_Item_Name=='Beans':
        return 8
    elif new_Item_Name=='Brinjal (W)': 
        return 9
    else:
        return 0
        

def findDay(): 
    born = datee = datetime.datetime.strptime(new_date, "%d-%m-%Y").weekday() 
    day=(calendar.day_name[born])   
    if day =='Monday':
        return 0
    elif day =='Tuesday':
        return 1
    elif day =='Wednesday':
        return 2
    elif day =='Thursday':
        return 3
    elif day =='Friday':
        return 4
    elif day =='Saturday':
        return 5
    elif day =='Sunday':
        return 6



day_name=findDay()
Item=wordd()
new_month=month()
new_year=year()
new_day=day()



inputtt=[Item,new_year,new_month,new_day,day_name]
inputtt = np.asarray(inputtt)
inputtt.reshape(-1,1)
print ('Predicted Item Price: \n', "Rs.",regressor.predict([inputtt]))
pickle.dump(regressor,open('costpred.pkl', 'wb'))


# In[ ]:




