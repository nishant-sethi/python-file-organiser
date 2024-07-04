#!/usr/bin/env python3

import numpy as np
from keras.applications.vgg16 import VGG16, preprocess_input # type: ignore
from keras.utils import load_img, img_to_array # type: ignore
from sklearn.metrics.pairwise import cosine_similarity # type: ignore

class ImageFeatureExtractor:
    def __init__(self, target_size=(224, 224)):
        self.target_size = target_size
        self.model = self.initialize_model()
        
    def initialize_model(self, input_shape=(224, 224, 3)):
        try:
            model = VGG16(weights='imagenet', include_top=False, pooling='max', input_shape=input_shape)
            # model.summary()
            print('Model initiatiated')
            return model
        except Exception as e:
            print('Something went wrong while initializing the model:', str(e))
            return None

    def preprocess_image(self, img_path):
        img = load_img(img_path, target_size=self.target_size)
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        return preprocess_input(x)

    def get_feature_embedding(self, img1=None, img2=None):
        try:
            feature_1 = self.model.predict(self.preprocess_image(img1))
            feature_2 = self.model.predict(self.preprocess_image(img2))
            return feature_1, feature_2
        except ValueError as e:
            print('Error occurred while getting features for images:', str(e))
            return None, None

    def similarity_score(self, feature_1, feature_2):
        return round(cosine_similarity(feature_1, feature_2)[0][0], 3)

    def get_similarity_score(self, img1, img2):
        feature_1, feature_2 = self.get_feature_embedding(img1, img2)
        if feature_1 is not None and feature_2 is not None:
            score = self.similarity_score(feature_1, feature_2)
            print('Similarity score:', score)
            return score