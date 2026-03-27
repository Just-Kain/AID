# core/pipeline.py
import pickle
from core.models import Submission, FeatureVector, SimilarityResult, Candidate
from data.collectors.codeforces.CodeforcesCollector import CodeforcesCollector
from parsing.ast.encoder import ASTEncoder
from features.extractor import FeatureExtractor
from similarity.engine import SimilarityEngine
from ranking.scorer import Ranker
from core.config import CF_KEY, CF_SECRET
#from report.generator import ReportGenerator

class Pipeline:
    def __init__(self):
        self.collector = CodeforcesCollector(CF_KEY, CF_SECRET)
        self.ast_parser = ASTEncoder()
        self.feature_extractor = FeatureExtractor()
        #self.similarity_engine = SimilarityEngine()
        # self.ranker = Ranker()
        #self.report_generator = ReportGenerator()

    def run(self, contest_id: str, group_id: str):

        print("MESSAGE: start work with 'fetch_submissions'")
        self.collector.fetch_submissions(contest_id, group_id)
        
        print("MESSAGE: collect ast")
        dirty_features = self.ast_parser.ASTEncoder()
        with open("stage_save.pkl", "wb") as f:
            pickle.dump(dirty_features, f)
            
        print("MESSAGE: ast collect and save")
        print("MESSAGE: feature in extraction")
        
        self.feature_extractor.extract(dirty_features)
        
        print("MESSAGE: feature is extract")
        
        # 3. Извлечение признаков

        # 4. Вычисление сходства

        # 5. Ранжирование

        # 6. Генерация отчёта
        #self.report_generator.generate(candidates)
        pass
        #return candidates