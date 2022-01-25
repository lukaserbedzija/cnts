from threading import Thread


has_stopped = True


def unit_stopped(fn):
  def fn_wrapper():
    global has_stopped

    has_stopped = False

    while not has_stopped:
      fn()

  return Thread(target=fn_wrapper).start()


def stop_all():
  global has_stopped
  
  has_stopped = True