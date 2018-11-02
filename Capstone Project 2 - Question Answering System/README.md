# Capstone Project 2 - Question Answering System with the Dynamic Memory Network

## Background/Context
Question Answering is a topic in Natural Language Processing concerned with computers answering questions posed by humans in natural language.
There are 2 types of Question Answering (QA) systems: open-domain question answering and closed-domain question answering. Closed-domain question answering is concerned
with building systems that answer domain-specific questions, put differently, the system can only answer questions if they are can be found within the textual input
given to the model (of which the questions are asked). Thus the focus of this project is an attempt to build a 'working' textual closed-domain question answering system.
We implement the QA system as a Dynamic Memory Network. You can find out more about open-domain QA systems on the wikipedia page:
https://en.wikipedia.org/wiki/Question_answering 

## Files and their Meanings
- **Question Answering with the Dynamic Memory Network** - slide deck regarding the project.
- **Building the Models Train Final.ipynb** - the main Jupyter Notebook containing all of the project code
- **Data Wrangling.ipynb** - data wrangling code
- **Data** - folder containing the datasets used in the project (Stanford Question Answering Dataset)
- **attention_gru** - code for an attention-based GRU (more details on this in the Final Report)
- **EpisodicMemoryModule** - code for the Episodic Memory Module (more details in the final report)


## References/Influences of the Project

- https://arxiv.org/pdf/1506.07285.pdf This is the main paper to read the Dynamic Memory Network
- https://arxiv.org/pdf/1603.01417.pdf This is the 2nd paper released by the founders of the model.
- https://towardsdatascience.com/nlp-building-a-question-answering-model-ed0529a68c54 
- https://github.com/patrickachase/dynamic-memory-networks 
- https://github.com/vchudinov/dynamic_memory_networks_with_keras
- https://www.oreilly.com/ideas/question-answering-with-tensorflow
- https://nlp.stanford.edu/projects/glove/
- https://cs224d.stanford.edu/reports/StrohMathur.pdf
- https://github.com/JRC1995/Dynamic-Memory-Network-Plus/blob/master/DMN%2B.ipynb
