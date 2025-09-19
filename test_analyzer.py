"""
Тестов файл за Scopus Journal Analyzer
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Добавяме текущата директория към Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import ScopusJournalAnalyzer
from scopus_api import ScopusAPIClient, ScopusEnhancer

class TestScopusJournalAnalyzer(unittest.TestCase):
    """Тестове за основния анализатор"""
    
    def setUp(self):
        """Настройка за тестовете"""
        self.analyzer = ScopusJournalAnalyzer()
    
    def test_analyzer_initialization(self):
        """Тест за инициализация на анализатора"""
        self.assertIsNotNone(self.analyzer.scopus_criteria)
        self.assertIsNotNone(self.analyzer.scopus_keywords)
        self.assertEqual(len(self.analyzer.scopus_criteria), 6)
    
    def test_criteria_weights_sum(self):
        """Тест дали теглата на критериите са 1.0"""
        total_weight = sum(self.analyzer.scopus_criteria.values())
        self.assertAlmostEqual(total_weight, 1.0, places=2)
    
    def test_calculate_editorial_standards(self):
        """Тест за изчисляване на редакционни стандарти"""
        journal_data = {
            'editorial_board': [
                'Prof. John Smith, University of Cambridge',
                'Dr. Jane Doe, Harvard University',
                'Prof. Michael Johnson, MIT',
                'Dr. Sarah Wilson, Oxford University',
                'Prof. David Brown, Stanford University'
            ]
        }
        
        score = self.analyzer._calculate_editorial_standards(journal_data)
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_calculate_peer_review_score(self):
        """Тест за изчисляване на peer review оценка"""
        journal_data = {
            'peer_review_info': 'This journal uses double blind peer review process with 2-4 weeks review time.'
        }
        
        score = self.analyzer._calculate_peer_review_score(journal_data)
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_calculate_technical_standards(self):
        """Тест за изчисляване на технически стандарти"""
        journal_data = {
            'issn': '1234-5678',
            'doi_prefix': '10.1234',
            'url': 'https://example.com/journal',
            'title': 'Test Journal Title',
            'description': 'This is a test journal description with sufficient length for analysis.'
        }
        
        score = self.analyzer._calculate_technical_standards(journal_data)
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_analyze_content_quality(self):
        """Тест за анализ на качеството на съдържанието"""
        journal_data = {
            'peer_review_info': 'Peer review process documented',
            'editorial_board': ['Prof. A', 'Dr. B', 'Prof. C'],
            'issn': '1234-5678',
            'doi_prefix': '10.1234',
            'description': 'This is a comprehensive description of the journal with sufficient detail.'
        }
        
        result = self.analyzer._analyze_content_quality(journal_data)
        self.assertIn('content_quality_score', result)
        self.assertIn('content_quality_factors', result)
        self.assertGreater(result['content_quality_score'], 0)
    
    def test_analyze_international_scope(self):
        """Тест за анализ на международния обхват"""
        journal_data = {
            'languages': ['English', 'French'],
            'editorial_board': [
                'Prof. John Smith, University of Cambridge',
                'Dr. Marie Dubois, Sorbonne University'
            ],
            'open_access': True,
            'description': 'This is an international journal with global reach.'
        }
        
        result = self.analyzer._analyze_international_scope(journal_data)
        self.assertIn('international_scope_score', result)
        self.assertIn('international_scope_factors', result)
        self.assertGreater(result['international_scope_score'], 0)
    
    def test_analyze_accessibility(self):
        """Тест за анализ на достъпността"""
        journal_data = {
            'open_access': True,
            'url': 'https://example.com/journal',
            'publication_frequency': 'monthly'
        }
        
        result = self.analyzer._analyze_accessibility(journal_data)
        self.assertIn('accessibility_score', result)
        self.assertIn('accessibility_factors', result)
        self.assertGreater(result['accessibility_score'], 0)
    
    def test_calculate_scopus_readiness(self):
        """Тест за изчисляване на общата готовност за Scopus"""
        journal_data = {
            'peer_review_info': 'Double blind peer review',
            'editorial_board': [
                'Prof. John Smith, University of Cambridge',
                'Dr. Jane Doe, Harvard University',
                'Prof. Michael Johnson, MIT'
            ],
            'issn': '1234-5678',
            'doi_prefix': '10.1234',
            'languages': ['English'],
            'open_access': True,
            'url': 'https://example.com/journal',
            'title': 'Test Journal',
            'description': 'A comprehensive test journal description.'
        }
        
        # Добавяме оценките
        journal_data.update(self.analyzer._analyze_content_quality(journal_data))
        journal_data.update(self.analyzer._analyze_international_scope(journal_data))
        journal_data.update(self.analyzer._analyze_accessibility(journal_data))
        
        result = self.analyzer.calculate_scopus_readiness(journal_data)
        
        self.assertIn('total_score', result)
        self.assertIn('readiness_level', result)
        self.assertIn('detailed_scores', result)
        self.assertIn('recommendations', result)
        
        self.assertGreater(result['total_score'], 0)
        self.assertLessEqual(result['total_score'], 100)
        self.assertIsInstance(result['recommendations'], list)

class TestScopusAPIClient(unittest.TestCase):
    """Тестове за Scopus API клиента"""
    
    def setUp(self):
        """Настройка за тестовете"""
        self.api_client = ScopusAPIClient()
    
    def test_api_client_initialization(self):
        """Тест за инициализация на API клиента"""
        self.assertIsNotNone(self.api_client.base_url)
        self.assertIsNotNone(self.api_client.headers)
    
    def test_extract_subject_areas(self):
        """Тест за извличане на предметни области"""
        # Тест с лист от речници
        subject_areas_list = [
            {'$': 'Computer Science'},
            {'$': 'Mathematics'},
            {'$': 'Physics'}
        ]
        result = self.api_client._extract_subject_areas(subject_areas_list)
        self.assertEqual(len(result), 3)
        self.assertIn('Computer Science', result)
        
        # Тест с единичен речник
        subject_area_dict = {'$': 'Biology'}
        result = self.api_client._extract_subject_areas(subject_area_dict)
        self.assertEqual(len(result), 1)
        self.assertIn('Biology', result)
        
        # Тест с празен лист
        result = self.api_client._extract_subject_areas([])
        self.assertEqual(len(result), 0)

class TestScopusEnhancer(unittest.TestCase):
    """Тестове за Scopus подобрителя"""
    
    def setUp(self):
        """Настройка за тестовете"""
        self.enhancer = ScopusEnhancer()
    
    def test_enhancer_initialization(self):
        """Тест за инициализация на подобрителя"""
        self.assertIsNotNone(self.enhancer.api_client)
    
    def test_calculate_scopus_compatibility(self):
        """Тест за изчисляване на Scopus съвместимост"""
        journal_data = {
            'issn': '1234-5678',
            'languages': ['English'],
            'open_access': True,
            'editorial_board': [
                'Prof. A', 'Dr. B', 'Prof. C', 'Dr. D', 'Prof. E'
            ],
            'peer_review_info': 'Peer review process documented'
        }
        
        result = self.enhancer.calculate_scopus_compatibility(journal_data)
        
        self.assertIn('compatibility_score', result)
        self.assertIn('compatibility_factors', result)
        self.assertIn('scopus_ready', result)
        
        self.assertGreater(result['compatibility_score'], 0)
        self.assertLessEqual(result['compatibility_score'], 100)
        self.assertIsInstance(result['compatibility_factors'], list)

def run_tests():
    """Стартира всички тестове"""
    print("Започвам тестовете на Scopus Journal Analyzer...")
    
    # Създаваме test suite
    test_suite = unittest.TestSuite()
    
    # Добавяме тестовете
    test_suite.addTest(unittest.makeSuite(TestScopusJournalAnalyzer))
    test_suite.addTest(unittest.makeSuite(TestScopusAPIClient))
    test_suite.addTest(unittest.makeSuite(TestScopusEnhancer))
    
    # Стартираме тестовете
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Показваме резултатите
    print(f"\nОбщо тестове: {result.testsRun}")
    print(f"Успешни: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Неуспешни: {len(result.failures)}")
    print(f"Грешки: {len(result.errors)}")
    
    if result.failures:
        print("\nНеуспешни тестове:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nГрешки в тестовете:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

