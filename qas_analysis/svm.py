#-*-coding:utf-8-*-

import sklearn, jieba
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn import metrics
from utils import *
import numpy as np

'''
qa_class:
    ns : 地名
    i : 成语
    m : 数字
    nr : 人名
    nt : 机构团体
    n : 名词
    t : 时间词（明朝）
    nexts: 下一句
    befs: 上一句
'''

class SVM(object):
    def __init__(self, load = None):
        # self.vocab, self.max_len = Loader.build_vocab()
        # print ("data loaded!")
        # print ("vocab size: " + str(len(self.vocab)))
        # print ("max sentence length: " + str(self.max_len))
        # self.w2v = Loader.load_word_vec(self.vocab)
        # print ("word2vec loaded!")
        # print ("num words already in word2vec: " + str(len(self.w2v)))
        # Loader.add_unknown_words(self.w2v, self.vocab)
        # self.W, self.word_idx_map = Loader.get_W(self.w2v)
        
        self.cl = Pipeline([('vec', TfidfVectorizer(ngram_range = (1,2))),\
                     ('svm', SVC(kernel='linear'))])

        self.c2id, self.id2c = Loader.build_class()
        print (self.c2id)
        self.model_path = "../../data/svm_model.m"
        if load:
            self.cl = Loader.load_model(self.model_path, "svm")
            
    def train_save(self):
        train_data, train_target, test_data, test_target = self.get_train_test_data()
        print (len(train_data), len(train_target))
        print (len(test_data), len(test_target))
        # train_data = np.array(train_data, dtype = 'float')
        # test_data = np.array(test_data, dtype = 'float')
        self.cl.fit(train_data, train_target)

        predict = self.cl.predict(test_data)
        Loader.save_model(self.cl, self.model_path, "svm")

        print (metrics.accuracy_score(test_target, predict))
    
    def forward(self, sent):
        if '下一句' in sent or '下句' in sent:
            print ('nexts')
            return
        if '上一句' in sent or '上句' in sent:
            print ('befs')
            return

        sent = ' '.join(jieba.lcut(sent))
        # sent = jieba.lcut(sent)
        # ss = []
        # for s in sent:
        #     ss.append(self.word_idx_map[s])

        predict = self.cl.predict([sent])
        print (self.id2c[predict[0]])

    def get_train_test_data(self):
        train_data, test_data = [], []
        train_target, test_target = [], []
        train_dict, test_dict = Loader.build_train_test()
        for key, value in train_dict.items():
            for v in value:
                train_data.append(v)
                train_target.append(self.c2id[key])

        for key, value in test_dict.items():
            for v in value:
                test_data.append(v)
                test_target.append(self.c2id[key])

        return train_data, train_target, test_data, test_target
    def get_train_test_data_vec(self):
        train_data, test_data = [], []
        train_target, test_target = [], []
        train_dict, test_dict = Loader.build_train_test()
        for key, value in train_dict.items():
            for v in value:
                ids = []
                for i in v.split():
                    ids.append(self.word_idx_map[i])
                train_data.append(ids)
                train_target.append(self.c2id[key])

        for key, value in test_dict.items():
            for v in value:
                ids = []
                for i in v.split():
                    ids.append(self.word_idx_map[i])
                test_data.append(ids)
                test_target.append(self.c2id[key])

        return train_data, train_target, test_data, test_target


if __name__ == "__main__":
    # qa = qa_classifier()
    # qa.train_save()
    # sent = '国籍是'
    # qa.forward(sent)
    pass

