"""
Constant used in tran53 hash function, contains values 0 <= x <= 255
see implementation of tran_hash() below for details on usage
"""

TRAN = [ord(x) for x in
        "\x02\xD6\x9E\x6F\xF9\x1D\x04\xAB\xD0\x22\x16\x1F\xD8\x73\xA1\xAC"
        "\x3B\x70\x62\x96\x1E\x6E\x8F\x39\x9D\x05\x14\x4A\xA6\xBE\xAE\x0E"
        "\xCF\xB9\x9C\x9A\xC7\x68\x13\xE1\x2D\xA4\xEB\x51\x8D\x64\x6B\x50"
        "\x23\x80\x03\x41\xEC\xBB\x71\xCC\x7A\x86\x7F\x98\xF2\x36\x5E\xEE"
        "\x8E\xCE\x4F\xB8\x32\xB6\x5F\x59\xDC\x1B\x31\x4C\x7B\xF0\x63\x01"
        "\x6C\xBA\x07\xE8\x12\x77\x49\x3C\xDA\x46\xFE\x2F\x79\x1C\x9B\x30"
        "\xE3\x00\x06\x7E\x2E\x0F\x38\x33\x21\xAD\xA5\x54\xCA\xA7\x29\xFC"
        "\x5A\x47\x69\x7D\xC5\x95\xB5\xF4\x0B\x90\xA3\x81\x6D\x25\x55\x35"
        "\xF5\x75\x74\x0A\x26\xBF\x19\x5C\x1A\xC6\xFF\x99\x5D\x84\xAA\x66"
        "\x3E\xAF\x78\xB3\x20\x43\xC1\xED\x24\xEA\xE6\x3F\x18\xF3\xA0\x42"
        "\x57\x08\x53\x60\xC3\xC0\x83\x40\x82\xD7\x09\xBD\x44\x2A\x67\xA8"
        "\x93\xE0\xC2\x56\x9F\xD9\xDD\x85\x15\xB4\x8A\x27\x28\x92\x76\xDE"
        "\xEF\xF8\xB2\xB7\xC9\x3D\x45\x94\x4B\x11\x0D\x65\xD5\x34\x8B\x91"
        "\x0C\xFA\x87\xE9\x7C\x5B\xB1\x4D\xE5\xD4\xCB\x10\xA2\x17\x89\xBC"
        "\xDB\xB0\xE2\x97\x88\x52\xF7\x48\xD3\x61\x2C\x3A\x2B\xD1\x8C\xFB"
        "\xF1\xCD\xE4\x6A\xE7\xA9\xFD\xC4\x37\xC8\xD2\xF6\xDF\x58\x72\x4E"]


class Hash64(object):
    """A class for generating hash strings of length 64 (characters represent base 16 numbers) in python 3.4.
    The only callable method is `string_to_64hash` that receives a string and returns the hash strings.
    for more information please see: `https://en.wikipedia.org/wiki/Nilsimsa_Hash`."""

    def _tran_hash(self, a, b, c, n):
        """Implementation of the tran53 hash function"""

        return ((TRAN[(a + n) & 255] ^ TRAN[b] * (n + n + 1)) + TRAN[c ^ TRAN[n]]) & 255

    def _hexdigest(self, vec):
        """Computes the hex of the digest"""

        return ''.join('%02x' % i for i in vec)

    def _compute_digest(self, acc, num_char):
        """Using a threshold (mean of the accumulator), computes the nilsimsa digest"""

        num_trigrams = 0
        if num_char == 3:  # 3 chars -> 1 trigram
            num_trigrams = 1
        elif num_char == 4:  # 4 chars -> 4 trigrams
            num_trigrams = 4
        elif num_char > 4:  # > 4 chars -> 8 for each char
            num_trigrams = 8 * num_char - 28

        # threshhold is the mean of the acc buckets
        threshold = num_trigrams / 256.0

        digest = [0] * 32
        for i in range(256):
            if acc[i] > threshold:
                digest[i >> 3] += 1 << (i & 7)  # equivalent to i/8, 2**(i mod 7)

        return digest[::-1]  # store result in digest, reversed

    def _process(self, chunk):
        """Computes the hash of all of the trigrams in the chunk using a window of length 5"""

        num_char = 0
        acc = [0] * 256
        window = []
        if isinstance(chunk, str):
            chunk = chunk.encode('utf-8')

        # chunk is a byte string
        for char in chunk:
            num_char += 1
            c = char
            if len(window) > 1:  # seen at least three characters
                acc[self._tran_hash(c, window[0], window[1], 0)] += 1
            if len(window) > 2:  # seen at least four characters
                acc[self._tran_hash(c, window[0], window[2], 1)] += 1
                acc[self._tran_hash(c, window[1], window[2], 2)] += 1
            if len(window) > 3:  # have a full window
                acc[self._tran_hash(c, window[0], window[3], 3)] += 1
                acc[self._tran_hash(c, window[1], window[3], 4)] += 1
                acc[self._tran_hash(c, window[2], window[3], 5)] += 1
                # duplicate hashes, used to maintain 8 trigrams per character
                acc[self._tran_hash(window[3], window[0], c, 6)] += 1
                acc[self._tran_hash(window[3], window[2], c, 7)] += 1

            # add current character to the window, remove the previous character
            if len(window) < 4:
                window = [c] + window
            else:
                window = [c] + window[:3]
        return acc, num_char

    def string_to_64hash(self, string):
        """
        :param string: Unicode string (text) to be hashed
        :return: a hashed  string of length 64
        """
        
        acc, num_char = self._process(string)
        return self._hexdigest(self._compute_digest(acc=acc, num_char=num_char))

if __name__ == "__main__":
    hash_generator = Hash64()
    print(list(hash_generator.string_to_64hash("All work and no play made Hossein a dull boy")))
    print(list(hash_generator.string_to_64hash("All work and no play made Hossein a dull boy / ")))
