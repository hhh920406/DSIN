import os

import pandas as pd
import tensorflow as tf
from sklearn.metrics import log_loss, roc_auc_score
from tensorflow.python.keras import backend as K

from config import DSIN_SESS_COUNT, DSIN_SESS_MAX_LEN, FRAC
from dsin import DSIN

os.environ["CUDA_VISIBLE_DEVICES"] = "3"
tfconfig = tf.ConfigProto()
tfconfig.gpu_options.allow_growth = True
K.set_session(tf.Session(config=tfconfig))


if __name__ == "__main__":
    SESS_COUNT = DSIN_SESS_COUNT
    SESS_MAX_LEN = DSIN_SESS_MAX_LEN

    fd = pd.read_pickle('../model_input/dsin_fd_' +
                        str(FRAC) + '_' + str(SESS_COUNT) + '.pkl')
    model_input = pd.read_pickle(
        '../model_input/dsin_input_' + str(FRAC) + '_' + str(SESS_COUNT) + '.pkl')
    label = pd.read_pickle('../model_input/dsin_label_' +
                           str(FRAC) + '_' + str(SESS_COUNT) + '.pkl')

    sample_sub = pd.read_pickle(
        '../sampled_data/raw_sample_' + str(FRAC) + '.pkl')

    sample_sub['idx'] = list(range(sample_sub.shape[0]))
    train_idx = sample_sub.loc[sample_sub.time_stamp <
                               1494633600, 'idx'].values
    test_idx = sample_sub.loc[sample_sub.time_stamp >=
                              1494633600, 'idx'].values

    train_input = [i[train_idx] for i in model_input]
    test_input = [i[test_idx] for i in model_input]

    train_label = label[train_idx]
    test_label = label[test_idx]

    sess_count = SESS_COUNT
    sess_len_max = SESS_MAX_LEN
    BATCH_SIZE = 4096

    sess_feature = ['cate_id', 'brand']
    TEST_BATCH_SIZE = 2 ** 16
    REG = 1e-6

    model = DSIN(fd, sess_feature, embedding_size=4, sess_max_count=sess_count,
                 sess_len_max=sess_len_max, dnn_hidden_units=(200, 80), att_head_num=8,
                 att_embedding_size=1, l2_reg_embedding=REG, encoding='bias', seed=2019)

    model.compile('adagrad', 'binary_crossentropy',
                  metrics=['binary_crossentropy', ])

    hist_ = model.fit(train_input, train_label, batch_size=BATCH_SIZE,
                      epochs=1, initial_epoch=0, verbose=1, )

    TEST_BATCH_SIZE = 2 ** 16

    pred_ans = model.predict(test_input, TEST_BATCH_SIZE)

    print()
    print("test LogLoss", round(log_loss(test_label, pred_ans), 4), "test AUC",
          round(roc_auc_score(test_label, pred_ans), 4))