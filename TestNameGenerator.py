# v0.1
import sublime, sublime_plugin, re

class ConvertTestNameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # get a list of [test name with separate words, test name with no spaces in between and camel cased] from the current cursor(s) or selection(s)
        extractedTestNames = []

        currentSyntax = self.getSyntax()
        if ((currentSyntax != "PHP") & (currentSyntax != "JavaScript")):
            return

        # iterate over all cursors
        for region in self.view.sel():
            # extract line contents from cursor(s)
            line = self.view.line(region)
            lineContents = self.view.substr(line).strip()

            # keep only alphanum and ",", ".", "(", ")"
            testNameExpanded = re.sub(r'[^a-zA-Z0-9., \(\)]', '', lineContents).strip()

            # if extracted line contents are not empty, add them to stack
            if (testNameExpanded):
                # convert to CamelCase and keep only alphanumeric chars
                testNameContracted = testNameExpanded.title()
                testNameContracted = re.sub(r'[^a-zA-Z0-9]', '', testNameContracted)

                # replace current line
                self.view.replace(edit, line, self.prepareTestContent(testNameExpanded, testNameContracted, currentSyntax))

    def prepareTestContent(self, testNameExpanded, testNameContracted, languageSyntax):
        returnContent = ""

        if (languageSyntax == "PHP"):
            returnContent = "    /**\n     * "+testNameExpanded+"\n     */\n    public function test"+testNameContracted+"()\n    {\n\n    }\n    "

        elif (languageSyntax == "JavaScript"):
            # will generate Jasmine blocks
            examineNameTypeParts = testNameExpanded.split(" ")

            if (examineNameTypeParts[0].lower() == "describe"):
                examineNameTypeParts.pop(0) # remove the "describe" prefix
                returnContent = "    describe('"+ (" ".join(examineNameTypeParts)) +"', function () {\n\n    });\n    "
            else:
                returnContent = "        it('"+testNameExpanded+"', function () {\n\n        });\n    "

        return returnContent

    def getSyntax(self):
        return self.view.settings().get('syntax').replace('.tmLanguage', '').split("/")[1]