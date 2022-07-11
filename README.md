# handy-plotter

A collection of python scripts to create the types of plots Ciberseguros most commonly needs from data types we most often collect.

## How to use

Take a look at the test cases to see how to use each function in more detail following is an overview of each plot type supported:

## Plot Likert Scale Data

![Sample Likert Scale Visualization](https://github.com/ciberseguros/handy-plotter/raw/main/tests/static/likert_test_instance.png)

    plot_likert_scales(rows, scale, outfile, row_labels=None)

`rows` must be a list of lists where rows are respondents and columns are questions.
Each cell contains a string like `"Strongly Disagree"` from the scale. Elements here are case insensitive.

    data = [
            ["Agree", "agree", "disagree"],
            ["Strongly Agree", "Neutral", "StronGLY DISAGREE"],
            ["Agree", "strongly Disagree", "agree"],
            ["Strongly Disagree", "Disagree", "Neutral"]
        ]

`scale` is a list of strings (in order) to display in the bars. These will also be the values shown. e.g.,

    ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]

By default, rows are labeled Q1, Q2, etc. You can specify different strings by putting them into `row_labels`

This visualization is from Nathan Malkin, a postdoc at U Maryland. See https://github.com/nmalkin/plot-likert 