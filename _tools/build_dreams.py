# -*- coding: utf-8 -*-
"""Сонник на сайте kuliktrade.com: страница на каждый сон × 9 языков + оглавления + sitemap.
Источник: oracle-apps/prototype-pulse-sistrum/tools/miller/merged.json (наш пересказ Миллера, 1901).
python3 _tools/build_dreams.py   → пишет dreams/, {lang}/dreams/, sitemap-dreams.xml"""
import json, os, re, html, shutil, datetime
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.expanduser('~/develop/oracle-apps/prototype-pulse-sistrum/tools/miller/merged.json')
BASE = 'https://kuliktrade.com'
LANGS = ['en', 'es', 'pt', 'de', 'fr', 'it', 'tr', 'ja', 'ru']
HREFLANG = {'en': 'en', 'es': 'es', 'pt': 'pt', 'de': 'de', 'fr': 'fr', 'it': 'it', 'tr': 'tr', 'ja': 'ja', 'ru': 'ru'}
TODAY = datetime.date.today().isoformat()

UI = {
 'en': dict(h1='{t} in a dream', title='{t} in a dream: meaning and interpretation', desc='What does it mean to dream of {l}? {o}',
   means='What it means', vars='Other versions of this dream', related='Related dreams', good='Usually a good sign', bad='Usually a warning',
   dict='Dream dictionary', dict_title='Dream dictionary: meanings of {n} dreams from A to Z', dict_desc='Find what your dream means. {n} dreams explained in plain words, retold from Gustavus Miller’s classic dream book.',
   search='Find your dream', source='Retold in modern words from Gustavus H. Miller, “Ten Thousand Dreams Interpreted” (1901).',
   cta='Place of Truth: an Egyptian oracle and dream book in your phone. Ask the temple about your dream, your day and your path.', cta_btn='About the app', soon='Coming soon on Google Play',
   all='All dreams', lang='Language'),
 'es': dict(h1='{t} en sueños', title='{t} en sueños: significado e interpretación', desc='¿Qué significa soñar con {l}? {o}',
   means='Qué significa', vars='Otras versiones de este sueño', related='Sueños relacionados', good='Suele ser buena señal', bad='Suele ser una advertencia',
   dict='Diccionario de sueños', dict_title='Diccionario de sueños: significado de {n} sueños de la A a la Z', dict_desc='Descubre qué significa tu sueño. {n} sueños explicados con palabras sencillas, a partir del clásico libro de sueños de Gustavus Miller.',
   search='Busca tu sueño', source='Contado con palabras de hoy a partir de Gustavus H. Miller, «Ten Thousand Dreams Interpreted» (1901).',
   cta='Place of Truth: un oráculo egipcio y un libro de sueños en tu teléfono. Pregunta al templo por tu sueño, tu día y tu camino.', cta_btn='Sobre la app', soon='Muy pronto en Google Play',
   all='Todos los sueños', lang='Idioma'),
 'pt': dict(h1='{t} em sonho', title='{t} em sonho: significado e interpretação', desc='O que significa sonhar com {l}? {o}',
   means='O que significa', vars='Outras versões deste sonho', related='Sonhos relacionados', good='Costuma ser um bom sinal', bad='Costuma ser um aviso',
   dict='Dicionário de sonhos', dict_title='Dicionário de sonhos: significado de {n} sonhos de A a Z', dict_desc='Descubra o que seu sonho significa. {n} sonhos explicados em palavras simples, a partir do clássico livro dos sonhos de Gustavus Miller.',
   search='Encontre seu sonho', source='Recontado em palavras de hoje a partir de Gustavus H. Miller, “Ten Thousand Dreams Interpreted” (1901).',
   cta='Place of Truth: um oráculo egípcio e um livro dos sonhos no seu celular. Pergunte ao templo sobre seu sonho, seu dia e seu caminho.', cta_btn='Sobre o app', soon='Em breve no Google Play',
   all='Todos os sonhos', lang='Idioma'),
 'de': dict(h1='{t} im Traum', title='{t} im Traum: Bedeutung und Deutung', desc='Was bedeutet es, von {l} zu träumen? {o}',
   means='Was es bedeutet', vars='Andere Varianten dieses Traums', related='Ähnliche Träume', good='Meist ein gutes Zeichen', bad='Meist eine Warnung',
   dict='Traumdeutung von A bis Z', dict_title='Traumdeutung: Bedeutung von {n} Träumen von A bis Z', dict_desc='Finde heraus, was dein Traum bedeutet. {n} Träume in einfachen Worten erklärt, nach dem klassischen Traumbuch von Gustavus Miller.',
   search='Finde deinen Traum', source='In heutigen Worten nacherzählt nach Gustavus H. Miller, „Ten Thousand Dreams Interpreted“ (1901).',
   cta='Place of Truth: ein ägyptisches Orakel und Traumbuch auf deinem Handy. Frag den Tempel nach deinem Traum, deinem Tag und deinem Weg.', cta_btn='Über die App', soon='Bald bei Google Play',
   all='Alle Träume', lang='Sprache'),
 'fr': dict(h1='{t} en rêve', title='{t} en rêve : signification et interprétation', desc='Que signifie rêver de {l} ? {o}',
   means='Ce que cela signifie', vars='Autres variantes de ce rêve', related='Rêves proches', good='Plutôt bon signe', bad='Plutôt un avertissement',
   dict='Dictionnaire des rêves', dict_title='Dictionnaire des rêves : la signification de {n} rêves de A à Z', dict_desc='Découvrez ce que signifie votre rêve. {n} rêves expliqués simplement, d’après le célèbre livre des rêves de Gustavus Miller.',
   search='Trouvez votre rêve', source='Raconté avec des mots d’aujourd’hui d’après Gustavus H. Miller, « Ten Thousand Dreams Interpreted » (1901).',
   cta='Place of Truth : un oracle égyptien et un livre des rêves dans votre téléphone. Interrogez le temple sur votre rêve, votre journée et votre chemin.', cta_btn='À propos de l’appli', soon='Bientôt sur Google Play',
   all='Tous les rêves', lang='Langue'),
 'it': dict(h1='{t} in sogno', title='{t} in sogno: significato e interpretazione', desc='Cosa significa sognare {l}? {o}',
   means='Cosa significa', vars='Altre versioni di questo sogno', related='Sogni simili', good='Di solito è un buon segno', bad='Di solito è un avvertimento',
   dict='Dizionario dei sogni', dict_title='Dizionario dei sogni: il significato di {n} sogni dalla A alla Z', dict_desc='Scopri cosa significa il tuo sogno. {n} sogni spiegati con parole semplici, dal classico libro dei sogni di Gustavus Miller.',
   search='Trova il tuo sogno', source='Raccontato con parole di oggi da Gustavus H. Miller, «Ten Thousand Dreams Interpreted» (1901).',
   cta='Place of Truth: un oracolo egizio e un libro dei sogni nel tuo telefono. Chiedi al tempio del tuo sogno, della tua giornata e del tuo cammino.', cta_btn='Scopri l’app', soon='Presto su Google Play',
   all='Tutti i sogni', lang='Lingua'),
 'tr': dict(h1='Rüyada {t} görmek', title='Rüyada {t} görmek: anlamı ve yorumu', desc='Rüyada {l} görmek ne anlama gelir? {o}',
   means='Ne anlama gelir', vars='Bu rüyanın diğer halleri', related='Benzer rüyalar', good='Genelde iyiye işaret', bad='Genelde bir uyarı',
   dict='Rüya tabirleri', dict_title='Rüya tabirleri: A’dan Z’ye {n} rüyanın anlamı', dict_desc='Rüyanın ne anlama geldiğini öğren. {n} rüya, Gustavus Miller’ın klasik rüya kitabından sade bir dille anlatıldı.',
   search='Rüyanı bul', source='Gustavus H. Miller’ın “Ten Thousand Dreams Interpreted” (1901) kitabından bugünün diliyle anlatıldı.',
   cta='Place of Truth: telefonunda bir Mısır kâhini ve rüya kitabı. Tapınağa rüyanı, gününü ve yolunu sor.', cta_btn='Uygulama hakkında', soon='Çok yakında Google Play’de',
   all='Tüm rüyalar', lang='Dil'),
 'ja': dict(h1='夢に見る「{t}」', title='夢に{t}が出てきたら：意味と夢占い', desc='{t}の夢にはどんな意味があるのでしょう。{o}',
   means='夢の意味', vars='この夢のほかのパターン', related='関連する夢', good='たいてい良いしるし', bad='たいてい注意のしるし',
   dict='夢辞典', dict_title='夢辞典：{n}の夢の意味をあいうえお順に', dict_desc='あなたの夢の意味を調べましょう。グスタフス・ミラーの古典的な夢の本から{n}の夢をやさしい言葉で解説します。',
   search='夢を探す', source='グスタフス・H・ミラー『Ten Thousand Dreams Interpreted』（1901年）を現代の言葉で語り直したものです。',
   cta='Place of Truth：スマホの中のエジプトの神託と夢の書。神殿にあなたの夢、今日、そして道を尋ねてみましょう。', cta_btn='アプリについて', soon='Google Playで近日公開',
   all='すべての夢', lang='言語'),
 'ru': dict(h1='{t} — к чему снится', title='{t} во сне: к чему снится, толкование', desc='{t} во сне — к чему? {o}',
   means='Что это значит', vars='Другие варианты этого сна', related='Похожие сны', good='Обычно добрый знак', bad='Обычно предупреждение',
   dict='Сонник от А до Я', dict_title='Сонник: толкование {n} снов от А до Я', dict_desc='Узнай, к чему снится твой сон. {n} снов простыми словами, по классическому соннику Густавуса Миллера.',
   search='Найди свой сон', source='Пересказано современным языком по книге Густавуса Х. Миллера «Ten Thousand Dreams Interpreted» (1901).',
   cta='Place of Truth — египетский оракул и сонник в твоём телефоне. Спроси храм о своём сне, своём дне и своём пути.', cta_btn='О приложении', soon='Скоро в Google Play',
   all='Все сны', lang='Язык'),
}
CATS = {
 'body': dict(en='Body and health', es='Cuerpo y salud', pt='Corpo e saúde', de='Körper und Gesundheit', fr='Corps et santé', it='Corpo e salute', tr='Beden ve sağlık', ja='体と健康', ru='Тело и здоровье'),
 'food': dict(en='Food and drink', es='Comida y bebida', pt='Comida e bebida', de='Essen und Trinken', fr='Nourriture et boissons', it='Cibo e bevande', tr='Yiyecek ve içecek', ja='食べ物と飲み物', ru='Еда и питьё'),
 'animals': dict(en='Animals', es='Animales', pt='Animais', de='Tiere', fr='Animaux', it='Animali', tr='Hayvanlar', ja='動物', ru='Животные'),
 'sky': dict(en='Nature, water and weather', es='Naturaleza, agua y clima', pt='Natureza, água e clima', de='Natur, Wasser und Wetter', fr='Nature, eau et météo', it='Natura, acqua e tempo', tr='Doğa, su ve hava', ja='自然・水・天気', ru='Природа, вода и погода'),
 'home': dict(en='Home, things and places', es='Casa, objetos y lugares', pt='Casa, objetos e lugares', de='Haus, Dinge und Orte', fr='Maison, objets et lieux', it='Casa, oggetti e luoghi', tr='Ev, eşyalar ve yerler', ja='家・物・場所', ru='Дом, вещи и места'),
 'people': dict(en='People and family', es='Personas y familia', pt='Pessoas e família', de='Menschen und Familie', fr='Personnes et famille', it='Persone e famiglia', tr='İnsanlar ve aile', ja='人と家族', ru='Люди и семья'),
 'love': dict(en='Love and relationships', es='Amor y relaciones', pt='Amor e relacionamentos', de='Liebe und Beziehungen', fr='Amour et relations', it='Amore e relazioni', tr='Aşk ve ilişkiler', ja='恋愛と人間関係', ru='Любовь и отношения'),
 'modern': dict(en='Modern life', es='Vida moderna', pt='Vida moderna', de='Modernes Leben', fr='Vie moderne', it='Vita moderna', tr='Modern hayat', ja='現代の暮らし', ru='Современная жизнь'),
}
LANG_NAME = dict(en='English', es='Español', pt='Português', de='Deutsch', fr='Français', it='Italiano', tr='Türkçe', ja='日本語', ru='Русский')

def esc(s): return html.escape(s or '', quote=True)
def slugify(s):
    s = re.sub(r'^(a|an|the)\s+', '', s.strip().lower())
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s or 'dream'
def tr_lower(s):
    return s.replace('I', 'ı').replace('İ', 'i').lower()
def low_first(s, lang):
    if lang == 'tr': return tr_lower(s)
    if lang in ('de', 'ja', 'ru') or not s: return s
    return s[0].lower() + s[1:]
def sentences(s, lang):
    if not s: return []
    parts = re.split(r'(?<=[。])' if lang == 'ja' else r'(?<=[.!?])\s+', s.strip())
    return [p.strip() for p in parts if p.strip()]
def path_for(lang, slug=None):
    root = '/dreams/' if lang == 'en' else f'/{lang}/dreams/'
    return root + (f'{slug}/' if slug else '')

CAT_IMG = dict(animals='oasis-moon', sky='nile-felucca', home='temple-hall', people='statue-moon', love='lotus-temple', body='abu-simbel', food='lotus-temple', modern='sphinx-night')
SHOT_LANG = dict(en='en', es='es', pt='pt', de='de', fr='fr', it='it', tr='tr', ja='ja', ru='ru')

def page(lang, title, desc, canonical, alternates, body, jsonld=None, hero='', img='sphinx-night'):
    ui = UI[lang]
    alt = '\n'.join(f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{BASE}{u}">' for l, u in alternates.items())
    alt += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}{alternates["en"]}">'
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ''
    cta_text = re.sub(r'^Place of Truth\s*[:：—–-]\s*', '', ui['cta'])
    cta_text = cta_text[:1].upper() + cta_text[1:]
    langs = ' · '.join(f'<a href="{alternates[l]}" hreflang="{l}">{LANG_NAME[l]}</a>' if l != lang else f'<b>{LANG_NAME[l]}</b>' for l in LANGS)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}{canonical}">
{alt}
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{BASE}/assets/pot/{img}-wide.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Cormorant+SC:wght@600&display=swap" rel="stylesheet">
<link rel="icon" href="/place-of-truth/icon.png" type="image/png">
<link rel="stylesheet" href="/dreams/dreams.css?v=2">
<style>.hero{{background-image:url(/assets/pot/{img}-wide.jpg)}}@media (max-width:700px){{.hero{{background-image:url(/assets/pot/{img}-tall.jpg)}}}}</style>
{ld}
</head>
<body>
<header class="top"><a class="brand" href="{path_for(lang)}"><img src="/place-of-truth/icon.png" alt="" width="32" height="32">{esc(ui['dict'])}</a></header>
{hero}
<main>
{body}
<aside class="cta">
  <img class="phone" src="/assets/pot/shots/{SHOT_LANG[lang]}/4.jpg" alt="Place of Truth" loading="lazy" width="150" height="267">
  <div><h3>Place of Truth</h3><p>{esc(cta_text)}</p><p class="soon">{esc(ui['soon'])}</p><a class="btn" href="/place-of-truth/">{esc(ui['cta_btn'])}</a></div>
</aside>
<p class="src">{esc(ui['source'])}</p>
</main>
<footer><span>{esc(ui['lang'])}:</span> {langs}<br><a href="/">K-Studio Apps</a></footer>
</body>
</html>
'''

def main():
    data = [d for d in json.load(open(SRC)) if not d.get('adult')]
    seen = {}
    for d in data:
        s = slugify(d['en']['title'])
        if s in seen: s = s + '-' + d['id'][2:].replace('_', '-')
        seen[s] = 1; d['slug'] = s
    # related: by shared words in en keys/near/title, then same category
    words = {d['id']: set((d['en'].get('keys', '') + ' ' + slugify(d['en']['title']).replace('-', ' ')).lower().split()) for d in data}
    near = {d['id']: set(d['en'].get('near', '').lower().split()) for d in data}
    for d in data:
        scored = []
        for e in data:
            if e is d: continue
            sc = 3 * len(near[d['id']] & words[e['id']]) + len(near[d['id']] & near[e['id']]) + (1 if e['category'] == d['category'] else 0)
            if sc: scored.append((sc, e['en']['title'], e))
        scored.sort(key=lambda x: (-x[0], x[1]))
        d['rel'] = [x[2] for x in scored[:8]]
    out_dirs = [os.path.join(SITE, 'dreams')] + [os.path.join(SITE, l, 'dreams') for l in LANGS if l != 'en']
    for od in out_dirs:
        if os.path.isdir(od):
            for f in os.listdir(od):
                p = os.path.join(od, f)
                if os.path.isdir(p): shutil.rmtree(p)
                elif f == 'index.html': os.remove(p)
    urls = []
    for lang in LANGS:
        ui = UI[lang]
        for d in data:
            t = d[lang]; title = t['title'] if lang != 'tr' else tr_lower(t['title'])
            alts = {l: path_for(l, d['slug']) for l in LANGS}
            canon = alts[lang]
            o = t['omen']
            gl = sentences(t.get('gloss', ''), lang)
            sign = ui['good'] if d.get('good') else ui['bad']
            rel = ''.join(f'<li><a href="{path_for(lang, e["slug"])}">{esc(e[lang]["title"])}</a></li>' for e in d['rel'])
            hero = f'''<section class="hero small"><div class="hero-in"><nav class="crumbs"><a href="{path_for(lang)}">{esc(ui['dict'])}</a> › {esc(CATS[d['category']][lang])}</nav><h1>{esc(ui['h1'].format(t=title))}</h1></div></section>'''
            body = f'''<article>
<div class="scroll">
<p class="dream">{esc(t['dream'])}</p>
<p class="omen">{esc(o)}</p>
<span class="sign {'good' if d.get('good') else 'bad'}">{esc(sign)}</span>
</div>
{('<h2>'+esc(ui['vars'])+'</h2><ul class="vars">'+''.join('<li>'+esc(g)+'</li>' for g in gl)+'</ul>') if gl else ''}
{('<h2>'+esc(ui['related'])+'</h2><ul class="rel">'+rel+'</ul>') if rel else ''}
</article>'''
            ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang,
                  "mainEntity": [{"@type": "Question", "name": ui['title'].format(t=title),
                                  "acceptedAnswer": {"@type": "Answer", "text": (o + ' ' + ' '.join(gl)).strip()}}]}
            html_ = page(lang, ui['title'].format(t=title), ui['desc'].format(l=low_first(title, lang), t=title, o=o)[:300], canon, alts, body, ld, hero=hero, img=CAT_IMG.get(d['category'], 'sphinx-night'))
            p = os.path.join(SITE, canon.strip('/'), 'index.html')
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, 'w', encoding='utf-8').write(html_)
            urls.append((canon, alts))
        # index
        n = len(data)
        groups = ''
        for cat in CATS:
            items = sorted([d for d in data if d['category'] == cat], key=lambda d: d[lang]['title'].lower())
            if not items: continue
            lis = ''.join(f'<li data-k="{esc((d[lang]["title"]+" "+d[lang].get("keys","")).lower())}"><a href="{path_for(lang, d["slug"])}">{esc(d[lang]["title"])}</a></li>' for d in items)
            groups += f'<section class="cat"><h2>{esc(CATS[cat][lang])}</h2><ul class="list">{lis}</ul></section>'
        alts = {l: path_for(l) for l in LANGS}
        hero = f'''<section class="hero"><div class="hero-in"><h1>{esc(ui['dict'])}</h1><p class="lead">{esc(ui['dict_desc'].format(n=n))}</p></div></section>'''
        body = f'''<input id="q" type="search" placeholder="{esc(ui['search'])}" aria-label="{esc(ui['search'])}" autocomplete="off">
{groups}
<script>
const q=document.getElementById('q');q.addEventListener('input',()=>{{const v=q.value.trim().toLowerCase();document.querySelectorAll('.list li').forEach(li=>{{li.hidden=v&&!li.dataset.k.includes(v)}});document.querySelectorAll('section.cat').forEach(s=>{{s.hidden=![...s.querySelectorAll('li')].some(li=>!li.hidden)}})}});
</script>'''
        html_ = page(lang, ui['dict_title'].format(n=n), ui['dict_desc'].format(n=n), alts[lang], alts, body, hero=hero, img='sphinx-night')
        p = os.path.join(SITE, alts[lang].strip('/'), 'index.html')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(html_)
        urls.append((alts[lang], alts))
    # sitemaps (Google: max 50k urls per file)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for u, alts in urls:
        sm.append(f'<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod>' + ''.join(f'<xhtml:link rel="alternate" hreflang="{HREFLANG[l]}" href="{BASE}{a}"/>' for l, a in alts.items()) + '</url>')
    sm.append('</urlset>')
    open(os.path.join(SITE, 'sitemap-dreams.xml'), 'w', encoding='utf-8').write('\n'.join(sm))
    print('dreams', len(data), 'pages', len(urls))

if __name__ == '__main__':
    main()
