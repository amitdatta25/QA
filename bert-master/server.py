import tensorflow as tf
import os

SAVE_PATH = '/datadrive/output/model.ckpt-5633'
MODEL_NAME = '/datadrive/output/model'
VERSION = 1
SERVE_PATH = './serve/{}/{}'.format(MODEL_NAME, VERSION)

checkpoint = tf.train.latest_checkpoint(SAVE_PATH)

tf.reset_default_graph()

with tf.Session() as sess:
    # import the saved graph
    saver = tf.train.import_meta_graph( '/datadrive/output/model.ckpt-5633.meta')
    # get the graph for this session
    graph = tf.get_default_graph()
    sess.run(tf.global_variables_initializer())
    # get the tensors that we need
    inputs = graph.get_tensor_by_name((tf.io.decode_json_example(
    '/datadrive/bert-squad1/bert-master/data/dev-v1.2.json',
    name=None
))
    
    predictions = graph.get_tensor_by_name('/datadrive/bert-squad1/bert-master/run_squad.py')

