Will convert plain text task/message into a test method, using the plain text as a comment for readability.

Uses the file's syntax to choose between PHPUnit syntax (for PHP files) or Jasmine's "describe" and "it" blocks (for JavaScript).
If the syntax is not PHP or JavaScript, no updates will be applied to the file.

Uses the editor's whitespace indent settings. If the cursor line is empty then use "blank" as the original phrase.<br/>
If the original phrase is inside a dockblock then it updates the method using the same pattern as when inserting a new test method.

Install
-----
Install by downloading the [1.0.1 release zip](https://github.com/bogdananton/Sublime-testNameGenerator/releases/download/1.0.1/testNameGenerator.zip) and unpacking it into the \Packages folder (SublimeText Menu \ Preferences \ Browse Packages).

Usage
-----
   * Write at least a test name in plain text, using spaces between words
   * Place cursor in the line(s) containing the test name(s)
   * Press `Ctrl+Shift+u` to convert the line(s) into test(s)

For JavaScript, the default action will be to create a Jasmine "it" block. Add "describe " as a prefix to the string to create a "describe block".

Limitations
-----
Only supports PHPUnit syntax and Jasmine (describe and it blocks), for now.

TODO: context menu for selecting different languages / syntaxes

Preview
-----
PHP<br/>
![](https://raw.githubusercontent.com/bogdananton/Sublime-testNameGenerator/master/preview.png)

JavaScript<br/>
![](https://raw.githubusercontent.com/bogdananton/Sublime-testNameGenerator/master/preview-jasmine.png)

Check out the [PhpStorm](https://github.com/bogdananton/PhpStorm-testNameGenerato) or [Eclipse](https://github.com/sorinstanila/Eclipse-testNameGenerator) versions of the plugin.
