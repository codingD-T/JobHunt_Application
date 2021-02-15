import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import nltk
nltk.download('punkt')
import pickle

class Vocabulary(object):
    """Simple vocabulary wrapper."""
    def __init__(self,vocab):
        self.word2idx = vocab

    def __call__(self, word):
        if not word in self.word2idx:
            return self.word2idx['<unk>']
        return self.word2idx[word]

    def __len__(self):
        return len(self.word2idx)

class Model(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers):
        super(Model, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True, bidirectional=True, dropout=0.3)
        self.relu = nn.ReLU()
        self.linear = nn.Linear(hidden_size * 2, 256)
        self.linear3 = nn.Linear(256, 19)

    def forward(self, captions):
        embeddings = self.embed(captions)
        hiddens, _ = self.lstm(embeddings)
        x = self.relu(self.linear(hiddens[:, -1, :]))
        outputs = self.linear3(x)
        return outputs
