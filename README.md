# ecthr_prediction
The ECTHR Prediction app, a Flask/Python webapp, applies human centered design principles to the European Court of Human Rights to make human rights accessible to people that lack financial resources and do not have professional legal experience. 

This app has three main fucntionalities: Issue Identifior, Predictor and the Search

## Issue Identifior


## Predictor
A multilabel classifier, fine tuned on the Hugging Face: lex_glue, ecthr_a dataset, to output a multi-label classifier for 10 labels. The 10 labels relate to the following human rights articles pursuant to the European Convention on Human Rights : [FILL IN ARTICLES]. The model is trained on 11k sequences that correspond to the 'facts' section of 11k cases from the European Court of Human Rights. The output probabilities a confidence score of whether a label can be associated with the input query from the Issue Identifior.  

The Predictor comes with two models, one where trunction is set to 512 tokens (RoBerta) and the second implements a sliding window technique to allow for a varying sequenth length that accepts all sequences lengths (Bert). The f1 scores are provided in the following file [FILL IN FILE]. 

To note, the RoBerta Model was chosen as all academic articles across the board, identified this model as producing the most accurate results for a multilabel classification exercise. We agree with this finding as it has beaten out BigBird, Bert, and HIER-Bert. The academic sources can be found below. 

## Search 


## Planned Improvements

### Dataset 

Firstly, we will expand the dataset from the Huggingface Publicly Available, lex_glue, dataset to the My-Rights Dataset. This will have the following benefits:
- Expand the number of cases from 11k cases to roughly 30k cases;
- Expand the number of human rights articles from 11 to all the substantive human rights articles of 24;
- Account for numerous underlying labelling and text issues in the dataset that are due to HUDOC (the ECtHR's official database) itself;
- Conduct NER and RegEx to remove spurious statistical patterns; and
- Create balanced datasets for testing.  

### Issue Identifior Improvements

We will move from the Chat GPT4 API to seq2seq T5 model that reformulate a user's input query, which will be in simple language, to text that is styled as a legal fact. This model will be fine tuned on the new dataset.

To create training pairs for the model, we plan to utilise Chat GPT4 API, with various temperature settings, to create the necessary pairs. Specifically, we will input actual legal facts and ask the model to generate simple language versions of the facts. The training pairs will assist the model in converting simple language commands to legal styled facts. 

The following provides an example of the way we would conduct the finetuning of the Issue Identifior: 

For example, these are the facts of a randomly selected ECTHR case: 

"The applicants complained that the authorities had failed to take adequate steps to protect the life of their family member, C.C., who had died of a drug overdose while being held in police custody."

Using a system prompt of: "Please rephrase the following legal statement in very simple language for someone who isn't familiar with legal terms. Create 5 different formulations of the simple language." 

The above provided:
1. The family says the police didn't keep C.C. safe, and he died from taking too many drugs.
2. C.C. took too many drugs and died while with the police. His family is upset about it.
3. C.C. was with the police when he died from drugs. His family thinks the police could have helped.
4. The police had C.C., and he died because of drugs. His family is sad and blames the police.
5. While C.C. was in jail, he died from drugs. His family says it's the police's fault.

The output provided is clearly written for a non-expert audience and will assist in reformulating user queries. 


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

