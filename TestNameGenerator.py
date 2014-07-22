# v0.1
import sublime, sublime_plugin, re

class ConvertTestNameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # get a list of [test name with separate words, test name with no spaces in between and camel cased] from the current cursor(s) or selection(s)
        extractedTestNames = []

        # iterate over all cursors
        for region in self.view.sel():
            # extract line contents from cursor(s)
            line = self.view.line(region)
            lineContents = self.view.substr(line).strip()

            # clear non-alpha and non-space chars
            testNameExpanded = re.sub(r'[^a-zA-Z0-9 \(\)]', '', lineContents).strip()

            # if extracted line contents are not empty, add them to stack
            if (testNameExpanded):
                # convert to CamelCase
                testNameContracted = testNameExpanded.title().replace(" ", "").replace("(", "").replace(")", "")

                # replace current line
                self.view.replace(edit, line, self.prepareTestContent(testNameExpanded, testNameContracted))

    def prepareTestContent(self, testNameExpanded, testNameContracted):
        return """    /**
     * """+testNameExpanded+"""
     */
    public function test"""+testNameContracted+"""()
    {

    }
    """