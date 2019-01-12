import unittest
import ChromosomeAtlas.LatexGenerator as LatexGen

class TestLatexGenerator(unittest.TestCase):

    SCIENTIFIC_NAME_TRANSFORM = {
       'A. graveolens L.': '{\\em A. graveolens} L.',
       'Acronema tenerum (DC.) Edgew.': '{\\em Acronema tenerum} (DC.) Edgew.',
       'Bupleurum candoleii Wall. Ex DC.': '{\\em Bupleurum candoleii} Wall. Ex DC.',
       'I. sikkimensis': '{\\em I. sikkimensis}',
       'Achyranthes aspera var. porphyristachya (Wall. ex Moq.) Hook. f.':
                '{\\em Achyranthes aspera} var. {\\em porphyristachya} (Wall. ex Moq.) Hook. f.',
        'Astragalus stipulatus var. phuchokiensis H. Ohashi':
                '{\\em Astragalus stipulatus} var. {\\em phuchokiensis} H. Ohashi'
    }

    def test_parse_scientific_name (self):
        lgen = LatexGen.LatexGenerator()
        for name in self.SCIENTIFIC_NAME_TRANSFORM.keys():
            transformed_name = lgen.parse_scientific_name(name) 
            self.assertEqual(self.SCIENTIFIC_NAME_TRANSFORM[name], transformed_name)
            
if __name__ == "__main__":
    unittest.main()