library(car)
library(MASS)
df_reg_q9 <- read.csv("E:\\01_learn\\test data\\python\\reg_q9.csv",header=TRUE)
ln_df_reg_q9=log(df_reg_q9) #取对数
ln_df_reg_q9_x = ln_df_reg_q9[,-1]
# 画出自变量相关系数图
pairs(~.,data = ln_df_reg_q9_x,main = "相关系数矩阵图")
cormatrix <- cor(ln_df_reg_q9_x) # 生成自变量相关系数矩阵
#度量多重共线性的严重程度的一个重要指标是方阵的XTX的条件数，用kappa函数计算出条件数，大于1000时存在严重的多重共线性
kappa(cormatrix,exact = FALSE)

fit=lm(y~.,data = ln_df_reg_q9) # .表示对数据框内所有变量
summary(fit) 
vif(fit) # 求方差膨胀因子判断多重共线性 vif<5 认为不存在共线性 5-10 中等程度 >10严重的多重共线性
hatvalues(fit) #hii>(2p/n)被视为极端样本 p为显著的自变量个数(含constant)


#共线性解决方法之一 PCA
ln_df_reg_q9_std=scale(ln_df_reg_q9[,-1]) #将数据进行统计标准化 均值为0 方差为1
pca=eigen(cor(ln_df_reg_q9_std)) # 对中心化数据的相关阵进行特征值分解 或对非中心化数据的协方差阵进行特征值分解
pca$values #特征根 特征值之后即表示总方差 每个特征值表示该主成分所代表的变差部分
pca$vectors#特征向量 即主成分系数

cca=pca$values/sum(pca$values)#单个主成分的贡献率
cca
ca=cumsum(pca$values)/sum(pca$values)#累计贡献率
ca
#计算loading，即主成分与各原始变量之间的相关系数 2表示列方向的运算
loadings=sweep(pca$vectors,2,sqrt(pca$values),"*") 

#计算每个样本的主成分得分 即用主成分系数乘以标准化后的样本值 
p1=ln_df_reg_q9_std%*%pca$vectors[,1] #第一主成分
p2=ln_df_reg_q9_std%*%pca$vectors[,2] #第二主成分
y=ln_df_reg_q9_std[,1] #取出因变量y
new=data.frame(y,p1,p2) # 将因变量y与第一主成分放进同一个数据框
fit=lm(y~p1,data = new) # 将因变量y与第一主成分进行回归
summary(fit)
#new.res=resid(fit) # 获取普通残差
new.res_sd = stdres(fit) #获取标准化残差 等价于rstandard(fit)

#mean(test)
#sd(new.res)

plot(new$y, new.res_sd, ylab="Residuals", xlab="第一主成分",main="标准化残差图") 
abline(0, 0)   #添加水平线

#估计置信区间
#help(confint)
confint(fit ,level = 0.99) #参数估计的置信区间 level位置信度 默认为0.95 即95%的置信区间

df_predict_data <- data.frame(p1=2) #prediction 
predict(fit,df_predict_data,interval = 'confidence',alpha=0.05) # 置信区间
predict(fit,df_predict_data,interval = 'prediction',alpha=0.05) # 预测区间

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

# ridge 与lasso
cement <- data.frame(X1 = c(7, 1, 11, 11, 7, 11, 3, 1, 2, 21, 1, 11, 10),
                     X2 = c(26,29, 56, 31, 52, 55, 71, 31, 54, 47, 40, 66, 68), 
                     X3 = c(6, 15, 8, 8, 6, 9, 17, 22, 18, 4, 23, 9, 8), 
                     X4 = c(60, 52, 20, 47, 33, 22, 6, 44, 22, 26,34, 12, 12),
                     Y = c(78.5, 74.3, 104.3, 87.6, 95.9, 109.2, 102.7, 72.5, 93.1, 115.9, 83.8, 113.3, 109.4))

lm.sol <- lm(Y ~ ., data = cement)
summary(lm.sol)

# 从结果看，截距和自变量的相关系数均不显，但F检验却能通过 可能存在多重共线性问题
# 下面利用car包中的vif（）函数查看各自变量间的共线情况
library(car)
vif(lm.sol)
# 从结果看，各自变量的VIF值都超过10，存在多重共线性，其中，X2与X4的VIF值均超过200.
plot(X2 ~ X4, col = "red", data = cement) # 从散点图上可以发现x2和x4存在明显的负相关
#接下来，利用MASS包中的函数lm.ridge()来实现岭回归。下面的计算试了151个lambda值，最后选取了使得广义交叉验证GCV最小的那个
ridge.sol <- lm.ridge(Y ~ ., lambda = seq(0, 1, length = 151), data = cement, 
                      model = TRUE)
names(ridge.sol)  # 变量名字
ridge.sol$lambda[which.min(ridge.sol$GCV)]  ##找到GCV最小时的lambdaGCV
## [1] 1
ridge.sol$coef[which.min(ridge.sol$GCV)]  ##找到GCV最小时对应的系数

par(mfrow = c(1, 2))
# 画出图形，并作出lambdaGCV取最小值时的那条竖直线
matplot(ridge.sol$lambda, t(ridge.sol$coef), xlab = expression(lamdba), ylab = "Cofficients", 
        type = "l", lty = 1:20)
abline(v = ridge.sol$lambda[which.min(ridge.sol$GCV)])
# 从上图看，lambda的选择并不是那么重要，只要不离lambda=0太近就没有多大差别。

# 下面的语句绘出lambda同GCV之间关系的图形
plot(ridge.sol$lambda, ridge.sol$GCV, type = "l", xlab = expression(lambda), 
     ylab = expression(beta))
abline(v = ridge.sol$lambda[which.min(ridge.sol$GCV)])
ridge.sol$lambda[which.min(ridge.sol$GCV)] #最小GCV对应的lambda值是0.3267

# 下面利用ridge包中的linearRidge()函数岭回归参数 lambda=0.3267
library(ridge)
mod <- linearRidge(Y ~ ., data = cement ,lambda = 0.3267)
summary(mod)


# lasso

# install.packages('lars')
library(lars)
x = as.matrix(cement[, 1:4])
y = as.matrix(cement[, 5])
(laa = lars(x, y, type = "lar"))  #lars函数值用于矩阵型数据
# 由此可见，LASSO的变量选择依次是X4，X1，X2，X3
plot(laa)  #绘出图
summary(laa)  #给出Cp值
# 根据Cp含义的解释（衡量多重共线性，其值越小越好），我们取到第3步，使得Cp值最小，也就是选择X4，X1，X2这三个变量。


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



##时间序列
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

## 时间序列 练习案例 尼罗河
plot(Nile,xlab = "年份" , ylab = "尼罗河流量")
acf(Nile,main = "自相关图")
tsdisplay(Nile) #也可以直接使用tsdisplay来观察，它包含了时序图，以及acf、pacf两个相关图

#adf检验
adf.test(Nile) #p-value=0.0642,故在95%的置信度下，无法拒绝不平稳的原假设，这与图示法结果一致
#故判断序列为非平稳序列
#从时序图可以看到序列再1990年有一个下降的趋势
#并且自相关图里自相关系数没有快速的减为0
#（一般认为自相关系数低于2倍标准差即图中蓝色虚线一下时即为0),而是呈现出拖尾的特征

#若序列为非平稳，则需将序列通过差分转化为平稳序列。
#差分可以消除序列的线性趋势。ndiffs()函数可以帮助我们判断需要进行几次差分。
#将序列取对数可以保证ARMA模型同方差的假设。

ndiffs(Nile)#值为1 故需要进行一次差分
Nile_diff=diff(Nile)
ndiffs(Nile_diff) # 值为0 故无需进行差分
tsdisplay(Nile_diff)
adf.test(Nile_diff) #p-value<0.01,故在95%的置信度下，拒绝不平稳的原假设，认为一阶差分后的序列平稳

#opar=par(mfrow=c(2,2))
#par(opar)
layout(matrix(c(1,1,2,3), nrow = 2, ncol = 2 , byrow = T))
plot(Nile_diff)
acf(Nile_diff)
pacf(Nile_diff)
#par(mfrow=c(1,1)) #还原绘图布局

auto.arima(Nile, trace = T) #基于未差分的序列 最好的是arima(1,1,1)
# auto.arima(Nile_diff, trace = T) #基于未差分的序列 最好的是arima(1,0,1)
#最好基于未差分的  方便预测 不然预测的结果也是差分后的结果
fit = arima(Nile , order = c(1,1,1) , method = "ML") #ML 最大似然 CSS 条件最小二乘
#默认拟合的是非中心化arima，均值记为intercept项，如果想中心化，可加上include.mean=F

#残差正态性检验
qqnorm(fit$residuals)
qqline(fit$residuals)

# 残差纯随机性检验
Box.test(fit$residuals , type = "Ljung-Box") # 接受纯随机的H0 即认为模型拟合的充分

#预测
pred = forecast(fit , h = 10 ,level = c(0.025 , 0.975))
plot(pred)
# predict=predict(fit,10)
# predict
# predict$pred
# plot(Nile)
# lines(predict$pred,col="red")
#预测时需注意：如果是取对数或者差分后的数据 应当还原

## 时间序列数据模拟 #系数必须要指定
# 根据给定系数模拟
a=arima.sim(n = 63, list(ar = c(0.8897, -0.4858), ma = c(-0.2279, 0.2488)), sd=sqrt(0.1796)) 
plot(a)
# 给定模型参数和ar的系数

## 模拟数据并估计
#q4
arma11.sim <- arima.sim(list(order = c(1,0,1), ar = 0.7 ,ma = 0.4 ), n = 100 )
plot(arma11.sim)
library(TSA)
arma11.sim.acf = acf(arma11.sim ,type = "correlation", plot = "T" )
arma11.sim.acf[1:2]

arima(arma11.sim ,order = c(1,0,1), include.mean = F, method = "ML") # MLE
arima(arma11.sim ,order = c(1,0,1), include.mean = F, method = "CSS") # 条件最小二乘估计

#q5
ar2.sim <- arima.sim(list(order = c(2,0,0), ar = c(1.5 , -0.75)), n = 100 ) # 模拟中心化ar2模型
ar2.sim = ar2.sim+100 # 加上均值
mean(ar2.sim)
ts.plot(ar2.sim)
# 取出前40个值进行训练
ar2.sim.train <- ar2.sim[1:40]
ar2.sim.test <- ar2.sim[41:52]
fit = arima(ar2.sim.train ,order = c(2,0,0),  method = "ML") # MLE
#预测12期
library(forecast)
pred = forecast(fit ,h=12 ,level = c(0.025,0.975))
plot(pred)
abline(h = mean(pred$mean) ,col ='red') # 在预测均值上画一条水平参考线

# 画出实际值的点图
x <- c(41:52)
y <- ar2.sim[41:52]
points(x,y,col = "black")

# plot(ar2.sim.train ,type = "l")
#plot(predict$pred ,ylim =c(80,110) ,xlim = c(40,55))
#lines(predict$pred+predict$se,col="green")
#lines(predict$pred-predict$se,col="green")
#lines(ar2.sim.test ,col='red')

ar2.sim = ar.sim(list(order()))
help(ar.sim)

# 拟合ar模型
e = -rnorm(52)
ar.sim = filter(e ,filter = c(1.5 , 0.75) ,method = 'recursive')
ar.sim
ts.plot(ar.sim)
mean(ar.sim)
mean(e)
help("filter")


