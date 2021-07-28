# earsketch-curriculum
Curriculum source files for the EarSketch project (https://earsketch.gatech.edu)

To build locally for development:

```shell
cd /path/to/earsketch-curricilum
./scripts/local_dev_curriculum_asciidoc_builder.sh /path/to/earsketch-curricilum
```

## For Authors
Here is a reference for question formatting in `asciidoc`

Here is the most basic question format:
```asciidoc
[question]
--
Which of these options is a string?
[answers]
* "Five"
* 5
* FIVE
* Five
--
```

If a question needs to be language-specific (python or javascript), prepend the question block with the same `[role="curriculum-javascript"]` block used in the rest of the curriculum for language-specific content. 

```asciidoc
[role="curriculum-python"]
[question]
--
Which of these options correctly defines the function `myFunction()` with the parameters `startMeasure` and `endMeasure` ?
[answers]
* `def myFunction(startMeasure, endMeasure):`
* `def myFunction():`
* `myFunction(startMeasure, endMeasure):`
* `myFunction(2, 5)`
--

[role="curriculum-javascript"]
[question]
--
Which of these options correctly defines the function `myFunction()` with the parameters `startMeasure` and `endMeasure` ?
[answers]
* `function myFunction(startMeasure, endMeasure) {}`
* `function myFunction() {}`
* `myFunction(startMeasure, endMeasure){}`
* `myFunction(2, 5)`
--
```

These examples show how do include a code sample at the top of the question.
```asciidoc
[role="curriculum-javascript"]
[question]
--
What does 0 represent in a beat pattern string?
[source,javascript]
----
// here is javascript some code
makeBeat(2, "000-00000-000--0");
----
[answers]
* Start playing the clip
* Rest
* Extend the clip
* End the clip
--

[role="curriculum-python"]
[question]
--
What does 0 represent in a beat pattern string?
[source,python]
----
# here is some python code
makeBeat(2, "000-00000-000--0")
----
[answers]
* Start playing the clip
* Rest
* Extend the clip
* End the clip
--
```