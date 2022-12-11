## Breakdown
If it is not blatantly obvious (to a human who is not you), please indicate where in your source code the evaluation happens, including where the per-query scores and overall average scoring are handled.
- Per-query scores calculated on ```line 93 -> line 115```
  - Each per-query score is added to a total count when calculated
  - After every query has been evaluated and written to file, divide totals by num queries and write on ```line 126 -> line 133```
  - Helper functions on ```line 50 -> line 76```

## Description 
Provide a description of system, design tradeoffs, etc., that you made.
- Reading input files
  - Using query relevance document, create 3 dicts
    - **ideal_rank**: map query to list of (docid,skip,relevance), initially unsorted, sort at ```line 95```
    - **total_rel**: map query to number of relevant documents
    - **relevance**: map query + docid to relevance of that document to that query
  - From query results, create 3 dicts
    - **only_rel**: only the relevant documents returned by a query
    - **queries**: map query to a list of results
    - **ap**: map query to its average precision
- Helper functions
  - **get_dcg**: calculate dcg of list of documents, if input is ideal ranking, produces IDCG
  - **precision**: calculate precision of list of documents, given a number of docs k
  - **recall**: calculate recall of list of documents, given the query name

## Libraries 
List the software libraries you used, and for what purpose. Implementation must be your own work. If you are thinking of using any other libraries for this assignment, please send us an email to check first.
- sys: allowing custom input
- os: create output files
- defaultdict: make creating inverse index and posting lists easier
- math: calculate dcg

## Dependencies
Provide instructions for downloading dependencies of the code. Not expecting anything here.
- Python version >= 3.9.13

## Building 
Provide instructions for building the code.
- Download the code
- Make sure Python version >= 3.9.13

## Running
Provide instructions for running the code
- CD into the directory which contains ```eval.py```
- In terminal, run the command "python eval.py" followed by optional args: ```"inputFile" "queryRel" "outputFile"```
