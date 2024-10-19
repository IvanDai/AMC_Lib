from tensorflow import keras
from numpy import *
from numpy import floor
import h5py


def FilterBank(input,filter):
    """
    Function to filtered the input vector into channels.
    [Parameters]:
        input   - signal input with length of l_sig, which should be complex.
        filter  - filter input with shape of [n_ch,l_fil], n_ch is the channel num.
    [Returns]:
        output  - signal output with the shape of [n_ch,l_sig/n_ch].
    """
    # get parameter values
    l_sig      = input.shape[0]
    n_ch,l_fil = filter.shape
    l_out      = l_sig//n_ch
    # pre-transform
    vec_supply = zeros([n_ch,l_fil])         # zero-vector with the same shape of the filter
    input_poly = reshape(input,(n_ch,-1))
    input_poly = concatenate((vec_supply[:,0:l_fil//2], input_poly , vec_supply[:,0:(l_fil+1)//2]) ,axis=1)
    # declare variables
    output    = zeros([n_ch,l_out,2])
    buff_poly = zeros([n_ch,l_fil])
    buff_cplx = zeros(n_ch)
    # filtered
    for i in range(l_fil):
        buff_poly = input_poly[:,i:i+l_fil]
        buff_cplx = fft.fftshift(n_ch*fft.ifft(sum(buff_poly*filter,axis=1)))
        output[:,i,0] = real(buff_cplx)
        output[:,i,1] = imag(buff_cplx)
    # return
    return output

class gen_RML2018_filterBank(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, pth, list_IDs, batch_size=32, dim=(1024,), n_channels=2,
                 n_classes=24, shuffle=True ,type = '1024x2'):
        'Initialization'
        self.pth = pth
        self.dim = dim                  # dimension
        self.batch_size = batch_size
        self.list_IDs = list_IDs
        self.n_channels = n_channels    # each dimension's channel
        self.n_classes = n_classes      # Y's classes
        self.shuffle = shuffle
        self.type = type
        # generation
        self.on_epoch_end()
    def __len__(self):          # 重写len方法,在本模块中调用len就会返回这里定义的内容
        'Denotes the number of batches per epoch'
        return int(floor(len(self.list_IDs) / self.batch_size))
    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]
        # Generate data
        X, Y = self.__data_generation(list_IDs_temp)
        return X, Y
    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = arange(len(self.list_IDs))
        if self.shuffle == True:
            random.shuffle(self.indexes)
    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = empty((self.batch_size, *self.dim, self.n_channels))
        Y = empty((self.batch_size, self.n_classes))
        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample
            Xd = h5py.File(self.pth)
            X[i,] = Xd['X'][ID,0:self.dim[0]]       # aim at IQ signals
            # Store class
            Y[i] = Xd['Y'][ID]
        if self.type == '1024x2' :          
            return X,Y                      # batch*1024*2
        elif self.type == '2x1024':
            return X.transpose(0,2,1), Y    # batch*2*1024


class gen_RML2018(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, pth, list_IDs, batch_size=32, dim=(1024,), n_channels=2,
                 n_classes=24, shuffle=True ,type = '1024x2'):
        'Initialization'
        self.pth = pth
        self.dim = dim        # dimension
        self.batch_size = batch_size
        self.list_IDs = list_IDs
        self.n_channels = n_channels # each dimension's channel
        self.n_classes = n_classes   # Y's classes
        self.shuffle = shuffle
        self.type = type
        # generation
        self.on_epoch_end()
    def __len__(self):
        # 重写len方法,在本模块中调用len就会返回这里定义的内容
        'Denotes the number of batches per epoch'
        return int(floor(len(self.list_IDs) / self.batch_size))
    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]
        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]
        # Generate data
        X, Y = self.__data_generation(list_IDs_temp)
        return X, Y
    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = arange(len(self.list_IDs))
        if self.shuffle == True:
            random.shuffle(self.indexes)
    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = empty((self.batch_size, *self.dim, self.n_channels))
        Y = empty((self.batch_size, self.n_classes))
        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample
            Xd = h5py.File(self.pth)
            X[i,] = Xd['X'][ID,0:self.dim[0]]       # aim at IQ signals
            # Store class
            Y[i] = Xd['Y'][ID]
        if self.type == '1024x2' :          
            return X,Y                      # batch*1024*2
        elif self.type == '2x1024':
            return X.transpose(0,2,1), Y    # batch*2*1024