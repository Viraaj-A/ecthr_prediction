# ecthr_prediction
The ECTHR Prediction app, a Flask/Python webapp, applies human centered design principles to the European Court of Human Rights to make human rights accessible to people that lack financial resources and do not have professional legal experience. 

This app has three main fucntionalities: Issue Identifior, Predictor and the Search

## Issue Identifior
A seq2seq T5 model that reformulate a user's input query, which will be in simple language, to text that is styled as a legal fact. This model will be fine tuned on the Hugging Face: lex_glue, ecthr_a dataset to create a factual reformulation that is in style with the European Court of Human Rights writing. 

## Predictor
A multilabel classifier, fine tuned on the Hugging Face: lex_glue, ecthr_a dataset, to output a multi-label classifier for 10 labels. The 10 labels relate to the following human rights articles pursuant to the European Convention on Human Rights : [FILL IN ARTICLES]. The model is trained on 11k sequences that correspond to the 'facts' section of 11k cases from the European Court of Human Rights. The output probabilities a confidence score of whether a label can be associated with the input query from the Issue Identifior.  

The Predictor comes with two models, one where trunction is set to 512 tokens (RoBerta) and the second implements a sliding window technique to allow for a varying sequenth length that accepts all sequences lengths (Bert). The f1 scores are provided in the following file [FILL IN FILE]. 

To note, the RoBerta Model was chosen as all academic articles across the board, identified this model as producing the most accurate results for a multilabel classification exercise. We agree with this finding as it has beaten out BigBird, Bert, and HIER-Bert. The academic sources can be found below. 

## Search 


## Planned Improvements

### Dataset 

Firstly, we will expand the dataset from the Huggingface Publicly Available, lex_glue, dataset to the My-Rights Dataset. This will have the following benefits:
- asdfadf

### Issue Identifior Improvements



### Predictor Improvements


### Search Improvements
The following improvements to the model are planned
1. Increase the dataset from the Huggingface Publicly Available library, which contains errors, to the My-Rights.info database that contains 3x the amount of cases and has corrected for underling data errors.
2. Conduct Named Entity Recognition and run multiple regex scripts to clean the dataset and improve bias scores, for examples, remove names of States that could lead to confounding issues for the Predictor and remove paragraph number labels, remove references to gender, remove references to specific religions.
3. Utilise multiple different language models to identify which model produces the best results at various sequence lenghts.
4. Link the questionnaire from the My-Rights.info website to the Prediction Tool to create one pathway for a user to identify their legal situation without having the need to know the law.
5. Convert the PostgreSQL full text search to  semantic search with FAISS to provide contextualised results based on the query from the Issue Identifior. As of late 2922,  FAISS is outperforming ElasticSearch and other vectir based search libraries, see the following for academic support to this finding: https://arxiv.org/pdf/2204.00820.pdf

## Academic Work Relied Upon

The ECTHR Prediction App, has been created from understanding and applying multiple leading academic sources, where the code base is not publicly available. The following freely accessible work has been relied upon:
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10130544
https://aclanthology.org/P19-1424/
https://aclanthology.org/2023.findings-eacl.44.pdf
https://aclanthology.org/2022.emnlp-main.74.pdf
https://ntnuopen.ntnu.no/ntnu-xmlui/bitstream/handle/11250/3033966/no.ntnu%3ainspera%3a112296943%3a24749335.pdf?sequence=1&isAllowed=y
https://arxiv.org/pdf/2110.00976v4.pdf
https://arxiv.org/pdf/2204.00820.pdf

Overall, the ECTHR Predictor App utilises state of the art mechanisms and the most upto date academic work to democratise legal prediction and search to ensure that people without sophisticated understanding can still access justice. 

