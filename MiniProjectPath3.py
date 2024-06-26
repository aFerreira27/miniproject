#MiniProjectPath3
import numpy as np
import matplotlib.pyplot as plt
# Import datasets, classifiers and performance metrics
from sklearn import datasets, svm, metrics
from sklearn.decomposition import KernelPCA
from sklearn.model_selection import train_test_split
#import models
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import copy


rng = np.random.RandomState(1)
digits = datasets.load_digits()
images = digits.images
labels = digits.target

#Get our training data
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.6, shuffle=False)

def dataset_searcher(number_list,images,labels):
  #insert code that when given a list of integers, will find the labels and images
  #and put them all in numpy arrary (at the same time, as training and testing data)

  images_nparray = np.empty((0, *images.shape[1:]))
  labels_nparray = np.empty(0)

  for i, number in enumerate(labels):
        if number in number_list:
            images_nparray = np.concatenate((images_nparray, [images[i]]), axis=0)  # Append image
            labels_nparray = np.append(labels_nparray, number)  # Append label
    
  return images_nparray, labels_nparray

def print_numbers(images,labels):
  #insert code that when given images and labels (of numpy arrays)
  #the code will plot the images and their labels in the title. 
  for i, image in enumerate(images):
        plt.title(f"Image #{i+1}, class {int(labels[i])}")
        plt.imshow(image, cmap='gray')
        plt.axis('off')
        plt.show()

class_numbers = [2,0,8,7,5]
#Part 1
class_number_images , class_number_labels = dataset_searcher(class_numbers, images, labels)
#Part 2
print_numbers(class_number_images , class_number_labels)


model_1 = GaussianNB()

#however, before we fit the model we need to change the 8x8 image data into 1 dimension
# so instead of having the Xtrain data beign of shape 718 (718 images) by 8 by 8
# the new shape would be 718 by 64
X_train_reshaped = X_train.reshape(X_train.shape[0], -1)

#Now we can fit the model
model_1.fit(X_train_reshaped, y_train)
#Part 3 Calculate model1_results using model_1.predict()
model1_results = model_1.predict(X_test.reshape(len(X_test), -1))


def OverallAccuracy(results, actual_values):
  correct = 0
  for i, prediction in enumerate(results):
      if prediction == actual_values[i]:
          correct += 1

  Accuracy = correct / len(actual_values)  
  return Accuracy


# Part 4
Model1_Overall_Accuracy = OverallAccuracy(model1_results, y_test)
print("The overall results of the Gaussian model (Test Data) is " + str(Model1_Overall_Accuracy))


#Part 5
allnumbers = [0,1,2,3,4,5,6,7,8,9]
allnumbers_images, allnumbers_labels = dataset_searcher(allnumbers, images, labels)

model1_results = model_1.predict(allnumbers_images.reshape(len(allnumbers_images), -1))
Model1_Overall_Accuracy = OverallAccuracy(model1_results, allnumbers_labels)
print("The overall results of the Gaussian model (ALL NUMBERS) is " + str(Model1_Overall_Accuracy))


#Part 6
#Repeat for K Nearest Neighbors
model_2 = KNeighborsClassifier(n_neighbors=10)

model_2.fit(X_train_reshaped, y_train)
model2_results = model_2.predict(X_test.reshape(len(X_test), -1))

Model2_Overall_Accuracy = OverallAccuracy(model2_results, y_test)
print("The overall results of the K Nearest Neighbors model (Test Data) is " + str(Model2_Overall_Accuracy))

model2_results = model_2.predict(allnumbers_images.reshape(len(allnumbers_images), -1))
Model2_Overall_Accuracy = OverallAccuracy(model2_results, allnumbers_labels)
print("The overall results of the K Nearest Neighbors model (ALL NUMBERS) is " + str(Model2_Overall_Accuracy))


#Repeat for the MLP Classifier
model_3 = MLPClassifier(random_state=0, max_iter=400)

model_3.fit(X_train_reshaped, y_train)
model3_results = model_3.predict(X_test.reshape(len(X_test), -1))

Model3_Overall_Accuracy = OverallAccuracy(model3_results, y_test)
print("The overall results of the MLP Classifier model (Test Data) is " + str(Model3_Overall_Accuracy))

model3_results = model_3.predict(allnumbers_images.reshape(len(allnumbers_images), -1))
Model3_Overall_Accuracy = OverallAccuracy(model3_results, allnumbers_labels)
print("The overall results of the MLP Classifier model (ALL NUMBERS) is " + str(Model3_Overall_Accuracy))


#Part 8
#Poisoning
# Code for generating poison data. There is nothing to change here.
noise_scale = 10.0
poison = rng.normal(scale=noise_scale, size=X_train.shape)

X_train_poison = X_train + poison

#Part 9-11
#Determine the 3 models performance but with the poisoned training data X_train_poison and y_train instead of X_train and y_train

X_train_poison_reshaped = X_train_poison.reshape(X_train_poison.shape[0], -1)

model_1.fit(X_train_poison_reshaped, y_train)
model1_results_poison = model_1.predict(X_test.reshape(len(X_test), -1))

Model1_poison_Overall_Accuracy = OverallAccuracy(model1_results_poison, y_test)
print("The overall results of the Gaussian model (Poisened Test Data) is " + str(Model1_poison_Overall_Accuracy))

model_2.fit(X_train_poison_reshaped, y_train)
model2_results_poison = model_2.predict(X_test.reshape(len(X_test), -1))

Model2_poison_Overall_Accuracy = OverallAccuracy(model2_results_poison, y_test)
print("The overall results of the K Nearest Neighbors model (Poisened Test Data) is " + str(Model2_poison_Overall_Accuracy))

model_3.fit(X_train_poison_reshaped, y_train)
model3_results_poison = model_3.predict(X_test.reshape(len(X_test), -1))

Model3_poison_Overall_Accuracy = OverallAccuracy(model3_results_poison, y_test)
print("The overall results of the MLP Classifier model (Poisened Test Data) is " + str(Model3_poison_Overall_Accuracy))

#Part 12-13
# Denoise the poisoned training data, X_train_poison. 
# hint --> Suggest using KernelPCA method from sklearn library, for denoising the data. 
# When fitting the KernelPCA method, the input image of size 8x8 should be reshaped into 1 dimension
# So instead of using the X_train_poison data of shape 718 (718 images) by 8 by 8, the new shape would be 718 by 64

X_train_poison_reshaped = X_train_poison.reshape((X_train_poison.shape[0], -1))

kernel_pca = KernelPCA(
    n_components=1000,
    kernel="rbf",
    gamma=1e-3,
    fit_inverse_transform=True,
    alpha=5e-3,
    random_state=42,
)

kernel_pca.fit(X_train_poison_reshaped)

X_reconstructed_kernel_pca = kernel_pca.inverse_transform(
    kernel_pca.transform(X_train_poison_reshaped)
)

#Part 14-15
#Determine the 3 models performance but with the denoised training data, X_train_denoised and y_train instead of X_train_poison and y_train
#Explain how the model performances changed after the denoising process.

model_1.fit(X_reconstructed_kernel_pca, y_train)
model1_results_denoised = model_1.predict(X_test.reshape(len(X_test), -1))
Model1_denoised_Overall_Accuracy = OverallAccuracy(model1_results_denoised, y_test)
print("The overall results of the Gaussian model (Denoised Test Data) is " + str(Model1_denoised_Overall_Accuracy))

model_2.fit(X_reconstructed_kernel_pca, y_train)
model2_results_denoised = model_2.predict(X_test.reshape(len(X_test), -1))
Model2_denoised_Overall_Accuracy = OverallAccuracy(model2_results_denoised, y_test)
print("The overall results of the K Nearest Neighbors model (Denoised Test Data) is " + str(Model2_denoised_Overall_Accuracy))

model_3.fit(X_reconstructed_kernel_pca, y_train)
model3_results_denoised = model_3.predict(X_test.reshape(len(X_test), -1))
Model3_denoised_Overall_Accuracy = OverallAccuracy(model3_results_denoised, y_test)
print("The overall results of the MLP Classifier model (Denoised Test Data) is " + str(Model3_denoised_Overall_Accuracy))