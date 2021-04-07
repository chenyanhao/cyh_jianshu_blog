# 经验一

pairwise 训练对搜索是有用的，对推荐的作用较小。
（1）搜索是带 query 的、有意识的被动推荐，对于搜索而言，相关性是及其重要的事情。query 限制了你召回商品相关性，比如 “ONLY 连衣裙”，召回回来一批相似性极高的连衣裙，同时用户心智也决定了他将高度关注商品之间的细微差别，比如价格、款式等，因此这些商品才有必要比个高下。
（2）推荐是发散的、无意识的主动推荐，相比搜索而言，准确性不再是第一要务（想象下因为你点过一些女装给你出一整屏的连衣裙的感觉），多样性是一个必要的指标，这导致了推荐结果极其发散。用户对推荐结果多样性的心智使得他不关注两个商品之间的比较，对于算法而言不再关注商品之间两两的比较，我只要每个都预测准了，反正最后也要打散的。而且多样性也导致了推荐场景没有像搜索一样适合做 pairwise 的样本。
（3）pointwise 模型预测出来的分数，具有实际的物理意义，代表了 target user 点击 target item 的预测概率，因此可以在全局或下游里做一些策略，比如截断之类的；pairwise or listwise 模型很难这么利用。
（4）pairwise or listwise 的模型，可以在重排阶段大放异彩，这里给一篇阿里的落地论文：https://arxiv.org/pdf/1904.06813.pdf。
> 可以参考这个解读，https://zhuanlan.zhihu.com/p/101596475

作者：忆丶昔
链接：https://www.zhihu.com/question/338044033/answer/815202813
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


# 经验二

个人感觉pointwise学的是全局性，因为正样本就增加相似，负样本就降低相似度。但pairwise学的是局部性，一般而言，假设max margin=0，对某个用户只需要其正样本相似大于负样本即可。比如负样本相似为-0.99（相似度值域-1，1），那正样本相似为-0.9模型也无需跟新参数了。但如果随机采一个样本平均相似假设为0，其实模型判定时，随便一个样本也比正样本好。这就导致模型效果极差。pairwise包括pointwise都需要及其合适的负样本，而pairwise要求则更高。

作者：Anticoder
链接：https://www.zhihu.com/question/338044033/answer/771686642
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


# 经验三

作者：忆丶昔
链接：https://www.zhihu.com/question/364930489/answer/1554563660
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

这里总结了这么几类已发表并广泛接受的重排或者 LTR 工作：
1.【Point-wise 模型】和经典的 CTR 模型基本结构类似，如 DNN [8]， WDL [9] 和 DeepFM [10]。和排序相比优势主要在于实时更新的模型、特征和调控权重。随着工程能力的升级，ODL [11] 和实时特征逐渐合并到排序阶段并且取得了较大提升。
2.【Pair-wise 模型】通过 pair-wise 损失函数来比较商品对之间的相对关系。 具体来说，RankSVM [12], GBRank [13] 和 RankNet [2] 分别使用了 SVM、GBT 和 DNN。但是，pair-wise 模型忽略了列表的全局信息，而且极大地增加了模型训练和预估的复杂度。
3.【List-wise 模型】建模输入商品列表的整体信息和对比信息，并通过 list-wise 损失函数来比较序列商品之间的关系。  LambdaMart [14]、MIDNN [3]、DLCM[6]、PRM [5] 和 SetRank [4] 分别通过 GBT、DNN、RNN、Self-attention 和 Induced self-attention 来提取这些信息。随着工程能力的升级，输入序列的信息和对比关系也上提到排序阶段中提取。
4.【Generative 模型】主要分为两种，一种如考虑了前序信息的，如 MIRNN [3] 和 Seq2Slate [15] 都通过 RNN 来提取前序信息，再通过 DNN 或者 Pointer-network 来从输入商品列表中一步步地生成最终推荐列表。最近的组合优化工作 Exact-K [16] 注重于直接对序列整体收益进行建模，设计了两段式结构，一个用来预测整体收益以指导另一个生成最终推荐列表。
5.【Diversity 模型】最近有很多工作考虑最终推荐列表里的相关性和多样性达到平衡，如 [17~20]。

[1] Cao, Zhe, et al. "Learning to rank: from pairwise approach to listwise approach." Proceedings of the 24th international conference on Machine learning. 2007.
[2] Burges, Chris, et al. "Learning to rank using gradient descent." Proceedings of the 22nd international conference on Machine learning. 2005.
[3] Ai, Qingyao, et al. "Learning a deep listwise context model for ranking refinement." The 41st International ACM SIGIR Conference on Research & Development in Information Retrieval. 2018.
[4] Pang, Liang, et al. "Setrank: Learning a permutation-invariant ranking model for information retrieval." Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval. 2020.
[5] Pei, Changhua, et al. "Personalized re-ranking for recommendation." Proceedings of the 13th ACM Conference on Recommender Systems. 2019.
[6] Zhuang, Tao, Wenwu Ou, and Zhirong Wang. "Globally optimized mutual influence aware ranking in e-commerce search." arXiv preprint arXiv:1805.08524 (2018).
[7] Gong, Yu, et al. "EdgeRec: Recommender System on Edge in Mobile Taobao." Proceedings of the 29th ACM International Conference on Information & Knowledge Management. 2020.
[8] Covington, Paul, Jay Adams, and Emre Sargin. "Deep neural networks for youtube recommendations." Proceedings of the 10th ACM conference on recommender systems. 2016.
[9] Cheng, Heng-Tze, et al. "Wide & deep learning for recommender systems." Proceedings of the 1st workshop on deep learning for recommender systems. 2016.
[10] Guo, Huifeng, et al. "DeepFM: a factorization-machine based neural network for CTR prediction." arXiv preprint arXiv:1703.04247 (2017).
[11] Sahoo, Doyen, et al. "Online deep learning: Learning deep neural networks on the fly." arXiv preprint arXiv:1711.03705 (2017).
[12] Lee, Ching-Pei, and Chih-Jen Lin. "Large-scale linear ranksvm." Neural computation 26.4 (2014): 781-817.
[13] Zheng, Zhaohui, et al. "A regression framework for learning ranking functions using relative relevance judgments." Proceedings of the 30th annual international ACM SIGIR conference on Research and development in information retrieval. 2007.
[14] Burges, Christopher JC. "From ranknet to lambdarank to lambdamart: An overview." Learning 11.23-581 (2010): 81.
[15] Bello, Irwan, et al. "Seq2slate: Re-ranking and slate optimization with rnns." arXiv preprint arXiv:1810.02019 (2018).
[16] Gong, Yu, et al. "Exact-k recommendation via maximal clique optimization." Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. 2019.
[17] Chen, Laming, Guoxin Zhang, and Eric Zhou. "Fast greedy map inference for determinantal point process to improve recommendation diversity." Advances in Neural Information Processing Systems. 2018.
[18] Gelada, Carles, et al. "Deepmdp: Learning continuous latent space models for representation learning." arXiv preprint arXiv:1906.02736 (2019).
[19] Gogna, Anupriya, and Angshul Majumdar. "Balancing accuracy and diversity in recommendations using matrix completion framework." Knowledge-Based Systems 125 (2017): 83-95.
[20] Wilhelm, Mark, et al. "Practical diversified recommendations on youtube with determinantal point processes." Proceedings of the 27th ACM International Conference on Information and Knowledge Management. 2018.








