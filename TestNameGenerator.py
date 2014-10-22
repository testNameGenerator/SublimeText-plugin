# v0.1
import sublime, sublime_plugin, re

class ConvertTestNameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # get a list of [test name with separate words, test name with no spaces in between and camel cased] from the current cursor(s) or selection(s)
        extractedTestNames = []

        currentSyntax = self.getSyntax()
        if ((currentSyntax != "PHP") & (currentSyntax != "JavaScript")):
            return

        cursor = 0
        # iterate over all cursors
        for region in self.view.sel():
            # extract line contents from cursor(s)
            line = self.view.line(region)
            lineContents = self.view.substr(line).strip()

            # keep only alphanum and ",", ".", "(", ")"
            testNameExpanded = re.sub(r'[^a-zA-Z0-9 \(\)_\:\.\,\[\]]', '', lineContents).strip()

            # if extracted line contents are empty, use "blank"
            if not testNameExpanded:
                testNameExpanded = "blank"
                if cursor > 0:
                    testNameExpanded += str(cursor)
                cursor += 1

            # convert to CamelCase and keep only alphanumeric chars
            testNameContracted = testNameExpanded.title()
            testNameContracted = re.sub(r'[^a-zA-Z0-9_]', '', testNameContracted)

            # replace current line
            self.view.replace(edit, line, self.prepareTestContent(testNameExpanded, testNameContracted, currentSyntax))

    def prepareTestContent(self, testNameExpanded, testNameContracted, languageSyntax):
        returnContent = ""

        tab = self.getWhitespaceTab()

        if (languageSyntax == "PHP"):
            returnContent = tab + "/**\n" + tab + " * " + testNameExpanded + "\n" + tab + " */\n" + tab + "public function test"+testNameContracted+"()\n" + tab + "{\n\n" + tab + "}\n\n" + tab

        elif (languageSyntax == "JavaScript"):
            # will generate Jasmine blocks
            examineNameTypeParts = testNameExpanded.split(" ")

            if (examineNameTypeParts[0].lower() == "describe"):
                examineNameTypeParts.pop(0) # remove the "describe" prefix
                returnContent = tab + "describe('"+ (" ".join(examineNameTypeParts)) +"', function () {\n\n" + tab + "});\n\n" + tab
            else:
                returnContent = tab + tab + "it('"+testNameExpanded+"', function () {\n\n" + tab + "" + tab + "});\n\n" + tab

        return returnContent

    def getWhitespaceTab(self):
        if (self.view.settings().get('translate_tabs_to_spaces')):
            return "".rjust(self.view.settings().get('tab_size'), ' ')
        return "\t";

    def getSyntax(self):
        return self.view.settings().get('syntax').replace('.tmLanguage', '').split("/")[1]