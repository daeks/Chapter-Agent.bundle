import hashlib, os, time

def Start():
  pass
  
def ValidatePrefs():
  pass

class ChapterAgent(Agent.Movies):

  name = 'Chapter Agent'
  languages = [Locale.Language.NoLanguage]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.none']

  def search(self, results, media, lang):

    results.Append(MetadataSearchResult(id = media.id, name = media.name, year = None, score = 100, lang = lang))

  def update(self, metadata, media, lang):

    part = media.items[0].parts[0]
    path = os.path.dirname(part.file)
    (root_file, ext) = os.path.splitext(os.path.basename(part.file))
    
    if Prefs['input'].strip() == 'edl':
      if os.path.isfile(os.path.join(path, root_file + '.edl')):
        data = Core.storage.load(os.path.join(path, root_file + '.edl'))
        
        duration = int(long(getattr(media.items[0].parts[0], 'duration')))
        Log('Duration is %s' % self.toTime(int(round(float(getattr(media.items[0].parts[0], 'duration')) / 1000))))
        metadata.chapters.clear()
        
        offset = 0
        cindex = 1
        ncindex = 1
        for line in data.splitlines():
          parts = line.split('	')
          start = self.toTime(int(round(float(parts[0]))))
          end = self.toTime(int(round(float(parts[1]))))
          
          if Prefs['commercial']:
            if offset > 0:
              chapter = metadata.chapters.new()
              chapter.title = 'Chapter %d' % ncindex
              chapter.start_time_offset = offset
              chapter.end_time_offset = int(round(float(parts[0]) * 1000))
              offset = 0
              ncindex += 1
            
            if cindex == 1:
              if float(parts[0]) > 0.0:
                chapter = metadata.chapters.new()
                chapter.title = 'Chapter %d' % ncindex
                chapter.start_time_offset = offset
                chapter.end_time_offset = int(round(float(parts[0]) * 1000))
                offset = 0
                ncindex += 1
            
          chapter = metadata.chapters.new()
          if Prefs['commercial']:
            chapter.title = 'Commercial %d' % cindex
          else:
            chapter.title = 'Chapter %d' % cindex
          chapter.start_time_offset = int(round(float(parts[0]) * 1000))
          chapter.end_time_offset = int(round(float(parts[1]) * 1000))
          offset = int(round(float(parts[1]) * 1000))
          cindex += 1
          
          Log('Found chapter at %s - %s' % (start, end))
        
        if Prefs['commercial']:
          if offset > 0:
            if offset < duration:
              chapter = metadata.chapters.new()
              chapter.title = 'Chapter %d' % ncindex
              chapter.start_time_offset = offset
              chapter.end_time_offset = duration
           
        Log('Chapters loaded for %s' % root_file)
      else:
        metadata.chapters.clear()
        Log('Chapters cleared for %s' % root_file)
        
    if Prefs['input'].strip() == 'dvrmstb':
      if os.path.isfile(os.path.join(path, root_file + '.xml')):
        data = Core.storage.load(os.path.join(path, root_file + '.xml'))
        xml_data = XML.ElementFromString(data)
        
        duration = int(long(getattr(media.items[0].parts[0], 'duration')))
        Log('Duration is %s' % self.toTime(int(round(float(getattr(media.items[0].parts[0], 'duration')) / 1000))))
        metadata.chapters.clear()
        
        offset = 0
        cindex = 1
        ncindex = 1
        for region in xml_data.xpath('//commercial'):
          start = self.toTime(int(round(float(region.attrib['start']))))
          end = self.toTime(int(round(float(region.attrib['end']))))
          
          if Prefs['commercial']:
            if offset > 0:
              chapter = metadata.chapters.new()
              chapter.title = 'Chapter %d' % ncindex
              chapter.start_time_offset = offset
              chapter.end_time_offset = int(round(float(region.attrib['start']) * 1000))
              offset = 0
              ncindex += 1
            
            if cindex == 1:
              if int(round(float(region.attrib['start']))) > 0:
                chapter = metadata.chapters.new()
                chapter.title = 'Chapter %d' % ncindex
                chapter.start_time_offset = offset
                chapter.end_time_offset = int(round(float(region.attrib['start']) * 1000))
                offset = 0
                ncindex += 1
            
          chapter = metadata.chapters.new()
          if Prefs['commercial']:
            chapter.title = 'Commercial %d' % cindex
          else:
            chapter.title = 'Chapter %d' % cindex
          chapter.start_time_offset = int(round(float(region.attrib['start']) * 1000))
          chapter.end_time_offset = int(round(float(region.attrib['end']) * 1000))
          offset = int(round(float(region.attrib['end']) * 1000))
          cindex += 1
          
          Log('Found chapter at %s - %s' % (start, end))
        
        if Prefs['commercial']:
          if offset > 0:
            if offset < duration:
              chapter = metadata.chapters.new()
              chapter.title = 'Chapter %d' % ncindex
              chapter.start_time_offset = offset
              chapter.end_time_offset = duration
           
        Log('Chapters loaded for %s' % root_file)
      else:
        metadata.chapters.clear()
        Log('Chapters cleared for %s' % root_file)
      
  def toTime(self, seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))
    
  def bts(self, duration, totalbytes, bytes):
    if bytes == 0.0:
      return int(bytes)
    else:
      bytes_per_ms = round(totalbytes / duration)
      ms = bytes / bytes_per_ms
      return int(round(ms))

  def dump(self, obj):
    for attr in dir(obj):
      Log('obj.%s = %s' % (attr, getattr(obj, attr)))