DNN 的泛化能力较强，但是为什么强呢，其实目前也较难说清楚。只能说多看看别人怎么说，加深理解。

深度网络的本质在于找到了问题的有效描述，比如图像的生成网络，可看作其所表述的图像子空间的投影操作，这个表述能力由网络结构和网络参数来确定，其中网络结构决定了数据的复杂度和整体统计分布，网络参数决定图像局部特征。
可以理解为，训练帮助网络提取了数据子空间的有效描述，从而导致了泛化能力。
如果是考察迁移能力，则大致可以归结为不同数据或问题，其子空间的复杂度和结构有统计相似性，所以从一类数据上获得的描述也可以通过简单映射来描述另一组数据。
> 作者：信息门下走狗
> 链接：https://www.zhihu.com/question/53656435/answer/391973300
> 来源：知乎
> 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


说一下个人对于泛化的浅薄见解。所有的问题都可以是X空间到Y空间的映射。这两个空间可以是无限的。但用来描述映射的规则是有限的。这个规则就学习的目标。对于无限的XY空间来说，无论我们有多少样本都是有限的。但假使我们碰巧得出了真实分布的规则。那么模型对于所有新的X都是有效的。得出真实的概率分布，问题越复杂，难度越大，而模型所谓的学习就是让自身表示的概率分布尽可能的逼近真实的概率分布。这就是我理解的泛化能力，用有限的规则解释无限的实体关系。至于如何去逼近真实概率分布，前面的大佬已经说的很明白了，就不赘述了。
> 作者：aluea
> 链接：https://www.zhihu.com/question/53656435/answer/655242476
> 来源：知乎
> 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


更深层次理解：https://mp.weixin.qq.com/s/h9fX_vvyajsbKQMsJjWMEg
