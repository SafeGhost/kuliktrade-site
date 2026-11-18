# -*- coding: utf-8 -*-
"""Бесплатные шаблоны смет и счетов для мастеров (EN + ES) → kuliktrade.com/handyslip/templates/ и /es/handyslip/plantillas/
python3 _tools/build_handyslip.py"""
import os, html, shutil, json, datetime
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://kuliktrade.com'
PLAY = 'https://play.google.com/store/apps/details?id=com.kuliktrade.handyslip'
TODAY = datetime.date.today().isoformat()
def esc(s): return html.escape(s or '', quote=True)

# trade: slug, names, items (en, es, unit_en, unit_es, qty, rate), trade tip
T = [
 dict(slug='handyman', en='Handyman', es='Handyman', es_slug='handyman',
  items=[('Mount a TV (up to 65")','Montar TV (hasta 65")','each','c/u',1,120),('Assemble furniture','Armar muebles','hour','hora',2,65),('Patch a drywall hole','Reparar hoyo en drywall','each','c/u',2,90),('Replace a light fixture','Cambiar lámpara','each','c/u',1,110),('Travel fee','Cargo por traslado','visit','visita',1,25)],
  tip=('Bundle small jobs into one visit and set a minimum charge, so a 20-minute fix still pays for the drive.','Junta trabajos pequeños en una visita y pon un cargo mínimo, para que un arreglo de 20 minutos pague el viaje.')),
 dict(slug='house-cleaning', en='House cleaning', es='Limpieza de casas', es_slug='limpieza-de-casas',
  items=[('Standard cleaning, 2 bed / 1 bath','Limpieza estándar, 2 recámaras / 1 baño','visit','visita',1,140),('Deep cleaning add-on','Limpieza profunda adicional','hour','hora',2,50),('Inside the oven','Interior del horno','each','c/u',1,35),('Inside the fridge','Interior del refrigerador','each','c/u',1,35),('Interior windows','Ventanas por dentro','window','ventana',8,8)],
  tip=('Price by the home size and add extras line by line: clients see exactly what they pay for, and repeat visits are one tap.','Cobra por tamaño de casa y agrega extras por línea: el cliente ve qué paga y las visitas repetidas son un toque.')),
 dict(slug='moving', en='Moving', es='Mudanzas', es_slug='mudanzas',
  items=[('2 movers × 3 hours','2 cargadores × 3 horas','mover-hour','hora-cargador',6,60),('Truck fee','Cargo por camión','each','c/u',1,150),('Packing materials','Material de empaque','set','juego',1,60),('Stairs','Escaleras','flight','tramo',2,25),('Heavy item (safe, piano)','Objeto pesado (caja fuerte, piano)','each','c/u',1,150)],
  tip=('Write the crew and hours in one line ("2 movers × 3 hours") and state the minimum hours, so nobody argues at the end of the day.','Escribe cuadrilla y horas en una línea («2 cargadores × 3 horas») y el mínimo de horas, para no discutir al final.')),
 dict(slug='painting', en='Painting', es='Pintura', es_slug='pintura',
  items=[('Interior walls, 2 coats','Paredes interiores, 2 manos','sq ft','pie²',400,2.75),('Ceiling','Techo','sq ft','pie²',150,1.50),('Trim and baseboards','Molduras y zoclos','linear ft','pie lineal',120,1.75),('Doors','Puertas','each','c/u',3,75),('Paint and supplies','Pintura y materiales','set','juego',1,180)],
  tip=('Measure square feet of wall, not of floor, and list materials separately, so the client understands why two rooms cost differently.','Mide pies² de pared, no de piso, y separa los materiales, para que el cliente entienda por qué dos cuartos cuestan distinto.')),
 dict(slug='lawn-care', en='Lawn care', es='Jardinería', es_slug='jardineria',
  items=[('Mowing, up to 1/4 acre','Corte de pasto, hasta 1/4 acre','visit','visita',1,45),('Edging and trimming','Orillas y recorte','visit','visita',1,20),('Leaf removal','Retiro de hojas','hour','hora',2,55),('Hedge trimming','Poda de setos','hour','hora',1,60),('Mulch, installed','Mantillo instalado','cubic yard','yarda³',2,85)],
  tip=('Offer a recurring plan (weekly or every two weeks): one estimate, then an invoice for each visit.','Ofrece un plan recurrente (semanal o quincenal): un presupuesto y luego una factura por visita.')),
 dict(slug='pressure-washing', en='Pressure washing', es='Lavado a presión', es_slug='lavado-a-presion',
  items=[('Driveway','Entrada de autos','sq ft','pie²',600,0.25),('House siding','Fachada de la casa','sq ft','pie²',1500,0.30),('Deck','Terraza de madera','sq ft','pie²',300,0.45),('Fence','Cerca','linear ft','pie lineal',100,1.25)],
  tip=('Price by square foot and show each surface on its own line; clients often add the deck or fence once they see the price.','Cobra por pie² y pon cada superficie en su línea; muchos clientes agregan la terraza o la cerca al ver el precio.')),
 dict(slug='drywall', en='Drywall', es='Drywall', es_slug='drywall',
  items=[('Hang drywall','Instalar drywall','sq ft','pie²',300,1.75),('Tape and finish','Encintar y acabado','sq ft','pie²',300,1.25),('Patch a small hole','Reparar hoyo pequeño','each','c/u',3,90),('Texture match','Igualar textura','each','c/u',1,75),('Materials','Materiales','set','juego',1,140)],
  tip=('Separate hanging from finishing: if the client only needs patches, they see the patch price, not a whole-wall number.','Separa instalación de acabado: si el cliente solo necesita parches, ve el precio del parche y no el de toda la pared.')),
 dict(slug='flooring', en='Flooring', es='Pisos', es_slug='pisos',
  items=[('Remove old carpet','Retirar alfombra vieja','sq ft','pie²',250,0.75),('Underlayment','Base acústica','sq ft','pie²',250,0.50),('Install luxury vinyl plank','Instalar piso vinílico (LVP)','sq ft','pie²',250,3.25),('Baseboards','Zoclos','linear ft','pie lineal',90,3.50),('Transition strips','Perfiles de transición','each','c/u',3,25)],
  tip=('Add 10% to the square footage for cuts and waste, and say so on the estimate.','Suma 10% a los pies² por cortes y desperdicio, y escríbelo en el presupuesto.')),
 dict(slug='furniture-assembly', en='Furniture assembly', es='Armado de muebles', es_slug='armado-de-muebles',
  items=[('Bed frame','Base de cama','each','c/u',1,80),('Dresser','Cómoda','each','c/u',2,75),('Desk','Escritorio','each','c/u',1,70),('Bookcase','Librero','each','c/u',1,50),('Haul away boxes','Llevarse las cajas','visit','visita',1,20)],
  tip=('Price per item, not per hour: clients compare flat prices faster, and you win when you are quick.','Cobra por pieza, no por hora: el cliente compara precios fijos más rápido y tú ganas si eres ágil.')),
 dict(slug='tv-mounting', en='TV mounting', es='Instalación de TV', es_slug='instalacion-de-tv',
  items=[('Mount a TV up to 55"','Montar TV hasta 55"','each','c/u',1,99),('Mount a TV 56–75"','Montar TV de 56 a 75"','each','c/u',1,129),('Hide wires in the wall','Ocultar cables en la pared','each','c/u',1,99),('Mount a soundbar','Montar barra de sonido','each','c/u',1,60)],
  tip=('Ask the size and the wall type before you go, and list the wire concealment as its own line: it is the most common add-on.','Pregunta el tamaño y el tipo de pared antes de ir, y pon el ocultar cables como línea aparte: es el extra más común.')),
 dict(slug='junk-removal', en='Junk removal', es='Retiro de basura', es_slug='retiro-de-basura',
  items=[('Single item pickup','Recoger un objeto','each','c/u',1,89),('Quarter truck load','Un cuarto de camión','load','carga',1,175),('Heavy item surcharge','Cargo por objeto pesado','each','c/u',1,50),('Disposal fee','Cargo de desecho','load','carga',1,40)],
  tip=('Price by the share of your truck and show the disposal fee separately; it explains why mattresses and appliances cost more.','Cobra por fracción de camión y muestra el cargo de desecho aparte; explica por qué colchones y aparatos cuestan más.')),
]
UI = {
 'en': dict(est='Estimate', inv='Invoice', h1_est='Free {t} Estimate Template', h1_inv='Free {t} Invoice Template',
   t_est='Free {t} Estimate Template (Printable) with Example Prices', t_inv='Free {t} Invoice Template (Printable) with Example Prices',
   d_est='A clean, printable {tl} estimate template with typical line items and example prices. Print it, or make it on your phone in under a minute.',
   d_inv='A clean, printable {tl} invoice template with deposit, balance due and payment details. Print it, or send it from your phone in a minute.',
   intro_est='Here is a ready {tl} estimate with the lines clients expect to see. Change the prices to your own and print it, or save it as PDF.',
   intro_inv='Here is a ready {tl} invoice with a deposit, the balance due and how to pay. Change the prices to your own and print it, or save it as PDF.',
   your='Your Business Name', lic='License # · Insured', client='Client', addr='Job address', date='Date', no='No.', desc='Description', qty='Qty', unit='Unit', rate='Rate', amt='Amount',
   sub='Subtotal', tax='Sales tax', dep='Deposit to schedule', paid='Deposit paid', total='Total', due='Balance due', terms_est='This estimate is valid for 30 days. A deposit is due to schedule the job. Changes to the work are quoted separately.',
   terms_inv='Payment is due on completion. Pay by Zelle, Venmo, Cash App or PayPal. Thank you for your business!', sign='Client signature',
   print='Print or save as PDF', note='Example prices for illustration only. Set your own prices for your area.',
   app_h='Do it on your phone in under a minute', app_p='HandySlip makes this {doc} from your own price list, right at the client’s place: tap the services or just say the job, add your logo, get the client’s signature on the screen and send it by text, WhatsApp or email. Then turn the estimate into an invoice in one tap.',
   play='Get it on Google Play', free='Free to start · no account · works offline',
   tips_h='What to put on a {tl} {doc}', tips=['Your business name, phone and license number, so the client can call you back and trust you.','Each service on its own line with quantity, unit and rate. Clients accept clear lines faster than one big number.','Minimum charge, travel fee and materials as separate lines.','Deposit amount and when the rest is due.','Short terms: how long the price is valid and what happens if the job changes.'],
   trade_h='A tip for {tl}', more='More free templates', all='All templates', idx_t='Free Estimate and Invoice Templates for Home Services', idx_h='Free estimate and invoice templates', idx_d='Printable estimate and invoice templates for handymen, cleaners, movers, painters, lawn care and more, with typical line items and example prices.',
   lang='En español'),
 'es': dict(est='Presupuesto', inv='Factura', h1_est='Plantilla de presupuesto para {t} gratis', h1_inv='Plantilla de factura para {t} gratis',
   t_est='Plantilla de presupuesto para {t} gratis (imprimible) con precios de ejemplo', t_inv='Plantilla de factura para {t} gratis (imprimible) con precios de ejemplo',
   d_est='Plantilla de presupuesto de {tl} lista para imprimir, con conceptos típicos y precios de ejemplo. Imprímela o hazla en tu teléfono en menos de un minuto.',
   d_inv='Plantilla de factura de {tl} lista para imprimir, con anticipo, saldo y forma de pago. Imprímela o envíala desde tu teléfono en un minuto.',
   intro_est='Aquí tienes un presupuesto de {tl} con los conceptos que el cliente espera ver. Cambia los precios por los tuyos e imprímelo o guárdalo como PDF.',
   intro_inv='Aquí tienes una factura de {tl} con anticipo, saldo pendiente y forma de pago. Cambia los precios por los tuyos e imprímela o guárdala como PDF.',
   your='Nombre de tu negocio', lic='Licencia # · Asegurado', client='Cliente', addr='Dirección del trabajo', date='Fecha', no='No.', desc='Concepto', qty='Cant.', unit='Unidad', rate='Precio', amt='Importe',
   sub='Subtotal', tax='Impuesto', dep='Anticipo para agendar', paid='Anticipo pagado', total='Total', due='Saldo pendiente', terms_est='Este presupuesto es válido por 30 días. Se requiere anticipo para agendar. Los cambios al trabajo se cotizan aparte.',
   terms_inv='El pago se hace al terminar. Paga por Zelle, Venmo, Cash App o PayPal. ¡Gracias por tu confianza!', sign='Firma del cliente',
   print='Imprimir o guardar PDF', note='Precios de ejemplo solo como referencia. Pon tus propios precios según tu zona.',
   app_h='Hazlo en tu teléfono en menos de un minuto', app_p='HandySlip arma este {doc} con tu propia lista de precios, en casa del cliente: toca los servicios o simplemente dicta el trabajo en español, agrega tu logo, el cliente firma en la pantalla y lo envías por mensaje, WhatsApp o correo. Luego conviertes el presupuesto en factura con un toque.',
   play='Disponible en Google Play', free='Gratis para empezar · sin cuenta · funciona sin internet',
   tips_h='Qué poner en un {doc} de {tl}', tips=['El nombre de tu negocio, teléfono y número de licencia, para que el cliente te llame y confíe en ti.','Cada servicio en su línea con cantidad, unidad y precio. El cliente acepta más rápido líneas claras que un solo número grande.','Cargo mínimo, traslado y materiales como líneas aparte.','El anticipo y cuándo se paga el resto.','Condiciones cortas: cuánto tiempo vale el precio y qué pasa si cambia el trabajo.'],
   trade_h='Un consejo para {tl}', more='Más plantillas gratis', all='Todas las plantillas', idx_t='Plantillas gratis de presupuesto y factura para servicios del hogar', idx_h='Plantillas gratis de presupuesto y factura', idx_d='Plantillas imprimibles de presupuesto y factura para handyman, limpieza, mudanzas, pintura, jardinería y más, con conceptos típicos y precios de ejemplo.',
   lang='In English'),
}
def url(lang, tr=None, kind=None):
    if lang == 'en':
        root = '/handyslip/templates/'
        return root if not tr else f"{root}{tr['slug']}-{'estimate' if kind=='est' else 'invoice'}-template/"
    root = '/es/handyslip/plantillas/'
    return root if not tr else f"{root}{'presupuesto' if kind=='est' else 'factura'}-{tr['es_slug']}/"
def money(x): return f"${x:,.2f}"

CSS = '''<style>
.tpl{background:#fff;color:#222;border:1px solid var(--line);border-radius:12px;padding:28px;margin:18px 0;box-shadow:0 8px 24px rgba(0,0,0,.06);font-size:15px}
.tpl .hd{display:flex;justify-content:space-between;gap:16px;border-bottom:3px solid #e8590c;padding-bottom:12px;margin-bottom:14px}
.tpl .hd b{font-size:19px}.tpl .doc{font-size:26px;font-weight:800;color:#e8590c;text-align:right}
.tpl table{width:100%;border-collapse:collapse;margin:12px 0}.tpl th{background:#fbeee6;text-align:left;font-size:13px;padding:7px}.tpl td{border-bottom:1px solid #eee;padding:7px}
.tpl .r{text-align:right;white-space:nowrap}.tpl .tot td{border:none;padding:3px 7px}.tpl .tot .big{font-size:18px;font-weight:800}
.tpl .meta{display:grid;grid-template-columns:1fr 1fr;gap:4px 18px;font-size:14px}.tpl .terms{font-size:13px;color:#555;margin-top:10px}.tpl .sig{margin-top:26px;border-top:1px solid #999;width:240px;font-size:12px;color:#666;padding-top:4px}
.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.pbtn{font:inherit;padding:10px 16px;border-radius:10px;border:1px solid var(--line);background:var(--card);color:var(--text);cursor:pointer}
.app{display:grid;grid-template-columns:150px 1fr;gap:20px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;margin:28px 0}
.app img{width:150px;border-radius:14px;border:1px solid var(--line)}.gp{display:inline-block;background:#000;color:#fff;text-decoration:none;padding:10px 16px;border-radius:10px;font-weight:600;margin-top:6px}
.small{font-size:14px;color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px;padding:0;list-style:none}.grid a{display:block;padding:10px 12px;background:var(--card);border:1px solid var(--line);border-radius:10px;text-decoration:none}
@media print{header,.bar,.app,.tips,.more,footer,.small,.noprint{display:none!important}.tpl{border:none;box-shadow:none;padding:0}body{background:#fff}}
@media (max-width:560px){.app{grid-template-columns:90px 1fr}.app img{width:90px}.tpl{padding:16px}.tpl .meta{grid-template-columns:1fr}}
</style>'''

def doc_html(lang, tr, kind):
    u = UI[lang]; rows = ''; sub = 0
    for it in tr['items']:
        name = it[0] if lang == 'en' else it[1]; unit = it[2] if lang == 'en' else it[3]; q = it[4] or 1; r = it[5]
        a = q * r; sub += a
        rows += f'<tr><td>{esc(name)}</td><td class="r">{q:g}</td><td>{esc(unit)}</td><td class="r">{money(r)}</td><td class="r">{money(a)}</td></tr>'
    tax = round(sub * 0.0, 2)
    dep = round(sub * 0.3, -1)
    total = sub + tax
    totals = f'<tr><td class="r" colspan="4">{u["sub"]}</td><td class="r">{money(sub)}</td></tr><tr><td class="r" colspan="4">{u["tax"]}</td><td class="r">{money(tax)}</td></tr><tr><td class="r big" colspan="4">{u["total"]}</td><td class="r big">{money(total)}</td></tr>'
    if kind == 'est': totals += f'<tr><td class="r" colspan="4">{u["dep"]}</td><td class="r">{money(dep)}</td></tr>'
    else: totals += f'<tr><td class="r" colspan="4">{u["paid"]}</td><td class="r">−{money(dep)}</td></tr><tr><td class="r big" colspan="4">{u["due"]}</td><td class="r big">{money(total-dep)}</td></tr>'
    docname = u['est'] if kind == 'est' else u['inv']
    return f'''<div class="tpl"><div class="hd"><div><b>{u["your"]}</b><br>(555) 123-4567 · you@email.com<br><span style="font-size:13px;color:#666">{u["lic"]}</span></div><div class="doc">{docname.upper()}<div style="font-size:13px;color:#666;font-weight:400">{u["no"]} 1024 · {u["date"]}: ____/____/______</div></div></div>
<div class="meta"><div><b>{u["client"]}:</b> ______________________</div><div><b>{u["addr"]}:</b> ______________________</div></div>
<table><tr><th>{u["desc"]}</th><th class="r">{u["qty"]}</th><th>{u["unit"]}</th><th class="r">{u["rate"]}</th><th class="r">{u["amt"]}</th></tr>{rows}</table>
<table class="tot">{totals}</table>
<p class="terms">{u["terms_est"] if kind=="est" else u["terms_inv"]}</p>{'<div class="sig">'+u["sign"]+'</div>' if kind=="est" else ''}</div>'''

def page(lang, title, desc, canon, alt, body):
    other = 'es' if lang == 'en' else 'en'
    alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{a}">' for l, a in alt.items()) + (f'<link rel="alternate" hreflang="x-default" href="{BASE}{alt["en"]}">' if 'en' in alt else '')
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}{canon}">
{alts}
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="{BASE}/handyslip/shots/1.jpg">
<link rel="icon" href="/handyslip/icon.png" type="image/png">
<link rel="stylesheet" href="/handyslip/style.css">
{CSS}
</head>
<body>
<main>
<header><img src="/handyslip/icon.png" alt=""><a href="/handyslip/">HandySlip</a></header>
{body}
</main>
<footer style="max-width:760px;margin:0 auto;padding:0 16px 40px;font-size:14px" class="small"><a href="{alt.get(other, url(other))}">{UI[lang]["lang"]}</a> · <a href="/">K-Studio Apps</a> · <a href="/handyslip/privacy.html">Privacy</a></footer>
</body>
</html>
'''

def app_block(lang, kind):
    u = UI[lang]; doc = (u['est'] if kind == 'est' else u['inv']).lower()
    return f'''<section class="app"><img src="/handyslip/shots/{'2' if kind=='est' else '4'}.jpg" alt="HandySlip app" loading="lazy"><div><h2 style="margin-top:0">{u["app_h"]}</h2><p>{esc(u["app_p"].format(doc=doc))}</p><a class="gp" href="{PLAY}&utm_source=kuliktrade&utm_medium=template">▶ {u["play"]}</a><p class="small">{u["free"]}</p></div></section>'''

def main():
    for d in ['handyslip/templates', 'es/handyslip/plantillas']:
        p = os.path.join(SITE, d)
        if os.path.isdir(p): shutil.rmtree(p)
    urls = []
    for lang in ['en', 'es']:
        u = UI[lang]
        for tr in T:
            tname = tr[lang]; tl = tname.lower() if lang == 'en' else tname.lower()
            for kind in ['est', 'inv']:
                alt = {l: url(l, tr, kind) for l in ['en', 'es']}
                canon = alt[lang]; doc = (u['est'] if kind == 'est' else u['inv']).lower()
                title = (u['t_est'] if kind == 'est' else u['t_inv']).format(t=tname)
                desc = (u['d_est'] if kind == 'est' else u['d_inv']).format(tl=tl)
                h1 = (u['h1_est'] if kind == 'est' else u['h1_inv']).format(t=tname if lang=='en' else tl)
                other_kind = 'inv' if kind == 'est' else 'est'
                more = ''.join(f'<li><a href="{url(lang, t2, kind)}">{esc((u["h1_est"] if kind=="est" else u["h1_inv"]).format(t=t2[lang] if lang=="en" else t2[lang].lower()))}</a></li>' for t2 in T if t2 is not tr)
                tip = tr['tip'][0 if lang == 'en' else 1]
                body = f'''<h1>{esc(h1)}</h1>
<p>{esc((u['intro_est'] if kind=='est' else u['intro_inv']).format(tl=tl))}</p>
<div class="bar noprint"><button class="pbtn" onclick="window.print()">🖨 {u["print"]}</button><a href="{url(lang, tr, other_kind)}">{esc((u["h1_inv"] if kind=="est" else u["h1_est"]).format(t=tname if lang=="en" else tl))} →</a></div>
{doc_html(lang, tr, kind)}
<p class="small">{u["note"]}</p>
{app_block(lang, kind)}
<section class="tips"><h2>{esc(u["tips_h"].format(tl=tl, doc=doc))}</h2><ul>{''.join('<li>'+esc(x)+'</li>' for x in u["tips"])}</ul>
<h2>{esc(u["trade_h"].format(tl=tl))}</h2><p>{esc(tip)}</p></section>
<section class="more"><h2>{u["more"]}</h2><ul class="grid">{more}</ul><p><a href="{url(lang)}">{u["all"]} →</a></p></section>'''
                p = os.path.join(SITE, canon.strip('/'), 'index.html'); os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, 'w', encoding='utf-8').write(page(lang, title, desc, canon, alt, body)); urls.append(canon)
        # index
        lis = ''
        for tr in T:
            t = tr[lang] if lang == 'en' else tr[lang]
            lis += f'<li><a href="{url(lang, tr, "est")}">{esc(t)}: {u["est"].lower()}</a></li><li><a href="{url(lang, tr, "inv")}">{esc(t)}: {u["inv"].lower()}</a></li>'
        alt = {l: url(l) for l in ['en', 'es']}
        body = f'<h1>{u["idx_h"]}</h1><p>{u["idx_d"]}</p><ul class="grid">{lis}</ul>{app_block(lang, "est")}'
        p = os.path.join(SITE, url(lang).strip('/'), 'index.html'); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(page(lang, u['idx_t'], u['idx_d'], url(lang), alt, body)); urls.append(url(lang))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'] + [f'<url><loc>{BASE}{x}</loc><lastmod>{TODAY}</lastmod></url>' for x in urls] + ['</urlset>']
    open(os.path.join(SITE, 'sitemap-handyslip.xml'), 'w', encoding='utf-8').write('\n'.join(sm))
    print('pages', len(urls))
if __name__ == '__main__': main()
