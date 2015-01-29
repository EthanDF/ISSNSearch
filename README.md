# ISSNSearch
## a script I wrote that leverages MarcEdit to find the "best" matching OCLC record within a set of downloaded records.

The problem that led to this script was that we get these big lists of ISSNs from serials vendors. There isn't really a good way to find catalog records for these ISSNs. So after ruling out a number of the records as already being in our catalog, we're left with a list of ISSNs for which I need to go find OCLC records. 

Instead of doing this one at a time, I can use (MarcEdit)[http://marcedit.reeset.net/] to download all of the matching OCLC records based on the ISSNs. Then, this script will use that downloaded list to find the best match.

Best match is defined by the following heuristics/assumptions:
- The record should be electronic (008[23] = 'o' or 's')
- The record should be described in English (040$b = 'eng')
- **The record with the most current holdings is the best unless...**
- the difference between amount held is less than 20 (eg record A has 120 holdings but record B has 101, go to tie-breaker)
- tie breaker is the sum of the following categories with each worth a point:
  - record is RDA (040$e)
  - record contains an 050 LCC value

The script will also take in the URL provided by the vendor and replace any 856 values with the provided URL. It logs the OCLC value found as the best record.

There is a known issue with it not handling encoding correctly so it will print when that happens and then you'll manually need to add the record to the file (or use MarcEdit)

To run you'll need to set the location of:
- mrcFile: the file with the downloaded OCLC records
- inputFile: the ISSNs that your passing. 
  - the first column should be the titles (or anything really)
  - the second column should be the ISSNs (####-####)
  - the third column should be the URLs
- outFile: the location of the logging for found OCLC records (will log None if no record is found)
- issnResults: the .mrc output of the found OCLC records

To run pass runISSN(None,None)
- first parameter allows a test ISSN
- if passing the first parameter, pass the test URL as well in the second parameter
- runISSN(None, None) runs the script using the provided files

Note that you'll still have to do some cleanup with MarcEdit of the downloaded files, but that part is beyond the scope of this script. 


 
  
