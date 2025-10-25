#!/usr/bin/env python3
"""Repair KB script

Attempts to improve short/partial articles in data/enhanced_robotics_knowledge.json by:
 - retrying the Wikipedia HTML endpoint (with retries)
 - falling back to the MediaWiki search API to find canonical titles
 - replacing content when a richer version is found
 - updating crawl statistics (total_words)
 - writing a repair report to data/repair_report.json

Run from repo root: python scripts/repair_kb.py
"""
from pathlib import Path
import json, time, re
from urllib.parse import quote
import requests

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
KB_FILE = DATA / 'enhanced_robotics_knowledge.json'
STATS_FILE = DATA / 'crawl_statistics.json'
REPORT_FILE = DATA / 'repair_report.json'

import sys
# ensure repo root is on path so we can import the crawler module
sys.path.insert(0, str(ROOT))
from enhanced_wikipedia_crawler import EnhancedWikipediaCrawler


def extract_text_from_html(html: str) -> str:
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def search_wikipedia(title: str, session: requests.Session):
    # Use MediaWiki search API
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': title,
        'format': 'json',
        'srlimit': 3
    }
    url = 'https://en.wikipedia.org/w/api.php'
    r = session.get(url, params=params, timeout=10)
    if r.status_code == 200:
        try:
            data = r.json()
            hits = data.get('query', {}).get('search', [])
            return [h.get('title') for h in hits]
        except Exception:
            return []
    return []


def try_fetch_html(title: str, session: requests.Session, retries=3, backoff=1.0):
    safe = quote(title, safe='')
    url = f'https://en.wikipedia.org/api/rest_v1/page/html/{safe}'
    for i in range(retries):
        try:
            r = session.get(url, timeout=12)
            return r
        except requests.RequestException as e:
            time.sleep(backoff * (2 ** i))
    return None


def main():
    kb = json.loads(KB_FILE.read_text(encoding='utf-8'))
    stats = json.loads(STATS_FILE.read_text(encoding='utf-8')) if STATS_FILE.exists() else {}

    short_threshold = 300
    short_entries = [a for a in kb if (a.get('word_count') or 0) < short_threshold]

    session = requests.Session()
    session.headers.update({'User-Agent': 'Radeon-SML-Repair/1.0 (contact: user@example.com)'})

    crawler = EnhancedWikipediaCrawler()  # to reuse quality scoring

    changes = []
    total_word_delta = 0

    for entry in short_entries:
        title = entry.get('title')
        original_wc = entry.get('word_count') or 0
        record = {'title': title, 'original_word_count': original_wc, 'url': entry.get('url'), 'attempts': []}

        # 1) Try HTML endpoint for the stored title
        r = try_fetch_html(title, session)
        if r is not None and r.status_code == 200:
            text = extract_text_from_html(r.text)
            wc = len(text.split())
            record['attempts'].append({'method': 'html', 'status': r.status_code, 'word_count': wc})
            if wc > original_wc + 50:  # significant improvement
                entry['content'] = text[:50000]
                entry['summary'] = text[:500]
                entry['word_count'] = wc
                entry['quality_score'] = crawler.calculate_quality_score(text, entry.get('summary',''))
                entry['url'] = entry.get('url') or f'https://en.wikipedia.org/wiki/{quote(title)}'
                entry['extracted_at'] = time.strftime('%Y-%m-%dT%H:%M:%S')
                delta = wc - original_wc
                total_word_delta += delta
                record['updated'] = True
                record['update_mode'] = 'replaced_from_html'
            else:
                record['updated'] = False
        else:
            status = r.status_code if r is not None else 'no-response'
            record['attempts'].append({'method': 'html', 'status': status})

            # 2) Fallback: search Wikipedia for alternate titles
            candidates = search_wikipedia(title, session)
            record['search_candidates'] = candidates
            found = False
            for cand in candidates:
                rc = try_fetch_html(cand, session)
                if rc is not None and rc.status_code == 200:
                    text = extract_text_from_html(rc.text)
                    wc = len(text.split())
                    record['attempts'].append({'method': 'html_cand', 'candidate': cand, 'status': rc.status_code, 'word_count': wc})
                    if wc > original_wc + 50:
                        entry['content'] = text[:50000]
                        entry['summary'] = text[:500]
                        entry['word_count'] = wc
                        entry['quality_score'] = crawler.calculate_quality_score(text, entry.get('summary',''))
                        entry['url'] = f'https://en.wikipedia.org/wiki/{quote(cand)}'
                        entry['extracted_at'] = time.strftime('%Y-%m-%dT%H:%M:%S')
                        delta = wc - original_wc
                        total_word_delta += delta
                        record['updated'] = True
                        record['update_mode'] = f'replaced_from_candidate:{cand}'
                        found = True
                        break
                else:
                    record['attempts'].append({'method': 'html_cand', 'candidate': cand, 'status': getattr(rc, 'status_code', None)})
                time.sleep(0.5)

            if not found:
                record['updated'] = False

        changes.append(record)
        # be polite
        time.sleep(0.5)

    # Update stats file
    if total_word_delta != 0 and stats:
        stats['total_words'] = stats.get('total_words', 0) + total_word_delta
        # recompute average
        if stats.get('articles_crawled'):
            stats['average_words_per_article'] = stats['total_words'] / max(stats['articles_crawled'], 1)
        stats['end_time'] = time.strftime('%Y-%m-%dT%H:%M:%S')

    # Save KB and stats and report
    KB_FILE.write_text(json.dumps(kb, indent=2, ensure_ascii=False), encoding='utf-8')
    if stats:
        STATS_FILE.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding='utf-8')

    report = {
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'short_threshold': short_threshold,
        'entries_checked': len(short_entries),
        'total_word_delta': total_word_delta,
        'changes': changes
    }
    REPORT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Repair complete. Entries checked: {len(short_entries)}; total_word_delta: {total_word_delta}")
    print(f"Report written to: {REPORT_FILE}")


if __name__ == '__main__':
    main()
