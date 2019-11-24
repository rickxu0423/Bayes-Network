# Bayes-Network

use `python3 exact.py File Query Evidence` to run Exact Inference\
use `python3 sample.py N File Query Evidence` to run Rejection Sampling

**Please have fun with it!**

## argv:
1. Files: 
    ```
    aima-alarm.xml
    aima-wet-grass.xml
    dog-problem.xml
    ```
2. N: Any Integer
3. Query/Evidence: See XML files

## Test Example:
1. aima-alarm: 
```
python3 exact.py aima-alarm.xml B J true M true  
python3 sample.py 1000000 aima-alarm.xml B J true M true
```
2. aima-wet-grass: 
```
python3 exact.py aima-wet-grass.xml R S true W true
python3 sample.py 10000 aima-wet-grass.xml R S true W true
```
3. dog-problem: 
```
python3 exact.py dog-problem.xml light-on bowel-problem true hear-bark true
python3 sample.py 500000 dog-problem.xml light-on bowel-problem true hear-bark true
```

## Contributers:
    1. Name: Jiyun Xu
       NetID: 31425711
    2. Name: Yangyang Shao
       NetID: 31434102