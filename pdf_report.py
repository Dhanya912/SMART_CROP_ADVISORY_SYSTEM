# -*- coding: utf-8 -*-
"""
pdf_report.py — Multilingual advisory PDF generator (fpdf2 + HarfBuzz shaping).
ReportLab cannot shape Kannada/Tamil/Devanagari/Telugu, which made those PDFs
unreadable. fpdf2's set_text_shaping(True) places matras correctly.

Public API unchanged:  generate_advisory_pdf(report, farmer_name) -> bytes
"""

import os
from datetime import datetime
from fpdf import FPDF
import i18n

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
FONT_FILES = {
    'kn': 'NotoSansKannada-Regular.ttf',
    'ta': 'NotoSansTamil-Regular.ttf',
    'hi': 'NotoSansDevanagari-Regular.ttf',
    'te': 'NotoSansTelugu-Regular.ttf',
    'en': 'NotoSans-Regular.ttf',
}

LEAF = (45, 106, 79); LEAFLT = (64, 145, 108); SKY = (27, 73, 101)
GOLD = (233, 196, 106); BARK = (107, 66, 38); ALERT = (230, 57, 70)
GREY = (120, 120, 120); INK = (26, 26, 46); WHITE = (255, 255, 255)


def _font_path(lang):
    p = os.path.join(FONT_DIR, FONT_FILES.get(lang, ''))
    return p if os.path.exists(p) else None


class Report(FPDF):
    def __init__(self, lang, title):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.lang = lang
        self.doc_title = title
        self.set_auto_page_break(True, margin=18)
        self.set_margins(16, 14, 16)
        self.family = 'helvetica'
        fp = _font_path(lang) or _font_path('en')
        if fp:
            self.add_font('noto', '', fp)
            self.family = 'noto'
        try:
            self.set_text_shaping(True)
        except Exception:
            pass
        self.set_font(self.family, '', 10)

    @property
    def cw(self):
        return self.w - self.l_margin - self.r_margin

    def footer(self):
        self.set_y(-14)
        self.set_font(self.family, '', 7.5)
        self.set_text_color(*GREY)
        self.cell(0, 5, f"CropAI  |  {self.doc_title}  |  Page {self.page_no()}",
                  align='C', new_x='LMARGIN', new_y='NEXT')

    def _wrap(self, text, width, size):
        self.set_font_size(size)
        words = str(text).split()
        lines, cur = [], ''
        for w in words:
            trial = (cur + ' ' + w).strip()
            if self.get_string_width(trial) <= width or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines or ['']

    def _guard(self):
        if self.get_y() > self.h - 26:
            self.add_page()

    def para(self, text, size=9.5, color=INK, indent=0, lh=5.6, gap=2):
        if text in (None, ''):
            return
        self.set_text_color(*color)
        for line in self._wrap(text, self.cw - indent, size):
            self._guard()
            self.set_x(self.l_margin + indent)
            self.cell(self.cw - indent, lh, line, new_x='LMARGIN', new_y='NEXT')
        self.ln(gap)

    def bullet(self, text, size=9.5):
        self._guard()
        self.set_font_size(size)
        self.set_text_color(*LEAF)
        self.set_x(self.l_margin + 2)
        self.cell(4, 5.6, '-')
        self.set_text_color(*INK)
        lines = self._wrap(text, self.cw - 8, size)
        self.cell(self.cw - 8, 5.6, lines[0], new_x='LMARGIN', new_y='NEXT')
        for extra in lines[1:]:
            self._guard()
            self.set_x(self.l_margin + 6)
            self.cell(self.cw - 8, 5.6, extra, new_x='LMARGIN', new_y='NEXT')

    def banner(self, text, color=LEAF):
        if self.get_y() > self.h - 45:
            self.add_page()
        self.ln(2)
        self.set_fill_color(*color)
        self.set_text_color(*WHITE)
        self.set_font_size(11)
        self.set_x(self.l_margin)
        self.cell(self.cw, 8.5, '  ' + str(text), fill=True, new_x='LMARGIN', new_y='NEXT')
        self.ln(2.5)

    def kv(self, label, value, lw=58):
        self._guard()
        self.set_font_size(9.5)
        self.set_text_color(*GREY)
        self.set_x(self.l_margin)
        self.cell(lw, 6, str(label))
        self.set_text_color(*INK)
        lines = self._wrap(str(value), self.cw - lw, 9.5)
        self.cell(self.cw - lw, 6, lines[0], new_x='LMARGIN', new_y='NEXT')
        for extra in lines[1:]:
            self._guard()
            self.set_x(self.l_margin + lw)
            self.cell(self.cw - lw, 6, extra, new_x='LMARGIN', new_y='NEXT')

    def bar(self, label, pct, color=LEAFLT):
        self._guard()
        pct = max(0.0, min(100.0, float(pct or 0)))
        self.set_font_size(9)
        self.set_text_color(*INK)
        self.set_x(self.l_margin)
        lbl = self._wrap(str(label), 53, 9)[0]
        self.cell(55, 6, lbl)
        x, y = self.get_x(), self.get_y()
        track = self.cw - 55 - 18
        self.set_fill_color(225, 232, 225)
        self.rect(x, y + 1.6, track, 3.2, 'F')
        self.set_fill_color(*color)
        self.rect(x, y + 1.6, track * pct / 100.0, 3.2, 'F')
        self.set_xy(x + track + 2, y)
        self.set_text_color(*GREY)
        self.cell(16, 6, f"{pct:.0f}%", new_x='LMARGIN', new_y='NEXT')


def generate_advisory_pdf(report, farmer_name='Farmer'):
    lang = i18n.norm_lang(report.get('lang', 'en'))
    L = report.get('labels') or {}

    def lb(key, fallback=''):
        return L.get(key) or i18n.t(key, lang) or fallback

    title = lb('report_title', 'Smart Crop Advisory Report')
    pdf = Report(lang, title)
    pdf.add_page()

    secs = report.get('sections', {}) or {}
    crop = secs.get('crop_recommendation', {}) or {}
    dis = secs.get('disease_detection', {}) or {}
    wx = secs.get('weather_analysis', {}) or {}
    soil = secs.get('soil_health', {}) or {}
    mkt = secs.get('market_intelligence', {}) or {}
    pol = secs.get('policy_advisory', {}) or {}
    plan = report.get('action_plan', []) or []
    loc = report.get('location', 'N/A')
    when = report.get('generated_at', datetime.now().strftime('%d %b %Y, %H:%M'))

    pdf.set_fill_color(*LEAF)
    pdf.rect(0, 0, pdf.w, 32, 'F')
    pdf.set_xy(pdf.l_margin, 7)
    pdf.set_text_color(*WHITE)
    pdf.set_font_size(16)
    pdf.cell(pdf.cw, 9, title, align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_font_size(8.5)
    pdf.set_text_color(*GOLD)
    pdf.set_x(pdf.l_margin)
    pdf.cell(pdf.cw, 5.5, f"{lb('prepared_for','Prepared for')}: {farmer_name}", align='C',
             new_x='LMARGIN', new_y='NEXT')
    pdf.set_x(pdf.l_margin)
    pdf.cell(pdf.cw, 5.5, f"{lb('location','Location')}: {loc}    {lb('generated_on','Generated on')}: {when}",
             align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_y(38)

    if lang != 'en' and not _font_path(lang):
        pdf.para(f"Note: the {lang.upper()} font file is missing from /fonts — "
                 f"run fetch_fonts.py once with internet access.", size=8, color=ALERT)

    pdf.banner(lb('executive_summary', 'Executive Summary'), SKY)
    pdf.para(report.get('executive_summary', ''), size=9.5, lh=5.8)

    pdf.banner(lb('sec_crop', 'Crop Recommendation'), LEAF)
    pdf.kv(lb('recommended_crop', 'Recommended Crop'), crop.get('top_crop', '-'))
    for c in (crop.get('all_crops') or [])[:5]:
        v = c.get('confidence', 0)
        pdf.bar(c.get('crop_display') or c.get('crop', '-'), v * 100 if v <= 1 else v)
    pdf.ln(1)
    pdf.kv(lb('method', 'Method'), crop.get('method', '-'))
    pdf.para(crop.get('key_insight', ''), size=9)

    pdf.banner(lb('sec_disease', 'Disease Detection'), ALERT)
    if dis.get('disease'):
        pdf.kv(lb('disease', 'Disease'), dis.get('disease', '-'))
        pdf.kv(lb('severity', 'Severity'), dis.get('severity', '-'))
        pdf.kv(lb('confidence', 'Confidence'), dis.get('confidence', '-'))
        pdf.kv(lb('cause', 'Cause'), dis.get('cause', '-'))
        for t in (dis.get('top3') or []):
            pdf.bar(t.get('disease', '-'), t.get('confidence', 0), ALERT)
        tx = dis.get('treatment') or []
        if tx:
            pdf.ln(1)
            pdf.para(lb('treatment_steps', 'Treatment Steps') + ':', size=9.5, color=LEAF, gap=1)
            for t in tx:
                pdf.bullet(t)
        if dis.get('prevention'):
            pdf.kv(lb('prevention', 'Prevention'), dis['prevention'])
    else:
        pdf.para(dis.get('key_insight') or lb('no_image_msg', 'No leaf image was submitted.'), size=9.5)

    pdf.banner(lb('sec_weather', 'Weather Analysis'), SKY)
    pdf.kv(lb('condition', 'Condition'), wx.get('condition', '-'))
    pdf.kv(lb('temperature', 'Temperature'), wx.get('temperature', '-'))
    pdf.kv(lb('humidity', 'Humidity'), wx.get('humidity', '-'))
    pdf.kv(lb('wind_speed', 'Wind Speed'), f"{wx.get('wind_speed', 0)} km/h")
    pdf.kv(lb('rainfall', 'Rainfall'), f"{wx.get('rainfall_mm', 0)} mm")
    pdf.kv(lb('irrigation_need', 'Irrigation Need'),
           f"{(wx.get('irrigation') or {}).get('net_irrigation', 0)} mm/day")
    adv = wx.get('advisory') or []
    if adv:
        pdf.para(lb('farm_advisories', 'Farm Advisories') + ':', size=9.5, color=LEAF, gap=1)
        for a in adv:
            pdf.bullet(a)

    pdf.banner(lb('sec_soil', 'Soil Health Analysis'), BARK)
    pdf.bar(lb('score', 'Score'), soil.get('health_score', 0), LEAFLT)
    pdf.kv(lb('nitrogen', 'Nitrogen (N)'), f"{soil.get('nitrogen','-')}  ({soil.get('nitrogen_status','-')})")
    pdf.kv(lb('phosphorus', 'Phosphorus (P)'), f"{soil.get('phosphorus','-')}  ({soil.get('phosphorus_status','-')})")
    pdf.kv(lb('potassium', 'Potassium (K)'), f"{soil.get('potassium','-')}  ({soil.get('potassium_status','-')})")
    pdf.kv(lb('ph', 'pH'), f"{soil.get('ph','-')}  ({soil.get('ph_status','-')})")
    pdf.kv(lb('soil_type', 'Soil Type'), soil.get('soil_type', '-'))
    am = soil.get('amendments') or []
    if am:
        pdf.para(lb('fertiliser_plan', 'Fertiliser Plan') + ':', size=9.5, color=LEAF, gap=1)
        for a in am:
            pdf.bullet(a)

    pdf.banner(lb('sec_market', 'Market Intelligence'), (184, 134, 11))
    pdf.kv(lb('crop', 'Crop'), mkt.get('crop', '-'))
    pdf.kv(lb('avg_price', 'Average Price'), mkt.get('avg_price', '-'))
    pdf.kv(lb('price_trend', 'Price Trend'), mkt.get('price_trend', '-'))
    pdf.kv(lb('best_market', 'Best Market'), mkt.get('best_market', '-'))
    pdf.kv(lb('yield_estimate', 'Yield Estimate'), mkt.get('yield_estimate', '-'))
    pdf.kv(lb('net_income', 'Net Income'), mkt.get('net_income', '-'))
    for a in (mkt.get('advisory') or []):
        pdf.bullet(a)

    pdf.banner(lb('sec_policy', 'Policy & Government Schemes'), LEAF)
    msp = pol.get('msp') or {}
    if msp.get('msp'):
        pdf.kv('MSP ' + str(msp.get('year', '')), f"Rs {msp.get('msp')} / {msp.get('unit','quintal')}")
    schemes = pol.get('schemes') or []
    if schemes:
        pdf.para(lb('applicable_schemes', 'Applicable Schemes') + ':', size=9.5, color=LEAF, gap=1)
        for s in schemes[:6]:
            pdf.bullet(f"{s.get('name','')} - {s.get('benefit','')}")
    pdf.para(pol.get('key_insight', ''), size=9)
    pdf.kv(lb('helpline', 'Helpline'), pol.get('helpline', '1800-180-1551'))

    if plan:
        pdf.banner(lb('sec_action_plan', 'Priority Action Plan'), SKY)
        for a in plan:
            pdf.bullet(f"{a.get('priority','')}. {a.get('action','')}  ({a.get('timeline','')})")

    pdf.ln(4)
    pdf.para(lb('footer_note', 'This report is AI-generated guidance. Confirm with your local agriculture officer.'),
             size=8, color=GREY)

    return bytes(pdf.output())
