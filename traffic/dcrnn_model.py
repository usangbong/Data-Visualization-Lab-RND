from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
from tensorflow.contrib import legacy_seq2seq

from lib.metrics import masked_mae_loss
from model.dcrnn_cell import DCGRUCell
import random

class DCRNNModel(object):
    def __init__(self, is_training, batch_size, scaler, adj_mx, **model_kwargs):
        # Scaler for data normalization.
        self._scaler = scaler

        # Train and loss
        self._loss = None
        self._mae = None
        self._train_op = None

        max_diffusion_step = int(model_kwargs.get('max_diffusion_step', 2))
        cl_decay_steps = int(model_kwargs.get('cl_decay_steps', 1000))
        filter_type = model_kwargs.get('filter_type', 'laplacian')
        horizon = int(model_kwargs.get('horizon', 1))
        max_grad_norm = float(model_kwargs.get('max_grad_norm', 5.0))
        num_nodes = int(model_kwargs.get('num_nodes', 1))
        num_rnn_layers = int(model_kwargs.get('num_rnn_layers', 1))
        rnn_units = int(model_kwargs.get('rnn_units'))
        seq_len = int(model_kwargs.get('seq_len'))
        use_curriculum_learning = bool(model_kwargs.get('use_curriculum_learning', False))
        input_dim = int(model_kwargs.get('input_dim', 1))
        output_dim = int(model_kwargs.get('output_dim', 1))

        # Input (batch_size, timesteps, num_sensor, input_dim)
        self._inputs = tf.placeholder(tf.float32, shape=(batch_size, seq_len, num_nodes, input_dim), name='inputs')
        # Labels: (batch_size, timesteps, num_sensor, input_dim), same format with input except the temporal dimension.
        self._labels = tf.placeholder(tf.float32, shape=(batch_size, horizon, num_nodes, input_dim), name='labels')

        # GO_SYMBOL = tf.zeros(shape=(batch_size, num_nodes * input_dim))
        GO_SYMBOL = tf.zeros(shape=(batch_size, num_nodes * output_dim))

        cell = DCGRUCell(rnn_units, adj_mx, max_diffusion_step=max_diffusion_step, num_nodes=num_nodes,
                         filter_type=filter_type)
        cell_with_projection = DCGRUCell(rnn_units, adj_mx, max_diffusion_step=max_diffusion_step, num_nodes=num_nodes,
                                         num_proj=output_dim, filter_type=filter_type)
        encoding_cells = [cell] * num_rnn_layers
        #decoding_cells = [cell] * (num_rnn_layers - 1) + [cell_with_projection]

        encoding_cells = tf.contrib.rnn.MultiRNNCell(encoding_cells, state_is_tuple=True)
        #decoding_cells = tf.contrib.rnn.MultiRNNCell(decoding_cells, state_is_tuple=True)





        global_step = tf.train.get_or_create_global_step()
        # Outputs: (batch_size, timesteps, num_nodes, output_dim)
        with tf.variable_scope('DCRNN_SEQ'):
            inputs = tf.unstack(tf.reshape(self._inputs, (batch_size, seq_len, num_nodes * input_dim)), axis=1)
            labels = tf.unstack(
                tf.reshape(self._labels[..., :output_dim], (batch_size, horizon,num_nodes * output_dim)), axis=1)
            labels.insert(0, GO_SYMBOL)
            print("라벨")
            print(labels)
            # def _loop_function(prev, i):
            #     if is_training:
            #         # Return either the model's prediction or the previous ground truth in training.
            #
            #         if use_curriculum_learning:
            #             #c = tf.random_uniform((), minval=0, maxval=1.)
            #             c=random.random()
            #             threshold = self._compute_sampling_threshold(i, cl_decay_steps)
            #             print(f"c ===={c}")
            #             print(f"트레싷ㄹ드: {threshold}")
            #             #result = tf.cond(tf.less(c, threshold), lambda: labels[i], lambda: prev)
            #
            #             if c<threshold:
            #                 result=labels[i]
            #             else:
            #                 #일단 임시로 이걸로 바꿈 원래는 prev임
            #                 result=labels[i]
            #
            #
            #             print(f"labels[i]: {labels[i]}")
            #             print(f"prev: {prev}")
            #             print("result")
            #             print(result)
            #         else:
            #             print("not use currui")
            #             result = labels[i]
            #     else:
            #         # Return the prediction of the model in testing.
            #         print("in testing")
            #         #일단 이거 임시로 원래는 prev
            #         result = labels[i]
            #     print("loop fun -> result")
            #     print(result)
            #     return result
            def _loop_function(prev, i):
                if is_training:
                    # Return either the model's prediction or the previous ground truth in training.
                    if use_curriculum_learning:
                        c = tf.random_uniform((), minval=0, maxval=1.)
                        threshold = self._compute_sampling_threshold(global_step, cl_decay_steps)
                        print("쓰레시홀드 낭ㅁ")
                        #result = tf.cond(tf.less(c, threshold), lambda: labels[i], lambda: prev)
                        #원본은 대신
                        result = prev
                    else:
                        print(" use_curriculum_learning아님 ")
                        result = labels[i]
                else:
                    # Return the prediction of the model in testing.
                    result = prev
                return result
                #인코딩 실행
            enc_output, enc_state = tf.contrib.rnn.static_rnn(encoding_cells, inputs, dtype=tf.float32)


            print("@@@@@@@@@@@@@@@@@@@@")
            print("enc_output")
            print(enc_output)
            print("@@@@@@@@@@@@@@@@@@@@")
            print("encstateeeeeeeee")

            # attention 구현

            attention_states = tf.transpose(enc_output, [1, 0, 2])




            attention_mechanism = tf.contrib.seq2seq.BahdanauAttention(num_nodes, attention_states,dtype=tf.float32)


            attention_cell = tf.contrib.seq2seq.AttentionWrapper(
                cell=cell, attention_mechanism=attention_mechanism,
                alignment_history=False, output_attention=False)
            attention_cell_with_projection = tf.contrib.seq2seq.AttentionWrapper(
                cell=cell_with_projection, attention_mechanism=attention_mechanism,
                alignment_history=False, output_attention=False)

            decoding_cells = [attention_cell] * (num_rnn_layers - 1) + [attention_cell_with_projection]

            decoding_cells = tf.contrib.rnn.MultiRNNCell(decoding_cells, state_is_tuple=True)






            decoder_initial_state = decoding_cells.zero_state(batch_size, dtype=tf.float32)

            decoder_initial_state = decoder_initial_state.clone(cell_state=enc_state)
            print(type(decoder_initial_state))
            #decoder_initial_state = decoding_cells.get_initial_state(batch_size, dtype=tf.float32).clone(cell_state=enc_state)

            print(decoder_initial_state)
            outputs, final_state = legacy_seq2seq.attention_decoder(labels, decoder_initial_state, attention_states ,decoding_cells, loop_function=_loop_function)

            print(outputs)
        # Project the output to output_dim.
        outputs = tf.stack(outputs[:-1], axis=1)


        self._outputs = tf.reshape(outputs, (batch_size, horizon, num_nodes, output_dim), name='outputs')
        self._merged = tf.summary.merge_all()

    @staticmethod
    def _compute_sampling_threshold(global_step, k):
        """
        Computes the sampling probability for scheduled sampling using inverse sigmoid.
        :param global_step:
        :param k:
        :return:
        """
        print("###global")
        # print((global_step))
        # print(k)
        return tf.cast(k / (k + tf.exp(global_step / k)), tf.float32)
        #return float(k/(k+np.exp(global_step+1/k)))
    @property
    def inputs(self):
        return self._inputs

    @property
    def labels(self):
        return self._labels

    @property
    def loss(self):
        return self._loss

    @property
    def mae(self):
        return self._mae

    @property
    def merged(self):
        return self._merged

    @property
    def outputs(self):
        return self._outputs
