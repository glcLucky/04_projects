###PCA
#read raw data
df_PCA =read.csv("E:\\04_project\\R\\PCA.csv",header=TRUE)
#标准化 标准化后的数据均值为0，方差为1，所以基于协方差矩阵的奇异值分解等价于基于相关阵的特征值分解
df_PCA_scale=scale(df_PCA)
#对相关阵进行特征值分解
pca=eigen(cor(df_PCA_scale))
pca$values #特征根 特征值之后即表示总方差 每个特征值表示该主成分所代表的变差部分
pca$vectors#特征向量 即主成分系数

cca=pca$values/sum(pca$values)#单个主成分的贡献率

ca=cumsum(pca$values)/sum(pca$values)#累计贡献率

#计算loading，即主成分与各原始变量之间的相关系数 2表示列方向的运算
loadings=sweep(pca$vectors,2,sqrt(pca$values),"*") 

#计算每个样本的主成分得分 即用主成分系数乘以标准化后的样本值 
df_PCA_scale%*%pca$vectors


