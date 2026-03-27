from core.models import FeatureVector

class FeatureExtractor:
    
    def __init__(self):
        self.features = dict() 
        
    def gen_feature(self, name: str, lang: str, submissions):
        
        for i in range(0, len(submissions['id'])):
            id = submissions['id'][i]
            code = submissions['code'][i]
            ast = submissions['ast'][i]
            yield FeatureVector(id, ast, code, len(code))
    
    def extract(self, submissions):
        features = dict()
                
        for name in submissions.keys():
            features[name] = dict()
            for lang in submissions[name].keys():
                features[name][lang] = list(self.gen_feature(name, lang, submissions[name][lang]))
        
        self.features = features
        
        return features
                
                    
                    
                