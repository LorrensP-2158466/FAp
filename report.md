# Report Apriori Assigment


papers_per_author weet ik niet hoe ik dat moet doen

# ALL DONE ON MAC M1 2020 SEQUOIA 15.0

## Data Exploration

We hebben voor de data exploratie 5 technieken gebruikt, de 2 die wij gekregen hadden en nog 3 bijgevonden:

- Amount of Publications
- Average Amount of Authors Per Paper
- Unique Authors
- Average Paper per Author
- papers_per_author (WEET NOG NIET HOE DIT MOET UITGELEGD WORDEN)


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

## Naive implementation

### Dataset Tiny

| k  | Frequent Itemset                                                                                      | Frequency | Elapsed Time (seconds)       |
|----|-------------------------------------------------------------------------------------------------------|-----------|-----------------------------|
| 1  | {'Jan Van den Bussche'}                                                                                | 250       | 0.004987250002159271         |
| 2  | {'Dirk Van Gucht', 'Marc Gyssens'}                                                                     | 67        | 0.0012827909959014505        |
| 3  | {'Yuqing Wu', 'Dirk Van Gucht', 'Marc Gyssens'}                                                        | 25        | 0.0012156250013504177        |
| 4  | {'Yuqing Wu', 'George H. L. Fletcher', 'Dirk Van Gucht', 'Marc Gyssens'}                               | 14        | 0.0007752919991617091        |
| 5  | {'Stijn Vansummeren', 'Marc Gyssens', 'Dirk Van Gucht', 'Jan Van den Bussche', 'George H. L. Fletcher'} | 11        | 0.00046941699838498607       |
| 6  | {'Stijn Vansummeren', 'Yuqing Wu', 'Marc Gyssens', 'Dirk Van Gucht', 'Jan Van den Bussche', 'George H. L. Fletcher'} | 9 | 0.0002464580029482022 |
| 7  | {'Stijn Vansummeren', 'Yuqing Wu', 'Marc Gyssens', 'Dirk Van Gucht', 'Jan Van den Bussche', 'George H. L. Fletcher', 'Dirk Leinders'} | 6 | 0.00012433299707481638 |
| 8  | {'Stijn Vansummeren', 'Yuqing Wu', 'Marc Gyssens', 'Dimitri Surinx', 'Dirk Van Gucht', 'Jan Van den Bussche', 'George H. L. Fletcher', 'Dirk Leinders'} | 3 | 7.358300354098901e-05 |
| 9  | {'Marc Gyssens', 'Jan Paredaens', 'Marc Gemis', 'Dirk Van Gucht', 'Jan Van den Bussche', 'Inge Thyssens', 'Marc Andries', 'Vijay M. Sarathy', 'Lawrence V. Saxton'} | 1 | 0.00027599999884841964 |

### Dataset Medium 1

| k  | Frequent Itemset                                                                                      | Frequency | Elapsed Time (seconds)       |
|----|-------------------------------------------------------------------------------------------------------|-----------|-----------------------------|
| 1  | {'Moshe Y. Vardi'}                                                                                   | 762       | 0.032561250001890585         |
| 2  | {'Dirk Habich', 'Wolfgang Lehner'}                                                                    | 182       | 0.06798625000374159          |
| 3  | {'Diego Calvanese', 'Maurizio Lenzerini', 'Giuseppe De Giacomo'}                                   | 104       | 0.08565833299508085          |
| 4  | {'Diego Calvanese', 'Maurizio Lenzerini', 'Riccardo Rosati 0001', 'Giuseppe De Giacomo'}          | 37        | 0.0809505419965717           |
| 5  | {'Diego Calvanese', 'Maurizio Lenzerini', 'Riccardo Rosati 0001', 'Domenico Lembo', 'Giuseppe De Giacomo'} | 25 | 0.08720758400158957       |
| 6  | {'Dirk Fahland', 'Hajo A. Reijers', 'Matthias Weidlich 0001', 'Jan Mendling', 'Stefan Zugal', 'Barbara Weber'} | 11 | 0.06906675000209361 |
| 7  | {'Hajo A. Reijers', 'Dirk Fahland', 'Matthias Weidlich 0001', 'Stefan Zugal', 'Jan Mendling', 'Barbara Weber', 'Jakob Pinggera'} | 9 | 0.02401220799947623 |
| 8  | {'Chiara Di Francescomarino', 'Federico Chesani', 'Daniela Loreti', 'Fabrizio Maria Maggi', 'Chiara Ghidini', 'Sergio Tessaris', 'Marco Montali', 'Paola Mello'} | 6 | 0.008335000005899929 |
| 9  | {'Marc Denecker', 'Anthony Labarre', 'Jan Ramon', 'Sicco Verwer', 'Broes De Cat', 'Stef De Pooter', 'Maurice Bruynooghe', 'Hendrik Blockeel', 'Bart Bogaerts 0001'} | 3 | 0.002401416000793688 |
| 10 | {'Victor Marsault', 'Paolo Guagliardo', 'Filip Murlak', 'Nadime Francis', 'Amélie Gheerbrant', 'Wim Martens', 'Liat Peterfreund', 'Leonid Libkin', 'Domagoj Vrgoc', 'Alexandra Rogova'} | 3 | 0.0007103750031092204 |

### Dataset Medium 2

| k  | Frequent Itemset                                                                                       | Frequency | Elapsed Time (seconds)      |
|----|--------------------------------------------------------------------------------------------------------|-----------|-----------------------------|
| 1  | {'Noga Alon'}                                                                                        | 634       | 0.03433170900098048         |
| 2  | {'Dirk Habich', 'Wolfgang Lehner'}                                                                   | 184       | 0.12396804099989822         |
| 3  | {'Maurizio Lenzerini', 'Giuseppe De Giacomo', 'Diego Calvanese'}                                   | 104       | 1.487937083998986           |
| 4  | {'Maurizio Lenzerini', 'Riccardo Rosati 0001', 'Giuseppe De Giacomo', 'Diego Calvanese'}          | 37        | 28.862211291998392          |


### Dataset Large & ALL

MOETEN WE EENS DE TIJD VOOR NEMEN OM TE RUNNEN


## Apriori

### Dataset Tiny

Treshold used = 5

| k  | Frequent Itemset                                                                                                        | Frequency | Elapsed Time (seconds)      |
|----|-------------------------------------------------------------------------------------------------------------------------|-----------|------------------------------|
| 1  | {'Jan Van den Bussche'}                                                                                                   | 250       | 0.0011538329999893904        |
| 2  | {'Marc Gyssens', 'Dirk Van Gucht'}                                                                                      | 67        | 0.0014696250000270084        |
| 3  | {'Marc Gyssens', 'Yuqing Wu', 'Dirk Van Gucht'}                                                                        | 25        | 0.0012704999971901998        |
| 4  | {'George H. L. Fletcher', 'Marc Gyssens', 'Yuqing Wu', 'Dirk Van Gucht'}                                              | 14        | 0.0007554170006187633        |
| 5  | {'Dirk Van Gucht', 'Jan Van den Bussche', 'George H. L. Fletcher', 'Stijn Vansummeren', 'Marc Gyssens'}                | 11        | 0.0004532919992925599        |
| 6  | {'Dirk Van Gucht', 'Yuqing Wu', 'Jan Van den Bussche', 'George H. L. Fletcher', 'Stijn Vansummeren', 'Marc Gyssens'} | 9         | 0.00022116700711194426       |
| 7  | {'Dirk Van Gucht', 'Yuqing Wu', 'Dirk Leinders', 'Jan Van den Bussche', 'George H. L. Fletcher', 'Stijn Vansummeren', 'Marc Gyssens'} | 6         | 0.00011137499677715823       |

### Dataset Medium 1

treshold used = 5

| k  | Frequent Itemset                                                                                                       | Frequency | Elapsed Time (seconds)      |
|----|------------------------------------------------------------------------------------------------------------------------|-----------|------------------------------|
| 1  | {'Moshe Y. Vardi'}                                                                                                     | 762       | 0.00471391600149218          |
| 2  | {'Dirk Habich', 'Wolfgang Lehner'}                                                                                     | 182       | 0.037213166993751656         |
| 3  | {'Giuseppe De Giacomo', 'Maurizio Lenzerini', 'Diego Calvanese'}                                                    | 104       | 0.045612540998263285         |
| 4  | {'Riccardo Rosati 0001', 'Giuseppe De Giacomo', 'Maurizio Lenzerini', 'Diego Calvanese'}                            | 37        | 0.02187320800294401          |
| 5  | {'Maurizio Lenzerini', 'Giuseppe De Giacomo', 'Riccardo Rosati 0001', 'Domenico Lembo', 'Diego Calvanese'}         | 25        | 0.008955457997217309         |
| 6  | {'Stefan Zugal', 'Dirk Fahland', 'Hajo A. Reijers', 'Barbara Weber', 'Jan Mendling', 'Matthias Weidlich 0001'}    | 11        | 0.004225042001053225         |
| 7  | {'Stefan Zugal', 'Dirk Fahland', 'Jakob Pinggera', 'Hajo A. Reijers', 'Barbara Weber', 'Jan Mendling', 'Matthias Weidlich 0001'} | 9         | 0.0018953749968204647        |
| 8  | {'Daniela Loreti', 'Sergio Tessaris', 'Fabrizio Maria Maggi', 'Paola Mello', 'Federico Chesani', 'Chiara Di Francescomarino', 'Marco Montali', 'Chiara Ghidini'} | 6         | 0.0009790000040084124        |

### Dataset Medium 2

treshold used = 5

| k  | Frequent Itemset                                                                                                       | Frequency | Elapsed Time (seconds)      |
|----|------------------------------------------------------------------------------------------------------------------------|-----------|------------------------------|
| 1  | {'Noga Alon'}                                                                                                         | 634       | 0.005184000001463573         |
| 2  | {'Dirk Habich', 'Wolfgang Lehner'}                                                                                    | 184       | 0.044204249999893364         |
| 3  | {'Diego Calvanese', 'Giuseppe De Giacomo', 'Maurizio Lenzerini'}                                                  | 104       | 0.07484733299497748          |
| 4  | {'Diego Calvanese', 'Riccardo Rosati 0001', 'Giuseppe De Giacomo', 'Maurizio Lenzerini'}                          | 37        | 0.06122624999989057          |
| 5  | {'Maurizio Lenzerini', 'Diego Calvanese', 'Riccardo Rosati 0001', 'Domenico Lembo', 'Giuseppe De Giacomo'}       | 25        | 0.06486616699839942          |
| 6  | {'Matthias Weidlich 0001', 'Jan Mendling', 'Stefan Zugal', 'Dirk Fahland', 'Hajo A. Reijers', 'Barbara Weber'}    | 11        | 0.09268004200566793          |
| 7  | {'Matthias Weidlich 0001', 'Jan Mendling', 'Stefan Zugal', 'Hajo A. Reijers', 'Barbara Weber', 'Dirk Fahland', 'Jakob Pinggera'} | 9         | 0.07100958399678348          |
| 8  | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'Rob Byrom'} | 6         | 0.08745191699563293          |
| 9  | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'James Magowan', 'Roney Cordenonsi'} | 6         | 0.05942191700160038          |
| 10 | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'James Magowan', 'Roney Cordenonsi', 'Rob Byrom'} | 6         | 0.06484062499657739          |
| 11 | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'James Magowan', 'Roney Cordenonsi', 'Linda Cornwall', 'Rob Byrom'} | 6         | 0.018852208995667752         |
| 12 | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'James Magowan', 'Roney Cordenonsi', 'Linda Cornwall', 'Paul Taylor', 'Andrew W. Cooke'} | 6         | 0.008063125002081506         |
| 13 | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'Rob Byrom', 'James Magowan', 'Roney Cordenonsi', 'Linda Cornwall', 'Paul Taylor', 'Andrew W. Cooke', 'Antony J. Wilson'} | 6         | 0.0035864590026903898        |
| 14 | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'Rob Byrom', 'James Magowan', 'Roney Cordenonsi', 'Linda Cornwall', 'Paul Taylor', 'Andrew W. Cooke', 'Antony J. Wilson', 'Norbert Podhorszki'} | 6         | 0.0016556249975110404        |
| 15 | {'Steve Fisher', 'Werner Nutt', 'Steve Hicks', "David O'Callaghan", 'Brian A. Coghlan', 'Stuart Kenny', 'Abdeslem Djaoui', 'Rob Byrom', 'James Magowan', 'Roney Cordenonsi', 'Linda Cornwall', 'Paul Taylor', 'Andrew W. Cooke', 'Antony J. Wilson', 'Norbert Podhorszki'} | 6         | 0.0007391670005745254        |


### Dataset Large

treshold used = 25

| k  | Frequent Itemset                                                                                                       | Frequency | Elapsed Time (seconds)      |
|----|------------------------------------------------------------------------------------------------------------------------|-----------|------------------------------|
| 1  | {'H. Vincent Poor'}                                                                                                   | 906       | 0.30515120799827855          |
| 2  | {'Makoto Takizawa 0001', 'Tomoya Enokido'}                                                                           | 242       | 2.21516820800025             |
| 3  | {'Tetsuya Ogata', 'Kazunori Komatani', 'Hiroshi G. Okuno'}                                                         | 122       | 0.8413427920022514           |
| 4  | {'Arnaud Virazel', 'Patrick Girard 0001', 'Luigi Dilillo', 'Alberto Bosio'}                                        | 53        | 0.39790841699868906          |
| 5  | {'Margaret J. Wright', 'Katie McMahon', 'Arthur W. Toga', 'Greig I. de Zubicaray', 'Paul M. Thompson'}            | 44        | 0.2104743750023772           |
| 6  | {'Alberto Gil-Solla', 'Ana Fernández Vilas', 'José Juan Pazos-Arias', 'Manuel Ramos Cabrer', 'Rebeca P. Díaz Redondo', 'Jorge García Duque'} | 31        |  0.10827104099735152                         |


### Dataset ALL

kheb gene tijd sorryryyyyy