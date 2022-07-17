# AutoMills


Alex; I'm currently working on the Mill's table file, I am trying to code in the Mill's table, so something like; if temp = 46 and rain hours >=18 then print '17 Days until Lesions' and code that in for
each temp in range. I am using this Mill's table as it is in farenheight, I will put a copy of it below:  https://extension.psu.edu/tree-fruit-disease-an-apple-scab-review

1-Temp  2-Wet	3-Lesion appearance
(°F)	(hours)	(days)
34	    41	    --
36	    35	    --
37	    30	    --
39	    28	    --
41	    21	    --
43	    18	    17
45	    15	    17
46	    13	    17
48	    12	    17
50	    11	    16
52	    9	    15
54-56	8	    14
57-59	7	    12-13
61-75	6	    9-10
77	    8	    --
79	    11	    --




This code is designed to implement the Mill's Apple Scab model on weather station data.

It is a work in progress...

Labeling: 

Label files according to what part of the project pipeline they will be in, for example; rain_events.py will deal with pulling out and processing rain events.
Label edited dataframe csv's so they can be indentified by their use, for example; rain_events.csv would be the data for rain_events.py
