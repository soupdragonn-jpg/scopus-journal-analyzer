"""
Scopus Journal Readiness Analyzer
Анализира научни списания за готовност за индексиране в Scopus
"""

import os
import re
import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

# Optional/Heavy deps (guarded)
HAVE_SELENIUM = False
try:
	from selenium import webdriver
	from selenium.webdriver.chrome.options import Options
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions as EC
	from selenium.common.exceptions import TimeoutException, WebDriverException
	HAVE_SELENIUM = True
except ImportError:
	# Selenium not available - will use requests only
	pass

# The following are not required on Render; mark optional
try:
	import pandas as pd  # noqa: F401
	import numpy as np   # noqa: F401
	from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: F401
	from sklearn.metrics.pairwise import cosine_similarity  # noqa: F401
	import matplotlib.pyplot as plt  # noqa: F401
	import seaborn as sns  # noqa: F401
except Exception:
	pass

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Зареждане на environment variables
load_dotenv()

# Настройка на logging
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s - %(message)s',
	handlers=[
		logging.FileHandler('scopus_analyzer.log'),
		logging.StreamHandler()
	]
)
logger = logging.getLogger(__name__)

class ScopusJournalAnalyzer:
	"""Основен клас за анализ на готовността на списания за Scopus"""
	
	def __init__(self):
		self.scopus_criteria = {
			'content_quality': 0.25,
			'editorial_standards': 0.20,
			'peer_review_process': 0.20,
			'international_scope': 0.15,
			'technical_standards': 0.10,
			'accessibility': 0.10
		}
		
		self.scopus_keywords = [
			'peer review', 'editorial board', 'international', 'academic',
			'research', 'scholarly', 'scientific', 'journal', 'publication',
			'impact factor', 'citation', 'indexing', 'abstract', 'keywords',
			'doi', 'issn', 'isbn', 'open access', 'subscription'
		]
		
		# Scopus API credentials (трябва да се настроят в .env файла)
		self.scopus_api_key = os.getenv('SCOPUS_API_KEY')
		self.scopus_base_url = 'https://api.elsevier.com/content/search/scopus'
		
	def setup_selenium_driver(self):
		"""Настройва Selenium WebDriver ако е наличен"""
		if not HAVE_SELENIUM:
			raise RuntimeError("Selenium не е наличен на текущия хостинг. Анализът ще продължи само с requests.")
		
		chrome_options = Options()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-dev-shm-usage')
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_argument('--window-size=1920,1080')
		chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
		
		try:
			driver = webdriver.Chrome(options=chrome_options)
			return driver
		except Exception as e:
			logger.error(f"Грешка при настройване на WebDriver: {e}")
			raise
	
	def extract_journal_data(self, url: str) -> Dict:
		"""Извлича данни от URL на списание"""
		logger.info(f"Започвам анализ на списание: {url}")
		
		journal_data = {
			'url': url,
			'title': '',
			'description': '',
			'editorial_board': [],
			'peer_review_info': '',
			'publication_frequency': '',
			'issn': '',
			'doi_prefix': '',
			'open_access': False,
			'languages': [],
			'subject_areas': [],
			'impact_metrics': {},
			'technical_standards': {},
			'accessibility_score': 0,
			'content_quality_score': 0,
			'international_scope_score': 0,
			'analysis_timestamp': datetime.now().isoformat()
		}
		
		try:
			# Първо опитваме с requests
			response = requests.get(url, timeout=30, headers={
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
			})
			response.raise_for_status()
			
			soup = BeautifulSoup(response.content, 'html.parser')
			
			# Извличане на основни данни
			journal_data.update(self._extract_basic_info(soup, url))
			journal_data.update(self._extract_editorial_info(soup))
			journal_data.update(self._extract_technical_info(soup))
			
			# Ако имаме нужда от JavaScript, използваме Selenium (само ако е наличен)
			if HAVE_SELENIUM and self._needs_selenium(soup):
				driver = self.setup_selenium_driver()
				try:
					driver.get(url)
					time.sleep(3)
					selenium_soup = BeautifulSoup(driver.page_source, 'html.parser')
					journal_data.update(self._extract_dynamic_content(selenium_soup))
				finally:
					driver.quit()
			
			# Анализ на качеството
			journal_data.update(self._analyze_content_quality(journal_data))
			journal_data.update(self._analyze_international_scope(journal_data))
			journal_data.update(self._analyze_accessibility(journal_data))
			
		except Exception as e:
			logger.error(f"Грешка при извличане на данни от {url}: {e}")
			journal_data['error'] = str(e)
		
		return journal_data
	
	def _extract_basic_info(self, soup: BeautifulSoup, url: str) -> Dict:
		"""Извлича основните данни за списанието"""
		data = {}
		
		# Заглавие
		title_selectors = ['h1', '.journal-title', '.page-title', 'title']
		for selector in title_selectors:
			title_elem = soup.select_one(selector)
			if title_elem and title_elem.get_text(strip=True):
				data['title'] = title_elem.get_text(strip=True)
				break
		
		# Описание
		desc_selectors = ['.description', '.about', '.journal-description', 'meta[name="description"]']
		for selector in desc_selectors:
			desc_elem = soup.select_one(selector)
			if desc_elem:
				if desc_elem.name == 'meta':
					data['description'] = desc_elem.get('content', '')
				else:
					data['description'] = desc_elem.get_text(strip=True)
				if data['description']:
					break
		
		# ISSN
		issn_pattern = r'ISSN[:\s]*(\d{4}-\d{3}[\dX])'
		text_content = soup.get_text()
		issn_match = re.search(issn_pattern, text_content, re.IGNORECASE)
		if issn_match:
			data['issn'] = issn_match.group(1)
		
		# DOI prefix
		doi_pattern = r'10\.\d{4,}'
		doi_match = re.search(doi_pattern, text_content)
		if doi_match:
			data['doi_prefix'] = doi_match.group(0)
		
		return data
	
	def _extract_editorial_info(self, soup: BeautifulSoup) -> Dict:
		"""Извлича информация за редакционния съвет"""
		data = {}
		
		# Редакционен съвет
		editorial_selectors = [
			'.editorial-board', '.editors', '.editorial-team',
			'.advisory-board', '.review-board'
		]
		
		editorial_members = []
		for selector in editorial_selectors:
			board_section = soup.select_one(selector)
			if board_section:
				members = board_section.find_all(['li', 'p', 'div'], string=re.compile(r'[A-Z][a-z]+ [A-Z][a-z]+'))
				for member in members:
					member_text = member.get_text(strip=True)
					if len(member_text.split()) >= 2:  # Име и фамилия
						editorial_members.append(member_text)
		
		data['editorial_board'] = list(set(editorial_members))  # Премахваме дубликати
		
		# Peer review информация
		peer_review_keywords = ['peer review', 'referee', 'review process', 'double blind']
		peer_review_text = ''
		
		for keyword in peer_review_keywords:
			elements = soup.find_all(string=re.compile(keyword, re.IGNORECASE))
			for element in elements:
				parent = element.parent
				if parent:
					peer_review_text += parent.get_text(strip=True) + ' '
		
		data['peer_review_info'] = peer_review_text.strip()
		
		return data
	
	def _extract_technical_info(self, soup: BeautifulSoup) -> Dict:
		"""Извлича техническа информация"""
		data = {}
		
		# Честота на публикуване
		frequency_keywords = ['monthly', 'quarterly', 'biannual', 'annual', 'weekly', 'daily']
		text_content = soup.get_text().lower()
		
		for freq in frequency_keywords:
			if freq in text_content:
				data['publication_frequency'] = freq
				break
		
		# Open Access
		oa_indicators = ['open access', 'creative commons', 'cc by', 'free access']
		data['open_access'] = any(indicator in text_content for indicator in oa_indicators)
		
		# Езици
		lang_pattern = r'language[s]?:[\s]*([A-Za-z\s,]+)'
		lang_match = re.search(lang_pattern, text_content, re.IGNORECASE)
		if lang_match:
			languages = [lang.strip() for lang in lang_match.group(1).split(',')]
			data['languages'] = languages
		
		return data
	
	def _needs_selenium(self, soup: BeautifulSoup) -> bool:
		"""Проверява дали е нужен Selenium за динамично съдържание"""
		if not HAVE_SELENIUM:
			return False
		# Проверяваме за JavaScript frameworks или динамично съдържание
		scripts = soup.find_all('script')
		for script in scripts:
			if script.string:
				if any(framework in script.string.lower() for framework in ['react', 'angular', 'vue', 'ajax']):
					return True
		# Проверяваме за елементи, които се зареждат динамично
		dynamic_selectors = ['.lazy-load', '[data-src]', '.dynamic-content']
		for selector in dynamic_selectors:
			if soup.select(selector):
				return True
		return False
	
	def _extract_dynamic_content(self, soup: BeautifulSoup) -> Dict:
		"""Извлича динамично съдържание с Selenium"""
		data = {}
		# Допълнителни данни, които могат да се зареждат динамично
		return data
	
	def _analyze_content_quality(self, journal_data: Dict) -> Dict:
		"""Анализира качеството на съдържанието"""
		score = 0
		factors = []
		
		# Проверка за рецензиране
		if journal_data.get('peer_review_info'):
			score += 30
			factors.append("Peer review процес е документиран")
		
		# Проверка за редакционен съвет
		if len(journal_data.get('editorial_board', [])) > 0:
			score += 25
			factors.append(f"Редакционен съвет с {len(journal_data['editorial_board'])} членове")
		
		# Проверка за ISSN
		if journal_data.get('issn'):
			score += 20
			factors.append("ISSN номер е наличен")
		
		# Проверка за DOI
		if journal_data.get('doi_prefix'):
			score += 15
			factors.append("DOI prefix е наличен")
		
		# Проверка за описание
		if journal_data.get('description') and len(journal_data['description']) > 100:
			score += 10
			factors.append("Подробно описание на списанието")
		
		return {
			'content_quality_score': min(score, 100),
			'content_quality_factors': factors
		}
	
	def _analyze_international_scope(self, journal_data: Dict) -> Dict:
		"""Анализира международния обхват на списанието"""
		score = 0
		factors = []
		
		# Проверка за многоезичност
		languages = journal_data.get('languages', [])
		if len(languages) > 1:
			score += 30
			factors.append(f"Многоезично списание: {', '.join(languages)}")
		elif 'english' in [lang.lower() for lang in languages]:
			score += 20
			factors.append("Английски език е включен")
		
		# Проверка за международни автори в редакционния съвет
		editorial_board = journal_data.get('editorial_board', [])
		international_indicators = ['university', 'college', 'institute', 'professor', 'dr.', 'phd']
		international_members = 0
		
		for member in editorial_board:
			if any(indicator in member.lower() for indicator in international_indicators):
				international_members += 1
		
		if international_members > 0:
			score += min(international_members * 5, 40)
			factors.append(f"{international_members} международни членове в редакционния съвет")
		
		# Проверка за Open Access
		if journal_data.get('open_access'):
			score += 20
			factors.append("Open Access списание")
		
		# Проверка за международни ключови думи в описанието
		description = journal_data.get('description', '').lower()
		international_keywords = ['international', 'global', 'worldwide', 'multinational']
		if any(keyword in description for keyword in international_keywords):
			score += 10
			factors.append("Международен фокус в описанието")
		
		return {
			'international_scope_score': min(score, 100),
			'international_scope_factors': factors
		}
	
	def _analyze_accessibility(self, journal_data: Dict) -> Dict:
		"""Анализира достъпността на списанието"""
		score = 0
		factors = []
		
		# Проверка за Open Access
		if journal_data.get('open_access'):
			score += 50
			factors.append("Open Access - безплатен достъп")
		
		# Проверка за онлайн достъпност
		url = journal_data.get('url', '')
		if url and url.startswith('https'):
			score += 20
			factors.append("HTTPS протокол за сигурност")
		
		# Проверка за мобилна съвместимост (базирано на URL структура)
		if any(indicator in url.lower() for indicator in ['mobile', 'responsive', 'm.']):
			score += 15
			factors.append("Мобилна съвместимост")
		
		# Проверка за честота на публикуване
		frequency = journal_data.get('publication_frequency', '')
		if frequency in ['monthly', 'quarterly']:
			score += 15
			factors.append(f"Регулярна публикация: {frequency}")
		
		return {
			'accessibility_score': min(score, 100),
			'accessibility_factors': factors
		}
	
	def calculate_scopus_readiness(self, journal_data: Dict) -> Dict:
		"""Изчислява общата готовност за Scopus"""
		
		# Вземаме оценките
		content_quality = journal_data.get('content_quality_score', 0)
		international_scope = journal_data.get('international_scope_score', 0)
		accessibility = journal_data.get('accessibility_score', 0)
		
		# Изчисляваме допълнителни оценки
		editorial_standards = self._calculate_editorial_standards(journal_data)
		peer_review_process = self._calculate_peer_review_score(journal_data)
		technical_standards = self._calculate_technical_standards(journal_data)
		
		# Обща оценка с тегла
		total_score = (
			content_quality * self.scopus_criteria['content_quality'] +
			editorial_standards * self.scopus_criteria['editorial_standards'] +
			peer_review_process * self.scopus_criteria['peer_review_process'] +
			international_scope * self.scopus_criteria['international_scope'] +
			technical_standards * self.scopus_criteria['technical_standards'] +
			accessibility * self.scopus_criteria['accessibility']
		)
		
		# Определяме готовността
		if total_score >= 80:
			readiness_level = "Високо готов"
		elif total_score >= 60:
			readiness_level = "Средно готов"
		elif total_score >= 40:
			readiness_level = "Ниско готов"
		else:
			readiness_level = "Не е готов"
		
		# Препоръки за подобрение
		recommendations = self._generate_recommendations(journal_data, {
			'content_quality': content_quality,
			'editorial_standards': editorial_standards,
			'peer_review_process': peer_review_process,
			'international_scope': international_scope,
			'technical_standards': technical_standards,
			'accessibility': accessibility
		})
		
		return {
			'total_score': round(total_score, 2),
			'readiness_level': readiness_level,
			'detailed_scores': {
				'content_quality': content_quality,
				'editorial_standards': editorial_standards,
				'peer_review_process': peer_review_process,
				'international_scope': international_scope,
				'technical_standards': technical_standards,
				'accessibility': accessibility
			},
			'recommendations': recommendations,
			'analysis_date': datetime.now().isoformat()
		}
	
	def _calculate_editorial_standards(self, journal_data: Dict) -> int:
		"""Изчислява оценката за редакционни стандарти"""
		score = 0
		
		# Редакционен съвет
		editorial_board = journal_data.get('editorial_board', [])
		if len(editorial_board) >= 10:
			score += 40
		elif len(editorial_board) >= 5:
			score += 25
		elif len(editorial_board) > 0:
			score += 15
		
		# Професионални титли в редакционния съвет
		professional_titles = ['professor', 'dr.', 'phd', 'md', 'director']
		professional_members = 0
		
		for member in editorial_board:
			if any(title in member.lower() for title in professional_titles):
				professional_members += 1
		
		if professional_members > 0:
			score += min(professional_members * 3, 30)
		
		# Международно представителство
		international_affiliations = ['university', 'college', 'institute', 'hospital']
		international_members = 0
		
		for member in editorial_board:
			if any(affiliation in member.lower() for affiliation in international_affiliations):
				international_members += 1
		
		if international_members > 0:
			score += min(international_members * 2, 30)
		
		return min(score, 100)
	
	def _calculate_peer_review_score(self, journal_data: Dict) -> int:
		"""Изчислява оценката за peer review процес"""
		score = 0
		
		peer_review_info = journal_data.get('peer_review_info', '').lower()
		
		# Ключови думи за peer review
		peer_review_keywords = [
			'peer review', 'double blind', 'single blind', 'open review',
			'referee', 'reviewer', 'review process', 'editorial review'
		]
		
		found_keywords = sum(1 for keyword in peer_review_keywords if keyword in peer_review_info)
		score += found_keywords * 15
		
		# Проверка за специфични процеси
		if 'double blind' in peer_review_info:
			score += 20
		elif 'single blind' in peer_review_info:
			score += 15
		elif 'open review' in peer_review_info:
			score += 10
		
		# Проверка за времеви рамки
		if any(timeframe in peer_review_info for timeframe in ['weeks', 'days', 'months']):
			score += 10
		
		return min(score, 100)
	
	def _calculate_technical_standards(self, journal_data: Dict) -> int:
		"""Изчислява оценката за технически стандарти"""
		score = 0
		
		# ISSN
		if journal_data.get('issn'):
			score += 25
		
		# DOI
		if journal_data.get('doi_prefix'):
			score += 25
		
		# HTTPS
		url = journal_data.get('url', '')
		if url.startswith('https'):
			score += 20
		
		# Структурирани данни
		if journal_data.get('title') and len(journal_data['title']) > 10:
			score += 15
		
		if journal_data.get('description') and len(journal_data['description']) > 50:
			score += 15
		
		return min(score, 100)
	
	def _generate_recommendations(self, journal_data: Dict, scores: Dict) -> List[str]:
		"""Генерира препоръки за подобрение"""
		recommendations = []
		
		if scores['content_quality'] < 70:
			recommendations.append("Подобрете документацията на peer review процеса")
			recommendations.append("Добавете подробна информация за редакционния съвет")
		
		if scores['editorial_standards'] < 70:
			recommendations.append("Разширете редакционния съвет с международни експерти")
			recommendations.append("Добавете професионални титли и афилиации")
		
		if scores['peer_review_process'] < 70:
			recommendations.append("Документирайте ясно peer review процеса")
			recommendations.append("Опишете времевите рамки за рецензиране")
		
		if scores['international_scope'] < 70:
			recommendations.append("Включете английски език в публикациите")
			recommendations.append("Привлечете международни автори и редактори")
		
		if scores['technical_standards'] < 70:
			recommendations.append("Получете ISSN номер")
			recommendations.append("Настройте DOI система")
			recommendations.append("Използвайте HTTPS протокол")
		
		if scores['accessibility'] < 70:
			recommendations.append("Помислете за Open Access модел")
			recommendations.append("Подобрете мобилната съвместимост")
		
		return recommendations

# Flask приложение
app = Flask(__name__)
CORS(app)

analyzer = ScopusJournalAnalyzer()

@app.route('/')
def index():
	"""Главна страница"""
	return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_journal():
	"""API endpoint за анализ на списание"""
	try:
		data = request.get_json()
		journal_url = data.get('url')
		
		if not journal_url:
			return jsonify({'error': 'URL е задължителен'}), 400
		
		# Валидация на URL
		if not journal_url.startswith(('http://', 'https://')):
			journal_url = 'https://' + journal_url
		
		# Анализ на списанието
		journal_data = analyzer.extract_journal_data(journal_url)
		
		if 'error' in journal_data:
			return jsonify({'error': journal_data['error']}), 500
		
		# Изчисляване на готовността за Scopus
		readiness_analysis = analyzer.calculate_scopus_readiness(journal_data)
		
		# Комбиниране на резултатите
		result = {
			'journal_data': journal_data,
			'readiness_analysis': readiness_analysis
		}
		
		return jsonify(result)
		
	except Exception as e:
		logger.error(f"Грешка при анализ: {e}")
		return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
	"""Health check endpoint"""
	return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)

