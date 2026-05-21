"""
INFNIT DUV Scraper — Combined Version
======================================
Combines your working connection/calendar approach with
improved time parsing, column detection, tier assignment,
and clean honest schema.

Run directly: python duv_scraper_combined.py

Change MODE and OUTPUT_FILE below to switch targets.
"""

import scrapy
from scrapy.crawler import CrawlerProcess
import re

# ── CONFIGURATION — edit these ────────────────────────────
MODE        = 'mds'      # test | mds | year | stage | full
TARGET_YEAR = 2025        # used when mode='year'
OUTPUT_FILE = r'E:\INFNIT\Vault\UltraMarathon\MDS_MASTER_DATASET_v2.csv'

# ── Known MDS Morocco edition IDs ────────────────────────
MDS_EDITION_IDS = [
    120942, 108360, 85505,  80158,  68358,  53571,  39445,
    33105,  28041,  22759,  19146,  14686,  11302,  7954,
    4280,   1942,   1388,   5493,   303,    7368,   7552,
    7719,   21390,  21389,  21388,  28922,  28921,  28920,
    28919,  74221,  28918,  76082,  76081,  76080,  75973,
    75824,  74226,  74225,  74224,
]

TEST_EVENT_IDS = [108360, 85505, 80158]  # MDS 2024, 2023, 2022


# ── Time parser ───────────────────────────────────────────
def parse_time_to_hours(raw):
    """
    Parse DUV time strings to float hours.
      "4:10:15 h"       → 4.171
      "36:40:19 h"      → 36.672
      "2d 12:34:56 h"   → 60.582
      "2d23:59:36 h"    → 71.993
    """
    if not raw:
        return None
    raw = str(raw).strip()
    # Multi-day with space
    m = re.match(r'^(\d+)d\s+(\d+):(\d+):(\d+)', raw)
    if m:
        return round(int(m.group(1))*24 + int(m.group(2))
                     + int(m.group(3))/60 + int(m.group(4))/3600, 4)
    # Multi-day no space
    m = re.match(r'^(\d+)d(\d+):(\d+):(\d+)', raw)
    if m:
        return round(int(m.group(1))*24 + int(m.group(2))
                     + int(m.group(3))/60 + int(m.group(4))/3600, 4)
    # Standard HH:MM:SS
    m = re.match(r'^(\d+):(\d+):(\d+)', raw)
    if m:
        return round(int(m.group(1)) + int(m.group(2))/60
                     + int(m.group(3))/3600, 4)
    return None


def assign_tier(hours):
    if hours is None:
        return 'UNKNOWN'
    if hours < 30.0:
        return 'ELITE'
    if hours < 45.0:
        return 'MID'
    return 'BACK'


# ── Spider ────────────────────────────────────────────────
class DuvSpider(scrapy.Spider):
    name = 'duv'
    allowed_domains = ['statistik.d-u-v.org']

    custom_settings = {
        'DOWNLOAD_DELAY': 2.0,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS': 1,
        'ROBOTSTXT_OBEY': False,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 2.0,
        'AUTOTHROTTLE_MAX_DELAY': 10.0,
        # HTTP Cache — avoids re-hitting server on reruns
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 86400,
        'HTTPCACHE_DIR': r'E:\INFNIT\Vault\UltraMarathon\duv_httpcache',
        'HTTPCACHE_IGNORE_HTTP_CODES': [403, 404, 500, 503],
        # Retry on server errors
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 429],
        'LOG_LEVEL': 'INFO',
        # Output
        'FEED_EXPORT_FIELDS': [
            'event_id', 'event_name', 'year', 'date',
            'distance_km', 'country',
            'rank', 'finish_time', 'finish_hours', 'tier', 'pace_min_km',
            'gender', 'rank_gender', 'age_cat', 'rank_cat',
            'nationality', 'yob', 'avg_speed', 'age_graded',
        ],
        'FEEDS': {
            OUTPUT_FILE: {
                'format': 'csv',
                'encoding': 'utf-8',
                'overwrite': True,
            }
        },
    }

    # ── Start requests ────────────────────────────────────
    async def start(self):
        base = 'https://statistik.d-u-v.org'

        if MODE == 'test':
            self.logger.info(f'TEST MODE — {len(TEST_EVENT_IDS)} events')
            for eid in TEST_EVENT_IDS:
                yield scrapy.Request(
                    f'{base}/getresultevent.php?event={eid}&Language=EN',
                    callback=self.parse_event,
                    cb_kwargs={'event_id': eid}
                )

        elif MODE == 'mds':
            self.logger.info(f'MDS MODE — {len(MDS_EDITION_IDS)} editions')
            for eid in MDS_EDITION_IDS:
                yield scrapy.Request(
                    f'{base}/getresultevent.php?event={eid}&Language=EN',
                    callback=self.parse_event,
                    cb_kwargs={'event_id': eid}
                )

        elif MODE == 'year':
            self.logger.info(f'YEAR MODE — {TARGET_YEAR}')
            yield scrapy.Request(
                f'{base}/calendar.php?year={TARGET_YEAR}&Language=EN',
                callback=self.parse_calendar,
                cb_kwargs={'year': TARGET_YEAR}
            )

        elif MODE == 'stage':
            self.logger.info('STAGE MODE — 2000-2025')
            for yr in range(2000, 2026):
                yield scrapy.Request(
                    f'{base}/calendar.php?year={yr}&dist=Stage&Language=EN',
                    callback=self.parse_calendar,
                    cb_kwargs={'year': yr}
                )

        elif MODE == 'full':
            self.logger.info('FULL MODE — all events 2000-2025')
            for yr in range(2000, 2026):
                yield scrapy.Request(
                    f'{base}/calendar.php?year={yr}&Language=EN',
                    callback=self.parse_calendar,
                    cb_kwargs={'year': yr}
                )

    # ── Calendar page ─────────────────────────────────────
    def parse_calendar(self, response, year):
        """Your working calendar parser — finds all event links."""
        base = 'https://statistik.d-u-v.org'
        seen = set()
        links = response.css(
            'a[href*="getresultevent.php?event="]::attr(href)'
        ).getall()

        for link in links:
            m = re.search(r'event=(\d+)', link)
            if m:
                eid = int(m.group(1))
                if eid not in seen:
                    seen.add(eid)
                    absolute_url = response.urljoin(link)
                    yield scrapy.Request(
                        absolute_url,
                        callback=self.parse_event,
                        cb_kwargs={'event_id': eid}
                    )

        self.logger.info(f'Calendar {year}: {len(seen)} events found')

    # ── Event page ────────────────────────────────────────
    def parse_event(self, response, event_id):
        """
        Your working table parser + my improvements:
        - Robust time column detection (scans all cells)
        - Dynamic column map from header row
        - Extracts nationality, gender, age_cat, YOB, rank
        - Parses finish_hours, assigns tier, calculates pace
        """
        # ── Extract event metadata ────────────────────────
        page_text = ' '.join(response.css('body *::text').getall())

        event_name = ''
        date_str   = ''
        distance   = 0.0
        country    = ''
        year       = None

        for table in response.css('table'):
            for row in table.css('tr'):
                cells = [td.css('::text').get('').strip()
                         for td in row.css('td')]
                cells = [c for c in cells if c]
                if len(cells) >= 2:
                    key = cells[0].lower()
                    val = cells[1]
                    if 'date' in key:
                        date_str = val
                        yr = re.search(r'\b(19|20)\d{2}\b', val)
                        if yr:
                            year = int(yr.group())
                    elif 'event' in key and not event_name:
                        event_name = val
                        cc = re.search(r'\(([A-Z]{3})\)', val)
                        if cc:
                            country = cc.group(1)
                    elif 'distance' in key or 'length' in key:
                        km = re.search(r'([\d.]+)\s*km', val, re.IGNORECASE)
                        if km:
                            try:
                                distance = float(km.group(1))
                            except ValueError:
                                pass

        # Fallback distance from page text
        if distance == 0.0:
            dm = re.search(r'(\d+[\.,]?\d*)\s*km', page_text, re.IGNORECASE)
            if dm:
                try:
                    distance = float(dm.group(1).replace(',', '.'))
                except ValueError:
                    pass

        # ── Find results table ────────────────────────────
        results_table = None
        for table in response.css('table'):
            headers = [h.strip() for h in
                       table.css('tr:first-child ::text').getall()
                       if h.strip()]
            if 'Performance' in headers or 'Rank' in headers:
                results_table = table
                break

        if not results_table:
            self.logger.warning(f'Event {event_id}: no results table')
            return

        # ── Map column names to positions ─────────────────
        header_cells = results_table.css('tr:first-child td, tr:first-child th')
        col_map = {}
        for i, cell in enumerate(header_cells):
            name = cell.css('::text').get('').strip()
            if name:
                col_map[name] = i

        def get_col(cells, *names):
            for name in names:
                if name in col_map and col_map[name] < len(cells):
                    v = cells[col_map[name]].strip()
                    if v and v not in ('#NA', '-', ''):
                        return v
            return ''

        # ── Parse each result row ─────────────────────────
        yielded = 0
        rows = results_table.css('tr')[1:]

        for row in rows:
            cols = row.css('td')
            if len(cols) < 4:
                continue

            cells = [td.css('::text').get('').strip() for td in cols]

            # ── Find time column — scan all cells ─────────
            # Your approach: try last column first, then second-last
            # My improvement: scan ALL cells for time pattern
            finish_time = None
            for cell in cells:
                if re.match(r'^(\d+d\s*)?(\d+):(\d+):(\d+)', cell):
                    finish_time = cell
                    break

            if not finish_time:
                # Fallback: your original approach
                for cell in [cells[-1], cells[-2]] if len(cells) >= 2 else []:
                    if cell and re.search(r'\d:\d', cell):
                        finish_time = cell
                        break

            if not finish_time:
                continue

            # ── Parse time ────────────────────────────────
            finish_hours = parse_time_to_hours(finish_time)
            if finish_hours is None:
                continue

            # ── Derive pace ───────────────────────────────
            pace = round(finish_hours * 60 / distance, 4) if distance > 0 else None

            # ── Build item ────────────────────────────────
            yield {
                # Race identity
                'event_id':    event_id,
                'event_name':  event_name,
                'year':        year,
                'date':        date_str,
                'distance_km': distance,
                'country':     country,
                # Result
                'rank':        get_col(cells, 'Rank'),
                'finish_time': finish_time,
                'finish_hours':finish_hours,
                'tier':        assign_tier(finish_hours),
                'pace_min_km': pace,
                # Athlete
                'gender':      get_col(cells, 'M/F', 'Sex', 'Gender'),
                'rank_gender': get_col(cells, 'Rank M/F', 'Rank_MF'),
                'age_cat':     get_col(cells, 'Cat', 'Age Cat', 'AgeGroup'),
                'rank_cat':    get_col(cells, 'Cat. Rank', 'Rank Cat'),
                'nationality': get_col(cells, 'Nat.', 'Nationality'),
                'yob':         get_col(cells, 'YOB', 'Born'),
                'avg_speed':   get_col(cells, 'Avg.Speed km/h', 'Speed'),
                'age_graded':  get_col(cells, 'Age graded performance'),
            }
            yielded += 1

        self.logger.info(
            f'Event {event_id} ({event_name[:35]}): {yielded} rows'
        )


# ── Run ───────────────────────────────────────────────────
if __name__ == '__main__':
    print(f'Mode     : {MODE}')
    print(f'Output   : {OUTPUT_FILE}')
    print('Starting...')
    process = CrawlerProcess()
    process.crawl(DuvSpider)
    process.start()
    print(f'Done. Check: {OUTPUT_FILE}')

