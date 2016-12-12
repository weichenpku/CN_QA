from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM

import jieba
from utils import Loader

class LSTM(object):
    def __init__(self, load = None):
        self.vocab, self.max_len = Loader.build_vocab()
        print ("data loaded!")
        print ("vocab size: " + str(len(self.vocab)))
        print ("max sentence length: " + str(self.max_len))
        self.w2v = Loader.load_word_vec(self.vocab)
        print ("word2vec loaded!")
        print ("num words already in word2vec: " + str(len(self.w2v)))
        Loader.add_unknown_words(self.w2v, self.vocab)
        self.W, self.word_idx_map = Loader.get_W(self.w2v)

        self.model = Sequential()
        self.model.add(Embedding(len(self.word_idx_map), 300, input_length=self.max_len, weights=self.W))
        self.model.add(LSTM(output_dim=100, activation='sigmoid', inner_activation='hard_sigmoid'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(7))
        self.model.add(Activation('softmax'))
    
        self.model_path = "../../data/lstm_model.json"
        self.params_path = "../../data/lstm_params.h5"
        if load:
            self.model = Loader.load_model(self.model_path, "lstm", self.params_path)

        self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics = ['categorical_accuracy'])
            
    def train_save(self):
        train_data, train_target, test_data, test_target = self.get_train_test_data()
        print (len(train_data), len(train_target))
        print (len(test_data), len(test_target))
        self.model.fit(train_data, train_target, batch_size=20, nb_epoch=10)
        score = model.evaluate(test_data, test_target, batch_size=20)

        # predict = self.model.predict(test_data)
        Loader.save_model(self.model, self.model_path, "lstm", self.params_path)

        print (score)
    
    def forward(self, sent):
        if '下一句' in sent or '下句' in sent:
            print ('nexts')
            return
        if '上一句' in sent or '上句' in sent:
            print ('befs')
            return

        sent = ' '.join(jieba.lcut(sent))
        predict = self.model.predict([sent])
        print (self.id2c[predict[0]])

    def get_train_test_data(self):
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

    