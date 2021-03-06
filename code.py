import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
train=pd.read_csv("C:/Users/A K Swami/Desktop/titanic/train.csv")
test=pd.read_csv("C:/Users/A K Swami/Desktop/titanic/test.csv")
train.describe(include="all")
print(train.columns)
print(pd.isnull(train).sum())
sns.barplot(x="Sex", y="Survived", data=train)
print("Percentage of women survived:", train["Survived"][train["Sex"]=='female'].value_counts(normalize=True)[1]*100)
print("Percentage of men survived:", train["Survived"][train["Sex"]=='male'].value_counts(normalize=True)[1]*100)
sns.barplot(x="Pclass",y="Survived", data=train)
print("Percentage of 1 Class survived:", train["Survived"][train["Pclass"]==1].value_counts(normalize=True)[1]*100)
print("Percentage of 2 Class survived:", train["Survived"][train["Pclass"]==2].value_counts(normalize=True)[1]*100)
print("Percentage of 3 Class survived:", train["Survived"][train["Pclass"]==3].value_counts(normalize=True)[1]*100)
train["Age"]=train["Age"].fillna(-0.5)
test["Age"]=test["Age"].fillna(0.5)
bins=[-1,0,5,12,18,24,35,60,np.inf]
labels=['Unknown','Baby','Child','Teenager','Student','Young Adult','Adult','Senior']
train['AgeGroup']=pd.cut(train["Age"], bins, labels=labels)
test['AgeGroup']=pd.cut(test["Age"], bins, labels=labels)
sns.barplot(x="AgeGroup", y="Survived", data=train)
plt.show()
train = train.drop(['Cabin'], axis = 1)
test = test.drop(['Cabin'], axis = 1)
train=train.drop(['Ticket'], axis=1)
train.head()
test=test.drop(['Ticket'], axis=1)
test.head()
print("Number of people embarking in s:")
s=train[train["Embarked"]=="S"].shape[0]
print(s)
print("Number of people embarking in c:")
c=train[train["Embarked"]=="C"].shape[0]
print(c)
print("Number of people embarking in q:")
q=train[train["Embarked"]=="Q"].shape[0]
print(q)
train=train.fillna({"Embarked":"S"})
train.head()
combine = [train, test]
for dataset in combine:
    dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)

pd.crosstab(train['Title'], train['Sex'])
for dataset in combine:
    dataset['Title'] = dataset['Title'].replace(['Lady', 'Capt', 'Col',
    'Don', 'Dr', 'Major', 'Rev', 'Jonkheer', 'Dona'], 'Rare')
    
    dataset['Title'] = dataset['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
    dataset['Title'] = dataset['Title'].replace('Mlle', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Mme', 'Mrs')

train[['Title', 'Survived']].groupby(['Title'], as_index=False).mean()
title_mapping={"Mr":1,"Miss":2,"Mrs": 3, "Master": 4, "Royal": 5, "Rare": 6}
for dataset in combine:
    dataset['Title']=dataset['Title'].map(title_mapping)
    dataset['Title']=dataset['Title'].fillna(0)
train.head()
mr_age = train[train["Title"] == 1]["AgeGroup"].mode() #Young Adult
miss_age = train[train["Title"] == 2]["AgeGroup"].mode() #Student
mrs_age = train[train["Title"] == 3]["AgeGroup"].mode() #Adult
master_age = train[train["Title"] == 4]["AgeGroup"].mode() #Baby
royal_age = train[train["Title"] == 5]["AgeGroup"].mode() #Adult
rare_age = train[train["Title"] == 6]["AgeGroup"].mode() #Adult
age_title_mapping = {1: "Young Adult", 2: "Student", 3: "Adult", 4: "Baby", 5: "Adult", 6: "Adult"}
for x in range(len(train["AgeGroup"])):
    if train["AgeGroup"][x] == "Unknown":
        train["AgeGroup"][x] = age_title_mapping[train["Title"][x]]
        
for x in range(len(test["AgeGroup"])):
    if test["AgeGroup"][x] == "Unknown":
        test["AgeGroup"][x] = age_title_mapping[test["Title"][x]]
age_mapping = {'Baby': 1, 'Child': 2, 'Teenager': 3, 'Student': 4, 'Young Adult': 5, 'Adult': 6, 'Senior': 7}
train['AgeGroup'] = train['AgeGroup'].map(age_mapping)
test['AgeGroup'] = test['AgeGroup'].map(age_mapping)

train.head()
train=train.drop(['Age'],axis=1)
test=test.drop(['Age'],axis=1)
train = train.drop(['Name'], axis = 1)
test = test.drop(['Name'], axis = 1)
sex_mapping = {"male": 0, "female": 1}
train['Sex'] = train['Sex'].map(sex_mapping)
test['Sex'] = test['Sex'].map(sex_mapping)
train.head()
embarked_mapping={"S":1,"C":2,"Q":3}
train["Embarked"]=train["Embarked"].map(embarked_mapping)
test["Embarked"]=test["Embarked"].map(embarked_mapping)
train.head()
for x in range(len(test["Fare"])):
    if pd.isnull(test["Fare"][x]):
        pclass = test["Pclass"][x] 
        test["Fare"][x] = round(train[train["Pclass"] == pclass]["Fare"].mean(), 4)
        
train['FareBand'] = pd.qcut(train['Fare'], 4, labels = [1, 2, 3, 4])
test['FareBand'] = pd.qcut(test['Fare'], 4, labels = [1, 2, 3, 4])

train = train.drop(['Fare'], axis = 1)
test = test.drop(['Fare'], axis = 1)

train.head()
from sklearn.cross_validation import train_test_split
predictors=train.drop(['Survived','PassengerId'],axis=1)
target=train["Survived"]
x_train,x_val,y_train,y_val=train_test_split(predictors,target,test_size=0.22,random_state=0)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

logreg=LogisticRegression()
logreg.fit(x_train,y_train)
y_pred=logreg.predict(x_val)
acc_logreg=round(accuracy_score(y_pred,y_val)*100,2)
print(acc_logreg)

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
gaussian=GaussianNB()
gaussian.fit(x_train,y_train)
y_pred=gaussian.predict(x_val)
acc_gaussian=round(accuracy_score(y_pred,y_val)*100,2)
print(acc_gaussian)

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

svc=SVC()
svc.fit(x_train,y_train)
y_pred=svc.predict(x_val)
acc_svc=round(accuracy_score(y_pred,y_val)*100,2)
print(acc_svc)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

random=RandomForestClassifier()
random.fit(x_train,y_train)
y_pred=random.predict(x_val)
acc_random=round(accuracy_score(y_pred,y_val)*100,2)
print(acc_random)

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

grad=GradientBoostingClassifier()
grad.fit(x_train,y_train)
y_pred=grad.predict(x_val)
acc_grad=round(accuracy_score(y_pred,y_val)*100,2)
print(acc_grad)

from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score

ada=AdaBoostClassifier()
ada.fit(x_train,y_train)
y_pred=ada.predict(x_val)
acc_ada=round(accuracy_score(y_pred,y_val)*100,2)
print(acc_ada)

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.cross_validation import train_test_split
predictors=train.drop(['Survived','PassengerId'],axis=1)
target=train["Survived"]
x_train,x_val,y_train,y_val=train_test_split(predictors,target,test_size=0.30,random_state=0)
#rf_cv = RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
rf_cv=GradientBoostingClassifier(n_estimators=10,max_depth=1)
rf_cv.fit(x_val,y_val)

ids = test['PassengerId']
predictions = rf_cv.predict(test.drop('PassengerId', axis=1))
output = pd.DataFrame({ 'PassengerId' : ids, 'Survived': predictions })
#output.to_csv('submission2.csv', index=True)
#print(output)
