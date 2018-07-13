import re

class TextWorker(object):

    def __init__(self):
        self.multSpace = re.compile(r'\s\s+')
        self.startSpace = re.compile(r'^\s+')
        self.endSpace = re.compile(r'\s+$')
        self.multDots = re.compile(r'\.\.\.\.\.+')
        self.newlines = re.compile(r'\s*\n\s*')
        self.handle = re.compile(r"(?<![A-Za-z0-9_!@#\$%&*])@(([A-Za-z0-9_]){20}(?!@))|(?<![A-Za-z0-9_!@#\$%&*])@(([A-Za-z0-9_]){1,19})(?![A-Za-z0-9_]*@)")
        self.url = re.compile(r"http\S+")
    
    def shrinkSpace(self, text):
        """
        Turns multiple spaces into 1
        """
        text = self.multSpace.sub(' ', text)
        text = self.multDots.sub('....', text)
        text = self.endSpace.sub('', text)
        text = self.startSpace.sub('', text)
        text = self.newlines.sub(' <NEWLINE> ', text)
        return text
    
    def remove_handles(self, text):
        """
        Remove Twitter username handles from text
        """
        text = self.handle.sub('<USER>', text)
        return text
    
    def remove_urls(self, text):
        """
        Remove URLs from text
        """
        text = self.url.sub('<URL>', text)
        return text

    


