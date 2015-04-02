'''
'''
class RC4(object):
    '''
    key is a list or tuple
    '''
    def __init__(self, key):
        self.index1 = 0
        self.index2 = 0

        perm = range(256)
        j = 0
        klen = len(key)
        for i in range(256):
            j = (j + perm[i] + ord(key[i % klen])) % 256
            perm[i], perm[j] = perm[j], perm[i]  # swap
        self.perm = perm

    '''
     * Encrypt some data using the supplied RC4 state buffer.
     * The input and output buffers may be the same buffer.
     * Since RC4 is a stream cypher, this function is used
     * for both encryption and decryption.
    ''' 
    def crypt(self, data):
        dlen = len(data)
        out = ""
        perm = self.perm
        for i in range(dlen):
            self.index1 = (self.index1 + 1) % 256
            self.index2 = (self.index2 + perm[self.index1]) % 256
            perm[self.index1], perm[self.index2] = perm[self.index2], perm[self.index1]

            j = (perm[self.index1] + perm[self.index2]) % 256
            out = out + chr((ord(data[i]) ^ perm[j]))
        return out

