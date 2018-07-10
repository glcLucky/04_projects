# -*- coding: utf-8 -*-

#取出字典中值满足特定条件的部分 并返回一个新字典
new={k:v for k,v in old.items() if v<0.25/len(snp)}

#读多个具有规律文件名的文件
for i in range(1,301):
    fr = open(r'E:\04_project\python\module\atcg\gene_info\gene_%s.dat' %(i))  #字符串格式化
    gene = [ins.strip('\n') for ins in fr.readlines()]

#数据的永久存储

#将字典永久存储，以方便调用
import pickle
export=open('chiPvalue.txt','wb')
pickle.dump(pvalue,export)
export.close()
#载入存储的数据
pickle_file=open('chiPvalue.txt','rb')
pvalue1=pickle.load(pickle_file)

#对字典元素进行排序
sorted(rsquare.items(),key=lambda x:x[1],reverse=True)[:11]
#与之等价的另一种方式为
import operator
sorted(pvalue.items(), key=operator.itemgetter(1))

#二分法查找
def search_biom(series,target,lower=0,upper=None):
    assert target in series ,"Not Exist"
    if upper is None:
        upper=len(series)-1
    if lower==upper:
        assert series[lower]==target,'Not match'
        return lower
    else:
        mid=(lower+upper)//2
        if target>series[mid]:
            return search_biom(series,target,mid+1,upper)
        else:
            return search_biom(series,target,lower,mid)

search_biom([1,2,3,4,5,6,7,8],5.5)

#利用format格式化字符串
aa='glc'
bb='better man'
cc='I belive {} is a {}'.format(aa,bb)
print(cc)

#Out[102]: 'I belive glc is a better man'

# 格式化字符串
# 生成20个字符串 形如group1-group20
['group{}'.format(i) for i in range(1,21)]

# 生成20个字符串 形如group001-group020
['group{:0>3}'.format(i) for i in range(1,21)]

# m>n n表示位数 m表示要补的数字 >表示向左补 <表示向右补
