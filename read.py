import os
import sys
import traceback
import socket
import urllib
import urllib2
import time
import logging
import logging.handlers

from Secrets import * 

sampledelay = 6
restartsocketsamplecount = (60*60)/sampledelay

url = 'https://io.adafruit.com/api/feeds/glass/data'

# values3 = {'value' : 35.0}
# data3 = urllib.urlencode(values3)
# req3 = urllib2.Request(url, data3)
# req3.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
# req3.add_header('x-aio-key',aiokey)

# response3 = urllib2.urlopen(req3)

startTimeStr = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())


my_logger = logging.getLogger('OmegaReader')
my_logger.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/var/run/syslog') #on mac /var/run/syslog, on unix /dev/log

my_logger.addHandler(handler)

my_logger.debug('this is debug')
my_logger.info('this is info')
my_logger.critical('this is critical')

def adafruitIoClient():
  print "starting up!"
  print startTimeStr
  print "-----------\n"
  my_logger.critical("STARTING ADAFRUIT IO CLIENT FOR GLASS")
  my_logger.critical(startTimeStr)


  try:
    samples = 0
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect(("10.1.10.95", 2000))

        i = 0
        # last = time.time()
        while i<restartsocketsamplecount: #about an hour ?
          s.send(b'*X01\r')
          r = s.recv(4096)

          val = r[3:]
          data = urllib.urlencode( {'value' : float(val)})
          req = urllib2.Request(url,data)
          req.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
          req.add_header('x-aio-key',aiokey)

          timeNowStr = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())

          sampleData = 's: %d, i: %d' % (samples,i)

          print timeNowStr
          print r
          print val
          print startTimeStr
          print sampleData
          print "\n"

          my_logger.critical(r)
          my_logger.critical(sampleData)

    #      print 'r:' + r + ' val:' + val + ' samples:' + str(samples) + ' i:' + str(i)
          # now = time.time()
          # print 1.0/(now - last)
          # last = now

          response = urllib2.urlopen(req)

          print 'Response Start'
          print response
          print 'Response End'

          time.sleep(sampledelay)
          i = i + 1
          samples = samples + 1

  except KeyboardInterrupt:
        print "Quitting, because you asked"
        s.close()
        sys.exit() # or quit() ??
  except:
    print "There was an exception!"
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    exceptionString = traceback.format_exc()
    my_logger.critical('EXCEPTION')
    my_logger.critical(exc_type)
    my_logger.critical(exc_value)
    my_logger.critical(exceptionString)
    print "Waiting 30 seconds"
    s.close()

    time.sleep(30)

if __name__ == '__main__':
  adafruitIoClient()
  # os.execv(__file__, sys.argv)
  os.execv(sys.executable, ['python'] + sys.argv)