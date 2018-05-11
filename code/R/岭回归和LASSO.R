#岭回归
#某种水泥在凝固时放出的热量Y与四种成分Xi有关，希望选出主要成分
cement <- data.frame(X1=c(7,1,11,11,7,11,3,1,2,21,1,11,10),
                     X2=c(26,29,56,31,52,55,71,31,54,47,40,66,68),
                     X3=c(6,15,8,8,6,9,17,22,18,4,23,9,8),
                     X4=c(60,52,20,47,33,22,6,44,22,26,34,12,12),
                     Y=c(78.5,74.3,104.3,87.6,95.9,109.2,102.7,72.5,93.1,115.9,83.8,113.3,109.4))
lm.sol <- lm(Y~.,data = cement)
summary(lm.sol)
install.packages("car")
library(car)
vif(lm.sol)
library(MASS)
#seq(0,1,length.out=100)语句生成一个100个值的等差数列，首项为0，末项为1
ridge.sol <- lm.ridge(Y~.,data = cement,lambda = seq(0,150,length.out=151),model = TRUE)
##找到GCV最小时的lambdaGCV
ridge.sol$lambda[which.min(ridge.sol$GCV)]
##找到GCV最小时对应的系数
ridge.sol$coef[which.min(ridge.sol$GCV)]
##matplot用矩阵的列画多线图 
par(mfrow = c(1, 2))
matplot(ridge.sol$lambda,t(ridge.sol$coef),xlab = expression(lamdba),ylab = "Cofficients",type = "l",lty = 1:20)
abline(v = ridge.sol$lambda[which.min(ridge.sol$GCV)])
# 下面的语句绘出lambda同GCV之间关系的图形
plot(ridge.sol$lambda, ridge.sol$GCV, type = "l", xlab = expression(lambda),ylab = expression(beta))
abline(v = ridge.sol$lambda[which.min(ridge.sol$GCV)])
#用ridge包自动选择
install.packages("ridge")
library(ridge)
mod <- linearRidge(Y ~ ., data = cement)
summary(mod)
##岭回归缺陷 
##1.主要靠目测选择岭参数
##2.计算岭参数时，各种方法结果差异较大
##所以一般认为，岭迹图只能看多重共线性，却很难做变量筛选。

#LASSO
install.packages("lars")
library(lars)
x <- as.matrix(cement[,1:4])
y <- as.matrix(cement[,5])
laa <- lars(x=x,y=y,type = "lar")
par(mfrow=c(1,1))
plot(laa)
summary(laa)
## 根据对Cp含义的解释（衡量多重共线性，其值越小越好）
##图中x3一直为0，可以去掉，我们取到第3步，使得Cp值最小，也就是选择X4，X1，X2这三个变量。

