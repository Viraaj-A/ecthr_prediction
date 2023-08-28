# ecthr_prediction
The ECTHR Prediction app, a Flask/Python webapp, applies human centered design principles to the European Court of Human Rights to make human rights accessible to people that lack financial resources and do not have professional legal experience. 


This app has three main fucntionalities: 

Issue Identifior: A seq2seq T5 model that reformulate a user's input query, which will be in simple language, to text that is styled as a legal fact. This model will be fine tuned on the Hugging Face: lex_glue, ecthr_a dataset to create a factual reformulation that is in style with the European Court of Human Rights writing. 

Predictor: A Roberta Model, fine tuned on the Hugging Face: lex_glue, ecthr_a dataset, to output a multi-label classifier for 10 labels. The 10 labels relate to the following human rights articles pursuant to the European Convention on Human Rights : [FILL IN ARTICLES]. The model is trained on 11k sequences that correspond to the 'facts' section of 11k cases from the European Court of Human Rights. The output probabilities a confidence score of whether a label can be associated with the input query from the Issue Identifior.  

The Predictor comes with two models, one where trunction is set to 512 tokens and the second implements a sliding window technique to allow for a varying sequenth length that accepts all sequences lengths. The f1 scores are provided in the following file [FILL IN FILE]. 

Search: Implements semantic search with FAISS to provide contextualised results based on the query from the Issue Identifior. 

All language models are fine tuned on the 
