# Report Apriori Assigment


# ALL MEASUREMENTS DONE ON MAC M1 2020 SEQUOIA 15.0

## Data Exploration

We hebben voor de data exploratie 5 technieken gebruikt, de 2 die gegeven waren en nog 3 anderen:

- Amount of Publications
- Average Amount of Authors Per Paper
- Unique Authors
- Average Paper per Author
- Papers per author (te veel voor in een tabel te weergeven)


### Dataset Tiny

| DataExploration Technique  | Result                |
|----------------------------|----------------------|
| Amount of Publications     | 629             |
| Average Amount of Authors Per Paper  | 3.31637519872814    |
| Unique Authors             | 290            |
| Average Paper per Author   | 2.168965517241379    |

### Dataset Medium

#### Medium 1

| DataExploration Technique  | Result                |
|----------------------------|----------------------|
| Amount of Publications     | 22,779             |
| Average Amount of Authors Per Paper  | 3.467140787567496    |
| Unique Authors             | 14,885            |
| Average Paper per Author   | 1.5303325495465234    |

#### Medium 2

| DataExploration Technique  | Result                |
|----------------------------|----------------------|
| Amount of Publications     | 21,092              |
| Average Amount of Authors Per Paper  | 4.006447942347809    |
| Unique Authors             | 17,707            |
| Average Paper per Author   | 1.1911673349522787    |



### Dataset LARGE

| DataExploration Technique  | Result                |
|----------------------------|----------------------|
| Amount of Publications     | 2,004,723              |
| Average Amount of Authors Per Paper | 3.0292613992057755    |
| Unique Authors             | 1,258,951            |
| Average Paper per Author   | 1.59237571597306    |

### Dataset ALL

| DataExploration Technique  | Result                |
|----------------------------|----------------------|
| Amount of Publications     | 7,142,501            |
| Average Amount of Authors Per Paper | 3.381567324946822    |
| Unique Authors             | 3,658,503            |
| Average Paper per Author   | 1.952301528794701    |

### Combined Data Exploration Table

| DataExploration Technique           | Tiny                 | Medium 1             | Medium 2             | Large                | All                  |
|-------------------------------------|----------------------|----------------------|----------------------|----------------------|----------------------|
| Amount of Publications              | 629                  | 22,779               | 21,092               | 2,004,723            | 7,142,501            |
| Average Amount of Authors Per Paper | 3.31637519872814     | 3.467140787567496    | 4.006447942347809    | 3.0292613992057755   | 3.381567324946822    |
| Unique Authors                      | 290                  | 14,885               | 17,707               | 1,258,951            | 3,658,503            |
| Average Paper per Author            | 2.168965517241379    | 1.5303325495465234   | 1.1911673349522787   | 1.59237571597306     | 1.952301528794701    |


## Implementation details

### Data exploration
We chose to use the `polars` library to load the file and store its rows. It is a faster alternative to the `pandas` framework.
We also used it in the implementation of the other algorithms to read and store the baskets from the file.
...

### Naive
The code starts in the `main.py` file where a loop iteratively calls `Naive.run(k)`. The `Naive` object will then
search for the most frequent itemset(s) of size k using a counter dictionary. It does 
this by going through each basket/row of the table and:
- Generating every combination of the current basket
- For each combination: 
    - if it is already in the counter dictionary, increase the count by one
    - if it is a new entry, add it to the dict and set the counter to 1

After all baskets have been looped through it looks for the highest count, and returns one of the elements
with this maximum count.


### Apriori

The code starts in the `main.py` file where while loop calls the generator of the Apriori implementation
and collects it's results. The reason we used a generator is because it makes it easier to collect to large `k`'s
because the next call to the generator can use the results of the previous results.

The `APriori.run(k)` method is the main entry point and is structured like this:

- Produce frequent singletons and yield one of the maximal ones.
- Produce frequent pairs and yield one of the maximal ones.
- Produce the rest of the fruquent itemsets and yield one of the maximal ones.

We chose to make seperate functions for cases k=1 and k=2. This way we can optimize them using some special properties.
Lets now discuss each part of our implementation: <br> 

**The general case for k > 2 (`Apriori.count()` and `Apriori.filter()`):** <br>
The 'original/naive' explanation of the a priori algorithm says that for each basket:
- Generate every combination of size k with the elements of the current basket
- For each one of these combinations:
    - Generate every combination of size k-1 of the
    - Check for each combination if they are frequent (using the data of the previous iteration)
    - If all combinations of size k-1 are frequent, then the set of size k is considered frequent and is added to the table (or has its count increased) <br>
- Filter the table to only contain elements that have a count higher than the given treshold

While this approach helps understand the algorithm, implementing it as described has several drawbacks. 
The main issue is that generating every possible combination of size k for each basket leads to a combinatorial explosion, especially when the number of items in the baskets is large. It becomes even slower when considering the  need to generate combinations of size k−1 for each k-sized candidate. The number of calculations grows exponentially with the number of items, causing performance to degrade rapidly.
Another problem with implementing it literally is that storing all combinations of size k and k−1 can require substantial (main) memory, particularly when dealing with large datasets. The need to repeatedly store combinations increases memory consumption and slows down the process due to frequent memory accesses. <br>

To address these issues efficiently we came up with the following approach:
1. We use two tables: `curr_map` for tracking the current frequent itemsets of size k, and `prev_map` for tracking the frequent itemsets of size k−1
2. We only consider baskets containing at least k items
3. We create a set `prev_frequents`, which includes every author who was frequent in iteration k-1
4. As we loop through each basket, we discard any item not present in `prev_frequents`. If the resulting basket has fewer than k items, it is ignored
5. We generate every combination of size k-1 from the filtered basket. If a combination is frequent (based on `prev_map`), we add its elements to a set `possible_candidates`. We now end up with a flat set that has **exactly** the elements that the frequent combinations of size k can exists of. This is also our main optimization: Unlike the naive approach, which generates combinations of size k and then checks their subsets of size k-1, we restrict ourselves to generating the sets in `prev_map` exist of the items in the current basket, resulting in fewer combinations, fewer condition checks, and reduced memory usage
6. Since we identified exactly which elements are in the sets of size k that are frequent, we only need to generate these combinations. If they are already in `curr_map` we increase the count by 1, otherwise we add them and set the count to 1 (note that we dont have any conditional checks in this step).
7. When we have looped through each basket, the final thing to do is to filter each item that has a count less then the given treshold in `curr_map`

**For pairs case (`Apriori.produce_frequent_pairs()`):** <br>
Pairs are a special case of the previously mentioned algorithm due to the following reasons:
- The previous iteration generates all frequent singletons (itemsets of size 1)
- The sets `prev_frequents` and `prev_map` contain elements with the same amount of dimensions, namely one.
- It is clear now that when k=2, steps 4 and 5 of the general algorithm essentially perform the same action: filtering the items in the current basket based on frequent singletons. As a result, we only need to perform either step 4 **or** step 5, but not both.

In our implementation, we chose to skip step 5 for this specific case, as step 4 alone is sufficient for generating frequent pairs.


**For singletons (`Apriori.produce_frequent_singletons()`):** <br>
To count the singletons in the dataset we use the `group_by()` function provided by polars.
It works perfectly for the k=1 case because we only count sets of size 1,
and by using the built in polars funcitonality we make sure this step is as quick as possible.

## Implementation Results

### Naive implementation

#### Dataset Tiny

| k | Author Set | Support | Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|------------------|---------------------|
| 1 | Jan Van den Bussche | 250 | 0.001001 | 0.001001 |
| 2 | Dirk Van Gucht, Marc Gyssens | 67 | 0.001257 | 0.002258 |
| 3 | Yuqing Wu, Dirk Van Gucht, Marc Gyssens | 25 | 0.001143 | 0.003401 |
| 4 | George H. L. Fletcher, Yuqing Wu, Dirk Van Gucht, Marc Gyssens | 14 | 0.000731 | 0.004131 |
| 5 | Stijn Vansummeren, Dirk Van Gucht, George H. L. Fletcher, Jan Van den Bussche, Marc Gyssens | 11 | 0.000429 | 0.004561 |
| 6 | Stijn Vansummeren, Dirk Van Gucht, George H. L. Fletcher, Jan Van den Bussche, Yuqing Wu, Marc Gyssens | 9 | 0.000222 | 0.004783 |
| 7 | Stijn Vansummeren, Dirk Van Gucht, George H. L. Fletcher, Dirk Leinders, Jan Van den Bussche, Yuqing Wu, Marc Gyssens | 6 | 0.000113 | 0.004896 |
| 8 | Stijn Vansummeren, Dirk Van Gucht, George H. L. Fletcher, Dirk Leinders, Dimitri Surinx, Jan Van den Bussche, Yuqing Wu, Marc Gyssens | 3 | 0.000077 | 0.004973 |
| 9 | Inge Thyssens, Dirk Van Gucht, Marc Gemis, Vijay M. Sarathy, Lawrence V. Saxton, Jan Paredaens, Jan Van den Bussche, Marc Andries, Marc Gyssens | 1 | 0.000066 | 0.005039 |

#### Dataset Medium 1

| k | Author Set | Support | Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|------------------|---------------------|
| 1 | Moshe Y. Vardi | 762 | 0.033490 | 0.033490 |
| 2 | Wolfgang Lehner, Dirk Habich | 182 | 0.066958 | 0.100448 |
| 3 | Diego Calvanese, Maurizio Lenzerini, Giuseppe De Giacomo | 104 | 0.084235 | 0.184684 |
| 4 | Diego Calvanese, Maurizio Lenzerini, Giuseppe De Giacomo, Riccardo Rosati 0001 | 37 | 0.078047 | 0.262731 |
| 5 | Giuseppe De Giacomo, Riccardo Rosati 0001, Diego Calvanese, Domenico Lembo, Maurizio Lenzerini | 25 | 0.086718 | 0.349449 |
| 6 | Jan Mendling, Stefan Zugal, Hajo A. Reijers, Barbara Weber, Matthias Weidlich 0001, Dirk Fahland | 11 | 0.048373 | 0.397822 |
| 7 | Jakob Pinggera, Stefan Zugal, Jan Mendling, Hajo A. Reijers, Barbara Weber, Matthias Weidlich 0001, Dirk Fahland | 9 | 0.026607 | 0.424429 |
| 8 | Chiara Di Francescomarino, Fabrizio Maria Maggi, Paola Mello, Federico Chesani, Daniela Loreti, Chiara Ghidini, Marco Montali, Sergio Tessaris | 6 | 0.007767 | 0.432196 |
| 9 | Marc Denecker, Stef De Pooter, Maurice Bruynooghe, Broes De Cat, Bart Bogaerts 0001, Anthony Labarre, Sicco Verwer, Jan Ramon, Hendrik Blockeel | 3 | 0.002016 | 0.434213 |
| 10 | Domagoj Vrgoc, Leonid Libkin, Paolo Guagliardo, Nadime Francis, Wim Martens, Alexandra Rogova, Filip Murlak, Liat Peterfreund, Amélie Gheerbrant, Victor Marsault | 3 | 0.000476 | 0.434689 |

#### Dataset Medium 2

| k | Author Set | Support | Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|------------------|---------------------|
| 1 | Noga Alon | 634 | 0.055396 | 0.055396 |
| 2 | Dirk Habich, Wolfgang Lehner | 184 | 0.188788 | 0.244184 |
| 3 | Maurizio Lenzerini, Diego Calvanese, Giuseppe De Giacomo | 104 | 2.042030 | 2.286214 |
| 4 | Riccardo Rosati 0001, Maurizio Lenzerini, Diego Calvanese, Giuseppe De Giacomo | 37 | 35.333536 | 37.619750 |

Met K > 4 duurde het langer dan 20 minuten en gebruikte meer dan 50GB aan geheugen op de gebruikte machine.
#### Dataset Large & ALL

MOETEN WE EENS DE TIJD VOOR NEMEN OM TE RUNNEN


### Apriori Implementation

#### Dataset Tiny

Treshold used = 5

| k | Author Set | Support | Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|------------------|---------------------|
| 1 | Jan Van den Bussche | 250 | 0.001258 | 0.001258 |
| 2 | Dirk Van Gucht, Marc Gyssens | 67 | 0.001109 | 0.002367 |
| 3 | Dirk Van Gucht, Marc Gyssens, Yuqing Wu | 25 | 0.001312 | 0.003679 |
| 4 | Dirk Van Gucht, George H. L. Fletcher, Marc Gyssens, Yuqing Wu | 14 | 0.000752 | 0.004431 |
| 5 | Dirk Van Gucht, George H. L. Fletcher, Marc Gyssens, Stijn Vansummeren, Jan Van den Bussche | 11 | 0.000407 | 0.004838 |
| 6 | Dirk Van Gucht, George H. L. Fletcher, Marc Gyssens, Stijn Vansummeren, Yuqing Wu, Jan Van den Bussche | 9 | 0.000231 | 0.005069 |
| 7 | Dirk Van Gucht, George H. L. Fletcher, Marc Gyssens, Stijn Vansummeren, Dirk Leinders, Yuqing Wu, Jan Van den Bussche | 6 | 0.000106 | 0.005175 |


#### Dataset Medium 1

treshold used = 5

| k | Author Set | Support | Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|------------------|---------------------|
| 1 | Moshe Y. Vardi | 762 | 0.004446 | 0.004446 |
| 2 | Dirk Habich, Wolfgang Lehner | 182 | 0.037631 | 0.042076 |
| 3 | Giuseppe De Giacomo, Maurizio Lenzerini, Diego Calvanese | 104 | 0.045699 | 0.087776 |
| 4 | Riccardo Rosati 0001, Giuseppe De Giacomo, Maurizio Lenzerini, Diego Calvanese | 37 | 0.022120 | 0.109896 |
| 5 | Giuseppe De Giacomo, Riccardo Rosati 0001, Domenico Lembo, Maurizio Lenzerini, Diego Calvanese | 25 | 0.009197 | 0.119093 |
| 6 | Jan Mendling, Hajo A. Reijers, Stefan Zugal, Dirk Fahland, Matthias Weidlich 0001, Barbara Weber | 11 | 0.003712 | 0.122805 |
| 7 | Jan Mendling, Hajo A. Reijers, Stefan Zugal, Jakob Pinggera, Dirk Fahland, Matthias Weidlich 0001, Barbara Weber | 9 | 0.001704 | 0.124509 |
| 8 | Daniela Loreti, Federico Chesani, Sergio Tessaris, Chiara Ghidini, Chiara Di Francescomarino, Fabrizio Maria Maggi, Paola Mello, Marco Montali | 6 | 0.000931 | 0.125440 |

                                                                                                   | 

#### Dataset Medium 2

treshold used = 5

| k | Author Set | Support | Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|------------------|---------------------|
| 1 | Noga Alon | 634 | 0.004588 | 0.004588 |
| 2 | Dirk Habich, Wolfgang Lehner | 184 | 0.043097 | 0.047686 |
| 3 | Maurizio Lenzerini, Giuseppe De Giacomo, Diego Calvanese | 104 | 0.074677 | 0.122362 |
| 4 | Maurizio Lenzerini, Giuseppe De Giacomo, Riccardo Rosati 0001, Diego Calvanese | 37 | 0.060328 | 0.182690 |
| 5 | Domenico Lembo, Maurizio Lenzerini, Giuseppe De Giacomo, Riccardo Rosati 0001, Diego Calvanese | 25 | 0.063571 | 0.246261 |
| 6 | Hajo A. Reijers, Stefan Zugal, Dirk Fahland, Jan Mendling, Matthias Weidlich 0001, Barbara Weber | 11 | 0.088002 | 0.334263 |
| 7 | Hajo A. Reijers, Stefan Zugal, Dirk Fahland, Jan Mendling, Matthias Weidlich 0001, Jakob Pinggera, Barbara Weber | 9 | 0.069009 | 0.403273 |
| 8 | Brian A. Coghlan, Andrew W. Cooke, Linda Cornwall, Abdeslem Djaoui, Antony J. Wilson, Steve Hicks, Steve Fisher, Stuart Kenny | 6 | 0.082689 | 0.485962 |
| 9 | Brian A. Coghlan, Andrew W. Cooke, Linda Cornwall, Abdeslem Djaoui, Antony J. Wilson, Steve Hicks, Steve Fisher, James Magowan, Stuart Kenny | 6 | 0.057364 | 0.543326 |
| 10 | Brian A. Coghlan, Andrew W. Cooke, Linda Cornwall, Abdeslem Djaoui, Antony J. Wilson, Steve Hicks, Steve Fisher, James Magowan, Werner Nutt, David O'Callaghan | 6 | 0.041579 | 0.584905 |
| 11 | Brian A. Coghlan, Andrew W. Cooke, Linda Cornwall, Abdeslem Djaoui, Antony J. Wilson, Steve Hicks, Steve Fisher, James Magowan, Werner Nutt, David O'Callaghan, Paul Taylor | 6 | 0.065246 | 0.650151 |
| 12 | Brian A. Coghlan, Andrew W. Cooke, Linda Cornwall, Abdeslem Djaoui, Antony J. Wilson, Steve Hicks, Steve Fisher, James Magowan, Werner Nutt, David O'Callaghan, Rob Byrom, Paul Taylor | 6 | 0.007334 | 0.657485 |
| 13 | Brian A. Coghlan, Andrew W. Cooke, Abdeslem Djaoui, Linda Cornwall, Antony J. Wilson, Steve Hicks, Steve Fisher, James Magowan, Werner Nutt, David O'Callaghan, Rob Byrom, Roney Cordenonsi, Paul Taylor | 6 | 0.002906 | 0.660391 |
| 14 | Brian A. Coghlan, Andrew W. Cooke, Linda Cornwall, Abdeslem Djaoui, Antony J. Wilson, Steve Hicks, Steve Fisher, James Magowan, Werner Nutt, David O'Callaghan, Rob Byrom, Roney Cordenonsi, Norbert Podhorszki, Stuart Kenny | 6 | 0.001273 | 0.661664 |
| 15 | Brian A. Coghlan, Andrew W. Cooke, Linda Cornwall, Abdeslem Djaoui, Antony J. Wilson, Stuart Kenny, Steve Hicks, Steve Fisher, James Magowan, Werner Nutt, David O'Callaghan, Rob Byrom, Roney Cordenonsi, Norbert Podhorszki, Paul Taylor | 6 | 0.000911 | 0.662575 |


#### Dataset Large

treshold used = 25

| k | Author Set | Support | Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|------------------|---------------------|
| 1 | H. Vincent Poor | 906 | 0.322604 | 0.322604 |
| 2 | Makoto Takizawa 0001, Tomoya Enokido | 242 | 2.436293 | 2.758897 |
| 3 | Kazunori Komatani, Tetsuya Ogata, Hiroshi G. Okuno | 122 | 0.897391 | 3.656288 |
| 4 | Patrick Girard 0001, Alberto Bosio, Luigi Dilillo, Arnaud Virazel | 53 | 0.412360 | 4.068648 |
| 5 | Arthur W. Toga, Paul M. Thompson, Greig I. de Zubicaray, Katie McMahon, Margaret J. Wright | 44 | 0.217062 | 4.285710 |
| 6 | José Juan Pazos-Arias, Rebeca P. Díaz Redondo, Jorge García Duque, Alberto Gil-Solla, Ana Fernández Vilas, Manuel Ramos Cabrer | 31 | 0.110591 | 4.396301 |

#### Dataset ALL

treshold used = 25

| k | Author Set | Support | Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|------------------|---------------------|
| 1 | H. Vincent Poor | 2986 | 1.300479 | 1.300479 |
| 2 | Tomoya Enokido, Makoto Takizawa 0001 | 531 | 18.661060 | 19.961539 |
| 3 | Shaoping Ma, Min Zhang 0006, Yiqun Liu 0001 | 282 | 6.117888 | 26.079427 |
| 4 | Ramon Casellas, Raul Muñoz 0001, Ricardo Martínez 0001, Ricard Vilalta | 149 | 3.489365 | 29.568792 |
| 5 | Albert Reuther, Peter Michaleas, Jeremy Kepner, Matthew Hubbell, David Bestor | 100 | 1.572940 | 31.141731 |
| 6 | Andrew Prout, Albert Reuther, Peter Michaleas, Jeremy Kepner, Matthew Hubbell, David Bestor | 98 | 1.578864 | 32.720595 |
| 7 | Antonio Rosa, Andrew Prout, Albert Reuther, Peter Michaleas, Jeremy Kepner, Matthew Hubbell, David Bestor | 96 | 1.798832 | 34.519427 |
| 8 | Antonio Rosa, William Arcand, Andrew Prout, Albert Reuther, Peter Michaleas, Jeremy Kepner, Matthew Hubbell, David Bestor | 94 | 2.365928 | 36.885355 |
| 9 | Antonio Rosa, William Arcand, Andrew Prout, Chansup Byun, Albert Reuther, Peter Michaleas, Jeremy Kepner, Matthew Hubbell, David Bestor | 92 | 2.684623 | 39.569978 |
| 10 | Antonio Rosa, William Arcand, Andrew Prout, Vijay Gadepally, Chansup Byun, Albert Reuther, Peter Michaleas, Jeremy Kepner, Matthew Hubbell, David Bestor | 83 | 2.583578 | 42.153556 |
| 11 | Antonio Rosa, William Arcand, Charles Yee, Andrew Prout, Vijay Gadepally, Chansup Byun, Albert Reuther, Peter Michaleas, Jeremy Kepner, Matthew Hubbell, David Bestor | 79 | 2.041043 | 44.194599 |
| 12 | Antonio Rosa, William Arcand, Michael Jones 0001, Andrew Prout, Vijay Gadepally, Lauren Milechin, Chansup Byun, Albert Reuther, Peter Michaleas, Jeremy Kepner, Matthew Hubbell, David Bestor | 69 | 1.292799 | 45.487398 |
| 13 | Antonio Rosa, William Arcand, Michael Jones 0001, Charles Yee, Andrew Prout, Vijay Gadepally, Lauren Milechin, Chansup Byun, Albert Reuther, Peter Michaleas, Jeremy Kepner, Matthew Hubbell, David Bestor | 65 | 0.629513 | 46.116911 |
| 14 | Antonio Rosa, William Arcand, Michael Jones 0001, Charles Yee, Andrew Prout, Vijay Gadepally, Siddharth Samsi, Lauren Milechin, Chansup Byun, Albert Reuther, Peter Michaleas, Jeremy Kepner, Matthew Hubbell, David Bestor | 61 | 0.250736 | 46.367647 |
| 15 | Antonio Rosa, William Arcand, Michael Jones 0001, Charles Yee, Andrew Prout, Vijay Gadepally, Siddharth Samsi, Julie Mullen, Lauren Milechin, Chansup Byun, Albert Reuther, Peter Michaleas, Jeremy Kepner, Matthew Hubbell, David Bestor | 51 | 0.092668 | 46.460314 |
| 16 | Antonio Rosa, Jeremy Kepner, William Arcand, Michael Jones 0001, Charles Yee, Andrew Prout, Vijay Gadepally, Siddharth Samsi, Lauren Milechin, Chansup Byun, Albert Reuther, Peter Michaleas, Julie Mullen, Matthew Hubbell, David Bestor, Anna Klein | 40 | 0.040990 | 46.501304 |
| 17 | Antonio Rosa, William Arcand, Michael Jones 0001, Charles Yee, Andrew Prout, Vijay Gadepally, Siddharth Samsi, Julie Mullen, Michael Houle 0001, Lauren Milechin, Chansup Byun, Albert Reuther, Peter Michaleas, Jeremy Kepner, Matthew Hubbell, David Bestor, Anna Klein | 26 | 0.026291 | 46.527596 |

