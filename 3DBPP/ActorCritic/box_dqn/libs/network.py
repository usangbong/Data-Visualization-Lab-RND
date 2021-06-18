# class DQN_CNN(tf.keras.Model):
#     def __init__(self, state_size, selected_size, remain_size, loading_size, output_size):
#         super(DQN_CNN, self).__init__()
#         self.case_cnn1 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid", input_shape = state_size)
#         #self.case_cnn2 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid")
        
#         # location - selected boxes
#         self.sel_cnn1 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid", input_shape = selected_size)
#         #self.sel_cnn2 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid")
        
#         # remain boxes
#         self.r_cnn1 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid", input_shape = remain_size )
#         #self.r_cnn2 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid")
        
#         # all
#         n_ch = state_size[-1] + selected_size[-1] + remain_size[-1] + loading_size[-1] 
#         self.a_cnn1 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid", input_shape = state_size[:-1]+(n_ch,))
        
#         # merge 
#         self.fc1 = Dense(256, activation='relu')
#         self.fc2 = Dense(128, activation='relu')
#         self.fc_out = Dense(output_size)

#     def call(self, cb_list):
#         c, s, r = cb_list[0], cb_list[1], cb_list[2]
#         a =  tf.concat([c, s, r], -1)
#         ### case
#         c = self.case_cnn1(c)
#         c = MaxPooling2D(pool_size=(2, 2))(c)
#         #c = self.case_cnn2(c)
#         #c = MaxPooling2D(pool_size=(2, 2))(c)
#         c = Flatten()(c)
        
#         ### location - selected boxes
#         s = self.sel_cnn1(s)
#         s = MaxPooling2D(pool_size=(2, 2))(s)
#         #s = self.sel_cnn2(s)
#         #s = MaxPooling2D(pool_size=(2, 2))(s)
#         s = Flatten()(s)
        
#         ### remain boxes
#         r = self.r_cnn1(r)
#         r = MaxPooling2D(pool_size=(2, 2))(r)
#         #r = self.r_cnn2(r)
#         #r = MaxPooling2D(pool_size=(2, 2))(r)
#         r = Flatten()(r)
        
#         ### all
#         a = self.a_cnn1(a)
#         a = MaxPooling2D(pool_size=(2, 2))(a)
#         a = Flatten()(a)
        
#         ### merge
#         x = concatenate([c,s,r,l,a])
#         x = self.fc1(x)
#         x = self.fc2(x)
#         q = self.fc_out(x)
#         return q


# class DQN_CNN(tf.keras.Model):
#     def __init__(self, state_size, selected_size, remain_size, loading_size, output_size):
#         super(DQN_CNN, self).__init__()
#         # all
#         n_ch = state_size[-1] + selected_size[-1] + remain_size[-1] #+ loading_size[-1] 
#         self.a_cnn1 = Conv2D(filters=32, kernel_size=3, activation='relu', padding="valid", input_shape = state_size[:-1]+(n_ch,))
#         self.a_cnn2 = Conv2D(filters=32, kernel_size=3, activation='relu', padding="valid")
#         self.a_cnn2 = Conv2D(filters=16, kernel_size=3, activation='relu', padding="valid")
#         # merge 
#         self.fc1 = Dense(256, activation='relu')
#         self.fc2 = Dense(128, activation='relu')
#         self.fc_out = Dense(output_size)

#     def call(self, cb_list):
#         c, s, r = cb_list[0], cb_list[1], cb_list[2]
#         a =  tf.concat([c, s, r], -1)
#         ### all
#         a = self.a_cnn1(a)
#         a = MaxPooling2D(pool_size=(2, 2))(a)
#         a = self.a_cnn2(a)
#         a = MaxPooling2D(pool_size=(2, 2))(a)
#         x = Flatten()(a)
#         ### merge
#         x = self.fc1(x)
#         x = self.fc2(x)
#         q = self.fc_out(x)
#         return q
    
# class DQN(tf.keras.Model):
#     def __init__(self, state_size, selected_size, remain_size, loading_size, output_size):
#         super(DQN, self).__init__()
#         # case network
#         l1,b1,k1 = state_size # 배치 사이즈 제외된 사이즈
#         self.state_size = (l1*b1*k1,)
#         self.case_dnn1 = Dense(64, activation='relu',input_shape = self.state_size)
#         self.case_dnn2 = Dense(64, activation='relu')#
#         # location - selected boxes
#         l2,b2,k2 = selected_size
#         self.selected_size = (l2*b2*k2,)
#         self.sel_dnn1 = Dense(64, activation='relu',input_shape = self.selected_size)
#         self.sel_dnn2 = Dense(64, activation='relu')#
#         # remain boxes
#         l3,b3,k3 = remain_size
#         self.remain_size = (l3*b3*k3, )
#         self.r_dnn1 = Dense(128, activation='relu', input_shape = self.remain_size  )
#         self.r_dnn2 = Dense(128, activation='relu')
#         # all
#         #self.all_size = (self.state_size[0]+self.selected_size[0]+self.remain_size[0]+self.loading_size[0], )
#         #self.a_dnn1 = Dense(128, activation='relu', input_shape = self.all_size  )
#         # merge 
#         self.fc1 = Dense(256, activation='relu')
#         self.fc2 = Dense(256, activation='relu')
#         self.fc2 = Dense(128, activation='relu')
#         self.fc_out = Dense(output_size)

#     def call(self, cb_list):
#         c, s, r = cb_list[0], cb_list[1], cb_list[2]
#         c = tf.reshape(c, [-1, self.state_size[0]])
#         s = tf.reshape(s, [-1, self.selected_size[0]])
#         r = tf.reshape(r, [-1, self.remain_size[0]])
#         #a =  tf.concat([c, s, r, l], -1)
#         ### case
#         c = self.case_dnn1(c)
#         c = self.case_dnn2(c)
#         ### location - selected boxes
#         s = self.sel_dnn1(s)
#         s = self.sel_dnn2(s)
#         ### remain boxes
#         r = self.r_dnn1(r)
#         r = self.r_dnn2(r)
#         ### all
#         #a = self.a_dnn1(a)
#         ### merge
#         x = concatenate([c,s,r])#x = concatenate([c,s,r,l,a])
#         x = self.fc1(x)
#         x = self.fc2(x)
#         q = self.fc_out(x)
#         return q
class DQN_CNNDNN(tf.keras.Model):
    def __init__(self, state_size, selected_size, remain_size, loading_size, output_size):
        super(DQN_CNNDNN, self).__init__()
        self.case_cnn1 = Conv2D(filters=5, kernel_size=3, activation='relu', padding="valid", input_shape = state_size)
        self.case_dnn1 = Dense(32, activation='relu')
        # location - selected boxes
        #self.sel_cnn1 = Conv2D(filters=5, kernel_size=3, activation='relu', padding="valid", input_shape = selected_size)
        #self.sel_dnn1 = Dense(32, activation='relu')
        # remain boxes
        self.r_cnn1 = Conv2D(filters=8, kernel_size=3, activation='relu', padding="valid", input_shape = remain_size )
        self.r_dnn1 = Dense(64, activation='relu')
        # size - selected boxes
        self.l_cnn1 = Conv2D(filters=5, kernel_size=3, activation='relu', padding="valid", input_shape = loading_size )
        self.l_dnn1 = Dense(32, activation='relu')
        # all
        #n_ch = state_size[-1] + selected_size[-1] + remain_size[-1] + loading_size[-1] 
        #self.a_cnn1 = Conv2D(filters=8, kernel_size=3, activation='relu', padding="valid", input_shape = state_size[:-1]+(n_ch,))
        self.a_cnn1 = Conv2D(filters=8, kernel_size=3, activation='relu', padding="valid")
        self.a_dnn1 = Dense(32, activation='relu')
        # merge 
        self.fc1 = Dense(256, activation='relu')
        self.fc2 = Dense(128, activation='relu')
        if output_size > 1: #DDQN
            self.fc_out = Dense(output_size, activation='softmax')
        else:
            self.fc_out = Dense(output_size)

    def call(self, cb_list):
        c, s, r,l = cb_list[0], cb_list[1], cb_list[2], cb_list[3]
        #c, s, r = cb_list[0], cb_list[1], cb_list[2]
        #a =  tf.concat([c, s, r], -1)
        ### case
        c = self.case_cnn1(c)
        c = MaxPooling2D(pool_size=(2, 2))(c)
        cf = Flatten()(c)
        cf = self.case_dnn1(cf)
        ### location - selected boxes
        #s = self.sel_cnn1(s)
        #s = MaxPooling2D(pool_size=(2, 2))(s)
        #s = Flatten()(s)
        #s = self.sel_dnn1(s)
        ### remain boxes
        r = self.r_cnn1(r)
        r = MaxPooling2D(pool_size=(2, 2))(r)
        rf = Flatten()(r)
        rf = self.r_dnn1(rf)
        ### size - selected boxes
        l = self.l_cnn1(l)
        l = MaxPooling2D(pool_size=(2, 2))(l)
        lf = Flatten()(l)
        lf = self.l_dnn1(lf)
        ### all
        a =  tf.concat([c, r, l], -1)
        a = self.a_cnn1(a)
        a = MaxPooling2D(pool_size=(2, 2))(a)
        af = Flatten()(a)
        af = self.a_dnn1(af)
        ### merge
        x = concatenate([cf,rf,lf,af])#x = concatenate([c,s,r,l,a])#x = concatenate([c,s,r])#
        x = self.fc1(x)
        x = self.fc2(x)
        q = self.fc_out(x)
        return q    