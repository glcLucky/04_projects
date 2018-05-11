setwd('E:/learning documents/regression analysis/ppt1/ppt/ppt1')
ex1<-read.csv("example1.csv")
head(ex1)
Y<-ex1$Y
X<-ex1$X
plot(X,Y)
model1<-lm(Y~X)
summary(model1)
model12<-lm(Y~X+I(X^2))
summary(model12)
anova(model1)
LwrUpr<-predict(model1,newdata=data.frame(X=X),interval = "prediction")
fit<-LwrUpr[1:13]
lwr<-LwrUpr[14:26]
upr<-LwrUpr[27:39]
plot(X,fit,ylim=c(min(fit,upr,lwr),max(fit,upr,lwr)))
points(X,upr)
points(X,lwr)
plot(model1)

#example1-2
ex1_2<-read.csv("example1_2.csv")
head(ex1_2)
Y<-ex1_2[,1]
X1<-ex1_2[,2]
X2<-ex1_2[,3]
plot(X1,Y)
plot(X2,Y)
model1_2<-lm(Y~X1+X2)
summary(model1_2)
plot(model1_2)
plot(model1_2$fitted.values,model1_2$residuals)

ex1_2ou<-ex1_2
ex1_2ou[17,]=c(0,0,0)
Y<-ex1_2ou[,1]
X1<-ex1_2ou[,2]
X2<-ex1_2ou[,3]
model1_2_2<-lm(Y~X1+X2)
plot(model1_2_2)
hatvalues(model1_2_2)

rstandard(model1_2_2)
qt(0.025,15)
qt(0.975,15)

rstudent(model1_2_2)
qt(0.025,14)

cooks.distance(model1_2_2)





#example2
install.packages("car")
library(car)
library(MASS)
ex2<-read.csv("example2.csv")
head(ex2)
Y<-ex2$R...D费用支出
X<-ex2$销售额
plot(X,Y)
model2<-lm(Y~X)
summary(model2)
plot(X,residuals(model2))
boxcox(Y~ X,lambda = seq(-2, 2, length = 100))
summary(p1 <- powerTransform(Y))
Y2<-log(Y)
model2_2<-lm(Y2~X)
summary(model2_2)
plot(X,residuals(model2_2))
summary(p2 <- powerTransform(Y2))
summary(model2_2)


#example3
library(car)
library(MASS)
ex3<-read.csv("example3.csv")
head(ex3)
M<-ex3[c(2,3,4,5)]
cor(M)
M2<-as.matrix(M)
M3<-scale(M2)
eigen(t(M3)%*%M3)
model3<-lm(ex3$Y~ex3$X1+ex3$X2+ex3$X3+ex3$X4)
summary(model3)
vif(model3)
#Ridge方法
plot(lm.ridge(ex3$Y~ex3$X1+ex3$X2+ex3$X3+ex3$X4,longley,lambda = seq(0,1,0.0001)))
select(lm.ridge(ex3$Y~ex3$X1+ex3$X2+ex3$X3+ex3$X4,longley,lambda = seq(0,1,0.0001)))
model3_2<-lm.ridge(ex3$Y~ex3$X1+ex3$X2+ex3$X3+ex3$X4,lambda =0.1461 )
summary(model3_2)
model3_2[1]
#主成分分析
ev<-eigen(cor(M))
plot(ev$values,type='l')
ev$values[1]/sum(ev$values)
y1<-t(as.matrix(ev$vectors[,1]))%*%t(M2)
y2<-t(as.matrix(ev$vectors[,2]))%*%t(M2)
y3<-t(as.matrix(ev$vectors[,3]))%*%t(M2)
y4<-t(as.matrix(ev$vectors[,4]))%*%t(M2)

model3_4<-lm(ex3$Y~as.vector(y1))
summary(model3_4)

model3_5<-lm(ex3$Y~as.vector(y1)+as.vector(y2))
summary(model3_5)

model3_6<-lm(ex3$Y~as.vector(y1)+as.vector(y2)+as.vector(y3))
summary(model3_6)

model3_7<-lm(ex3$Y~as.vector(y1)+as.vector(y2)+as.vector(y3)++as.vector(y4))
summary(model3_7)

model3_3<-princomp(M)
summary(model3_3)
screeplot(model3_3)
loadings(model3_3)

#LASS0
library(glmnet)
M3<-scale(M2)
Y2<-scale(ex3$Y)
la<-glmnet(M3,Y2,alpha=1,lambda=seq(0,1,0.1))
coef(la)
#library(lars)
#las = lars(M3, y2, type = "lasso") 
#las
#plot(las)
#coef(las)
#summary(las)

#example4
ex4<-read.csv("example4.csv")
head(ex4)
X1<-ex4[,1]
X2<-ex4[,2]
X3<-ex4[,3]
Y<-as.factor(ex4[,4])
model4<-glm(formula=Y~X1+X2+X3,family=binomial)
summary(model4)
X<-data.frame(ex4[,c(1,2,3)])
predict(model4, newdata =X,type = "response")
T<-seq(1,32,1)
model4$fitted.values
round(model4$fitted.values)==Y
model4_2<-glm(formula=Y~X1+X3,family=binomial)
summary(model4_2)
sum(round(model4_2$fitted.values)==Y)
#泊松分布
counts <- c(18,17,15,20,10,20,25,13,12)
outcome <- gl(3,1,9)
treatment <- gl(3,3)
model4_3 <- glm(counts ~ outcome + treatment, family = poisson())
summary(model4_3)
T<-seq(1,9,1)
plot(T,counts,type="l")
points(T,model4_3$fitted.values)


#example5
ex5<-read.csv("example5.csv")
head(ex5)
X<-as.matrix(ex5[,-16])
Y<-ex5[,16]
x1<-X[,1]
x2<-X[,2]
x3<-X[,3]
x4<-X[,4]
x5<-X[,5]
x6<-X[,6]
x7<-X[,7]
x8<-X[,8]
x9<-X[,9]
x10<-X[,10]
x11<-X[,11]
x12<-X[,12]
x13<-X[,13]
x14<-X[,14]
x15<-X[,15]
model5<-lm(Y~x1+x2+x3+x4+x5+x6+x7+x8+x9+x10+x11+x12+x13+x14+x15)
summary(model5)


主成分
co<-cor(X)
ev<-eigen(co)
plot(ev$values,type='l')
sum(ev$values[1:5])/sum(ev$values)
y1<-t(as.matrix(ev$vectors[,1]))%*%t(X)
y2<-t(as.matrix(ev$vectors[,2]))%*%t(X)
y3<-t(as.matrix(ev$vectors[,3]))%*%t(X)
y4<-t(as.matrix(ev$vectors[,4]))%*%t(X)
y5<-t(as.matrix(ev$vectors[,5]))%*%t(X)
model5_2<-lm(Y~as.vector(y1)+as.vector(y2)+as.vector(y3)+as.vector(y4)+as.vector(y5))
summary(model5_2)
#
library(MASS)
stepba<-stepAIC(model5,direction = "backward")
summary(stepba)



plot(lm.ridge(ex5[,16]~X,lambda = seq(0,5,0.0001)))
select(lm.ridge(ex5[,16]~X,longley,lambda = seq(0,5,0.0001)))
model5_3<-lm.ridge(ex5[,16]~X,lambda = 3.2304  )
summary(model5_3)



#LASS0
library(glmnet)
X2<-scale(as.matrix(X))
Y2<-scale(as.matrix(ex5[,16]))
la<-glmnet(X2,Y2,alpha=1,lambda=seq(0,1,0.1))
coef(la)

