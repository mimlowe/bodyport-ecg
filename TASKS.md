# Senior Software Engineer - Programming Assignment
### Expected Duration: 4-6 hours

Your task is to build a web application which can compress an ECG signal. You may use whatever
programming language you are comfortable with, but Python is strongly recommended. The attached
`sample_ecg_raw.bin` file contains ECG data for you to test with.


Please ensure all the requirements are met. Your submission will be evaluated on performance, code quality,
and clarity of documentation.

## Requirements

- Allow a user to upload a binary ECG file ✅
- Include a button to initiate compression ✅
- Once compression is complete, display the following:
  - original file size ✅
  - compressed file size ✅
  - compression ratio ✅
  - a button to download the compressed file ✅
- Implement a lossless compression algorithm ✅
- You must not use a compression library ✅
- You may use your choice of web frameworks and/or libraries

## Required Deliverables
- Source code for your web application ✅
- Documentation including
  - instructions to run your application
  - design considerations and key decisions
  - the specifications of your compression algorithm
  
### ECG Data Structure
`sample_ecg_raw.bin`: 4095 samples of Signed Int 24 bit values (3 bytes each).

### Hints
- You may want to use the Construct library for parsing (https://construct.readthedocs.io/en/latest/)
- Consider plotting the data before implementing your compression algorithm. Huffman coding is the
standard, but there are simpler methods that could be suitable given the nature of the data