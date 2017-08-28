#!/bin/python

import prepro2
import tensorflow as tf
import numpy as np
import param

'''prepro2から引いてくるもの
data_x(文書をidxで表したもの、shape=(1541,128)
data_y(one_hot_label(クラス4つ)、shape=(1541,4)

'''
#param.pyから引いてくるもの

data_x = prepro2.data_x
data_y = prepro2.data_y
idx_dic = prepro2.idx_dic
NUM_MINI_BATCH = param.NUM_MINI_BATCH
EMBEDDING_SIZE = param.EMBEDDING_SIZE
NUM_CLASSES = param.NUM_CLASSES
NUM_FILTERS = param.NUM_FILTERS
FILTER_SIZES = param.FILTER_SIZES
NUM_TESTS = param. NUM_TESTS
L2_LAMBDA = param. L2_LAMBDA
LEARNING_RATE = param.LEARNING_RATE
SUMMARY_LOG_DIR = param.SUMMARY_LOG_DIR
NUM_MINI_BATCH = param.NUM_MINI_BATCH
NUM_EPOCHS = param.NUM_EPOCHS
EVALUATE_EVERY = param.EVALUATE_EVERY


#---------------------------------------------------------------------
#split original data into two groups for tarining and testing

train_x, train_y = data_x[:-NUM_TESTS], data_y[:-NUM_TESTS] #テスト分を除いた分
test_x, test_y   = data_x[-NUM_TESTS:], data_y[-NUM_TESTS:] #テスト分の頭からうしろ全部

idx_entity_other = prepro2.idx_dic["entity_other"]
idx_entity1 = prepro2.idx_dic["entity1"]
idx_entity2 = prepro2.idx_dic["entity2"]
print(idx_entity_other)
print(idx_entity1)
print(idx_entity2)

#property for dropout. This is probability of keeping cell.
keep = tf.placeholder(tf.float32) #←feedの時にkeeoに値を与える

#-----------------------------------------------------------------------------
#Build CNN
#-----------------------------------------------------------------------------

#Define input layer
x_dim = train_x.shape[1] #[1]は列の長さ:テキストの長さ
input_x = tf.placeholder(tf.int32, [None, x_dim      ]) #shape=None×テキストの長さ
input_y = tf.placeholder(tf.int32, [None, NUM_CLASSES]) #shape=None×クラス数
input_mask = tf.cast(tf.not_equal(input_x, 0), dtype=tf.float32) # shape=[batch(None), seq_len]

#Define 2nd layer(Word embedding layer)
with tf.name_scope('embedding'):
    w = tf.Variable(tf.random_uniform([len(idx_dic), EMBEDDING_SIZE], -1.0, 1.0), name='weight')
    e = tf.nn.embedding_lookup(w, input_x) # shape=[batch(None), seq_len, embedding_size]
    ex = tf.expand_dims(e, 2) # shape=[batch(None), seq_len, 1, embedding_size]
    ex = ex * tf.reshape(input_mask, [-1, x_dim, 1, 1])
    ex = tf.nn.dropout(ex, keep)

    onehot_entity1 = tf.equal(input_x, idx_entity1)
    onehot_entity2 = tf.equal(input_x, idx_entity2)
    entity_pos = tf.cast(tf.stack([onehot_entity1, onehot_entity2], axis=2), dtype=tf.float32)
    entity_pos = tf.expand_dims(entity_pos, 2) # shape=[batch, seq_len, 1, 2]
    ex = tf.concat([ex, entity_pos], axis=3)

#Define 3rd and 4th layer(Temporal 1-D convolutional and max-pooling layer)
p_array = []
for filter_size in FILTER_SIZES:
    with tf.name_scope('conv-%d' % filter_size):
        #w = tf.Variable(tf.truncated_normal([filter_size, 1, EMBEDDING_SIZE, NUM_FILTERS], stddev=0.02), name='weight')
        w = tf.Variable(tf.truncated_normal([filter_size, 1, EMBEDDING_SIZE+2, NUM_FILTERS], stddev=0.02), name='weight')
        b = tf.Variable(tf.constant(0.1, shape=[NUM_FILTERS]), name='bias')
        c0 = tf.nn.conv2d(ex, w, [1, 1, 1, 1], 'VALID')
        c1 = tf.nn.relu(tf.nn.bias_add(c0, b))
        c2 = tf.nn.max_pool(c1, [1, x_dim - filter_size + 1, 1, 1], [1, 1, 1, 1], 'VALID')

        p_array.append(c2)
#p = tf.concat(3, p_array)
p = tf.concat(p_array,3)
total_filters = NUM_FILTERS * len(FILTER_SIZES)
h0 = tf.reshape(p, [-1, total_filters])
h0 = tf.nn.dropout(h0, keep)

#Define output layer(fully-connected layer).
with tf.name_scope('fc'):
    w = tf.Variable(tf.truncated_normal([total_filters, NUM_CLASSES], stddev=0.02), name='weight')
    b = tf.Variable(tf.constant(0.1, shape=[NUM_CLASSES]), name='bias')
    predict_y = tf.nn.softmax(tf.matmul(h0, w)+b)

#---------------------------------------------------------------------------------------------------
#Create optimizer
#---------------------------------------------------------------------------------------------------

#Use cross entropy for softmax as a cost function
x_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=predict_y,labels=input_y))
#cross_entropy = -tf.reduce_sum(input_y*tf.log(predict_y))
loss = x_entropy + L2_LAMBDA * (tf.nn.l2_loss(w))

#Create Optimizer for my cost function
global_step = tf.Variable(0, name='global_step', trainable=False)
train_step = tf.train.AdamOptimizer(LEARNING_RATE).minimize(loss, global_step=global_step)

#-------------------------------------------------------------------------------------------
#Measurement of accuracy and summary for TensorBoard
#-------------------------------------------------------------------------------------------

predict = tf.equal(tf.argmax(predict_y, 1), tf.argmax(input_y, 1))#←？わからん
accuracy = tf.reduce_mean(tf.cast(predict, tf.float32))

#loss_sum = tf.scalar_sumarry('train loss', loss)
#accur_sum = tf.scalar_sumarry('train accuracy', accuracy)
#t_loss_sum = tf.scalar_sumarry('general loss', loss)
#t_accur_sum = tf.scalar_sumarry('general accuracy', accuracy)

saver = tf.train.Saver()

#-------------------------------------------------------------------------------------------
#Start Tensorflow session
#-------------------------------------------------------------------------------------------

with tf.Session() as sess:
    #sess.run(tf.initialize_all_variables())
    sess.run(tf.global_variables_initializer())
    #writer = tf.train.Summarywriter(SUMMARY_LOG_DIR, sess.graph_def)

    train_x_length = len(train_x)
    batch_count= int(train_x_length / NUM_MINI_BATCH) + 1

    #Start training.
    counter = 0
    ten = 0
    for epoch in range(NUM_EPOCHS):
        #randomize training data every epoch in order tro coverage tarining more quickly.
        random_indice = np.random.permutation(train_x_length)

        #Split training data into mini batch for SGD
        for i in range(batch_count):
            #Take mini batch from training data
            mini_batch_x = []
            mini_batch_y = []

            for j in range(min(train_x_length - i * NUM_MINI_BATCH, NUM_MINI_BATCH)):#←わからん
                mini_batch_x.append(train_x[random_indice[i*NUM_MINI_BATCH+j]])
                mini_batch_y.append(train_y[random_indice[i*NUM_MINI_BATCH+j]])

            #TRAINING
            #_, loss, accuracy, t_loss_sum, t_accur_sum = sess.run(
                 #[train_step, loss, accuracy, loss_sum, accr_sum],

            _, los, acr = sess.run(
                [train_step, loss, accuracy],
                feed_dict={input_x: mini_batch_x, input_y: mini_batch_y, keep: 0.5}
            )
            print("t_loss{},t_accuracy{}".format(los,acr))
            #write out loss and accuracy value into summary logs for Tensorboard
            current_step = tf.train.global_step(sess, global_step)
            #writer.add_summary(v3, current_step)
            #bwriter.add_Summary(v4, current_step)

            #Save all variables to a file every checkpoints

            #Evaluate the model by test data every evaluation point
            
            if current_step % EVALUATE_EVERY == 0:
                
                

                print("---------------------"+str(ten)+"0cycle----------------------")
                ten += 1
                random_test_indice = np.random.permutation(100)
                random_test_x = test_x[random_test_indice]
                random_test_y = test_y[random_test_indice]

                #loss, accuracy, t_loss_sum, t_accur_sum = sess.run(
                #    [loss, accuracy, t_loss_sum, t_accr_sum],
                accuracy_ev = sess.run(
                    [accuracy],
                    feed_dict={input_x: random_test_x, input_y: random_test_y, keep: 1.0}
                )
                print("accuracy{}".format(accuracy_ev))
                #print("loss, accuracy, t_loss_sum, t_accr_sum", '{} {} {} {}'.format(loss,accuracy,t_loss_sum,t_accr_sum))
                

                                    
