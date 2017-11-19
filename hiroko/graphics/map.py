import numpy as np
import time
import json
import cv2
import os


class Map:
    PTH = os.path.dirname(os.path.abspath(__file__)).split('hiroko')[0] + 'hiroko/data/sanitized/'
    MASK_FILE = 'mapa_color.png'
    DAY_COLOR_FILE = 'color_days.json'
    RELATION_COLOR_FILE = 'color_relations.json'

    @staticmethod
    def jread(filename):
        with open(Map.PTH + filename, 'rb') as jfile:
            jin = json.loads(jfile.read().decode('utf-8'))

        for k in jin.keys():
            jin[k] = np.array(jin[k], dtype=np.uint8)
        return jin

    @staticmethod
    def iread(filename):
        img = cv2.imread(Map.PTH + filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        return img

    def __init__(self, neigborhood_enumerator=None):
        # Retain data in memory to speed up the process
        self.mask = Map.iread(Map.MASK_FILE)
        self.day_colors = Map.jread(Map.DAY_COLOR_FILE)
        self.relation_colors = Map.jread(Map.RELATION_COLOR_FILE)
        self.coloring_enabled = True
        self.neigborhood_enumerator = neigborhood_enumerator

        if self.neigborhood_enumerator is None:
            self.coloring_enabled = False

        self.neighborholder = dict()
        if self.coloring_enabled:
            for k in self.relation_colors.keys():
                out = np.zeros(self.mask.shape, dtype=np.uint8)
                mask_color = self.relation_colors[k]
                out = np.all(self.mask == mask_color, axis=-1)
                out = np.stack([out, out, out], axis=2)
                out = out.astype(np.uint8)
                self.neighborholder[k] = out

    def colorMap(self, color_array=None):
        if not self.coloring_enabled:
            return

        color_array = [2] * 329
        t1 = time.time()
        out = np.zeros(self.mask.shape, dtype=np.uint8)
        if color_array is None:
            return self.mask
        for i in range(len(color_array)):
            color = self.day_colors[str(color_array[i])]
            out += self.neighborholder[self.neigborhood_enumerator[i].gis] * color
        print('Elapsed time:', time.time() - t1)
        return out
