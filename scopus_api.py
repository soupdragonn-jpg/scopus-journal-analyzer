"""
Scopus API интеграция за допълнителен анализ на списания
"""

import requests
import logging
from typing import Dict, List, Optional
from config import Config

logger = logging.getLogger(__name__)

class ScopusAPIClient:
    """Клиент за работа с Scopus API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.SCOPUS_API_KEY
        self.base_url = Config.SCOPUS_BASE_URL
        self.headers = {
            'Accept': 'application/json',
            'X-ELS-APIKey': self.api_key
        }
    
    def search_journal(self, journal_title: str, issn: str = None) -> Dict:
        """Търси списание в Scopus базата данни"""
        if not self.api_key:
            logger.warning("Scopus API ключ не е настроен")
            return {'error': 'API ключ не е наличен'}
        
        try:
            # Конструиране на заявката
            query_parts = [f'title("{journal_title}")']
            if issn:
                query_parts.append(f'issn({issn})')
            
            query = ' AND '.join(query_parts)
            
            params = {
                'query': query,
                'field': 'title,issn,subject-area,source-type,openaccess',
                'count': 25,
                'start': 0
            }
            
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._process_search_results(data)
            else:
                logger.error(f"Scopus API грешка: {response.status_code}")
                return {'error': f'API грешка: {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Грешка при търсене в Scopus: {e}")
            return {'error': str(e)}
    
    def _process_search_results(self, data: Dict) -> Dict:
        """Обработва резултатите от Scopus търсенето"""
        try:
            entries = data.get('search-results', {}).get('entry', [])
            
            if not entries:
                return {
                    'found': False,
                    'message': 'Списанието не е намерено в Scopus'
                }
            
            # Вземаме първия резултат (най-близкото съвпадение)
            journal = entries[0]
            
            return {
                'found': True,
                'scopus_id': journal.get('dc:identifier', '').replace('SCOPUS_ID:', ''),
                'title': journal.get('dc:title', ''),
                'issn': journal.get('prism:issn', ''),
                'subject_areas': self._extract_subject_areas(journal.get('subject-area', [])),
                'source_type': journal.get('prism:aggregationType', ''),
                'open_access': journal.get('openaccess', 0) == 1,
                'total_results': len(entries),
                'all_matches': entries[:5]  # Първите 5 съвпадения
            }
            
        except Exception as e:
            logger.error(f"Грешка при обработка на Scopus резултати: {e}")
            return {'error': str(e)}
    
    def _extract_subject_areas(self, subject_areas: List) -> List[str]:
        """Извлича предметните области от Scopus резултатите"""
        if isinstance(subject_areas, list):
            return [area.get('$', '') for area in subject_areas if isinstance(area, dict)]
        elif isinstance(subject_areas, dict):
            return [subject_areas.get('$', '')]
        return []
    
    def get_journal_metrics(self, scopus_id: str) -> Dict:
        """Получава метрики за списание от Scopus"""
        if not self.api_key or not scopus_id:
            return {'error': 'API ключ или Scopus ID не е наличен'}
        
        try:
            # Използваме Scopus Sources API за метрики
            sources_url = 'https://api.elsevier.com/content/serial/title'
            params = {
                'scopus_id': scopus_id,
                'field': 'title,issn,subject-area,metrics'
            }
            
            response = requests.get(
                sources_url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._process_metrics_data(data)
            else:
                logger.error(f"Scopus Sources API грешка: {response.status_code}")
                return {'error': f'API грешка: {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Грешка при получаване на метрики: {e}")
            return {'error': str(e)}
    
    def _process_metrics_data(self, data: Dict) -> Dict:
        """Обработва данните за метрики"""
        try:
            # Това е опростена обработка - реалната структура може да варира
            return {
                'metrics_available': True,
                'data': data
            }
        except Exception as e:
            logger.error(f"Грешка при обработка на метрики: {e}")
            return {'error': str(e)}
    
    def check_indexing_status(self, journal_data: Dict) -> Dict:
        """Проверява статуса на индексиране в Scopus"""
        title = journal_data.get('title', '')
        issn = journal_data.get('issn', '')
        
        if not title:
            return {'error': 'Заглавие на списанието е задължително'}
        
        # Търсим списанието в Scopus
        search_result = self.search_journal(title, issn)
        
        if search_result.get('error'):
            return search_result
        
        if search_result.get('found'):
            return {
                'indexed': True,
                'scopus_data': search_result,
                'recommendation': 'Списанието вече е индексирано в Scopus'
            }
        else:
            return {
                'indexed': False,
                'recommendation': 'Списанието не е намерено в Scopus. Може да се кандидатира за индексиране.'
            }

class ScopusEnhancer:
    """Клас за подобряване на анализа с данни от Scopus"""
    
    def __init__(self):
        self.api_client = ScopusAPIClient()
    
    def enhance_journal_analysis(self, journal_data: Dict) -> Dict:
        """Подобрява анализа на списанието с данни от Scopus"""
        enhanced_data = journal_data.copy()
        
        # Проверяваме статуса на индексиране
        indexing_status = self.api_client.check_indexing_status(journal_data)
        enhanced_data['scopus_indexing_status'] = indexing_status
        
        # Ако списанието е индексирано, получаваме допълнителни данни
        if indexing_status.get('indexed'):
            scopus_data = indexing_status.get('scopus_data', {})
            enhanced_data['scopus_metrics'] = scopus_data
            
            # Добавяме Scopus предметни области
            if scopus_data.get('subject_areas'):
                enhanced_data['scopus_subject_areas'] = scopus_data['subject_areas']
            
            # Добавяме Scopus ID
            if scopus_data.get('scopus_id'):
                enhanced_data['scopus_id'] = scopus_data['scopus_id']
        
        return enhanced_data
    
    def calculate_scopus_compatibility(self, journal_data: Dict) -> Dict:
        """Изчислява съвместимостта със Scopus стандартите"""
        compatibility_score = 0
        factors = []
        
        # Проверка за ISSN
        if journal_data.get('issn'):
            compatibility_score += 20
            factors.append("ISSN номер е наличен")
        
        # Проверка за английски език
        languages = journal_data.get('languages', [])
        if any('english' in lang.lower() for lang in languages):
            compatibility_score += 25
            factors.append("Английски език е включен")
        
        # Проверка за Open Access
        if journal_data.get('open_access'):
            compatibility_score += 15
            factors.append("Open Access модел")
        
        # Проверка за международен редакционен съвет
        editorial_board = journal_data.get('editorial_board', [])
        if len(editorial_board) >= 5:
            compatibility_score += 20
            factors.append(f"Редакционен съвет с {len(editorial_board)} членове")
        
        # Проверка за peer review
        if journal_data.get('peer_review_info'):
            compatibility_score += 20
            factors.append("Peer review процес е документиран")
        
        return {
            'compatibility_score': min(compatibility_score, 100),
            'compatibility_factors': factors,
            'scopus_ready': compatibility_score >= 70
        }
