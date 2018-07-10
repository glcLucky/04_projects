# coder-Tips
1、定义函数时：
*attribute_args 是位置参数，返回的是一个元组
**attribute_args 是关键字参数，返回的是一个字典，键是对应关键字参数，值是对应关键字参数的值，没有指定的话则是一个空字典
对于嵌套函数，子函数形参中的关键字参数如果是父函数的关键字参数，那么则是将字典传递到子函数
2、调用函数时：
**成为参数收集的逆过程，即分割参数，它可以将以字典形式存储的值传递给形参。

下面一些例子，供读者思考。


例子如下
##收集位置参数放入字典中**
def test(a,**args):
    print('a=',a)
    print('args=',args)
    print('b=',args['b']) ##key一定要加引号
test(a="I am 'a'",b="I am 'b'",z="I am 'z'")
##嵌套情形
def sub_func(w,**kwargs):
    print('w=',w)
    print('kwargs=',kwargs)
    print('z=',kwargs['z'])
    
def parent_func(a,**args):
    print('a=',a)
    print(args)
    sub_func(w="I am 'w",**args) #这里不要写成kwargs=**args
#args是一个包含key为z和h的字典，用**号来进行分割传递给子函数的收集关键字参数kwargs，
# 所以kwargs就成了包含z和h的字典
parent_func(a="I am 'a'",z="I am 'z'",h="I am 'w'")

##字典传递参数
def dict_trasmit(dd,**args):
    # print('a=', a)
    # print('b=', b)
    # print('c=', c)
    # print('dd=',dd)
    print(args['a'])

dic={'a':"I am 'a'",'b':"I am 'b'",'c':"I am 'c'"}
dict_trasmit(dd=99,**dic)
