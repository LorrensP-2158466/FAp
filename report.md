# Report Apriori Assigment

Authors:

- Ivan Molenaers (2157801)
- Lorrens Pantelis (2158466)
 
ALL MEASUREMENTS DONE ON MAC M1 2020 SEQUOIA 15.0

<small>Recomended to read in md viewer not pdf (vscode, ...)</small>

## The program

The main entry point of the program is the python file [`main.py`](./main.py). We define the argument parser and based on those arguments we can run a different subprogram.

You can ask the usage of the program by running:

```python main.py -h```

Note: ignore the `positional arguments` and `options` section after the usage, this is boilerplate by argsparse which we can't remove.

There are 3 subprograms:

- data-expl
- naive
- apriori

They are straightforward in their function by their name each with their own seperate args. The usage of the program is:

### Usage

```
usage: main.py [ARGS] [SUBCOMMAND] [SUBCOMMAND ARGS]

ARGS:
    --md                  Output the results of th subcommand in a  markdown table
    --dataset DATASETPATH Set the dataset path the subcommand should use

SUBCOMMAND:
    data-expl Perform the data explorations
    naive     Perform the naive algorithm on the dataset
    apriori   Perform the apriori algorithm on the dataset

SUCOMMAND ARGS:
    data-expl:
        --explorations=[DATA_EXPLS] Choose one or more data explorations to perform on the dataset.
        --output-ppa                Output `papers_per_auhtor` technique to a csv file
    naive:
        --k Which maximal author set you would like to calculate
    apriori:
        --k int        Till which maximal author set you would like to calculate (this also outputs intermediate results)
        --treshold int Set the treshold for the apriori algorithm

DATA_EXPLS:
    You can define multiple data_explorations seperated by a comma
    all // does all the explorations
    amt_publications, average_amt_authors, unique_authors, papers_per_author, average_paper_per_author, 
    count_marc_dirk, most_papers_published_by_one_author, median_amt_authors

BDA Project frequent itemsets and apriori
...
```

### Examples:

```python
python main.py --dataset=datasets/dataset_all.txt apriori --treshold 25 # run apriori on dataset_all with treshold 25
python main.py --dataset=datasets/dataset_medium1.txt naive --k  10  # run naive on dataset_medium for maximal authorsets of size k in 1,...,10
python main.py --dataset=datasets/dataset_medium2.txt data-expl --explorations=papers_per_author,count_marc_dirk --output-ppa
```

## Data Exploration

We used five techniques for data exploration, namely the two that were provided and three additional ones:

- Number of Publications
- Average Number of Authors Per Paper
- Unique Authors
- Average Papers per Author
- Papers per Author (too many to display in a table)

The "papers per author" can be viewed in the standard output of the program when we run:
```
python3 ./main.py [DATASET_PATH] data-expl --explorations=papers_per_author
```

This will print a `polars.Datafram` to standard out, which will be truncated ofcourse, you can add the subcommand arg `--output_ppa` which will create a csv file with each name and their publication count. The name of the file will be the name of the dataset file followed by `papers_per_author`.

We ran every technique (besides `count_marc_dirk` and `papers_per_author`) on every given dataset and got following results:

#### Combined Data Exploration Table

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

We can perform data explorations by running the command:

```
python main.py --md --dataset [DATASET_PATH] data-expl --explorations=[EXPLORATIONS]
```
This will print a markdown table of the results to standard output. You can also leave out --md and just print raw results to standard output.

### Naive
The code starts in the `main.py` file where a loop iteratively calls `Naive.run(k)`. The `Naive` object will then
search for the most frequent itemset(s) of size k using a counter dictionary. It does this by going through each basket/row of the table and:

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
- Produce the rest of the frequent itemsets and yield one of the maximal ones.

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

1. We use two tables: `curr_map` for tracking the current frequent itemsets of size `k`, and `prev_map` for tracking the frequent itemsets of size `k−1`
2. We only consider baskets containing at least `k` items, because you can't do: N choose K with K < N.
3. We create a set `prev_frequents`, which includes every author who was frequent in iteration `k-1`
4. As we loop through each basket, we discard any item not present in `prev_frequents`. If the resulting basket has fewer than `k` items, it is ignored
5. We generate every combination of size `k-1` from the filtered basket. If a combination is frequent (based on `prev_map`), we add its elements to a set `possible_candidates`. We now end up with a flat set that has **exactly** the elements that the frequent combinations of size k can exists of. This is also our main optimization: Unlike the naive approach, which generates combinations of size k and then checks their subsets of size k-1, we restrict ourselves to generating the sets in `prev_map` exist of the items in the current basket, resulting in fewer combinations, fewer condition checks, and reduced memory usage
6. Since we identified exactly which elements are in the sets of size k that are frequent, we only need to generate these combinations and add them to the dict (note that we don't have any conditional checks in this step).
7. If they are already in `curr_map` we increase the count by 1, otherwise we add them and set the count to 1.
8. When we have looped through each basket, the final thing to do is to filter each item that has a count less then the given treshold in `curr_map`

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

### Challenges and possible improvements

#### Challenges

When we initially implemented a naive version of the A Priori algorithm, it became clear that optimization was necessary. For small values of k the naive implementation was faster, and for higher values where naive failed, it was still very slow. We started to look for conceptual improvements at first and iteratively made it faster. <br>
The first optimization involved only considering baskets of at least size k, reducing the number of iterations needed. We then found that generating candidate pairs directly was more efficient than iterating over the map and checking for their presence individually. Several other ideas were tested along the way; some proved totally ineffective, while others did not significant provide performance gains. Our main focus was on experimenting with loop order, which led to the most significant improvements in the end. <br> 
After making conceptual enhancements, we employed tools like `cProfile` to apply targeted optimizations. The most important one was making specialized functions for the cases k=1 and k=2. Since these are "unqiue" cases, we could leverage specific attributes to make them faster. Also, when making a list or a dictionary, list/dictionary comprehension gave faster results than using `map()` or `filter()`, leading to further gains. <br>

#### Improvements

An additional optimization we considered was memoization. While generating combinations of size k-1 from the baskets, we noticed that some combinations appeared multiple times throughout the whole process. By storing the combinations made in previous iterations in a map, we could avoid recalculating them, potentially saving significant computation time. <br>
However, we did not implement memoization due to limitations with `itertools.combinations()`. This built-in function is highly optimized, and since integrating our own memoization code is not possible, it would require custom combination generation, which could negate the benefits. <br>
We also experimented with opening the file directly in Python (`open()`) instead of using Polars, which resulted in a significant speed improvement for the k=2 case. However, this approach did not yield performance benefits for the other cases. To maintain cleaner and more consistent code, we decided against using two different file-opening methods in our program.

## Implementation Results

We ran the 2 implementations on all the datasets and collected their results in a table that has the following format:

| k | Author Set | Support | # Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|----------------------|------------------|---------------------|


|column| explanation|
|--|--|
| k | maximal author set of size `k`|
| Author Set | the found maximal authorset of size `k`|
| Support | The support of the maximal author set|
| # Maximal Author Set| The amount of maximal author sets of size `k`|
| Time Elasped (s) | Time it took to only calculate that `k` |
|Cumulative Time (s) | Total time it took to calculate till this `k` (sum of Time elasped) |

### Naive implementation

#### Dataset Tiny

| k | Author Set | Support | # Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|----------------------|------------------|---------------------|
| 1 | Jan Van den Bussche | 250 | 290 | 0.001031 | 0.001031 |
| 2 | Marc Gyssens, Dirk Van Gucht | 67 | 936 | 0.001286 | 0.002318 |
| 3 | Yuqing Wu, Marc Gyssens, Dirk Van Gucht | 25 | 1116 | 0.001269 | 0.003586 |
| 4 | Yuqing Wu, George H. L. Fletcher, Marc Gyssens, Dirk Van Gucht | 14 | 772 | 0.000776 | 0.004362 |
| 5 | Marc Gyssens, Stijn Vansummeren, George H. L. Fletcher, Jan Van den Bussche, Dirk Van Gucht | 11 | 404 | 0.000439 | 0.004801 |
| 6 | Marc Gyssens, Yuqing Wu, Stijn Vansummeren, George H. L. Fletcher, Jan Van den Bussche, Dirk Van Gucht | 9 | 170 | 0.000330 | 0.005131 |
| 7 | Marc Gyssens, Yuqing Wu, Stijn Vansummeren, Dirk Leinders, George H. L. Fletcher, Jan Van den Bussche, Dirk Van Gucht | 6 | 54 | 0.000120 | 0.005251 |
| 8 | Marc Gyssens, Yuqing Wu, Stijn Vansummeren, Dirk Leinders, Dimitri Surinx, George H. L. Fletcher, Jan Van den Bussche, Dirk Van Gucht | 3 | 11 | 0.000097 | 0.005347 |
| 9 | Inge Thyssens, Marc Andries, Dirk Van Gucht, Marc Gyssens, Vijay M. Sarathy, Lawrence V. Saxton, Jan Van den Bussche, Marc Gemis, Jan Paredaens | 1 | 1 | 0.000079 | 0.005426 |


#### Dataset Medium 1

| k | Author Set | Support | # Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|----------------------|------------------|---------------------|
| 1 | Moshe Y. Vardi | 762 | 14885 | 0.034293 | 0.034293 |
| 2 | Dirk Habich, Wolfgang Lehner | 182 | 58748 | 0.066232 | 0.100525 |
| 3 | Diego Calvanese, Maurizio Lenzerini, Giuseppe De Giacomo | 104 | 94156 | 0.084676 | 0.185200 |
| 4 | Diego Calvanese, Maurizio Lenzerini, Giuseppe De Giacomo, Riccardo Rosati 0001 | 37 | 100343 | 0.077701 | 0.262902 |
| 5 | Maurizio Lenzerini, Riccardo Rosati 0001, Domenico Lembo, Diego Calvanese, Giuseppe De Giacomo | 25 | 81263 | 0.087921 | 0.350822 |
| 6 | Jan Mendling, Matthias Weidlich 0001, Stefan Zugal, Barbara Weber, Hajo A. Reijers, Dirk Fahland | 11 | 50131 | 0.048560 | 0.399383 |
| 7 | Matthias Weidlich 0001, Jan Mendling, Jakob Pinggera, Stefan Zugal, Barbara Weber, Hajo A. Reijers, Dirk Fahland | 9 | 22599 | 0.026483 | 0.425865 |
| 8 | Paola Mello, Chiara Di Francescomarino, Federico Chesani, Daniela Loreti, Fabrizio Maria Maggi, Marco Montali, Chiara Ghidini, Sergio Tessaris | 6 | 6961 | 0.007378 | 0.433243 |
| 9 | Stef De Pooter, Hendrik Blockeel, Sicco Verwer, Broes De Cat, Bart Bogaerts 0001, Marc Denecker, Anthony Labarre, Maurice Bruynooghe, Jan Ramon | 3 | 1304 | 0.001972 | 0.435216 |
| 10 | Paolo Guagliardo, Liat Peterfreund, Alexandra Rogova, Amélie Gheerbrant, Wim Martens, Victor Marsault, Domagoj Vrgoc, Nadime Francis, Filip Murlak, Leonid Libkin | 3 | 112 | 0.000474 | 0.435690 |

#### Dataset Medium 2

| k | Author Set | Support | # Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|----------------------|------------------|---------------------|
| 1 | Noga Alon | 634 | 17707 | 0.035916 | 0.035916 |
| 2 | Wolfgang Lehner, Dirk Habich | 184 | 126034 | 0.129785 | 0.165700 |
| 3 | Giuseppe De Giacomo, Diego Calvanese, Maurizio Lenzerini | 104 | 1230115 | 1.543562 | 1.709262 |
| 4 | Giuseppe De Giacomo, Diego Calvanese, Maurizio Lenzerini, Riccardo Rosati 0001 | 37 | 21022041 | 26.949563 | 28.658825 |

With k > 4, it took longer than 20 minutes and used more than 50GB of memory on the machine in use. This is due to the fact that we count every possible combination, which will take a very long time. At first this is rather strange, since the file size is smaller than the [Medium1](#dataset-medium-1) dataset. But if look back to our data exploration results we can see why this is. We will paste the results of `Medium 1` and `Medium 2` here:

| DataExploration Technique           | Medium 1             | Medium 2             |
|-------------------------------------|----------------------|----------------------|
| Amount of Publications              | 22,779               | 21,092               |
| Average Amount of Authors Per Paper | 3.467140787567496    | 4.006447942347809    |
| Unique Authors                      | 14,885               | 17,707               |
| Average Paper per Author            | 1.5303325495465234   | 1.1911673349522787   |

Even though `Medium2` has less publications, it has more authors and more authors per paper and less papers per author. This will result in more combinations than `Medium1` that than need to be counted which will bottleneck the application.

#### Dataset Large

| k | Author Set | Support | # Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|----------------------|------------------|---------------------|
| 1 | H. Vincent Poor | 906 | 1258951 | 4.880382 | 4.880382 |
| 2 | Tomoya Enokido, Makoto Takizawa 0001 | 242 | 5187688 | 10.304312 | 15.184694 |
| 3 | Hiroshi G. Okuno, Tetsuya Ogata, Kazunori Komatani | 122 | 15370210 | 23.671696 | 38.856390 |

Running for `k > 3` took longer than 20 minutes and was not included in the table. This is because of the number of combinations that need to be calculated and put in to memory which will bottleneck the program.

#### Dataset ALL

| k | Author Set | Support | # Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|----------------------|------------------|---------------------|
| 1 | H. Vincent Poor | 2986 | 3658503 | 19.464302 | 19.464302 |
| 2 | Tomoya Enokido, Makoto Takizawa 0001 | 531 | 24614074 | 54.792152 | 74.256455 |

Running for larger k's resulted in waiting times longer than 20 minutes, which is too long.

### Apriori Implementation

#### Dataset Tiny

Treshold 5:

| k | Author Set | Support |# Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|---------------------|------------------|---------------------|
| 1 | Jan Van den Bussche | 250 | 66 | 0.001180 | 0.001180 |
| 2 | Marc Gyssens, Dirk Van Gucht | 67 | 119 | 0.001088 | 0.002268 |
| 3 | Yuqing Wu, Dirk Van Gucht, Marc Gyssens | 25 | 84 | 0.001267 | 0.003535 |
| 4 | George H. L. Fletcher, Yuqing Wu, Dirk Van Gucht, Marc Gyssens | 14 | 50 | 0.000730 | 0.004265 |
| 5 | Stijn Vansummeren, Marc Gyssens, Jan Van den Bussche, George H. L. Fletcher, Dirk Van Gucht | 11 | 23 | 0.000435 | 0.004700 |
| 6 | Stijn Vansummeren, Marc Gyssens, Jan Van den Bussche, George H. L. Fletcher, Yuqing Wu, Dirk Van Gucht | 9 | 7 | 0.000227 | 0.004927 |
| 7 | Stijn Vansummeren, Marc Gyssens, George H. L. Fletcher, Jan Van den Bussche, Dirk Leinders, Yuqing Wu, Dirk Van Gucht | 6 | 1 | 0.000147 | 0.005074 |

The Apriori implementation found every maximal authorset with treshold equal to 5. This is less than the naive implementation, but this is due to the treshold used. Lower treshold will yield maximal author sets for higher `k`'s.

Example with `--treshold 1`:

| k | Author Set | Support |# Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|---------------------|------------------|---------------------|
| 1 | Jan Van den Bussche | 250 | 290 | 0.001322 | 0.001322 |
| 2 | Marc Gyssens, Dirk Van Gucht | 67 | 936 | 0.001542 | 0.002864 |
| 3 | Marc Gyssens, Dirk Van Gucht, Yuqing Wu | 25 | 1116 | 0.002561 | 0.005425 |
| 4 | Marc Gyssens, George H. L. Fletcher, Dirk Van Gucht, Yuqing Wu | 14 | 772 | 0.002046 | 0.007471 |
| 5 | Marc Gyssens, Stijn Vansummeren, Dirk Van Gucht, George H. L. Fletcher, Jan Van den Bussche | 11 | 404 | 0.001379 | 0.008850 |
| 6 | Marc Gyssens, Stijn Vansummeren, Dirk Van Gucht, George H. L. Fletcher, Jan Van den Bussche, Yuqing Wu | 9 | 170 | 0.000853 | 0.009703 |
| 7 | Marc Gyssens, Stijn Vansummeren, Dirk Leinders, Dirk Van Gucht, George H. L. Fletcher, Jan Van den Bussche, Yuqing Wu | 6 | 54 | 0.000443 | 0.010146 |
| 8 | Marc Gyssens, Stijn Vansummeren, Dirk Leinders, Dirk Van Gucht, Dimitri Surinx, George H. L. Fletcher, Jan Van den Bussche, Yuqing Wu | 3 | 11 | 0.000143 | 0.010289 |
| 9 | Vijay M. Sarathy, Marc Gyssens, Marc Gemis, Inge Thyssens, Dirk Van Gucht, Lawrence V. Saxton, Jan Paredaens, Marc Andries, Jan Van den Bussche | 1 | 1 | 0.000088 | 0.010377 |

#### Dataset Medium 1
Running with flag `--treshold 5` gives us:

| k | Author Set | Support |# Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|---------------------|------------------|---------------------|
| 1 | Moshe Y. Vardi | 762 | 2329 | 0.004456 | 0.004456 |
| 2 | Wolfgang Lehner, Dirk Habich | 182 | 3702 | 0.037373 | 0.041830 |
| 3 | Giuseppe De Giacomo, Maurizio Lenzerini, Diego Calvanese | 104 | 1927 | 0.045704 | 0.087534 |
| 4 | Giuseppe De Giacomo, Maurizio Lenzerini, Riccardo Rosati 0001, Diego Calvanese | 37 | 675 | 0.023541 | 0.111074 |
| 5 | Domenico Lembo, Giuseppe De Giacomo, Maurizio Lenzerini, Riccardo Rosati 0001, Diego Calvanese | 25 | 208 | 0.009043 | 0.120117 |
| 6 | Hajo A. Reijers, Jan Mendling, Barbara Weber, Matthias Weidlich 0001, Stefan Zugal, Dirk Fahland | 11 | 57 | 0.003504 | 0.123621 |
| 7 | Hajo A. Reijers, Jakob Pinggera, Jan Mendling, Barbara Weber, Matthias Weidlich 0001, Stefan Zugal, Dirk Fahland | 9 | 11 | 0.001565 | 0.125186 |
| 8 | Fabrizio Maria Maggi, Chiara Di Francescomarino, Paola Mello, Sergio Tessaris, Federico Chesani, Marco Montali, Chiara Ghidini, Daniela Loreti | 6 | 1 | 0.000896 | 0.126082 |


The Apriori implementation found every maximal authorset with treshold equal to 5. This is less than the naive implementation, but this is due to the treshold used. Lower treshold will yield maximal author sets for higher `k`'s.
Example with `--treshold 1`:

| k | Author Set | Support |# Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|---------------------|------------------|---------------------|
| 1 | Moshe Y. Vardi | 762 | 7937 | 0.006884 | 0.006884 |
| 2 | Dirk Habich, Wolfgang Lehner | 182 | 24281 | 0.061025 | 0.067910 |
| 3 | Maurizio Lenzerini, Diego Calvanese, Giuseppe De Giacomo | 104 | 30454 | 0.149133 | 0.217042 |
| 4 | Maurizio Lenzerini, Riccardo Rosati 0001, Giuseppe De Giacomo, Diego Calvanese | 37 | 26430 | 0.094832 | 0.311875 |
| 5 | Maurizio Lenzerini, Giuseppe De Giacomo, Riccardo Rosati 0001, Diego Calvanese, Domenico Lembo | 25 | 18674 | 0.106678 | 0.418552 |
| 6 | Barbara Weber, Matthias Weidlich 0001, Hajo A. Reijers, Dirk Fahland, Stefan Zugal, Jan Mendling | 11 | 10611 | 0.049169 | 0.467721 |
| 7 | Barbara Weber, Matthias Weidlich 0001, Jakob Pinggera, Hajo A. Reijers, Dirk Fahland, Stefan Zugal, Jan Mendling | 9 | 4535 | 0.026185 | 0.493906 |
| 8 | Daniela Loreti, Fabrizio Maria Maggi, Chiara Di Francescomarino, Marco Montali, Federico Chesani, Sergio Tessaris, Paola Mello, Chiara Ghidini | 6 | 1345 | 0.010061 | 0.503967 |
| 9 | Hendrik Blockeel, Maurice Bruynooghe, Bart Bogaerts 0001, Broes De Cat, Sicco Verwer, Marc Denecker, Stef De Pooter, Anthony Labarre, Jan Ramon | 3 | 246 | 0.003844 | 0.507810 |
| 10 | Nadime Francis, Domagoj Vrgoc, Paolo Guagliardo, Amélie Gheerbrant, Filip Murlak, Leonid Libkin, Victor Marsault, Liat Peterfreund, Wim Martens, Alexandra Rogova | 3 | 21 | 0.000934 | 0.508745 |

This gives us different results in the Number of Maximal Author Sets and in our execution time, which is expected.

#### Dataset Medium 2

Running with flag `--treshold 5` gives us:

| k | Author Set | Support |# Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|---------------------|------------------|---------------------|
| 1 | Noga Alon | 634 | 2511 | 0.011461 | 0.011461 |
| 2 | Dirk Habich, Wolfgang Lehner | 184 | 4457 | 0.044398 | 0.055859 |
| 3 | Diego Calvanese, Maurizio Lenzerini, Giuseppe De Giacomo | 104 | 3329 | 0.075810 | 0.131669 |
| 4 | Diego Calvanese, Maurizio Lenzerini, Giuseppe De Giacomo, Riccardo Rosati 0001 | 37 | 3016 | 0.060688 | 0.192357 |
| 5 | Domenico Lembo, Diego Calvanese, Riccardo Rosati 0001, Maurizio Lenzerini, Giuseppe De Giacomo | 25 | 4056 | 0.063895 | 0.256252 |
| 6 | Matthias Weidlich 0001, Dirk Fahland, Stefan Zugal, Hajo A. Reijers, Jan Mendling, Barbara Weber | 11 | 5696 | 0.096258 | 0.352510 |
| 7 | Matthias Weidlich 0001, Dirk Fahland, Stefan Zugal, Hajo A. Reijers, Jan Mendling, Jakob Pinggera, Barbara Weber | 9 | 6831 | 0.069966 | 0.422476 |
| 8 | Antony J. Wilson, Norbert Podhorszki, Stuart Kenny, Linda Cornwall, Rob Byrom, Steve Hicks, Andrew W. Cooke, Werner Nutt | 6 | 6612 | 0.086500 | 0.508977 |
| 9 | Antony J. Wilson, Norbert Podhorszki, Stuart Kenny, Rob Byrom, Linda Cornwall, Steve Hicks, Andrew W. Cooke, Roney Cordenonsi, Werner Nutt | 6 | 5061 | 0.059982 | 0.568958 |
| 10 | Antony J. Wilson, Norbert Podhorszki, Stuart Kenny, Rob Byrom, Linda Cornwall, Steve Hicks, Andrew W. Cooke, Roney Cordenonsi, Abdeslem Djaoui, Brian A. Coghlan | 6 | 3014 | 0.044368 | 0.613326 |
| 11 | Antony J. Wilson, Norbert Podhorszki, Stuart Kenny, Rob Byrom, Steve Hicks, Linda Cornwall, Andrew W. Cooke, Roney Cordenonsi, James Magowan, Werner Nutt, Brian A. Coghlan | 6 | 1366 | 0.033431 | 0.646757 |
| 12 | Antony J. Wilson, Norbert Podhorszki, Stuart Kenny, Rob Byrom, Steve Hicks, Linda Cornwall, Andrew W. Cooke, Roney Cordenonsi, James Magowan, David O'Callaghan, Werner Nutt, Abdeslem Djaoui | 6 | 455 | 0.007972 | 0.654730 |
| 13 | Antony J. Wilson, Norbert Podhorszki, Stuart Kenny, Rob Byrom, Steve Hicks, Linda Cornwall, Andrew W. Cooke, Roney Cordenonsi, Brian A. Coghlan, James Magowan, David O'Callaghan, Werner Nutt, Abdeslem Djaoui | 6 | 105 | 0.003259 | 0.657989 |
| 14 | Antony J. Wilson, Norbert Podhorszki, Stuart Kenny, Linda Cornwall, Steve Hicks, Rob Byrom, Andrew W. Cooke, Roney Cordenonsi, Brian A. Coghlan, James Magowan, David O'Callaghan, Werner Nutt, Abdeslem Djaoui, Paul Taylor | 6 | 15 | 0.001362 | 0.659351 |
| 15 | Antony J. Wilson, Norbert Podhorszki, Stuart Kenny, Rob Byrom, Steve Hicks, Linda Cornwall, Andrew W. Cooke, Roney Cordenonsi, Brian A. Coghlan, James Magowan, David O'Callaghan, Werner Nutt, Abdeslem Djaoui, Paul Taylor, Steve Fisher | 6 | 1 | 0.001038 | 0.660389 |

The Apriori implementation found every maximal authorset with support higher than the treshold. This is far more than the `naive` implementation, this is our first illustration that our Apriori implementation is faster and better in finding frequent item sets than the naive. This also shows how innefective counting every combintation really is (`naive`), espacially if the dataset has a lot of possible combinations. We also tried to use a lower treshold, to see if we could get all maximal authorsets.
We notices during the data exploration that the average amount of papers per author in the `Medium2 dataset` was ~4, so we tried and set the treshold to 3 with `--treshol 3`:

| k | Author Set | Support |# Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|---------------------|------------------|---------------------|
| 1 | Noga Alon | 634 | 3974 | 0.005067 | 0.005067 |
| 2 | Dirk Habich, Wolfgang Lehner | 184 | 9007 | 0.052440 | 0.057508 |
| 3 | Giuseppe De Giacomo, Diego Calvanese, Maurizio Lenzerini | 104 | 10189 | 0.112693 | 0.170201 |
| 4 | Giuseppe De Giacomo, Riccardo Rosati 0001, Diego Calvanese, Maurizio Lenzerini | 37 | 14606 | 0.187883 | 0.358084 |
| 5 | Diego Calvanese, Riccardo Rosati 0001, Giuseppe De Giacomo, Domenico Lembo, Maurizio Lenzerini | 25 | 27404 | 0.598756 | 0.956840 |
| 6 | Dirk Fahland, Jan Mendling, Matthias Weidlich 0001, Hajo A. Reijers, Stefan Zugal, Barbara Weber | 11 | 49336 | 1.764300 | 2.721141 |
| 7 | Jakob Pinggera, Dirk Fahland, Matthias Weidlich 0001, Jan Mendling, Hajo A. Reijers, Stefan Zugal, Barbara Weber | 9 | 74952 | 2.569869 | 5.291010 |
| 8 | Antony J. Wilson, David O'Callaghan, Werner Nutt, Linda Cornwall, Rob Byrom, Brian A. Coghlan, James Magowan, Andrew W. Cooke | 6 | 92986 | 3.730908 | 9.021918 |
| 9 | Antony J. Wilson, David O'Callaghan, Werner Nutt, Linda Cornwall, Rob Byrom, Brian A. Coghlan, James Magowan, Andrew W. Cooke, Steve Hicks | 6 | 93270 | 5.463847 | 14.485765 |
| 10 | Antony J. Wilson, David O'Callaghan, Werner Nutt, Linda Cornwall, Rob Byrom, Brian A. Coghlan, James Magowan, Abdeslem Djaoui, Andrew W. Cooke, Steve Hicks | 6 | 75156 | 8.422534 | 22.908299 |
| 11 | Antony J. Wilson, David O'Callaghan, Werner Nutt, Linda Cornwall, Rob Byrom, Brian A. Coghlan, James Magowan, Abdeslem Djaoui, Andrew W. Cooke, Paul Taylor, Steve Hicks | 6 | 48230 | 9.003405 | 31.911703 |
| 12 | Roney Cordenonsi, Antony J. Wilson, David O'Callaghan, Werner Nutt, Linda Cornwall, Rob Byrom, Brian A. Coghlan, James Magowan, Abdeslem Djaoui, Andrew W. Cooke, Paul Taylor, Steve Hicks | 6 | 24311 | 10.742044 | 42.653748 |
| 13 | Roney Cordenonsi, Antony J. Wilson, David O'Callaghan, Norbert Podhorszki, Werner Nutt, Linda Cornwall, Rob Byrom, Brian A. Coghlan, James Magowan, Abdeslem Djaoui, Andrew W. Cooke, Paul Taylor, Steve Hicks | 6 | 9416 | 1.774850 | 44.428598 |
| 14 | Roney Cordenonsi, Antony J. Wilson, David O'Callaghan, Norbert Podhorszki, Werner Nutt, Linda Cornwall, Rob Byrom, Brian A. Coghlan, James Magowan, Abdeslem Djaoui, Andrew W. Cooke, Paul Taylor, Stuart Kenny, Steve Hicks | 6 | 2705 | 1.097006 | 45.525604 |
| 15 | Roney Cordenonsi, Antony J. Wilson, David O'Callaghan, Norbert Podhorszki, Werner Nutt, Linda Cornwall, Rob Byrom, Brian A. Coghlan, James Magowan, Abdeslem Djaoui, Andrew W. Cooke, Paul Taylor, Stuart Kenny, Steve Fisher, Steve Hicks | 6 | 543 | 0.612315 | 46.137919 |
| 16 | Roney Cordenonsi, Antony J. Wilson, David O'Callaghan, Norbert Podhorszki, Werner Nutt, Laurence Field, Linda Cornwall, Rob Byrom, Brian A. Coghlan, James Magowan, Abdeslem Djaoui, Andrew W. Cooke, Paul Taylor, Stuart Kenny, Steve Fisher, Steve Hicks | 5 | 68 | 0.254339 | 46.392258 |
| 17 | Roney Cordenonsi, Antony J. Wilson, David O'Callaghan, Norbert Podhorszki, Manish Soni, Werner Nutt, Laurence Field, Linda Cornwall, Rob Byrom, Brian A. Coghlan, James Magowan, Abdeslem Djaoui, Andrew W. Cooke, Paul Taylor, Stuart Kenny, Steve Fisher, Steve Hicks | 4 | 4 | 0.085113 | 46.477371 |

This resulted in more maximal author sets (as expected) but also larger maximal authors sets. Our algorithm does not find any maximal author sets with `k>17`. But given the fast execution time we can assume these do not exists with support larger than 3.

#### Dataset Large

Running with flag `--treshold 25` gives us these results:

| k | Author Set | Support |# Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|---------------------|------------------|---------------------|
| 1 | H. Vincent Poor | 906 | 41125 | 0.326388 | 0.326388 |
| 2 | Tomoya Enokido, Makoto Takizawa 0001 | 242 | 7044 | 2.190252 | 2.516639 |
| 3 | Hiroshi G. Okuno, Kazunori Komatani, Tetsuya Ogata | 122 | 843 | 0.927813 | 3.444453 |
| 4 | Arnaud Virazel, Alberto Bosio, Luigi Dilillo, Patrick Girard 0001 | 53 | 157 | 0.405572 | 3.850024 |
| 5 | Margaret J. Wright, Arthur W. Toga, Katie McMahon, Greig I. de Zubicaray, Paul M. Thompson | 44 | 41 | 0.214771 | 4.064795 |
| 6 | Manuel Ramos Cabrer, Ana Fernández Vilas, Jorge García Duque, Alberto Gil-Solla, José Juan Pazos-Arias, Rebeca P. Díaz Redondo | 31 | 6 | 0.110383 | 4.175178|

The Apriori implementation found every maximal authorset with treshold set to 25. This is again better and faster than the naive implementation. But we also tried with a lower treshold value. 

Running with flag `--treshold 10` gives us:

| k | Author Set | Support |# Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|---------------------|------------------|---------------------|
| 1 | H. Vincent Poor | 906 | 121897 | 0.361983 | 0.361983 |
| 2 | Makoto Takizawa 0001, Tomoya Enokido | 242 | 58538 | 4.334162 | 4.696145 |
| 3 | Kazunori Komatani, Hiroshi G. Okuno, Tetsuya Ogata | 122 | 13434 | 2.233520 | 6.929665 |
| 4 | Luigi Dilillo, Alberto Bosio, Patrick Girard 0001, Arnaud Virazel | 53 | 3782 | 0.653010 | 7.582675 |
| 5 | Arthur W. Toga, Katie McMahon, Margaret J. Wright, Paul M. Thompson, Greig I. de Zubicaray | 44 | 1719 | 0.280215 | 7.862890 |
| 6 | Alberto Gil-Solla, Ana Fernández Vilas, Rebeca P. Díaz Redondo, Manuel Ramos Cabrer, Jorge García Duque, José Juan Pazos-Arias | 31 | 827 | 0.145842 | 8.008732 |
| 7 | Alberto Gil-Solla, Ana Fernández Vilas, Rebeca P. Díaz Redondo, Martín López Nores, Manuel Ramos Cabrer, Jorge García Duque, José Juan Pazos-Arias | 25 | 301 | 0.072122 | 8.080854 |
| 8 | Alberto Gil-Solla, Ana Fernández Vilas, Yolanda Blanco-Fernández, Rebeca P. Díaz Redondo, Martín López Nores, Manuel Ramos Cabrer, Jorge García Duque, José Juan Pazos-Arias | 20 | 68 | 0.044415 | 8.125269 |
| 9 | Sebastiano Fabio Schifano, Enzo Marinari, Victor Martin-Mayor, Juan Jesus Ruiz-Lorenzo, Alfonso Tarancón, Sergio Perez Gaviro, Denis Navarro, Raffaele Tripiccione, Andrea Maiorano | 11 | 7 | 0.029653 | 8.154922 |

#### Dataset ALL

The moment of truth, the largest dataset. When we ran this on our first attempt when the default implementation worked, we got a runtime of about 20 minutes. But after rigorously optimizing the code we got down to just under 50 seconds.

Running with flag `--treshold 25` gives us these results:

| k | Author Set | Support |# Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|---------------------|------------------|---------------------|
| 1 | H. Vincent Poor | 2986 | 174653 | 1.296617 | 1.296617 |
| 2 | Makoto Takizawa 0001, Tomoya Enokido | 531 | 55802 | 18.074362 | 19.370979 |
| 3 | Min Zhang 0006, Yiqun Liu 0001, Shaoping Ma | 282 | 10415 | 6.171474 | 25.542453 |
| 4 | Ramon Casellas, Ricardo Martínez 0001, Raul Muñoz 0001, Ricard Vilalta | 149 | 5400 | 2.486111 | 28.028564 |
| 5 | David Bestor, Peter Michaleas, Matthew Hubbell, Jeremy Kepner, Albert Reuther | 100 | 10553 | 1.572462 | 29.601026 |
| 6 | David Bestor, Peter Michaleas, Matthew Hubbell, Jeremy Kepner, Albert Reuther, Andrew Prout | 98 | 21769 | 2.597004 | 32.198030 |
| 7 | Antonio Rosa, David Bestor, Peter Michaleas, Matthew Hubbell, Jeremy Kepner, Albert Reuther, Andrew Prout | 96 | 36032 | 1.804431 | 34.002461 |
| 8 | Antonio Rosa, David Bestor, Jeremy Kepner, Matthew Hubbell, Chansup Byun, Peter Michaleas, Albert Reuther, Andrew Prout | 94 | 47021 | 2.387933 | 36.390394 |
| 9 | Antonio Rosa, David Bestor, Chansup Byun, Jeremy Kepner, Peter Michaleas, Matthew Hubbell, William Arcand, Albert Reuther, Andrew Prout | 92 | 48371 | 2.703247 | 39.093642 |
| 10 | Vijay Gadepally, Antonio Rosa, David Bestor, Peter Michaleas, Matthew Hubbell, Jeremy Kepner, Chansup Byun, William Arcand, Albert Reuther, Andrew Prout | 83 | 39091 | 2.616066 | 41.709708 |
| 11 | Vijay Gadepally, Antonio Rosa, David Bestor, Chansup Byun, Jeremy Kepner, Peter Michaleas, Matthew Hubbell, Charles Yee, William Arcand, Albert Reuther, Andrew Prout | 79 | 24589 | 2.064556 | 43.774264 |
| 12 | Vijay Gadepally, Antonio Rosa, David Bestor, Chansup Byun, Matthew Hubbell, Peter Michaleas, Jeremy Kepner, Lauren Milechin, William Arcand, Albert Reuther, Michael Jones 0001, Andrew Prout | 69 | 11841 | 1.284280 | 45.058544 |
| 13 | Vijay Gadepally, Antonio Rosa, David Bestor, Chansup Byun, Matthew Hubbell, Siddharth Samsi, Jeremy Kepner, Lauren Milechin, Peter Michaleas, William Arcand, Albert Reuther, Michael Jones 0001, Andrew Prout | 65 | 4253 | 0.646402 | 45.704945 |
| 14 | Vijay Gadepally, Antonio Rosa, David Bestor, Chansup Byun, Matthew Hubbell, Peter Michaleas, Lauren Milechin, Siddharth Samsi, Charles Yee, Jeremy Kepner, William Arcand, Albert Reuther, Michael Jones 0001, Andrew Prout | 61 | 1095 | 0.267673 | 45.972619 |
| 15 | Vijay Gadepally, Antonio Rosa, David Bestor, Chansup Byun, Matthew Hubbell, Peter Michaleas, Lauren Milechin, Jeremy Kepner, Charles Yee, Siddharth Samsi, William Arcand, Albert Reuther, Michael Jones 0001, Andrew Prout, Julie Mullen | 51 | 190 | 0.093067 | 46.065685 |
| 16 | Vijay Gadepally, Anna Klein, Antonio Rosa, David Bestor, Chansup Byun, Jeremy Kepner, Matthew Hubbell, Peter Michaleas, Lauren Milechin, Siddharth Samsi, Charles Yee, William Arcand, Albert Reuther, Michael Jones 0001, Andrew Prout, Julie Mullen | 40 | 20 | 0.041125 | 46.106811 |
| 17 | Vijay Gadepally, Anna Klein, Antonio Rosa, David Bestor, Chansup Byun, Jeremy Kepner, Matthew Hubbell, Peter Michaleas, Lauren Milechin, Siddharth Samsi, Charles Yee, William Arcand, Albert Reuther, Michael Jones 0001, Andrew Prout, Michael Houle 0001, Julie Mullen | 26 | 1 | 0.026387 | 46.133198 |

But we also wanted to know how low we could set the treshold and still compute `k=17` in the bounds of the given assigment, which was 15 minutes. To our surprise this was not as straightforward as we thought. When using a treshold of 13 we got a runtime of wel over 20 minutes (we stopped the program by this point) but using a treshold of 14 got us less than 2 minutes. So here are the results of `--treshol 14`:

| k | Author Set | Support |# Maximal Author Sets| Time Elapsed (s) | Cumulative Time (s) |
|---|------------|---------|---------------------|------------------|---------------------|
| 1 | H. Vincent Poor | 2986 | 313049 | 1.450663 | 1.450663 |
| 2 | Tomoya Enokido, Makoto Takizawa 0001 | 531 | 180019 | 25.823299 | 27.273962 |
| 3 | Min Zhang 0006, Yiqun Liu 0001, Shaoping Ma | 282 | 49344 | 16.048799 | 43.322762 |
| 4 | Raul Muñoz 0001, Ricardo Martínez 0001, Ricard Vilalta, Ramon Casellas | 149 | 20861 | 5.163861 | 48.486622 |
| 5 | Jeremy Kepner, Matthew Hubbell, Albert Reuther, Peter Michaleas, David Bestor | 100 | 26329 | 4.488417 | 52.975039 |
| 6 | Matthew Hubbell, Albert Reuther, Peter Michaleas, David Bestor, Andrew Prout, Jeremy Kepner | 98 | 48238 | 2.531082 | 55.506121 |
| 7 | Antonio Rosa, Matthew Hubbell, Albert Reuther, Peter Michaleas, David Bestor, Andrew Prout, Jeremy Kepner | 96 | 79769 | 3.387000 | 58.893121 |
| 8 | Antonio Rosa, William Arcand, Matthew Hubbell, Albert Reuther, Peter Michaleas, David Bestor, Andrew Prout, Jeremy Kepner | 94 | 108550 | 4.494584 | 63.387705 |
| 9 | Antonio Rosa, William Arcand, Chansup Byun, Jeremy Kepner, Matthew Hubbell, Albert Reuther, Peter Michaleas, Andrew Prout, David Bestor | 92 | 119735 | 5.339214 | 68.726919 |
| 10 | Antonio Rosa, William Arcand, Chansup Byun, Jeremy Kepner, Matthew Hubbell, Vijay Gadepally, Albert Reuther, Peter Michaleas, Andrew Prout, David Bestor | 83 | 106694 | 5.658954 | 74.385873 |
| 11 | Antonio Rosa, Charles Yee, William Arcand, Chansup Byun, Matthew Hubbell, Vijay Gadepally, Albert Reuther, Peter Michaleas, David Bestor, Andrew Prout, Jeremy Kepner | 79 | 76507 | 4.894688 | 79.280562 |
| 12 | Antonio Rosa, William Arcand, Chansup Byun, Jeremy Kepner, Matthew Hubbell, Vijay Gadepally, Lauren Milechin, Albert Reuther, Peter Michaleas, Andrew Prout, Michael Jones 0001, David Bestor | 69 | 43808 | 3.236356 | 82.516918 |
| 13 | Antonio Rosa, Charles Yee, William Arcand, Chansup Byun, Jeremy Kepner, Matthew Hubbell, Vijay Gadepally, Lauren Milechin, Albert Reuther, Peter Michaleas, Andrew Prout, Michael Jones 0001, David Bestor | 65 | 19764 | 1.805939 | 84.322857 |
| 14 | Antonio Rosa, William Arcand, Charles Yee, Chansup Byun, Jeremy Kepner, Siddharth Samsi, Matthew Hubbell, Vijay Gadepally, Lauren Milechin, Albert Reuther, Peter Michaleas, Andrew Prout, Michael Jones 0001, David Bestor | 61 | 6875 | 0.831641 | 85.154498 |
| 15 | Antonio Rosa, Charles Yee, William Arcand, Chansup Byun, Jeremy Kepner, Siddharth Samsi, Julie Mullen, Matthew Hubbell, Vijay Gadepally, Lauren Milechin, Albert Reuther, Peter Michaleas, Andrew Prout, Michael Jones 0001, David Bestor | 51 | 1781 | 0.309170 | 85.463668 |
| 16 | Antonio Rosa, Charles Yee, William Arcand, Chansup Byun, Jeremy Kepner, Siddharth Samsi, Julie Mullen, Matthew Hubbell, Vijay Gadepally, Lauren Milechin, Albert Reuther, Peter Michaleas, Anna Klein, Andrew Prout, Michael Jones 0001, David Bestor | 40 | 324 | 0.099175 | 85.562844 |
| 17 | Antonio Rosa, Charles Yee, William Arcand, Chansup Byun, Jeremy Kepner, Siddharth Samsi, Julie Mullen, Michael Houle 0001, Matthew Hubbell, Vijay Gadepally, Lauren Milechin, Albert Reuther, Peter Michaleas, Anna Klein, Andrew Prout, Michael Jones 0001, David Bestor | 26 | 37 | 0.040799 | 85.603642 |
| 18 | Antonio Rosa, Charles Yee, William Arcand, Chansup Byun, Jeremy Kepner, Siddharth Samsi, Julie Mullen, Michael Houle 0001, Matthew Hubbell, Vijay Gadepally, Lauren Milechin, Bill Bergeron, Peter Michaleas, Anna Klein, Andrew Prout, Albert Reuther, Michael Jones 0001, David Bestor | 17 | 2 | 0.023784 | 85.627426 |

## Conclusion

Apriori is definitely more efficient and effective in finding frequent item sets than the naive approach. But we also notices that larger datasets are more difficult for the algorithm, especially in finding frequent pairs. But to reflect on our implementation:

- relatively fast (< 50 seconds for `all dataset`)
- efficient in memory (a lot of pruning)
- optimized for special cases (`k=1`, `k=2`)

We are very happy with our final implementation of the assigment.