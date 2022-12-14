#-------------------------------------------------------------------------
# AUTHOR: Roberto Toribio
# FILENAME: Bagging Random Forest
# SPECIFICATION: description of the program
# FOR: CS 4210- Assignment #3
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard vectors and arrays

#importing some Python libraries
from sklearn import tree
from sklearn import ensemble
from sklearn.utils import resample
from sklearn.ensemble import RandomForestClassifier
import csv
dbTraining = []
dbTest = []
X_training = []
y_training = []
classVotes = [] #this array will be used to count the votes of each classifier

#reading the training data from a csv file and populate dbTraining
#--> add your Python code here

with open('optdigits.tra', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
      if i > 0: #skipping the header
         dbTraining.append (row)
         #print(row)
#reading the test data from a csv file and populate dbTest
#--> add your Python code here

with open('optdigits.tes', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
      if i > 0: #skipping the header
         dbTest.append (row)
         #print(row)
#inititalizing the class votes for each test sample. Example: classVotes.append([0,0,0,0,0,0,0,0,0,0])
#--> add your Python code here
class_votes = [[0,0,0,0,0,0,0,0,0,0] for i in range(len(dbTest))]
#print("Class votes at start are", class_votes)
print("Started my base and ensemble classifier ...")

accuracy = 0
for k in range(20): #we will create 20 bootstrap samples here (k = 20). One classifier will be created for each bootstrap sample

  bootstrapSample = resample(dbTraining, n_samples=len(dbTraining), replace=True)

  #populate the values of X_training and y_training by using the bootstrapSample
  #--> add your Python code here
  for sample in bootstrapSample:
      X_training.append(sample[0:64])
      y_training.append(sample[64])
  #fitting the decision tree to the data
  #print("bagging sample is:", X_training[k])
  clf = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth=None) #we will use a single decision tree without pruning it
  clf = clf.fit(X_training, y_training)
  correct_cnt = 0
  for i, testSample in enumerate(dbTest):
      
      #make the classifier prediction for each test sample and update the corresponding index value in classVotes. For instance,
      # if your first base classifier predicted 2 for the first test sample, then classVotes[0,0,0,0,0,0,0,0,0,0] will change to classVotes[0,0,1,0,0,0,0,0,0,0].
      # Later, if your second base classifier predicted 3 for the first test sample, then classVotes[0,0,1,0,0,0,0,0,0,0] will change to classVotes[0,0,1,1,0,0,0,0,0,0]
      # Later, if your third base classifier predicted 3 for the first test sample, then classVotes[0,0,1,1,0,0,0,0,0,0] will change to classVotes[0,0,1,2,0,0,0,0,0,0]
      # this array will consolidate the votes of all classifier for all test samples
      #--> add your Python code here
      prediction = clf.predict([testSample[0:64]])[0]
      class_votes[i][int(prediction)] +=1
  
  
      if k == 0: #for only the first base classifier, compare the prediction with the true label of the test sample here to start calculating its accuracy
         #--> add your Python code here
         if prediction == testSample[64]:
            correct_cnt +=1

  if k == 0: #for only the first base classifier, print its accuracy here
     #--> add your Python code here
     accuracy = correct_cnt / len(dbTest)
     print("Finished my base classifier (fast but relatively low accuracy) ...")
     print("My base classifier accuracy: " + str(accuracy))
     print("")

#now, compare the final ensemble prediction (majority vote in classVotes) for each test sample with the ground truth label to calculate the accuracy of the ensemble classifier 
# (all base classifiers together)
#--> add your Python code here
ensemble_correct_cnt = 0
for i in range(len(class_votes)):
   ensemble_prediction = class_votes[i].index(max(class_votes[i]))
   if ensemble_prediction == int(dbTest[i][64]):
      ensemble_correct_cnt +=1
   #printing the ensemble accuracy here
accuracy = ensemble_correct_cnt / len(class_votes)

print("Finished my ensemble classifier (slow but higher accuracy) ...")
print("My ensemble accuracy: " + str(accuracy))
print("")

print("Started Random Forest algorithm ...")

#Create a Random Forest Classifier
clf=RandomForestClassifier(n_estimators=20) #this is the number of decision trees that will be generated by Random Forest. The sample of the ensemble method used before

#Fit Random Forest to the training data
clf.fit(X_training,y_training)

#make the Random Forest prediction for each test sample. Example: class_predicted_rf = clf.predict([[3, 1, 2, 1, ...]]
#--> add your Python code here
rf_correct_cnt = 0
for test_sample in dbTest:
   class_predicted_rf = clf.predict([test_sample[0:64]])[0]
  
   #compare the Random Forest prediction for each test sample with the ground truth label to calculate its accuracy
   #--> add your Python code here
   
   if int(class_predicted_rf) == int(test_sample[64]):
      rf_correct_cnt +=1

accuracy = rf_correct_cnt/ len(dbTest)
#printing Random Forest accuracy here
print("Random Forest accuracy: " + str(accuracy))
print("Finished Random Forest algorithm (much faster and higher accuracy!) ...")
