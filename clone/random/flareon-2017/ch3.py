from distorm3 import Decode, Decode16Bits, Decode32Bits, Decode64Bits

from itertools import cycle, izip

def xor2(plaintext, key):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(plaintext, key))

def xor1(plaintext, key):
    return "".join(chr(ord(a) ^ ord(b)) for a, b in izip(plaintext, cycle(key)))

blob = "33E1C49911068116F0329FC49117068114F0068115F1C4911A06811BE2068118F2068119F106811EF0C4991FC4911C06811DE6068162EF068163F2068160E3C49961068166BC068167E6068164E80681659D06816AF2C4996B068168A9068169EF06816EEE06816FAE06816CE306816DEF068172E90681737C"
blob = blob.decode('hex')


for i in xrange(0x00, 0xFF):
  key = chr(i)
  blob = xor1(blob, key)

  blob2 = ""

  for char in blob:
    blob2 += chr((ord(char) + 0x22) % 256)

  # print blob2.encode('hex')

  dis = Decode(0x40107C, blob2, Decode32Bits)

  sizeOne = 0
  
  for (offset, size, instruction, hexdump) in dis:
    if (size == 1):
      sizeOne += 1

  if sizeOne < 10000:
    print "key: ", key.encode('hex')
    print "size one:", sizeOne

    for i in dis:
      print "0x%08x(%02x) %-20s %s" % (i[0],  i[1],  i[3],  i[2])

    print "\n --------------------- \n"