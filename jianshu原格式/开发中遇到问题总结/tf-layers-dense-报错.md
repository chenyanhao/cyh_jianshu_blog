
dense_output = tf.layers.dense(f_dense_input, embedding_dim)

报错：Keras AttributeError: 'NoneType' object has no attribute '_inbound_nodes'
这里用的是 tf1.13。这个报错是由于 keras 和 tf 混用导致的。通过读源码，发现 tf.layers.dense 底层调用了 keras。可能是在安装 tf 时安装了 tf 自带的 keras，但是自带的这个 keras 不符合版本要求，正常的 pip install 不会触及已经是最新的包。解决办法就是加上   pip install -I keras==2.0.6  以重装 keras2.0.6。
