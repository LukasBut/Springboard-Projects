import tensorflow as tf
from keras import backend as K
from keras.engine.topology import Layer
from keras.layers import Bidirectional, Dense
from attention_gru import SoftAttnGRU

from keras import regularizers


class EpisodicMemoryModule(Layer):

    def __init__(self, units,  emb_dim,
                 batch_size, memory_steps=3, dropout=0.0, reuglarization=1e-3, **kwargs):
        """Initializes the Episodic Memory Module from
         https://arxiv.org/pdf/1506.07285.pdf and https://arxiv.org/pdf/1603.01417.pdf.
        The module has internally 2 dense layers used to compute attention,
        one attention GRU unit, that modifies the layer input based on the computed attention,
        and finally, one Dense layer that generates the new memory.
        Have a look at the call method to get an idea of how everything works.
        Parameters
        ----------
        units : (int)
            The number of hidden units in the attention and memory networks
        memory_steps : (int)
            Number of steps to iterate over the input and generate the memory.
        emb_dim : (int)
            The size of the embeddings, and thus the number of units for the
            attention computation
        batch_size : (int)
            Size of the batch
        dropout : (float)
            The dropout rate for the module
        **kwargs : (arguments)
            Extra arguments
        """

        # TODO: Dropout

        self.memory_steps = memory_steps
        self.dropout = dropout
        self.name = "episodic_memory_module"
        self._input_map = {}
        self.supports_masking = True
        self.units = units

        # attention net.
        self.l_1 = Dense(units=emb_dim,
                         batch_size=batch_size,
                         activation='tanh',
                         kernel_regularizer=regularizers.l2(reuglarization))

        self.l_2 = Dense(units=1,
                         batch_size=batch_size,
                         activation=None,
                         kernel_regularizer=regularizers.l2(reuglarization))

        # Episode net
        self.episode_GRU = SoftAttnGRU(units=units,
                                       return_sequences=False,
                                       batch_size=batch_size,
                                       kernel_regularizer=regularizers.l2(
                                           0.001),
                                       recurrent_regularizer=regularizers.l2(reuglarization))

        # Memory generating net.
        self.memory_net = Dense(units=units,
                                activation='relu',
                                kernel_regularizer=regularizers.l2(reuglarization))

        super(EpisodicMemoryModule, self).__init__()

    def get_config():
        # TODO: Fix this to allow saving the entire model
        raise NotImplementedError

    def compute_output_shape(self, input_shape):

        q_shape = list(input_shape[1])
        q_shape[-1] = self.units * 2

        return tuple(q_shape)

    def build(self, input_shape):
        super(EpisodicMemoryModule, self).build(input_shape)

    def call(self, inputs):
        """Generates a new memory based on thequestion and
        current inputs.
        Parameters
        ----------
        inputs : (list) of (K.Tensor)
            A list of size two, where each element is a tensor. The first one is
            the facts vector, and the second - the question vector.
        Returns
        -------
        K.Tensor
            A memory generated from the question and fact_vectors
        """

        def compute_attention(fact, question, memory):
            """Computes an attention score over a single fact vector,
            question and memoty
            Parameters
            ----------
            fact : (K.tensor)
                A single fact vector
            question : (K.tensor)
                Description of parameter `question`.
            memory : (K.tensor)
                The previous memory
            Returns
            -------
            (K.tensor)
                The scalar attention score for the current fact.
            """

            f_i = [
                fact * question,
                fact * memory,
                K.abs(
                    fact - question),
                K.abs(
                    fact - memory)]
            g_t_i = self.l_1(K.concatenate(f_i, axis=1))
            g_t_i = self.l_2(g_t_i)
            return g_t_i

        facts = inputs[0]
        question = inputs[1]
        memory = K.identity(question)   # Initialize memory to the question
        fact_list = tf.unstack(facts, axis=1)

        for step in range(self.memory_steps):

            # Adapted from
            # https://github.com/barronalex/Dynamic-Memory-Networks-in-TensorFlow/

            # Looks recurrent? In a way it is
            attentions = [tf.squeeze(
                compute_attention(fact, question, memory), axis=1)
                for i, fact in enumerate(fact_list)]

            attentions = tf.stack(attentions)
            attentions = tf.transpose(attentions)
            attentions = tf.nn.softmax(attentions)
            attentions = tf.expand_dims(attentions, axis=-1)

            episode = K.concatenate([facts, attentions], axis=2)
            # Last state. Correct? Maybe not
            episode = self.episode_GRU(episode)

            memory = self.memory_net(K.concatenate(
                [memory, episode, question], axis=1))

        return K.concatenate([memory, question], axis=1)