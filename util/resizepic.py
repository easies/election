import os
from PIL import Image

def resize_pic(src, dst, size):
  try:
    image = Image.open(src)
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(dst)
    os.chmod(dst, 0770)
  except:
    return False 
  
  return True

def rename_image(src, username):
  file_ext = os.path.splitext(src)[1].lower().replace('jpg', 'jpeg')
  dst = 'election_profiles/%s%s' % (username, file_ext)
  return dst

