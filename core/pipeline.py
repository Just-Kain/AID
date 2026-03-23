# core/pipeline.py

from core.models import Submission, FeatureVector, SimilarityResult, Candidate
from data.collectors.codeforces.CodeforcesCollector import CodeforcesCollector
from parsing.ast.encoder import ASTEncoder
from features.extractor import FeatureExtractor
from similarity.engine import SimilarityEngine
from ranking.scorer import Ranker
#from report.generator import ReportGenerator

class Pipeline:
    def __init__(self):
        self.collector = CodeforcesCollector()
        self.ast_parser = ASTEncoder()
        self.feature_extractor = FeatureExtractor()
        self.similarity_engine = SimilarityEngine()
        self.ranker = Ranker()
        #self.report_generator = ReportGenerator()

    def run(self, contest_id: str, group_id: str, cf_key: str, cf_secret: str):
        # 1. Сбор данных
        submission = self.collector.fetch_submissions(contest_id, group_id, cf_key, cf_secret)

        # 2. Парсинг AST

        # 3. Извлечение признаков

        # 4. Вычисление сходства

        # 5. Ранжирование

        # 6. Генерация отчёта
        #self.report_generator.generate(candidates)
        pass
        #return candidates