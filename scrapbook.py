class TextAnalyzer(object):

    def __init__(self, text):
        # remove punctuation
        clean_text = text.replace('.', '').replace('!', '').replace(',', '').replace('?', '')
        # make text lowercase
        lower_text = clean_text.lower()
        self.fmtText = lower_text

    def freqAll(self):
        # split text into words
        words = self.fmtText.split()
        # Create dictionary
        dict = {}
        for word in words:
            dict[word] = words.count(word)
        print(dict)
        return dict

    def freqOf(self, word):
        # get frequency map
        dict = self.freqAll()
        if word in dict:
            return dict[word]
        else:
            return "No such word in the text."

ta1 = TextAnalyzer("Accomplished financial professional with over 20 years of experience in credit trading, portfolio management, \n"
                   "and risk management within global fixed income capital markets. Expertise spans buy- and sell-side roles, employing long/short, \n"
                   "long-only, algorithmic, and discretionary strategies. Deep understanding of market macro- and micro-structure. \n"
                   "Proven track record of building scalable, profitable businesses with an ownership mindset. Skilled in leading small teams \n"
                   " of traders and analysts, fostering collaboration, and managing stakeholder relationships to drive success in fixed income trading environments.")

print(ta1.freqOf("barbarous"))







