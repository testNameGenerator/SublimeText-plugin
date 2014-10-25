import sublime, sublime_plugin, re

class ConvertTestNameCommand(sublime_plugin.TextCommand):
    def isAllowedSyntax(self, syntax):
        return ((syntax == "PHP") | (syntax == "JavaScript"))

    # keep only alphanum and ",", ".", "(", ")"
    def getCleanLineContents(self, lineContents):
        pattern = TextHelper.patternCleanLine()
        return re.sub(pattern, '', lineContents)

    def getFallbackLineContent(self, i):
        return "blank" + str(i)

    # convert to CamelCase and keep only alphanumeric chars
    def getMethodName(self, lineContents):
        pattern = TextHelper.patternMethodName()
        return re.sub(pattern, '', lineContents.title())

    def getExistingMethod(self, lineContents, cursorLine):
        pageContents   = SublimeConnect.getPageContents(cursorLine)
        lineContents   = re.escape(lineContents)
        pattern        = TextHelper.patternExistingMethodPHP(lineContents)

        searchExisting = re.search(pattern, pageContents)
        if searchExisting != None:
            if (searchExisting.group(7) is None) == False:
                return searchExisting.group(7)
        return False

    # get a list of [test name with separate words, test name with no spaces in between and camel cased] from the current cursor(s) or selection(s)
    def run(self, edit):
        SublimeConnect.init(self)
        currentSyntax      = SublimeConnect.getSyntax()
        extractedTestNames = []
        
        if False == self.isAllowedSyntax(currentSyntax):
            return

        i = 0
        for cursor in SublimeConnect.getCursors():
            cursorLine   = SublimeConnect.getLine(cursor)
            lineContents = SublimeConnect.getLineContents(cursorLine)
            phrase       = self.getCleanLineContents(lineContents)

            # if extracted line contents are empty, use "blank"
            if not phrase:
                phrase = self.getFallbackLineContent(i)
                i += 1

            if (currentSyntax == "PHP"):
                methodName     = self.getMethodName(phrase)
                existingMethod = self.getExistingMethod(lineContents, cursorLine)
                print(existingMethod)

                if existingMethod == False:
                    SublimeConnect.insertMethodName(edit, cursorLine, TextHelper.prepareTestBlockPHP(phrase, methodName))
                else:
                    SublimeConnect.updateMethodNamePHP(edit, cursorLine, methodName, existingMethod)

            else:
                # JS will add a new test method because the text is inside the test method
                SublimeConnect.insertMethodName(edit, cursorLine, TextHelper.prepareTestBlockJS(phrase))

class TextHelper():
    def patternExistingMethodPHP(lineContents):
        # complete block: return r'\/\*([\*\n\s]+)' + lineContents + '([a-zA-Z0-9\n\s\*@]+)\*\/([\s]+)(public)?(\s)?function(\s)?test([a-zA-Z0-9_]+)(\s\n)?\('
        return r'([\*\n\s]+)' + lineContents + '([a-zA-Z0-9\n\s\*@]+)\*\/([\s]+)(public)?(\s)?function(\s)?test([a-zA-Z0-9_]+)(\s\n)?\('

    def patternCleanLine():
        return r'[^a-zA-Z0-9 \(\)_\:\.\,\[\]]'

    def patternMethodName():
        return r'[^a-zA-Z0-9_]'

    def prepareTestBlockPHP(phrase, methodName):
        tab = SublimeConnect.getWhitespaceTab()
        return tab + "/**\n" + tab + " * " + phrase + "\n" + tab + " */\n" + tab + "public function test" + methodName + "()\n" + tab + "{\n\n" + tab + "}\n\n" + tab

    # will generate Jasmine blocks
    def prepareTestBlockJS(phrase):
        tab                  = SublimeConnect.getWhitespaceTab()
        examineNameTypeParts = phrase.split(" ")

        if (examineNameTypeParts[0].lower() == "describe"):
            phrase = " ".join(examineNameTypeParts.pop(0)) # remove the "describe" prefix
            return self.getJasmineDescribeBlock(phrase, tab)

        else:
            return self.getJasmineItBlock(phrase, tab)

    def getJasmineDescribeBlock(phrase, tab):
        return tab + "describe('" +  phrase + "', function () {\n\n" + tab + "});\n\n" + tab

    def getJasmineItBlock(phrase, tab):
        return tab + tab + "it('" + phrase + "', function () {\n\n" + tab + "" + tab + "});\n\n" + tab

# connector to the sublime api
class SublimeConnect():
    context = False

    @classmethod
    def getPageContents(self, cursorLine):
        cursorPosition = cursorLine.begin()
        return self.context.view.substr(sublime.Region(0, self.context.view.size()))

    @classmethod
    def updateMethodNamePHP(self, edit, cursorLine, methodName, existingMethodResults):
        tab            = SublimeConnect.getWhitespaceTab()
        searchExisting = "test" + existingMethodResults # search for current test name
        methodPosition = self.getPageContents(cursorLine).find(searchExisting)
        region         = sublime.Region(methodPosition, methodPosition + len(searchExisting))
        # debug: self.context.view.add_regions('highlighted_lines', [region] , 'mark', 'dot', sublime.DRAW_OUTLINED) 

        lineToUpdate   = self.context.view.line(region)
        lineContents   = self.context.view.substr(lineToUpdate).strip().replace(searchExisting, "test" + methodName)
        
        self.context.view.replace(edit, lineToUpdate, tab + lineContents)

    @classmethod
    def insertMethodName(self, edit, cursorLine, testBlock):
        self.context.view.replace(edit, cursorLine, testBlock)

    @classmethod
    def getLine(self, region):
        return self.context.view.line(region)

    @classmethod
    def getLineContents(self, cursorLine):
        return self.context.view.substr(cursorLine).strip()

    @classmethod
    def getCursors(self):
        return self.context.view.sel()

    @classmethod
    def init(self, mainContext):
        self.context = mainContext
        return self
    
    # returns: PHP,JavaScript,...
    @classmethod
    def getSyntax(self):
        return self.context.view.settings().get('syntax').replace('.tmLanguage', '').split("/")[1]

    # returns tab character or spaces as an indent unit, based on the editor's settings
    @classmethod
    def getWhitespaceTab(self):
        settings = self.context.view.settings()
        if (settings.get('translate_tabs_to_spaces')):
            return "".rjust(settings.get('tab_size'), ' ')
        return "\t";
