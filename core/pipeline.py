# core/pipeline.py
import pickle
from core.models import Submission, FeatureVector, SimilarityResult, Candidate
from data.collectors.codeforces.CodeforcesCollector import CodeforcesCollector
from data.repositories.result_repository import SimilarityResultRepository
from data.repositories.candidate_repository import SimilarityCandidateRepository
from parsing.encoder import ASTEncoder
from features.extractor import FeatureExtractor
from similarity.engine import SimilarityEngine
from ranking.scorer import Ranker
from core.config import CF_KEY, CF_SECRET
from logger_config import get_logger


#from report.generator import ReportGenerator



class Pipeline:

    def __init__(self):
        self.logger = get_logger(__name__) 
        self.collector = CodeforcesCollector(CF_KEY, CF_SECRET)
        self.ast_parser = ASTEncoder()
        self.feature_extractor = FeatureExtractor()
        self.engine = SimilarityEngine()
        self.result_repo = SimilarityResultRepository()
        self.rank_repo = SimilarityCandidateRepository()
        self.ranker = Ranker()
        self.logger.info("initialization successful")
        #self.report_generator = ReportGenerator()

    def run(self, contest_id: str, group_id: str):


        self.logger.info("start work with 'fetch_submissions'")
        
        self.collector.fetch_submissions(contest_id, group_id)
        
        self.logger.info("collect ast")
        dirty_features = self.ast_parser.encode()
        with open("stage_save.pkl", "wb") as f:
            pickle.dump(dirty_features, f)
            
        self.logger.info("ast collect and save")
        self.logger.info("feature in extraction")
        
        features = self.feature_extractor.extract(dirty_features)
        
        self.logger.info("feature is extract")
        
        results = self.engine.extract(features)
        self.result_repo.save_many(results)
        
        
        candidates = self.ranker.rate(results)
        self.rank_repo.save_many(candidates)
        self.logger.info("ranking is extract")

        return candidates