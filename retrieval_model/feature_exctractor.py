import numpy as np
import os
import tensorflow as tf
import tensorflow_hub as hub


class SentenceEncoder:
    def __init__(self, module_url=""):
        self.module_url = module_url
        self.model = self.load()

    def load(self):
        embed = hub.load(self.module_url)
        return embed

    def encode(self, sentences, save=False, file_name="questions_embeddings"):
        encoded = self.model(sentences)["outputs"]
        if save:
            print("Saving the embeddings ....")
            np.save(file_name, questions_norm)
            print("Saving done ....")

        return encoded

    def find_closest_k_questions(self, topk, query_vect, questions_embeddings, questions_norm=""):
        if questions_norm == "":
            print("Calculating and saving the norm of the embeddings ....")
            questions_norm = np.linalg.norm(questions_embeddings, axis=1)
            np.save("questions_square_norm", questions_norm)
            print("Saving done ....")

        score = np.sum(query_vect * questions_embeddings,
                       axis=1) / questions_norm
        topk_idx = np.argsort(score)[::-1][:topk]
        return topk_idx, score
