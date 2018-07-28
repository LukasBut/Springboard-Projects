from tensorflow.python.ops import array_ops
from keras import backend as K
from keras import activations
from keras import initializers
from keras import regularizers
from keras import constraints
from keras.engine.topology import Layer

from keras import regularizers


class SoftAttnGRU(Layer):

    def __init__(self,
                 units,
                 activation='tanh',
                 recurrent_activation='hard_sigmoid',
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 recurrent_initializer='orthogonal',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 recurrent_regularizer=None,
                 bias_regularizer=None,
                 kernel_constraint=None,
                 recurrent_constraint=None,
                 bias_constraint=None,
                 dropout=0.,
                 recurrent_dropout=0.,
                 implementation=1,
                 return_sequences=False,
                 **kwargs):
        """Identical to keras.recurrent.GRUCell.
        The difference comes from the computation in self.call
        """


        super(SoftAttnGRU, self).__init__(**kwargs)

        self.units = units
        self.return_sequences = return_sequences
        self.activation = activations.get(activation)
        self.recurrent_activation = activations.get(recurrent_activation)
        self.use_bias = use_bias

        self.kernel_initializer = initializers.get(kernel_initializer)
        self.recurrent_initializer = initializers.get(recurrent_initializer)
        self.bias_initializer = initializers.get(bias_initializer)

        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.recurrent_regularizer = regularizers.get(recurrent_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)

        self.kernel_constraint = constraints.get(kernel_constraint)
        self.recurrent_constraint = constraints.get(recurrent_constraint)
        self.bias_constraint = constraints.get(bias_constraint)

        self.dropout = min(1., max(0., dropout))
        self.recurrent_dropout = min(1., max(0., recurrent_dropout))
        self.implementation = implementation
        self.state_size = self.units
        self._dropout_mask = None
        self._recurrent_dropout_mask = None

        self._input_map = {}

        super(SoftAttnGRU, self).__init__(**kwargs)

    def compute_output_shape(self, input_shape):

        out = list(input_shape)
        out[-1] = self.units
        if self.return_sequences:
            return out
        else:
            return (out[0], out[-1])

    def build(self, input_shape):

        input_dim = input_shape[-1] - 1

        self.kernel = self.add_weight(shape=(input_dim, self.units * 3),
                                      name='kernel',
                                      initializer=self.kernel_initializer,
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)

        self.recurrent_kernel = self.add_weight(
            shape=(self.units, self.units * 3),
            name='recurrent_kernel',
            initializer=self.recurrent_initializer,
            regularizer=self.recurrent_regularizer,
            constraint=self.recurrent_constraint)

        if self.use_bias:
            self.bias = self.add_weight(shape=(self.units * 3,),
                                        name='bias',
                                        initializer=self.bias_initializer,
                                        regularizer=self.bias_regularizer,
                                        constraint=self.bias_constraint)
        else:
            self.bias = None

        self.kernel_z = self.kernel[:, :self.units]
        self.recurrent_kernel_z = self.recurrent_kernel[:, :self.units]
        self.kernel_r = self.kernel[:, self.units: self.units * 2]
        self.recurrent_kernel_r = self.recurrent_kernel[:,
                                                        self.units:
                                                        self.units * 2]
        self.kernel_h = self.kernel[:, self.units * 2:]
        self.recurrent_kernel_h = self.recurrent_kernel[:, self.units * 2:]

        if self.use_bias:
            self.bias_z = self.bias[:self.units]
            self.bias_r = self.bias[self.units: self.units * 2]
            self.bias_h = self.bias[self.units * 2:]
        else:
            self.bias_z = None
            self.bias_r = None
            self.bias_h = None
        super(SoftAttnGRU, self).build(input_shape)

    def step(self, inputs, states, training=None):
        """Computes the output of a single step. Unlike the vanilla GRU, attention is applied to the
        output, as per https://arxiv.org/pdf/1603.01417.pdf
        ----------
        inputs : (K.Tensor)
            A tensor of shape [batch_size, input_size+1]. The last element of each example is the
            attention score.
        states : (K.Tensor)
            Initial (list) of states
        training : (bool)
            Whether the network is in training mode or not. 
        Returns
        -------
        (K.Tensor)
            The output for the current step, modified by attention
        """
            # Needs question as an input
        x_i, attn_gate = array_ops.split(inputs,
                                         num_or_size_splits=[self.units, 1], axis=1)
        h_tm1 = states[0]

        # dropout matrices for input units
        dp_mask = self._dropout_mask
        # dropout matrices for recurrent units
        rec_dp_mask = self._recurrent_dropout_mask

        if self.implementation == 1:
            if 0. < self.dropout < 1.:
                inputs_z = x_i * dp_mask[0]
                inputs_r = x_i * dp_mask[1]
                inputs_h = x_i * dp_mask[2]
            else:
                inputs_z = x_i
                inputs_r = x_i
                inputs_h = x_i
            x_z = K.dot(inputs_z, self.kernel_z)
            x_r = K.dot(inputs_r, self.kernel_r)
            x_h = K.dot(inputs_h, self.kernel_h)
            if self.use_bias:
                x_z = K.bias_add(x_z, self.bias_z)
                x_r = K.bias_add(x_r, self.bias_r)
                x_h = K.bias_add(x_h, self.bias_h)

            if 0. < self.recurrent_dropout < 1.:
                h_tm1_z = h_tm1 * rec_dp_mask[0]
                h_tm1_r = h_tm1 * rec_dp_mask[1]
                h_tm1_h = h_tm1 * rec_dp_mask[2]
            else:
                h_tm1_z = h_tm1
                h_tm1_r = h_tm1
                h_tm1_h = h_tm1

            z = self.recurrent_activation(
                x_z + K.dot(h_tm1_z, self.recurrent_kernel_z))
            r = self.recurrent_activation(
                x_r + K.dot(h_tm1_r, self.recurrent_kernel_r))

            hh = self.activation(x_h + K.dot(r * h_tm1_h,
                                             self.recurrent_kernel_h))
        else:
            if 0. < self.dropout < 1.:
                x_i *= dp_mask[0]
            matrix_x = K.dot(x_i, self.kernel)
            if self.use_bias:
                matrix_x = K.bias_add(matrix_x, self.bias)
            if 0. < self.recurrent_dropout < 1.:
                h_tm1 *= rec_dp_mask[0]
            matrix_inner = K.dot(h_tm1,
                                 self.recurrent_kernel[:, :2 * self.units])

            x_z = matrix_x[:, :self.units]
            x_r = matrix_x[:, self.units: 2 * self.units]
            recurrent_z = matrix_inner[:, :self.units]
            recurrent_r = matrix_inner[:, self.units: 2 * self.units]

            z = self.recurrent_activation(x_z + recurrent_z)
            r = self.recurrent_activation(x_r + recurrent_r)

            x_h = matrix_x[:, 2 * self.units:]
            recurrent_h = K.dot(r * h_tm1,
                                self.recurrent_kernel[:, 2 * self.units:])
            hh = self.activation(x_h + recurrent_h)
        h = z * h_tm1 + (1 - z) * hh

        # Attention modulated output.
        h = attn_gate * h + (1 - attn_gate) * h_tm1

        if 0 < self.dropout + self.recurrent_dropout:
            if training is None:
                h._uses_learning_phase = True
        return h, [h]

    def call(self, input_list, initial_state=None, mask=None, training=None):

        inputs = input_list

        self._generate_dropout_mask(inputs, training=training)
        self._generate_recurrent_dropout_mask(inputs, training=training)

        # if has_arg(self.layer.call, 'training'):
        self.training = training
        uses_learning_phase = False
        initial_state = self.get_initial_state(inputs)

        input_shape = K.int_shape(inputs)
        last_output, outputs, _ = K.rnn(self.step,
                                        inputs=inputs,
                                        constants=[],
                                        initial_states=initial_state,
                                        input_length=input_shape[1],
                                        unroll=False)
        if self.return_sequences:
            y = outputs
        else:
            y = last_output

        if (hasattr(self, 'activity_regularizer') and
                self.activity_regularizer is not None):
            regularization_loss = self.activity_regularizer(y)
            self.add_loss(regularization_loss, inputs)

        if uses_learning_phase:
            y._uses_learning_phase = True

        if self.return_sequences:
            timesteps = input_shape[1]
            new_time_steps = list(y.get_shape())
            new_time_steps[1] = timesteps
            y.set_shape(new_time_steps)
        return y

    def _generate_dropout_mask(self, inputs, training=None):
        if 0 < self.dropout < 1:
            ones = K.ones_like(K.squeeze(inputs[:, 0:1, :-1], axis=1))

            def dropped_inputs():
                return K.dropout(ones, self.dropout)

            self._dropout_mask = [K.in_train_phase(
                dropped_inputs,
                ones,
                training=training)
                for _ in range(3)]
        else:
            self._dropout_mask = None

    def _generate_recurrent_dropout_mask(self, inputs, training=None):
        if 0 < self.recurrent_dropout < 1:
            ones = K.ones_like(K.reshape(inputs[:, 0, 0], (-1, 1)))
            ones = K.tile(ones, (1, self.units))

            def dropped_inputs():
                return K.dropout(ones, self.dropout)

            self._recurrent_dropout_mask = [K.in_train_phase(
                dropped_inputs,
                ones,
                training=training)
                for _ in range(3)]
        else:
            self._recurrent_dropout_mask = None

    def get_initial_state(self, inputs):
        # build an all-zero tensor of shape (samples, output_dim)
        initial_state = K.zeros_like(inputs)  # (samples, timesteps, input_dim)
        initial_state = initial_state[:, :, :-1]
        initial_state = K.sum(initial_state, axis=(1, 2))  # (samples,)
        initial_state = K.expand_dims(initial_state)  # (samples, 1)
        if hasattr(self.state_size, '__len__'):
            return [K.tile(initial_state, [1, dim])
                    for dim in self.state_size]
        else:
            return [K.tile(initial_state, [1, self.state_size])]
