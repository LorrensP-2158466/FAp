# Report Apriori Assigment


papers_per_author weet ik niet hoe ik dat moet doen

# ALL DONE ON MAC M1 2020 SEQUOIA 15.0

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

### A Priori
...

## Implementation metrics

### Naive implementation

#### Dataset Tiny

| k  | Frequent Itemset                                                                                      | Frequency | Elapsed Time (seconds)       | Cumulative Time (seconds) |
|----|-------------------------------------------------------------------------------------------------------|-----------|-----------------------------|----------------------------|
| 1  | {'Jan Van den Bussche'}                                                                                | 250       | 0.004987250002159271         | 0.004987250002159271       |
| 2  | {'Dirk Van Gucht', 'Marc Gyssens'}                                                                     | 67        | 0.0012827909959014505        | 0.006270040998060721       |
| 3  | {'Yuqing Wu', 'Dirk Van Gucht', 'Marc Gyssens'}                                                        | 25        | 0.0012156250013504177        | 0.007485666999411139       |
| 4  | {'Yuqing Wu', 'George H. L. Fletcher', 'Dirk Van Gucht', 'Marc Gyssens'}                               | 14        | 0.0007752919991617091        | 0.008260958998572847       |
| 5  | {'Stijn Vansummeren', 'Marc Gyssens', 'Dirk Van Gucht', 'Jan Van den Bussche', 'George H. L. Fletcher'} | 11        | 0.00046941699838498607       | 0.008730375996957833       |
| 6  | {'Stijn Vansummeren', 'Yuqing Wu', 'Marc Gyssens', 'Dirk Van Gucht', 'Jan Van den Bussche', 'George H. L. Fletcher'} | 9 | 0.0002464580029482022 | 0.008976833999906035 |
| 7  | {'Stijn Vansummeren', 'Yuqing Wu', 'Marc Gyssens', 'Dirk Van Gucht', 'Jan Van den Bussche', 'George H. L. Fletcher', 'Dirk Leinders'} | 6 | 0.00012433299707481638 | 0.009101166996980851 |
| 8  | {'Stijn Vansummeren', 'Yuqing Wu', 'Marc Gyssens', 'Dimitri Surinx', 'Dirk Van Gucht', 'Jan Van den Bussche', 'George H. L. Fletcher', 'Dirk Leinders'} | 3 | 7.358300354098901e-05 | 0.00917474900052184 |
| 9  | {'Marc Gyssens', 'Jan Paredaens', 'Marc Gemis', 'Dirk Van Gucht', 'Jan Van den Bussche', 'Inge Thyssens', 'Marc Andries', 'Vijay M. Sarathy', 'Lawrence V. Saxton'} | 1 | 0.00027599999884841964 | 0.009450748999370259 |

#### Dataset Medium 1

| k   | Frequent Itemset                                                                                      | Frequency | Elapsed Time (seconds)       | Cumulative Time (seconds) |
|-----|-------------------------------------------------------------------------------------------------------|-----------|------------------------------|---------------------------|
| 1   | {'Moshe Y. Vardi'}                                                                                   | 762       | 0.032561250001890585         | 0.032561250001890585      |
| 2   | {'Dirk Habich', 'Wolfgang Lehner'}                                                                    | 182       | 0.06798625000374159          | 0.10054750000563217       |
| 3   | {'Diego Calvanese', 'Maurizio Lenzerini', 'Giuseppe De Giacomo'}                                   | 104       | 0.08565833299508085          | 0.18620583200071302       |
| 4   | {'Diego Calvanese', 'Maurizio Lenzerini', 'Riccardo Rosati 0001', 'Giuseppe De Giacomo'}          | 37        | 0.0809505419965717           | 0.2671563739972847        |
| 5   | {'Diego Calvanese', 'Maurizio Lenzerini', 'Riccardo Rosati 0001', 'Domenico Lembo', 'Giuseppe De Giacomo'} | 25 | 0.08720758400158957       | 0.35436395799887427       |
| 6   | {'Dirk Fahland', 'Hajo A. Reijers', 'Matthias Weidlich 0001', 'Jan Mendling', 'Stefan Zugal', 'Barbara Weber'} | 11 | 0.06906675000209361 | 0.42343070700096787 |
| 7   | {'Hajo A. Reijers', 'Dirk Fahland', 'Matthias Weidlich 0001', 'Stefan Zugal', 'Jan Mendling', 'Barbara Weber', 'Jakob Pinggera'} | 9 | 0.02401220799947623 | 0.4474429140004441  |
| 8   | {'Chiara Di Francescomarino', 'Federico Chesani', 'Daniela Loreti', 'Fabrizio Maria Maggi', 'Chiara Ghidini', 'Sergio Tessaris', 'Marco Montali', 'Paola Mello'} | 6 | 0.008335000005899929 | 0.45577791400634405 |
| 9   | {'Marc Denecker', 'Anthony Labarre', 'Jan Ramon', 'Sicco Verwer', 'Broes De Cat', 'Stef De Pooter', 'Maurice Bruynooghe', 'Hendrik Blockeel', 'Bart Bogaerts 0001'} | 3 | 0.002401416000793688 | 0.45817933000713774 |
| 10  | {'Victor Marsault', 'Paolo Guagliardo', 'Filip Murlak', 'Nadime Francis', 'Amélie Gheerbrant', 'Wim Martens', 'Liat Peterfreund', 'Leonid Libkin', 'Domagoj Vrgoc', 'Alexandra Rogova'} | 3 | 0.0007103750031092204 | 0.45888970501024695 |

#### Dataset Medium 2

| k   | Frequent Itemset                                                                                       | Frequency | Elapsed Time (seconds)      | Cumulative Time (seconds) |
|-----|--------------------------------------------------------------------------------------------------------|-----------|-----------------------------|---------------------------|
| 1   | {'Noga Alon'}                                                                                        | 634       | 0.03433170900098048         | 0.03433170900098048       |
| 2   | {'Dirk Habich', 'Wolfgang Lehner'}                                                                   | 184       | 0.12396804099989822         | 0.1582997490008787        |
| 3   | {'Maurizio Lenzerini', 'Giuseppe De Giacomo', 'Diego Calvanese'}                                   | 104       | 1.487937083998986           | 1.6462368329998647        |
| 4   | {'Maurizio Lenzerini', 'Riccardo Rosati 0001', 'Giuseppe De Giacomo', 'Diego Calvanese'}          | 37        | 28.862211291998392          | 30.508448124998256        |

#### Dataset Large & ALL

MOETEN WE EENS DE TIJD VOOR NEMEN OM TE RUNNEN


### Apriori

#### Dataset Tiny

Treshold used = 5

| k  | Frequent Itemset                                                                                                        | Frequency | Elapsed Time (seconds)      | Cumulative Time (seconds) |
|----|-------------------------------------------------------------------------------------------------------------------------|-----------|------------------------------|----------------------------|
| 1  | {'Jan Van den Bussche'}                                                                                                   | 250       | 0.0011538329999893904        | 0.0011538329999893904      |
| 2  | {'Marc Gyssens', 'Dirk Van Gucht'}                                                                                      | 67        | 0.0014696250000270084        | 0.0026234570000163988      |
| 3  | {'Marc Gyssens', 'Yuqing Wu', 'Dirk Van Gucht'}                                                                        | 25        | 0.0012704999971901998        | 0.0038939569972065986      |
| 4  | {'George H. L. Fletcher', 'Marc Gyssens', 'Yuqing Wu', 'Dirk Van Gucht'}                                              | 14        | 0.0007554170006187633        | 0.004649373997825362       |
| 5  | {'Dirk Van Gucht', 'Jan Van den Bussche', 'George H. L. Fletcher', 'Stijn Vansummeren', 'Marc Gyssens'}                | 11        | 0.0004532919992925599        | 0.005102665997117922       |
| 6  | {'Dirk Van Gucht', 'Yuqing Wu', 'Jan Van den Bussche', 'George H. L. Fletcher', 'Stijn Vansummeren', 'Marc Gyssens'} | 9         | 0.00022116700711194426       | 0.005323833004229866       |
| 7  | {'Dirk Van Gucht', 'Yuqing Wu', 'Dirk Leinders', 'Jan Van den Bussche', 'George H. L. Fletcher', 'Stijn Vansummeren', 'Marc Gyssens'} | 6         | 0.00011137499677715823       | 0.005435208000007024       |

#### Dataset Medium 1

treshold used = 5

| k  | Frequent Itemset                                                                                                       | Frequency | Elapsed Time (seconds)      | Cumulative Time (seconds) |
|----|------------------------------------------------------------------------------------------------------------------------|-----------|------------------------------|----------------------------|
| 1  | {'Moshe Y. Vardi'}                                                                                                     | 762       | 0.00471391600149218          | 0.00471391600149218        |
| 2  | {'Dirk Habich', 'Wolfgang Lehner'}                                                                                     | 182       | 0.037213166993751656         | 0.04192708299524384        |
| 3  | {'Giuseppe De Giacomo', 'Maurizio Lenzerini', 'Diego Calvanese'}                                                    | 104       | 0.045612540998263285         | 0.08753962399350713        |
| 4  | {'Riccardo Rosati 0001', 'Giuseppe De Giacomo', 'Maurizio Lenzerini', 'Diego Calvanese'}                            | 37        | 0.02187320800294401          | 0.10941283199645114        |
| 5  | {'Maurizio Lenzerini', 'Giuseppe De Giacomo', 'Riccardo Rosati 0001', 'Domenico Lembo', 'Diego Calvanese'}         | 25        | 0.008955457997217309         | 0.11836828999366845        |
| 6  | {'Stefan Zugal', 'Dirk Fahland', 'Hajo A. Reijers', 'Barbara Weber', 'Jan Mendling', 'Matthias Weidlich 0001'}    | 11        | 0.004225042001053225         | 0.12259333199472167        |
| 7  | {'Stefan Zugal', 'Dirk Fahland', 'Jakob Pinggera', 'Hajo A. Reijers', 'Barbara Weber', 'Jan Mendling', 'Matthias Weidlich 0001'} | 9         | 0.0018953749968204647        | 0.12448870699154213        |
| 8  | {'Daniela Loreti', 'Sergio Tessaris', 'Fabrizio Maria Maggi', 'Paola Mello', 'Federico Chesani', 'Chiara Di Francescomarino', 'Marco Montali', 'Chiara Ghidini'} | 6         | 0.0009790000040084124        | 0.12546770699555054        |

#### Dataset Medium 2

treshold used = 5

| k  | Frequent Itemset                                                                                                       | Frequency | Elapsed Time (seconds)      | Cumulative Time (seconds) |
|----|------------------------------------------------------------------------------------------------------------------------|-----------|------------------------------|----------------------------|
| 1  | {'Noga Alon'}                                                                                                         | 634       | 0.005184000001463573         | 0.005184000001463573       |
| 2  | {'Dirk Habich', 'Wolfgang Lehner'}                                                                                    | 184       | 0.044204249999893364         | 0.04938825000135694        |
| 3  | {'Diego Calvanese', 'Giuseppe De Giacomo', 'Maurizio Lenzerini'}                                                  | 104       | 0.07484733299497748          | 0.12423558299633443        |
| 4  | {'Diego Calvanese', 'Riccardo Rosati 0001', 'Giuseppe De Giacomo', 'Maurizio Lenzerini'}                          | 37        | 0.06122624999989057          | 0.185461832996225          |
| 5  | {'Maurizio Lenzerini', 'Diego Calvanese', 'Riccardo Rosati 0001', 'Domenico Lembo', 'Giuseppe De Giacomo'}       | 25        | 0.06486616699839942          | 0.25032799999462444        |
| 6  | {'Matthias Weidlich 0001', 'Jan Mendling', 'Stefan Zugal', 'Dirk Fahland', 'Hajo A. Reijers', 'Barbara Weber'}    | 11        | 0.09268004200566793          | 0.34300804199929236        |
| 7  | {'Matthias Weidlich 0001', 'Jan Mendling', 'Stefan Zugal', 'Hajo A. Reijers', 'Barbara Weber', 'Dirk Fahland', 'Jakob Pinggera'} | 9         | 0.07100958399678348          | 0.41401762599607584        |
| 8  | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'Rob Byrom'} | 6         | 0.08745191699563293          | 0.5014695429917088         |
| 9  | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'James Magowan', 'Roney Cordenonsi'} | 6         | 0.05942191700160038          | 0.5608914599933092         |
| 10 | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'James Magowan', 'Roney Cordenonsi', 'Rob Byrom'} | 6         | 0.06484062499657739          | 0.6257320849898866         |
| 11 | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'James Magowan', 'Roney Cordenonsi', 'Linda Cornwall', 'Rob Byrom'} | 6         | 0.018852208995667752         | 0.6445842939855544         |
| 12 | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'James Magowan', 'Roney Cordenonsi', 'Linda Cornwall', 'Paul Taylor', 'Andrew W. Cooke'} | 6         | 0.008063125002081506         | 0.6526474189876359         |
| 13 | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'Rob Byrom', 'James Magowan', 'Roney Cordenonsi', 'Linda Cornwall', 'Paul Taylor', 'Andrew W. Cooke', 'Antony J. Wilson'} | 6         | 0.0035864590026903898        | 0.6562338779903263         |
| 14 | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'Rob Byrom', 'James Magowan', 'Roney Cordenonsi', 'Linda Cornwall', 'Paul Taylor', 'Andrew W. Cooke', 'Antony J. Wilson', 'Norbert Podhorszki'} | 6         | 0.0016556249975110404        | 0.6578895029878373         |
| 15 | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'Rob Byrom', 'James Magowan', 'Roney Cordenonsi', 'Linda Cornwall', 'Paul Taylor', 'Andrew W. Cooke', 'Antony J. Wilson', 'Norbert Podhorszki'} | 6         | 0.0007391670005745254        | 0.6586286699884119         |

#### Dataset Large

treshold used = 25

| k  | Frequent Itemset                                                                                                       | Frequency | Elapsed Time (seconds)      | Cumulative Time (seconds) |
|----|------------------------------------------------------------------------------------------------------------------------|-----------|------------------------------|----------------------------|
| 1  | {'H. Vincent Poor'}                                                                                                   | 906       | 0.30515120799827855          | 0.30515120799827855        |
| 2  | {'Makoto Takizawa 0001', 'Tomoya Enokido'}                                                                           | 242       | 2.21516820800025             | 2.5203194159985285         |
| 3  | {'Tetsuya Ogata', 'Kazunori Komatani', 'Hiroshi G. Okuno'}                                                         | 122       | 0.8413427920022514           | 3.36166220700078           |
| 4  | {'Arnaud Virazel', 'Patrick Girard 0001', 'Luigi Dilillo', 'Alberto Bosio'}                                        | 53        | 0.39790841699868906          | 3.759570623999469          |
| 5  | {'Margaret J. Wright', 'Katie McMahon', 'Arthur W. Toga', 'Greig I. de Zubicaray', 'Paul M. Thompson'}            | 44        | 0.2104743750023772           | 3.9700450000018464         |
| 6  | {'Alberto Gil-Solla', 'Ana Fernández Vilas', 'José Juan Pazos-Arias', 'Manuel Ramos Cabrer', 'Rebeca P. Díaz Redondo', 'Jorge García Duque'} | 31        | 0.10827104099735152                         | 4.078316041999198           |

#### Dataset ALL

treshold used = 25

kheb gene tijd sorryryyyyy