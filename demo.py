"""
Демонстрационен скрипт за Scopus Journal Analyzer
Показва как да използвате анализатора програмно
"""

import json
from app import ScopusJournalAnalyzer
from scopus_api import ScopusEnhancer

def demo_analysis():
    """Демонстрация на анализа на списание"""
    
    print("=" * 60)
    print("SCOPUS JOURNAL READINESS ANALYZER - ДЕМО")
    print("=" * 60)
    
    # Създаваме анализатора
    analyzer = ScopusJournalAnalyzer()
    enhancer = ScopusEnhancer()
    
    # Примерни URL адреси за тестване
    test_urls = [
        "https://www.nature.com/nature/",
        "https://www.science.org/journal/science",
        "https://www.cell.com/cell/",
        "https://www.nejm.org/",
        "https://www.thelancet.com/"
    ]
    
    print("Доступни тестови URL адреси:")
    for i, url in enumerate(test_urls, 1):
        print(f"{i}. {url}")
    
    # Питаме потребителя за избор
    try:
        choice = input("\nИзберете номер (1-5) или въведете собствен URL: ")
        
        if choice.isdigit() and 1 <= int(choice) <= len(test_urls):
            selected_url = test_urls[int(choice) - 1]
        else:
            selected_url = choice
            if not selected_url.startswith(('http://', 'https://')):
                selected_url = 'https://' + selected_url
        
        print(f"\nАнализирам: {selected_url}")
        print("Моля изчакайте...")
        
        # Извършваме анализа
        journal_data = analyzer.extract_journal_data(selected_url)
        
        if 'error' in journal_data:
            print(f"Грешка при анализ: {journal_data['error']}")
            return
        
        # Подобряваме анализа с Scopus данни
        enhanced_data = enhancer.enhance_journal_analysis(journal_data)
        
        # Изчисляваме готовността
        readiness_analysis = analyzer.calculate_scopus_readiness(enhanced_data)
        
        # Показваме резултатите
        display_results(enhanced_data, readiness_analysis)
        
        # Запазваме резултатите
        save_results(enhanced_data, readiness_analysis, selected_url)
        
    except KeyboardInterrupt:
        print("\nАнализът е прекъснат от потребителя")
    except Exception as e:
        print(f"Грешка: {e}")

def display_results(journal_data, readiness_analysis):
    """Показва резултатите от анализа"""
    
    print("\n" + "=" * 60)
    print("РЕЗУЛТАТИ ОТ АНАЛИЗА")
    print("=" * 60)
    
    # Основна информация
    print(f"\n📰 ЗАГЛАВИЕ: {journal_data.get('title', 'Не е намерено')}")
    print(f"🔗 URL: {journal_data.get('url', 'Не е намерено')}")
    print(f"📄 ISSN: {journal_data.get('issn', 'Не е намерено')}")
    print(f"🔢 DOI Prefix: {journal_data.get('doi_prefix', 'Не е намерено')}")
    print(f"🌐 Open Access: {'Да' if journal_data.get('open_access') else 'Не'}")
    print(f"🗣️ Езици: {', '.join(journal_data.get('languages', ['Не е намерено']))}")
    print(f"📅 Честота: {journal_data.get('publication_frequency', 'Не е намерено')}")
    print(f"👥 Редакционен съвет: {len(journal_data.get('editorial_board', []))} членове")
    
    # Обща оценка
    total_score = readiness_analysis['total_score']
    readiness_level = readiness_analysis['readiness_level']
    
    print(f"\n🎯 ОБЩА ОЦЕНКА: {total_score:.1f}%")
    print(f"📊 НИВО НА ГОТОВНОСТ: {readiness_level}")
    
    # Цветово кодиране
    if total_score >= 80:
        emoji = "🟢"
        status = "ОТЛИЧНО"
    elif total_score >= 60:
        emoji = "🟡"
        status = "ДОБРЕ"
    elif total_score >= 40:
        emoji = "🟠"
        status = "СРЕДНО"
    else:
        emoji = "🔴"
        status = "СЛАБО"
    
    print(f"{emoji} СТАТУС: {status}")
    
    # Детайлни оценки
    print(f"\n📈 ДЕТАЙЛНИ ОЦЕНКИ:")
    detailed_scores = readiness_analysis['detailed_scores']
    
    criteria_names = {
        'content_quality': 'Качество на съдържанието',
        'editorial_standards': 'Редакционни стандарти',
        'peer_review_process': 'Peer Review процес',
        'international_scope': 'Международен обхват',
        'technical_standards': 'Технически стандарти',
        'accessibility': 'Достъпност'
    }
    
    for key, score in detailed_scores.items():
        name = criteria_names.get(key, key)
        bar = "█" * int(score / 5) + "░" * (20 - int(score / 5))
        print(f"  {name}: {score:5.1f}% {bar}")
    
    # Scopus статус
    scopus_status = journal_data.get('scopus_indexing_status', {})
    if scopus_status.get('indexed'):
        print(f"\n✅ SCOPUS СТАТУС: Вече е индексирано")
        scopus_data = scopus_status.get('scopus_data', {})
        if scopus_data.get('scopus_id'):
            print(f"🆔 Scopus ID: {scopus_data['scopus_id']}")
        if scopus_data.get('subject_areas'):
            print(f"📚 Предметни области: {', '.join(scopus_data['subject_areas'])}")
    else:
        print(f"\n❌ SCOPUS СТАТУС: Не е индексирано")
        print(f"💡 Препоръка: {scopus_status.get('recommendation', 'Може да се кандидатира')}")
    
    # Препоръки
    recommendations = readiness_analysis.get('recommendations', [])
    if recommendations:
        print(f"\n💡 ПРЕПОРЪКИ ЗА ПОДОБРЕНИЕ:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    else:
        print(f"\n🎉 ПРЕПОРЪКИ: Списанието отговаря на всички основни критерии!")

def save_results(journal_data, readiness_analysis, url):
    """Запазва резултатите във файл"""
    
    results = {
        'url': url,
        'analysis_date': journal_data.get('analysis_timestamp'),
        'journal_data': journal_data,
        'readiness_analysis': readiness_analysis
    }
    
    filename = f"analysis_results_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Резултатите са запазени в: {filename}")
    except Exception as e:
        print(f"Грешка при запазване: {e}")

def demo_batch_analysis():
    """Демонстрация на групов анализ"""
    
    print("\n" + "=" * 60)
    print("ГРУПОВ АНАЛИЗ НА СПИСАНИЯ")
    print("=" * 60)
    
    # Списък с URL адреси за анализ
    urls = [
        "https://www.nature.com/nature/",
        "https://www.science.org/journal/science",
        "https://www.cell.com/cell/"
    ]
    
    analyzer = ScopusJournalAnalyzer()
    results = []
    
    for i, url in enumerate(urls, 1):
        print(f"\nАнализирам {i}/{len(urls)}: {url}")
        
        try:
            journal_data = analyzer.extract_journal_data(url)
            if 'error' not in journal_data:
                readiness_analysis = analyzer.calculate_scopus_readiness(journal_data)
                results.append({
                    'url': url,
                    'title': journal_data.get('title', 'Не е намерено'),
                    'score': readiness_analysis['total_score'],
                    'level': readiness_analysis['readiness_level']
                })
                print(f"✓ Завършен - Оценка: {readiness_analysis['total_score']:.1f}%")
            else:
                print(f"✗ Грешка: {journal_data['error']}")
        except Exception as e:
            print(f"✗ Грешка: {e}")
    
    # Показваме обобщените резултати
    if results:
        print(f"\n📊 ОБОБЩЕНИ РЕЗУЛТАТИ:")
        print("-" * 60)
        results.sort(key=lambda x: x['score'], reverse=True)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title'][:50]}...")
            print(f"   URL: {result['url']}")
            print(f"   Оценка: {result['score']:.1f}% ({result['level']})")
            print()

def main():
    """Основна функция"""
    
    print("Изберете режим:")
    print("1. Анализ на едно списание")
    print("2. Групов анализ на няколко списания")
    print("3. Изход")
    
    choice = input("\nВашият избор (1-3): ")
    
    if choice == '1':
        demo_analysis()
    elif choice == '2':
        demo_batch_analysis()
    elif choice == '3':
        print("Довиждане!")
    else:
        print("Невалиден избор!")

if __name__ == '__main__':
    main()
