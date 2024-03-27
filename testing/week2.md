# Week 2 Testing Questions

### Select a number of testable functions from the code of your application, or features from the application to be tested with the input domain modeling. Make sure to have a good reason for your selection.
The tests.py file contains functions we will be testing. The functions are:
`toint32`, `sign_extend_24bit`, `sign_extend_2bit`, `_trycast`.
The reason for these choices is there ability to be tested with known domain inputs.

[//]: # (~~ If we decide to do more:)
[//]: # (context.py has the following functions:)
[//]: # (`add_frame`, `get+past_value`, `count_skipped_frames` which all have a return value and can be tested with known domain inputs. ~~)

### List all of the input variables for the selected set of functions.
#### toint32(), sign_extend_24bit(), sign_extend_2bit(), _trycast()
- positive integer
- negative integer
- overflow integer
- zero
- string
- float
- None

#### add_frame(), get_past_value()
- Frame
- integer
- string
- None

count_skipped_frames()
- self?

### Define the characteristics of the input variables. Make sure you cover all input variables.

### Partition the characteristics into blocks.
- Numbers
- Non-numeric valid inputs
- Invalid inputs
- None

### Define values for each block.

#### Numbers
-1, 0, 1, 2^31, 2^32, 2^24, 2^2, 2.0, 0.0

[//]: # (NOt sure Valid is the right word here)
#### Non-numeric valid inputs
"1", "number", true

#### Invalid inputs

[//]: # (This made sense when I wrote it, but now I can't think of what this would be.)

#### None
None

### Select the coverage criteria.
Function coverage for all but _trycast() which will be tested with branch coverage.

### Define a test set that satisfies the selected coverage criteria.

### Execute the test cases on the application and report the results.


