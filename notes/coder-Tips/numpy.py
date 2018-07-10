# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
arr1=np.arange(10)
arr2=np.random.randn(10)
np.save('arr1',arr1) #保存数组npy文件
np.savez('arr',a=arr1,b=arr2)  #保存多个数组到npz文件，相当于一个字典

x=np.load('arr1.npy')
y=np.load('arr.npz')
y['a']
y['b']

#生成一个来自均值为2，标准差为2.5的正态分布的3*4型的随机数数组
x=np.random.normal(loc=2,scale=2.5,size=(3,4))

#花式索引，与切片不同，不是视图，而是复制
arr=np.arange(32).reshape(8,4)
arr[[1,5,7,2]][:,[0,3,1,2]]

#通用函数
x=np.random.randn(8)
y=np.random.randn(8)
np.maximum(x,y)
z=np.random.uniform(2,4,9)
np.modf(z)
np.isnan(z)

#数学和统计方法
arr=np.random.randn(5,4)
help(np.random.randint)
arr=np.random.randint(1,5,12).reshape(3,4)
arr.mean()
arr.mean(axis=0)
arr.cumsum(1)
arr.argmax(0)

#用于布尔型数组的方法
#计算为true的个数
arr=np.random.randn(100)
(arr>0).sum()
#any &all
bools=arr>0
bools.any() #测试数组中是否存在一个或多个ture，存在返回1
bools.all() #测试数组中的元素是否全部为ture，全为true返回1

#数组排序
arr=np.random.randint(1,50,20).reshape(4,5)
arr.sort(0) #按行排序
arr.sort(1) #按列排序
arr=np.random.randint(1,50,20)
arr1=arr.reshape(20)
np.unique(arr)

#数组的存取
arr=np.arange(10)
np.save('some_array',arr)  #存单个数组到npy文件
np.load('some_array.npy') #取

#存储多个数组至压缩文件
arr1=np.arange(10)
arr2=np.random.randint(1,50,20).reshape(4,5)
np.savez('array_archive.npz',a=arr1,b=arr2)  #a、b是为每个数组指定别名
arch=np.load('array_archive.npz')
arch['b']