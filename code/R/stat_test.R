library(car)
library(MASS)
#install.packages('car')
#Q3
df_reg_q3 <- read.table("E:\\01_learn\\test data\\python\\reg_q3.csv",header=TRUE)

fit <- lm(y ~ x1 + x2, data=df_reg_q3)
summary(fit) 
confint(fit) #参数估计的置信区间
df_reg_q3_new <- data.frame(x1=10,x2=480) #prediction
predict(fit,df_reg_q3_new,interval = 'confidence',alpha=0.05) # 置信区间
predict(fit,df_reg_q3_new,interval = 'prediction',alpha=0.05) # 预测区间

# 残差的正态性检验和异方差检验
# 图示法
par(mfrow=c(2,2)) # init 4 charts in 1 panel
plot(fit)
# 正态性检验可以看右上角的qq图 如果基本在直线左右浮动 可以认为残差服从正态分布
# 异方差检验可以观察左下角的图，如果不存在异方差，残差应该随机上下波动 没有明显的规律

# BP检验法
library(zoo)
library(lmtest)
bptest(fit)  # Breusch-Pagan test H0:具有方差齐性
shapiro.test(fit$residuals) # 夏皮罗检验 # H0 该数据来自正态分布
# 自相关检验
# dw取值在0-4之间 原假设为无自相关 此时p值大于显著性水平 dw=0代表rho=1 dw=4代表rho=-1
# 若dw检验的p值小于0.05 即拒绝无自相关的原假设，此时有两种可能：
#如果dw值小于2，则认为存在正自相关；dw大于2 则认为存在负自相关
dwtest(fit)
??bptest
#Q4
df_reg_q4 <- read.table("E:\\01_learn\\test data\\python\\reg_q4.csv",header=TRUE)
fit<-lm(y~x1+x2,data = df_reg_q4)
summary(fit)

df_reg_q4.res=resid(fit) #get residual 
plot(df_reg_q4$y, df_reg_q4.res, ylab="Residuals", xlab="粘度",main="残差图") 
abline(0, 0)   #添加水平线

df_reg_q4.stdres=rstandard(fit)
plot(df_reg_q4$y, df_reg_q4.stdres, ylab="STD Residuals", xlab="粘度",main="标准化残差图") 
abline(0, 0)   #添加水平线

#Q5
df_reg_q5 = read.csv("E:\\04_project\\data\\R\\practise\\reg_q5.csv", header=T)

fit = lm(y~pca1, data = df_reg_q5)
summary(fit)

#Q8
df_reg_q8 <- read.csv("E:\\04_project\\data\\R\\practise\\reg_q8.csv",header=T)
ln_df_reg_q8=log(df_reg_q8)
fit<-lm(y~.,data = ln_df_reg_q8)
summary(fit)
vif(fit)

fit<-lm(y~gdp,data = ln_df_reg_q8)
summary(fit)

fit<-lm(y~cpi,data = ln_df_reg_q8)
summary(fit)

fit<-lm(gdp~cpi,data = ln_df_reg_q8)
summary(fit)

#Q9
df_reg_q9 <- read.csv("E:\\04_project\\data\\R\\practise\\reg_q9.csv",header=TRUE)
ln_df_reg_q9=log(df_reg_q9)
fit=lm(y~.,data = ln_df_reg_q9)
summary(fit)
vif(fit)

ln_df_reg_q9_std=scale(ln_df_reg_q9[,-1])
pca=eigen(cor(ln_df_reg_q9_std))

pca$values #特征根 特征值之后即表示总方差 每个特征值表示该主成分所代表的变差部分
pca$vectors#特征向量 即主成分系数

cca=pca$values/sum(pca$values)#单个主成分的贡献率

ca=cumsum(pca$values)/sum(pca$values)#累计贡献率

#计算loading，即主成分与各原始变量之间的相关系数 2表示列方向的运算
loadings=sweep(pca$vectors,2,sqrt(pca$values),"*") 

#计算每个样本的主成分得分 即用主成分系数乘以标准化后的样本值 
p1=ln_df_reg_q9_std%*%pca$vectors[,1]
y=ln_df_reg_q9_std[,1]
a=data.frame(y,p1)
fit=lm(y~p1,data = a)
summary(fit)


#q10
#车
library(car)
library(ridge)
library(MASS)
car <- read.csv(file = "E:\\04_project\\data\\R\\practise\\car.csv",header = TRUE)
car_x <- car[,-1] 
cormax <- cor(car_x) # 生成自变量相关系数矩阵
cormax

pairs(~.,data = car_x,main = "相关系数矩阵图")

#度量多重共线性的严重程度的一个重要指标是方阵的XTX的条件数，用kappa函数计算出条件数，大于1000时存在严重的多重共线性
kappa(cormax,exact = FALSE)
#λmax(XTX),λmin(XTX)表示的是XTX的最大,最小的特征值.
eigenvalue <- eigen(cormax)
#特征值7、8、9、10、11均比较小，对应的7-11列特征向量可以找出存在共线性的变量
carfit <- lm(car$Y~.,data = car)
vif(carfit) # X1,x2,x3,x7,x8,x9,x10的vif值均大于10 故认为这些变量受到多重共线性影响较为严重
#Ridge方法
plot(lm.ridge(car$Y~.,data = car,lambda = seq(0,1,0.0001)))

#对应广义交叉验证对应的值最小GCV,手动拟合
select(lm.ridge(car$Y~.,data = car,lambda = seq(0,1,0.0001)))
modelcar<-lm.ridge(car$Y~.,data = car,lambda =1 )
summary(modelcar)
modelcar[1]
#自动拟合方法
install.packages("ridge")
library("ridge")
modelcar1 <- linearRidge(car$Y~.,data = car)
summary(modelcar1)
# 从模型运行结果看，测岭回归参数值为0.2652975，之前所有变量均不显著，回归后有三个变量显著

#LASSO方法
library(lars)
x <- as.matrix(car[,2:11])
y <- as.matrix(car[,1])
laa <- lars(x=x,y=y,type = "lar")
par(mfrow=c(1,1))
plot(laa)
summary(laa)
## 逻辑回归
install.packages("AER")
data(Affairs, package="AER") # 导入数据集
head(Affairs)
summary(Affairs) # 查看数据集相关统计量
table(Affairs$affairs) # 统计affairs的取值个数

#将affair转换为二分类变量 命名为ynaffair
Affairs$ynaffair[Affairs$affairs > 0] <- 1 # 有婚外情
Affairs$ynaffair[Affairs$affairs == 0] <- 0 # 无婚外情
Affairs$ynaffair <- factor(Affairs$ynaffair,
                             levels=c(0,1),
                             labels=c("No","Yes"))

table(Affairs$ynaffair) # 没有婚外情的451例 有婚外情的 150例

# 逻辑回归建模
fit.full <- glm(ynaffair ~ gender + age + yearsmarried + children +
                  religiousness + education + occupation +rating,
                data=Affairs, family=binomial(link = 'logit'))
summary(fit.full)
# 年龄、结婚时间、宗教信仰程度、婚姻的自我评价程度这几个变量显著

#剔除不显著的变量重新建立逻辑回归模型
fit.reduced <- glm(ynaffair ~ age + yearsmarried + religiousness +
                     rating, data=Affairs, family=binomial(link = 'logit'))
summary(fit.reduced)

# 利用anova比较fit.full和fit.reduced是否有显著差异
anova(fit.reduced, fit.full, test="Chisq")
# 卡方检验结果不显著 p=0.2108 所以两个模型效果差不多 因此更加坚信不显著的变量没有影响

#解释模型参数
coef(fit.reduced) #系数表示对数优势比 不好解释 因子进行指数化
exp(coef(fit.reduced)) # 得到优势比
# 比如婚龄=1.106 可以解释为婚龄每增加1年 婚外情的优势比增加10.6% 即发生婚外情的可能性增加10.6%
# 再比如年龄=0.965 可以解释为年龄每增加1年 婚外情的优势比减少4.5% 即发生婚外情的可能性增加4.5%

# 获得系数的置信区间
confint(fit.reduced)

#预测 基于特定的新样本
testdata <- data.frame(rating=c(1, 2, 3, 4, 5), age=mean(Affairs$age),
                       yearsmarried=mean(Affairs$yearsmarried),
                       religiousness=mean(Affairs$religiousness))

pred <- predict(fit.reduced, newdata=testdata, type="response")
testdata$prob <- predict(fit.reduced, newdata=testdata, type="response")
testdata$result <- ifelse(pred>0.5, 1, 0)

testdata
#因此 在其他条件不变的情况下 当婚姻平凡从1增加到5时 发生婚外情的概率由0.53 下降到0.15

#预测 基于测试集
#首先将数据集拆分成训练集和测试集
split = sample(nrow(Affairs),nrow(Affairs)*0.2) #从Affairs中随机取30%的样本序号
Affairs_train <- Affairs[-split ,]
Affairs_test <- Affairs[split ,]

# 基于训练集进行逻辑回归建模
fit.full <- glm(ynaffair ~ gender + age + yearsmarried + children +
                  religiousness + education + occupation +rating,
                data=Affairs, family=binomial(link = 'logit'))
summary(fit.full)

# 测试
head(Affairs_test)
test_attr = Affairs_test[,c('gender','age','yearsmarried','children','religiousness','education','occupation','rating')]
pred = predict(fit.full, newdata = test_attr , type = 'response')

actual = Affairs_test[,'ynaffair']
test_label <- data.frame(actual,predict=ifelse(pred > 0.5, 'Yes' ,'No'))
accuracy_rate <- mean(test_label$actual == test_label$predict) # 预测准确率达72.5%

## 时间序列部分
# ts_q8
library(tseries)
library(forecast)
#install.packages('forecast')
ts=read.csv("E:/04_project/R/ts_q8.csv" , header = F)
ts1=ts(ts)
ts1
tsdisplay(ts1)#也可以直接使用tsdisplay来观察，它包含了时序图，以及acf、pacf两个相关图
plot.ts(ts1 ,xlab ="时间" , ylab = "降雪量" , main = "年份与降雪量时序图")
## 平稳性检验
adf.test(ts1) # 平稳性检验 默认备择假设是平稳 此处p=0.132 故解释原假设 认为序列不平稳
## 纯随机检验
Box.test(ts1 , type = "Ljung-Box")
#Ljung-Box检验 H0：序列是纯随机序列 p=0.01284 拒绝，认为原序列非纯随机 所以可以用于建模

##建模
auto.arima(ts1,trace = TRUE) # 选择结果为ARMA(0,1,1)
fit = arima(ts1 , order = c(0,1,1)) # 拟合ARMA(0,1,1)
summary(fit)

## 预测
forecast(fit,h=5)


diff_ts=diff(ts1)
tsdisplay(diff_ts)
plot.ts(diff_ts)
adf.test(diff_ts)
acf(diff_ts)
pacf(diff_ts)
a1=auto.arima(ts1,trace = TRUE)
a2=arima(ts1,order = c(0,1,1))
a3=forecast(a2)
a3
#然后使用tsdiag看一下各自的结果，图中表明残差标准差基本都在[-1,1]之间残差的自回归都为0（两虚线内）
#Ljung-Box检验的p值都在0.05之上
pre=predict(a3,5)
pre
tsdiag(fit1)
plot(a3, xlab= 'Year', ylab = 'Annual snow volume')
Box.test(a3$residuals)

# 练习案例 尼罗河
plot(Nile,xlab = "年份" , ylab = "尼罗河流量")
acf(Nile,main = "自相关图")
tsdisplay(Nile) #也可以直接使用tsdisplay来观察，它包含了时序图，以及acf、pacf两个相关图

#adf检验
adf.test(Nile) #p-value=0.0642,故在95%的置信度下，无法拒绝不平稳的原假设，这与图示法结果一致

#从时序图可以看到序列再1990年有一个下降的趋势
#并且自相关图里自相关系数没有快速的减为0
#（一般认为自相关系数低于2倍标准差即图中蓝色虚线一下时即为0),而是呈现出拖尾的特征
#故判断序列为非平稳序列。

#若序列为非平稳，则需将序列通过差分转化为平稳序列。
#差分可以消除序列的线性趋势。ndiffs()函数可以帮助我们判断需要进行几次差分。
#将序列取对数可以保证ARMA模型同方差的假设。

ndiffs(Nile)#值为1 故需要进行一次差分
Nile_diff=diff(Nile)
ndiffs(Nile_diff) # 值为0 故无需进行差分
tsdisplay(Nile_diff)

#opar=par(mfrow=c(2,2))
#par(opar)
layout(matrix(c(1,1,2,3), nrow = 2, ncol = 2 , byrow = T))
plot(Nile_diff)
acf(Nile_diff)
pacf(Nile_diff)
#par(mfrow=c(1,1)) #还原绘图布局

auto.arima(Nile, trace = T) #基于未差分的序列 最好的是arima(1,1,1)
auto.arima(Nile_diff, trace = T) #基于未差分的序列 最好的是arima(1,0,1)
#最好基于未差分的  方便预测 不然预测的结果也是差分后的结果
fit = arima(Nile , order = c(1,1,1) , method = "ML") #ML 最大似然 CSS 条件最小二乘
#默认拟合的是非中心化arima，均值记为intercept项，如果想中心化，可加上include.mean=F

#残差正态性检验
qqnorm(fit$residuals)
qqline(fit$residuals)

# 残差纯随机性检验
Box.test(fit$residuals , type = "Ljung-Box") # 接受纯随机的H0 即认为模型拟合的充分

##预测
#利用predict
predict=predict(fit,10)
predict$pred
plot(Nile)
lines(predict$pred,col="red")
lines(predict$pred+predict$se,col="green")
lines(predict$pred-predict$se,col="green")

#利用forecast
predict=forecast(fit, h = 10)
plot(predict) #可直接绘制预测图
#预测时需注意：如果是取对数或者差分后的数据 应当还原

## 时间序列数据模拟 #系数必须要指定
# 根据给定系数模拟
a=arima.sim(n = 63, list(ar = c(0.8897, -0.4858), ma = c(-0.2279, 0.2488)), sd=sqrt(0.1796)) 
plot(a)
# 给定模型参数和ar的系数
b <- arima.sim(list(order = c(2,1,0), ar = c(0.8897, -0.4858)), n = 200)
plot(b)

b <- arima.sim(list( ar = 0.8897, ma = -0.92), n = 200)
plot(b)
# 最大似然估计
fit = arima(b, order = c(1,0,1), method = "ML") 
summary(fit)
# 条件最小二乘估计
fit = arima(b, order = c(1,0,1), method = "CSS-ML") 
summary(fit)

#预测
predict = forecast(fit,h = 5)
plot(predict) # 绘制预测图

test = read.csv("E:\\04_project\\data\\R\\practise\\acf2.csv",header=TRUE)
plot(test[,'pacf'] ,ylim = c(-1,1),type = 'h', main = "偏自相关图")
abline(0,0)

plot(test[,'acf'] ,ylim = c(-1,1),type = 'h', main = "自相关图")
abline(0,0)

install.packages("TSA")
library(TSA)
w<-rnorm(550)
x<-filter(w,filter=c(1,-0.9),"recursive")
help(arma)
arma(x,method="yw")

#第一题
#车
car <- read.csv(file = "E:/04_project/R/car.csv",header = TRUE)
car_x <- car[,-1] 
cormax <- cor(car_x) # 生成自变量相关系数矩阵
library(car)
library(ridge)
library(MASS)
install.packages('ridge')
pairs(~.,data = carx,main = "相关系数矩阵图")

#度量多重共线性的严重程度的一个重要指标是方阵的XTX的条件数，用kappa函数计算出条件数，大于1000时存在严重的多重共线性
kappa(cormax,exact = FALSE)
#λmax(XTX),λmin(XTX)表示的是XTX的最大,最小的特征值.
eigenvalue <- eigen(cormax)
#特征值7、8、9、10、11均比较小，对应的7-11列特征向量可以找出存在共线性的变量
carfit <- lm(car$Y~.,data = car)
vif(carfit) # X1,x2,x3,x7,x8,x9,x10的vif值均大于10 故认为这些变量受到多重共线性影响较为严重
#Ridge方法
plot(lm.ridge(car$Y~.,data = car,lambda = seq(0,1,0.0001)))

#对应广义交叉验证对应的值最小GCV,手动拟合
select(lm.ridge(car$Y~.,data = car,lambda = seq(0,1,0.0001)))
modelcar<-lm.ridge(car$Y~.,data = car,lambda =1 )
summary(modelcar)
modelcar[1]
#自动拟合方法
install.packages("ridge")
library("ridge")
modelcar1 <- linearRidge(car$Y~.,data = car)
summary(modelcar1)
# 从模型运行结果看，测岭回归参数值为0.2652975，之前所有变量均不显著，回归后有三个变量显著

#LASSO方法
library(lars)
x <- as.matrix(car[,2:11])
y <- as.matrix(car[,1])
laa <- lars(x=x,y=y,type = "lar")
par(mfrow=c(1,1))
plot(laa)
summary(laa)

#第二题
#白血病
leuke <- read.csv(file = "E:/04_project/R/leukemia.csv",header = TRUE)
fit.leuke <- glm(leuke$Y~.,data = leuke,family = binomial())
summary(fit.leuke)

#极大似然估计
logitlink <- function(theta,x,y){
  beta0 = theta[1]
  beta1 = theta[2]
  beta2 = theta[3]
  beta3 = theta[4]
  x1 = x[1]
  x2 = x[2]
  x3 = x[3]
  p=1/(1+exp(-beta0-beta1*x1-beta2*x2-beta3*x3))
  logL = sum(y*log(p)+(1-y)*log(1-p))
  return(-logL)
}
optim(c(0,0,0,0), x = leuke[,1:3],y = leuke[,4],logitlink) 
# par的值依次为截距项和自变量系数估计值
#预测
testdata <- data.frame(X1 = 5,X2 = 2,X3 = 1)
testdata$prob <- predict(fit.leuke,newdata = testdata,type = "response")
testdata
