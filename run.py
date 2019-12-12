from textgenrnn import textgenrnn
import wikipedia
from googletrans import Translator

model_cfg = {
    'rnn_size': 128,
     'rnn_layers': 4,
     'rnn_bidirectional': True,
     'max_lenght': 40,
     'max_words': 10000,
     'dim_embeddings': 100,
     'word_level': 100
}
train_cfg = {
    'line_delimited': False,
    'num_epochs': 10,
    'gen_epochs': 2,
    'batch_size': 1024,
    'train_size': 0.8,
    'dropout': 0.0,
    'max_gen_lenght': 300,
    'validation': False,
    'is_csv': False
}

# translator = Translator()

# with open('traine.txt', 'r') as b:
#     print(translator.translate(b.read(), dest='pt'))
# with open('traine.txt', 'w') as f:
#     f.write(wikipedia.summary('michael jackson'))
textgen = textgenrnn()
textgen.train_from_file('bible.txt', num_epochs=1)
textgen.generate()
# textgen_2 = textgenrnn('textgenrnn_weights.hdf5')
# textgen_2.generate(3, temperature=1.0)
# translator.translate
