import numpy as np
from scipy.optimize import minimize
from scipy.io import loadmat
from numpy.linalg import det, inv
from math import sqrt, pi
import scipy.io
import matplotlib.pyplot as plt
import pickle
import sys

def ldaLearn(X,y):
    # Inputs
    # X - a N x d matrix with each row corresponding to a training example
    # y - a N x 1 column vector indicating the labels for each training example
    #
    # Outputs
    # means - A d x k matrix containing learnt means for each of the k classes
    # covmat - A single d x d learnt covariance matrix

    # IMPLEMENT THIS METHOD
    N,d = len(X),len(X[0])
    Xnew = np.hstack((X,y))
    kElements = np.unique(Xnew[:,-1])
    means = []
    for i in range(d):
        meanRow = []
        for ele in kElements:
            meanRow.append(Xnew[Xnew[:,-1] == ele,i].mean())
        means.append(meanRow)
    covmat = np.cov(np.transpose(X))

    return means,covmat

def qdaLearn(X,y):
    # Inputs
    # X - a N x d matrix with each row corresponding to a training example
    # y - a N x 1 column vector indicating the labels for each training example
    #
    # Outputs
    # means - A d x k matrix containing learnt means for each of the k classes
    # covmats - A list of k d x d learnt covariance matrices for each of the k classes

    # IMPLEMENT THIS METHOD
    N,d = len(X),len(X[0])
    Xnew = np.hstack((X,y))
    kElements = np.unique(Xnew[:,-1])
    means = []
    covmats = []
    for i in range(d):
        meanRow = []
        for ele in kElements:
            meanRow.append(Xnew[Xnew[:,-1] == ele,i].mean())
        means.append(meanRow)
    for ele in kElements:
        classX = Xnew[Xnew[:,-1] == ele,:-1]
        covmat = np.cov(np.transpose(classX))
        covmats.append(covmat)
    # print(means)
    # print(covmats)
    return means,covmats

def ldaTest(means,covmat,Xtest,ytest):
    # Inputs
    # means, covmat - parameters of the LDA model
    # Xtest - a N x d matrix with each row corresponding to a test example
    # ytest - a N x 1 column vector indicating the labels for each test example
    # Outputs
    # acc - A scalar accuracy value
    # ypred - N x 1 column vector indicating the predicted labels
    # IMPLEMENT THIS METHOD
    numClasses = len(means[0])
    kElements = [1,2,3,4,5]
    covmatInv = np.linalg.inv(covmat)
    means = np.array(means)
    predProbability = np.empty(shape = (len(Xtest),numClasses))
    ytestLen = len(ytest)
    for i in range(numClasses):
        for j in range(len(Xtest)):
            tranRow = Xtest[j,:] - means[:,i]
            mahaDist = np.dot(np.dot(np.transpose(tranRow),covmatInv),tranRow)
            numerator = np.exp(-(1/2)*mahaDist)
            denominator = np.sqrt(np.linalg.det(covmat))
            predProbability[j,i] = numerator/denominator
    ypred = np.argmax(predProbability,axis=1)
    match =0
    for i in range(ytestLen):
        if((kElements[ypred[i]]) == ytest[i,0]):
            match+=1
        ypred[i] = kElements[ypred[i]]
    acc = match/ytestLen
    ypred = ypred.reshape(ytestLen,1)
    return acc,ypred

def qdaTest(means,covmats,Xtest,ytest):
    # Inputs
    # means, covmats - parameters of the QDA model
    # Xtest - a N x d matrix with each row corresponding to a test example
    # ytest - a N x 1 column vector indicating the labels for each test example
    # Outputs
    # acc - A scalar accuracy value
    # ypred - N x 1 column vector indicating the predicted labels

    # IMPLEMENT THIS METHOD
    numClasses = len(means[0])
    kElements = [1,2,3,4,5]
    means = np.array(means)
    predProbability = np.empty(shape = (len(Xtest),numClasses))
    ytestLen = len(ytest)
    for i in range(numClasses):
        for j in range(len(Xtest)):
            tranRow = Xtest[j,:] - means[:,i]
            mahaDist = np.dot(np.dot(np.transpose(tranRow),np.linalg.inv(covmats[i])),tranRow)
            numerator = np.exp(-(1/2)*mahaDist)
            denominator = np.sqrt(np.linalg.det(covmats[i]))
            predProbability[j,i] = numerator/denominator
    ypred = np.argmax(predProbability,axis=1)
    match =0
    for i in range(ytestLen):
        if((kElements[ypred[i]]) == ytest[i,0]):
            match+=1
        ypred[i] = kElements[ypred[i]]
    acc = match/ytestLen
    ypred = ypred.reshape(ytestLen,1)
    return acc,ypred

def learnOLERegression(X,y):
    # Inputs:
    # X = N x d
    # y = N x 1
    # Output:
    # w = d x 1

    # IMPLEMENT THIS METHOD

    Xtranspose = np.transpose(X)
    w = np.dot(np.dot(np.linalg.inv(np.dot(Xtranspose,X)),Xtranspose),y)
    # print(w)
    return w

def learnRidgeRegression(X,y,lambd):
    # Inputs:
    # X = N x d
    # y = N x 1
    # lambd = ridge parameter (scalar)
    # Output:
    # w = d x 1

    # IMPLEMENT THIS METHOD
    Xshape = X.shape
    Xtranspose = np.transpose(X)
    identityMat = np.identity(Xshape[1])
    w = np.dot(np.dot(np.linalg.inv((lambd*identityMat)+ np.dot(Xtranspose,X)),Xtranspose),y)
    # print(w)
    return w

def testOLERegression(w,Xtest,ytest):
    # Inputs:
    # w = d x 1
    # Xtest = N x d
    # ytest = X x 1
    # Output:
    # mse

    # IMPLEMENT THIS METHOD
    Xshape = Xtest.shape
    N = Xshape[0]
    mse = np.sum(np.square(ytest - np.dot(Xtest,w)))/N
    return mse

def regressionObjVal(w, X, y, lambd):

    # compute squared error (scalar) and gradient of squared error with respect
    # to w (vector) for the given data X and y and the regularization parameter
    # lambda

    # IMPLEMENT THIS METHOD
    # print(w)
    wTranspose = np.transpose(w)
    Xtranspose = np.transpose(X)
    w = w.reshape(len(w),1)
    # print(X.shape,w.shape)
    error = 0.5*((np.sum(np.square(y - np.dot(X,w)))) +  lambd* np.dot(wTranspose,w))
    # print(error)
    error_grad = (((np.dot((np.dot(Xtranspose, X)),w))- np.dot(Xtranspose, y)) + (lambd * w))
    # print(error_grad)
    error_grad = error_grad.flatten()
    return error, error_grad

def mapNonLinear(x,p):
    # Inputs:
    # x - a single column vector (N x 1)
    # p - integer (>= 0)
    # Outputs:
    # Xp - (N x (p+1))

    # IMPLEMENT THIS METHOD
    Xp = np.ones((len(x),p+1))
    # print(p,Xp)
    for i in range(1,p+1):
        Xp[:,i] = pow(x,i)
    # print(Xp)
    return Xp

# Main script

# Problem 1
# load the sample data
if sys.version_info.major == 2:
    X,y,Xtest,ytest = pickle.load(open('sample.pickle','rb'))
else:
    X,y,Xtest,ytest = pickle.load(open('sample.pickle','rb'),encoding = 'latin1')

# LDA
means,covmat = ldaLearn(X,y)
ldaacc,ldares = ldaTest(means,covmat,Xtest,ytest)
print('LDA Accuracy = '+str(ldaacc))
# QDA
means,covmats = qdaLearn(X,y)
qdaacc,qdares = qdaTest(means,covmats,Xtest,ytest)
print('QDA Accuracy = '+str(qdaacc))

# # plotting boundaries
x1 = np.linspace(-5,20,100)
x2 = np.linspace(-5,20,100)
xx1,xx2 = np.meshgrid(x1,x2)
xx = np.zeros((x1.shape[0]*x2.shape[0],2))
xx[:,0] = xx1.ravel()
xx[:,1] = xx2.ravel()

fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)

zacc,zldares = ldaTest(means,covmat,xx,np.zeros((xx.shape[0],1)))
plt.contourf(x1,x2,zldares.reshape((x1.shape[0],x2.shape[0])),alpha=0.3)
plt.scatter(Xtest[:,0],Xtest[:,1],c=ytest.ravel())
plt.title('LDA')

plt.subplot(1, 2, 2)

zacc,zqdares = qdaTest(means,covmats,xx,np.zeros((xx.shape[0],1)))
plt.contourf(x1,x2,zqdares.reshape((x1.shape[0],x2.shape[0])),alpha=0.3)
plt.scatter(Xtest[:,0],Xtest[:,1],c=ytest.ravel())
plt.title('QDA')

plt.show()
# # # Problem 2
if sys.version_info.major == 2:
    X,y,Xtest,ytest = pickle.load(open('diabetes.pickle','rb'))
else:
    X,y,Xtest,ytest = pickle.load(open('diabetes.pickle','rb'),encoding = 'latin1')

# # add intercept
X_i = np.concatenate((np.ones((X.shape[0],1)), X), axis=1)
Xtest_i = np.concatenate((np.ones((Xtest.shape[0],1)), Xtest), axis=1)

w = learnOLERegression(X,y)
mle = testOLERegression(w,Xtest,ytest)

w_i = learnOLERegression(X_i,y)
mle_i = testOLERegression(w_i,Xtest_i,ytest)

#For test data
print('MSE without intercept '+str(mle))
print('MSE with intercept '+str(mle_i))

#for training data
mle = testOLERegression(w,X,y)
mle_i = testOLERegression(w_i,X_i,y)

print('MSE without intercept for train data '+str(mle))
print('MSE with intercept train data '+str(mle_i))
#Calculate MSE for training data and compare
# # Problem 3
k = 101
lambdas = np.linspace(0, 1, num=k)
i = 0
mses3_train = np.zeros((k,1))
mses3 = np.zeros((k,1))
for lambd in lambdas:
    w_l = learnRidgeRegression(X_i,y,lambd)
    mses3_train[i] = testOLERegression(w_l,X_i,y)
    mses3[i] = testOLERegression(w_l,Xtest_i,ytest)
    i = i + 1
# print("lambdas"," ","mse train","            ","mse test")
# minVal_train = mses3_train[0][1]
# minVal_test = mses3[0][1]
# for i in range(101):
#     if(minVal_train>mses3_train[i][0]):
#         minVal_train = mses3_train[i][0]
#     if(minVal_test>mses3[i][0]):
#         minVal_test = mses3[i][0]
# print(lambdas[i]," ",mses3_train[i][0]," ",mses3[i][0])
# print(minVal_train,minVal_test)
fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)
plt.plot(lambdas,mses3_train)
plt.title('MSE for Train Data')
plt.subplot(1, 2, 2)
plt.plot(lambdas,mses3)
plt.title('MSE for Test Data')

plt.show()
# # Problem 4
k = 101
lambdas = np.linspace(0, 1, num=k)
i = 0
mses4_train = np.zeros((k,1))
mses4 = np.zeros((k,1))
opts = {'maxiter' : 20}    # Preferred value.
w_init = np.ones((X_i.shape[1],1))
for lambd in lambdas:
    args = (X_i, y, lambd)
    w_l = minimize(regressionObjVal, w_init, jac=True, args=args,method='CG', options=opts)
    w_l = np.transpose(np.array(w_l.x))
    w_l = np.reshape(w_l,[len(w_l),1])
    mses4_train[i] = testOLERegression(w_l,X_i,y)
    mses4[i] = testOLERegression(w_l,Xtest_i,ytest)
    i = i + 1
# print("lambda"," ","MSE train"," ","MSE test")
# for i in range(50,101):
#     print(lambdas[i]," ",mses4_train[i][0]," ",mses4[i][0])
# print(" ",mses4_train," ",mses4)
# print(minVal_train,minVal_test)
fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)
plt.plot(lambdas,mses4_train)
plt.plot(lambdas,mses3_train)
plt.title('MSE for Train Data')
plt.legend(['Using scipy.minimize','Direct minimization'])

plt.subplot(1, 2, 2)
plt.plot(lambdas,mses4)
plt.plot(lambdas,mses3)
plt.title('MSE for Test Data')
plt.legend(['Using scipy.minimize','Direct minimization'])
plt.show()


# # Problem 5
pmax = 7
lambda_opt = 0.06 # REPLACE THIS WITH lambda_opt estimated from Problem 3
mses5_train = np.zeros((pmax,2))
mses5 = np.zeros((pmax,2))
for p in range(pmax):
    Xd = mapNonLinear(X[:,2],p)
    Xdtest = mapNonLinear(Xtest[:,2],p)
    w_d1 = learnRidgeRegression(Xd,y,0)
    mses5_train[p,0] = testOLERegression(w_d1,Xd,y)
    mses5[p,0] = testOLERegression(w_d1,Xdtest,ytest)
    w_d2 = learnRidgeRegression(Xd,y,lambda_opt)
    mses5_train[p,1] = testOLERegression(w_d2,Xd,y)
    mses5[p,1] = testOLERegression(w_d2,Xdtest,ytest)

fig = plt.figure(figsize=[12,6])
# print("p" , "No Regularization","     Regularization")
# for i in range(7):
#     print(i,mses5_train[i][0],mses5_train[i][1])
plt.subplot(1, 2, 1)
plt.plot(range(pmax),mses5_train)
plt.title('MSE for Train Data')
plt.legend(('No Regularization','Regularization'))
plt.subplot(1, 2, 2)
plt.plot(range(pmax),mses5)
plt.title('MSE for Test Data')
plt.legend(('No Regularization','Regularization'))
plt.show()
