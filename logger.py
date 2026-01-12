import logging


#------------------------------------------------------------------------------
class Logger(object):
  '''
    logfile=None,          file_only=True   ---> logging goes to stdout
    logfile=None,          file_only=False  ---> logging goes to stdout
    logfile='default.log', file_only=True   ---> logging goes to 'default.log'
    logfile='default.log', file_only=False  ---> logging goes to both 
  '''
  def __init__(me, name, level=logging.INFO, logfile=None, file_only=False):
    me.logger = logging.getLogger(name)
    me.logger.setLevel(level)
    formatter = logging.Formatter('%(levelname)-5s | %(message)s')
    me.lines = {}

    if not file_only:
      me.stream_logger = logging.StreamHandler()
      me.stream_logger.setLevel(level)
      me.stream_logger.setFormatter(formatter)
      me.logger.addHandler(me.stream_logger)

    if logfile is not None:
      me.file_logger = logging.FileHandler(logfile)
      me.file_logger.setLevel(level)
      me.file_logger.setFormatter(formatter)
      me.logger.addHandler(me.file_logger)

  def d(me, msg):
    me.logger.debug(msg)

  def i(me, msg):
    me.logger.info(msg)

  def w(me, msg):
    me.logger.warning(msg)

  def e(me, msg):
    me.logger.error(msg)

  def c(me, msg):
    me.logger.critical(msg)

