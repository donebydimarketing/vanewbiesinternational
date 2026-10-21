import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://www.vanewbiesinternational.com"
NAME = "VA Newbies International"
EMAIL = "hello@vanewbiesinternational.com"
PHONE_DISPLAY = "+1 (602) 623-5977"
PHONE_TEL = "+16026235977"
FORM = "https://form.jotform.com/262884618903064"
OG = SITE + "/assets/og-cover.png"

FAQS = [
    ("Do I need experience to join?",
     "No. Training starts from the basics. You do not need a portfolio or a past job to begin."),
    ("What is a virtual assistant?",
     "A virtual assistant, or VA, is a person who helps a business from a distance. A VA handles tasks such as email, scheduling, research, social media and customer support. The work is done online for clients in any country."),
    ("Is this only for Filipino VAs?",
     "No. Membership is open to English speakers from any country. Coach Di grew up in the Philippines and now lives in the United States. That background shapes the training, and it does not limit who can join."),
    ("Will I be paid during client training?",
     "No. The client practice is an unpaid internship. It gives you real experience and work samples. You finish ready to earn."),
    ("How much does it cost?",
     "There are three tiers. Starter is $97, Spark is $180 and Surge is $299. Each one is a one time fee. There are no payment plans and no monthly charges."),
    ("How long does training take?",
     "It depends on you. Most members move to client practice within weeks."),
    ("Which countries can I join from?",
     "You can join from any country. We welcome members from the US, the UK, Canada, Australia and beyond. All training is in English."),
    ("How is this different from other VA courses?",
     "Most VA courses are recorded lessons. This program is built around real client practice. You learn the skill, then you use it with a real business."),
]
HOME_FAQ = [0, 1, 3, 4, 2, 6]

TIERS = [
    ("starter", "Starter", "$97", ["The first step into VA training", "Core VA skills for complete beginners", "Learn at your own pace"]),
    ("spark", "Spark", "$180", ["2 hours of coaching calls for your questions", "Discord access", "3 months of portal access"]),
    ("surge", "Surge", "$299", ["Everything in Spark", "More practice with host businesses", "Built for the fastest path to client work"]),
]

NAV = [("/", "Home"), ("/about/", "About"), ("/services/", "Membership"), ("/faq/", "Questions"), ("/contact/", "Contact")]


def esc(s):
    return html.escape(s, quote=True)


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


ORG = {
    "@type": ["Organization", "EducationalOrganization"],
    "@id": SITE + "/#organization",
    "name": NAME,
    "url": SITE + "/",
    "logo": SITE + "/assets/logo.svg",
    "description": "VA Newbies International trains complete beginners to work as virtual assistants for international clients. Training is in English and includes group coaching and an unpaid internship with real businesses.",
    "founder": {"@id": SITE + "/about/#coach-di"},
    "email": EMAIL,
    "telephone": PHONE_TEL,
    "address": {"@type": "PostalAddress", "addressLocality": "Phoenix", "addressRegion": "AZ", "addressCountry": "US"},
    "areaServed": "Worldwide",
    "knowsLanguage": "en",
}
PERSON = {
    "@type": "Person",
    "@id": SITE + "/about/#coach-di",
    "name": "Coach Di",
    "jobTitle": "Founder and VA Trainer",
    "worksFor": {"@id": SITE + "/#organization"},
    "url": SITE + "/about/",
    "alumniOf": [
        {"@type": "CollegeOrUniversity", "name": "Polytechnic University of the Philippines"},
        {"@type": "CollegeOrUniversity", "name": "AMA Computer University"},
    ],
    "knowsAbout": ["Virtual assistant training", "Virtual assistant services", "Digital marketing", "Remote work"],
}
WEBSITE = {
    "@type": "WebSite",
    "@id": SITE + "/#website",
    "url": SITE + "/",
    "name": NAME,
    "publisher": {"@id": SITE + "/#organization"},
    "inLanguage": "en",
}


def faq_ld(idx):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": FAQS[i][0], "acceptedAnswer": {"@type": "Answer", "text": FAQS[i][1]}}
            for i in idx
        ],
    }


def crumbs_ld(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": n + 1, "name": name, "item": SITE + path}
            for n, (path, name) in enumerate(items)
        ],
    }


def head(title, desc, path, ld, noindex=False):
    graph = {"@context": "https://schema.org", "@graph": ld}
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{SITE}{path}">
<meta name="theme-color" content="#000000">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{OG}">
<meta property="og:image:alt" content="VA Newbies International, virtual assistant training worldwide">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{OG}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;600;700&family=Playfair+Display:ital,wght@0,600;0,800;0,900;1,600;1,700&display=swap">
<link rel="stylesheet" href="/assets/styles.css">
{jsonld(graph)}
</head>
<body>
<div class="progress" aria-hidden="true"></div>
<a class="skip" href="#main">Skip to main content</a>
"""


def header(current):
    links = ""
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        links += f'<a href="{href}"{cur}>{label}</a>'
    links += '<a class="cta" href="/apply/">Apply</a>'
    return f"""<header>
<div class="topbar"><div class="wrap"><span>Virtual assistant training, worldwide</span><span>Phoenix, Arizona, USA</span><span>Taught in English</span></div></div>
<div class="masthead"><a class="brand" href="/" aria-label="{NAME}, home">VA Newbies International<span>The training that turns beginners into virtual assistants</span></a></div>
<div class="navbar"><div class="wrap">
<button class="menu-btn" aria-expanded="false" aria-controls="site-nav">Menu</button>
<nav class="nav" id="site-nav" aria-label="Main">{links}</nav>
</div></div>
</header>
<main id="main">
"""


def footer():
    return f"""</main>
<a class="sticky-cta" href="/apply/">Apply now</a>
<footer class="foot">
<div class="wrap">
<div class="foot-grid">
<div>
<a class="brand" href="/">VA Newbies International</a>
<p style="margin-top:14px;max-width:26em">Virtual assistant training for complete beginners. Founded by Coach Di in Phoenix, Arizona.</p>
</div>
<div>
<h2>Read</h2>
<ul>
<li><a href="/">Home</a></li>
<li><a href="/about/">About</a></li>
<li><a href="/services/">Membership</a></li>
<li><a href="/faq/">Questions</a></li>
<li><a href="/apply/">Apply</a></li>
</ul>
</div>
<div>
<h2>Contact</h2>
<ul>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
<li><a href="/contact/#host-clients">Host clients</a></li>
</ul>
</div>
</div>
<small>&copy; <span id="year">2026</span> {NAME}. All rights reserved.</small>
</div>
</footer>
<script src="/assets/main.js" defer></script>
</body>
</html>
"""


def faq_block(idx):
    out = '<div class="faq">'
    for i in idx:
        q, a = FAQS[i]
        out += f'<details><summary>{esc(q)}</summary><div class="ans"><p>{esc(a)}</p></div></details>'
    return out + "</div>"


def quiz_block():
    def opts(name, rows):
        s = ""
        for val, text in rows:
            s += f'<label class="opt"><input type="radio" name="{name}" value="{val}"><span>{esc(text)}</span></label>'
        return s
    return f"""<form class="quiz" id="tier-quiz" aria-label="Find your tier">
<fieldset><legend>1. Where are you right now?</legend>
{opts("q1", [("starter", "I have never worked online."), ("spark", "I have tried a little."), ("surge", "I have done some VA work.")])}
</fieldset>
<fieldset><legend>2. What help do you want?</legend>
{opts("q2", [("starter", "I will learn on my own."), ("spark", "I want a coach to answer my questions."), ("surge", "I want to practice with real businesses.")])}
</fieldset>
<fieldset><legend>3. What is your goal?</legend>
{opts("q3", [("starter", "Learn the basics first."), ("spark", "Build skills with live help."), ("surge", "Get ready for clients fast.")])}
</fieldset>
<div class="result" id="quiz-result" aria-live="polite"></div>
</form>"""


def write(path, content):
    full = os.path.join(ROOT, path.strip("/"), "index.html") if path != "/" else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------- HOME ----------------
def home():
    title = "VA Newbies International | Virtual Assistant Training for Beginners"
    desc = "Learn to work as a virtual assistant with no experience. Get coaching, real client practice in an unpaid internship, and a worldwide member community."
    ld = [ORG, WEBSITE, PERSON, faq_ld(HOME_FAQ)]
    h = head(title, desc, "/", ld) + header("/")
    h += f"""
<section class="hero" style="padding-bottom:46px">
<div class="wrap hero-grid">
<div>
<div class="kicker">Cover story</div>
<h1>From complete beginner to <em>VA Newbies International member.</em></h1>
</div>
<div class="stand">
<p>This program trains people with no experience to work as virtual assistants for clients around the world. You do not need a portfolio to start.</p>
<div class="btns"><a class="btn" href="/apply/">Apply now</a><a class="btn ghost" href="#how">See how it works</a></div>
<a class="sub-link" href="/contact/#host-clients">Are you a host client? Start here.</a>
<div class="byline">By Coach Di, Founder and VA Trainer</div>
</div>
</div>
</section>

<div class="ticker" aria-hidden="true"><div class="ticker-track">
{"".join('<span>No experience needed</span><span>Real client practice</span><span>Group coaching</span><span>Taught in English</span><span>Members worldwide</span>' for _ in range(4))}
</div></div>

<section class="answer reveal" style="padding:34px 0"><div class="wrap answer-grid">
<h2>What is VA Newbies International?</h2>
<p>VA Newbies International is an English language virtual assistant training program. Coach Di founded it in Phoenix, Arizona. It trains complete beginners to work as virtual assistants for international clients. Members learn core VA skills, join group coaching, and practice with real businesses in an unpaid internship.</p>
</div></section>

<div class="wrap reveal" style="padding-bottom:20px">
<div class="stats" role="list">
<div class="stat" role="listitem"><b data-count="24" data-suffix="K+">24K+</b><small>Page followers</small></div>
<div class="stat" role="listitem"><b data-count="2.5" data-suffix="K+">2.5K+</b><small>Free group members</small></div>
<div class="stat" role="listitem"><b data-count="350" data-suffix="+">350+</b><small>VAs trained</small></div>
<div class="stat" role="listitem"><b data-count="9" data-suffix="+">9+</b><small>Years of experience</small></div>
</div>
</div>

<section id="who">
<div class="wrap">
<div class="label reveal">Feature 01 <span>Who this is for</span></div>
<h2 class="sec-title reveal">You do not need experience. You need a starting point.</h2>
<div class="three reveal">
<article><span class="num" aria-hidden="true">1</span><h3>Complete beginners</h3><p>You have never worked online. You start from zero and we start with you.</p></article>
<article><span class="num" aria-hidden="true">2</span><h3>Career shifters</h3><p>You were laid off, burned out, or ready for a change. Your willingness to learn matters more than your past jobs.</p></article>
<article><span class="num" aria-hidden="true">3</span><h3>Parents going remote</h3><p>You want income that fits around your family. VA work can be done from home, on a flexible schedule.</p></article>
</div>
</div>
</section>

<section class="dark" id="get">
<div class="wrap">
<div class="label reveal">Feature 02 <span>What you get</span></div>
<h2 class="sec-title reveal">Training built around real client work, not theory.</h2>
<div class="four reveal">
<article><h3>Skill training</h3><p>Learn the core VA skills step by step. This includes the tools international clients use.</p></article>
<article><h3>Group coaching</h3><p>Join live sessions. Ask your questions and get answers in real time.</p></article>
<article><h3>Real client practice</h3><p>Work with real businesses in a structured, unpaid internship. No simulations.</p></article>
<article><h3>A member community</h3><p>Learn next to people at the same stage. You are never starting alone.</p></article>
</div>
</div>
</section>

<div class="pull reveal"><div class="wrap"><blockquote>Your first client is closer than you think.</blockquote></div></div>

<section id="how" style="padding-top:20px">
<div class="wrap">
<div class="label reveal">Feature 03 <span>How it works</span></div>
<h2 class="sec-title reveal">Four steps from beginner to member.</h2>
<ol class="steps reveal">
<li><div><h3>Apply</h3><p>Fill in a short application. It includes a work style assessment so we can place you well.</p></div></li>
<li><div><h3>Train</h3><p>Learn the core VA skills and join group coaching with Coach Di.</p></div></li>
<li><div><h3>Practice with real clients</h3><p>Work with real businesses in an unpaid internship. You build experience and work samples.</p></div></li>
<li><div><h3>Become a member</h3><p>Graduate as a VA Newbies International member and take your skills to international clients.</p></div></li>
</ol>
</div>
</section>

<section class="dark" id="coach">
<div class="wrap">
<div class="label reveal">Feature 04 <span>Meet the trainer</span></div>
<div class="profile reveal">
<div class="monogram" role="img" aria-label="Coach Di, founder of VA Newbies International, virtual assistant trainer"><span>Founder</span><b>Di</b><span>Coach Di</span></div>
<div>
<h2 class="sec-title">Nine years of client work in one training path.</h2>
<p class="lede">Coach Di has more than nine years of digital work behind her. She has trained over 350 virtual assistants and served clients in more than 100 businesses around the world.</p>
<p>The training teaches by practice. You do the work with guidance until the skill feels natural.</p>
<div class="btns"><a class="btn" href="/about/">Read her story</a></div>
</div>
</div>
</div>
</section>

<section id="find">
<div class="wrap">
<div class="label reveal">Interactive <span>Find your tier</span></div>
<h2 class="sec-title reveal">Answer three questions. Get your match.</h2>
<div class="reveal">{quiz_block()}</div>
<p class="note">Want to compare every tier? <a href="/services/">See all membership tiers</a>.</p>
</div>
</section>

<section class="dark" id="questions">
<div class="wrap">
<div class="label reveal">Questions <span>Answered</span></div>
<h2 class="sec-title reveal">What people ask us most.</h2>
<div class="reveal" style="color:#000;background:#fff;padding:10px 30px">{faq_block(HOME_FAQ)}</div>
<p class="note"><a href="/faq/">Read all questions</a></p>
</div>
</section>

<section class="cta-final">
<div class="wrap reveal">
<h2>Ready to start your VA career?</h2>
<div class="btns"><a class="btn" href="/apply/">Join VA Newbies International</a><a class="btn ghost" href="/contact/">Ask a question</a></div>
</div>
</section>
"""
    h += footer()
    write("/", h)


# ---------------- ABOUT ----------------
def about():
    title = "About Coach Di | VA Newbies International"
    desc = "Meet Coach Di, founder of VA Newbies International. She has 9+ years of digital work, has trained 350+ virtual assistants and has served clients worldwide."
    ld = [ORG, WEBSITE, PERSON, crumbs_ld([("/", "Home"), ("/about/", "About")])]
    h = head(title, desc, "/about/", ld) + header("/about/")
    h += """
<div class="page-head"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / About</div>
<h1>The story behind the training.</h1>
<p>VA Newbies International was built for people who were told they needed experience they did not have.</p>
</div></div>

<section>
<div class="wrap">
<div class="profile reveal">
<div>
<div class="monogram" role="img" aria-label="Coach Di, founder of VA Newbies International, virtual assistant trainer"><span>Founder and VA Trainer</span><b>Di</b><span>Phoenix, Arizona</span></div>
<ul class="facts">
<li><b>Experience</b><span>9+ years in digital work</span></li>
<li><b>Trained</b><span>350+ virtual assistants</span></li>
<li><b>Served</b><span>100+ clients worldwide</span></li>
<li><b>Base</b><span>Phoenix, Arizona, USA</span></li>
</ul>
</div>
<div class="cols" style="column-count:1">
<p class="lede dropcap">Coach Di never worked in a corporate job. Every role she looked at asked for experience she did not have. She started anyway.</p>
<p>She built her career as a virtual assistant and worked her way up. By her second year she was managing four clients at once. Over time she worked with authors, publishers and growing businesses in many countries.</p>
<p>She holds a bachelor's degree in Marketing Management from the Polytechnic University of the Philippines. She also holds a two year associate degree in Business Management from AMA Computer University.</p>
<p>Today she trains new virtual assistants. She has trained more than 350 of them. The training is simple. You learn a skill, you practice it with a real business, and you keep going until it feels natural.</p>
<p>VA Newbies International is open to English speakers from any country. Members start as newbies. They graduate as VA Newbies International members.</p>
<div class="btns"><a class="btn" href="/apply/">Apply now</a><a class="btn ghost" href="/services/">See membership tiers</a></div>
</div>
</div>
</div>
</section>

<section class="dark">
<div class="wrap">
<div class="label reveal">What we stand for</div>
<div class="three reveal" style="border-color:#fff">
<article style="border-color:#fff"><span class="num" aria-hidden="true">1</span><h3>Start where you are</h3><p>No portfolio and no past job needed. A starting point is enough.</p></article>
<article style="border-color:#fff"><span class="num" aria-hidden="true">2</span><h3>Practice over theory</h3><p>You learn by doing real work for real businesses.</p></article>
<article style="border-color:#fff"><span class="num" aria-hidden="true">3</span><h3>Plain, honest training</h3><p>The client practice is an unpaid internship. We say so up front. It builds the experience you need to earn.</p></article>
</div>
</div>
</section>

<section class="cta-final"><div class="wrap reveal">
<h2>Your first client is closer than you think.</h2>
<div class="btns"><a class="btn" href="/apply/">Join VA Newbies International</a></div>
</div></section>
"""
    h += footer()
    write("/about/", h)


# ---------------- SERVICES ----------------
def services():
    title = "Membership Tiers and Prices | VA Newbies International"
    desc = "VA Newbies International membership: Starter $97, Spark $180, Surge $299. One time fees with no monthly charges. Find the tier that fits you."
    courses = []
    for _, name, price, feats in TIERS:
        courses.append({
            "@type": "Course",
            "name": f"VA Newbies International {name}",
            "description": "; ".join(feats),
            "provider": {"@id": SITE + "/#organization"},
            "inLanguage": "en",
            "offers": {"@type": "Offer", "price": price.replace("$", ""), "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": SITE + "/apply/"},
            "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online"},
        })
    ld = [ORG, WEBSITE] + courses + [crumbs_ld([("/", "Home"), ("/services/", "Membership")])]
    h = head(title, desc, "/services/", ld) + header("/services/")
    cards = ""
    for key, name, price, feats in TIERS:
        lis = "".join(f"<li>{esc(f)}</li>" for f in feats)
        cards += f'<article class="tier" data-tier="{key}"><div class="name">{name}</div><div class="price">{price}</div><div class="once">One time fee</div><ul>{lis}</ul><a class="btn" href="/apply/">Apply for {name}</a></article>'
    h += f"""
<div class="page-head"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / Membership</div>
<h1>Pick the tier that fits you.</h1>
<p>Three tiers. One time fees. No payment plans and no monthly charges. All prices are in US dollars.</p>
</div></div>

<section>
<div class="wrap">
<div class="tiers reveal">{cards}</div>
<p class="note">Every member starts with the application. Payments are processed through Stripe.</p>
<div class="invite reveal">
<div><div class="kicker">By invitation only</div><h3>Executive Function</h3><p>This level is not for sale. Members are invited from within the program.</p></div>
<div><div class="kicker">By invitation only</div><h3>Vaulted VA</h3><p>A premium placement level. Members are invited from within the program.</p></div>
</div>
</div>
</section>

<section class="dark">
<div class="wrap">
<div class="label reveal">Interactive <span>Not sure? Take the quiz</span></div>
<h2 class="sec-title reveal">Answer three questions. We will highlight your tier above.</h2>
<div class="reveal" style="background:#fff;color:#000">{quiz_block()}</div>
</div>
</section>

<section>
<div class="wrap">
<div class="label reveal">Questions <span>About membership</span></div>
<div class="reveal">{faq_block([4, 3, 0])}</div>
</div>
</section>

<section class="cta-final"><div class="wrap reveal">
<h2>Ready when you are.</h2>
<div class="btns"><a class="btn" href="/apply/">Apply now</a></div>
</div></section>
"""
    h += footer()
    write("/services/", h)


# ---------------- FAQ ----------------
def faq():
    title = "Questions and Answers | VA Newbies International"
    desc = "Answers about VA Newbies International: experience needed, cost, the unpaid internship, countries, training time and how it differs from other VA courses."
    ld = [ORG, WEBSITE, faq_ld(range(len(FAQS))), crumbs_ld([("/", "Home"), ("/faq/", "Questions")])]
    h = head(title, desc, "/faq/", ld) + header("/faq/")
    h += f"""
<div class="page-head"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / Questions</div>
<h1>Questions, answered.</h1>
<p>Short, direct answers about the program.</p>
</div></div>
<section><div class="wrap"><div class="reveal">{faq_block(range(len(FAQS)))}</div>
<p class="note">Your question is not here? <a href="/contact/">Send it to us</a>.</p></div></section>
<section class="cta-final dark"><div class="wrap reveal">
<h2>Ready to begin?</h2>
<div class="btns"><a class="btn" href="/apply/">Apply now</a></div>
</div></section>
"""
    h += footer()
    write("/faq/", h)


# ---------------- APPLY ----------------
def apply():
    title = "Apply | VA Newbies International"
    desc = "Apply to join VA Newbies International. The application takes a few minutes and includes a short work style assessment."
    ld = [ORG, WEBSITE, crumbs_ld([("/", "Home"), ("/apply/", "Apply")])]
    h = head(title, desc, "/apply/", ld) + header("/apply/")
    h += f"""
<div class="page-head"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / Apply</div>
<h1>Apply to join.</h1>
<p>The application takes a few minutes. It includes a short work style assessment so we can place you well.</p>
</div></div>
<section><div class="wrap">
<div class="three" style="border-top:0">
<article><span class="num" aria-hidden="true">1</span><h3>Fill in the form</h3><p>Tell us about you and answer the short assessment.</p></article>
<article><span class="num" aria-hidden="true">2</span><h3>We review it</h3><p>We read every application and reply by email.</p></article>
<article><span class="num" aria-hidden="true">3</span><h3>Start training</h3><p>You begin on your tier and join the community.</p></article>
</div>
<div class="embed"><iframe src="{FORM}" title="VA Newbies International application form" loading="lazy" allow="geolocation"></iframe></div>
<p class="note">The form does not load? <a href="{FORM}" rel="noopener">Open the application in a new tab</a>.</p>
</div></section>
"""
    h += footer()
    write("/apply/", h)


# ---------------- CONTACT ----------------
def contact():
    title = "Contact | VA Newbies International"
    desc = "Contact VA Newbies International by email, phone or WhatsApp. Host clients can also ask how to give members real practice work."
    ld = [ORG, WEBSITE, crumbs_ld([("/", "Home"), ("/contact/", "Contact")])]
    h = head(title, desc, "/contact/", ld) + header("/contact/")
    h += f"""
<div class="page-head"><div class="wrap">
<div class="crumbs"><a href="/">Home</a> / Contact</div>
<h1>Talk to us.</h1>
<p>We reply by message. Send an email or a WhatsApp and we will get back to you.</p>
</div></div>
<section><div class="wrap">
<div class="contact-grid reveal">
<div><h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p><h3>Phone</h3><p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p><h3>WhatsApp</h3><p><a href="https://wa.me/19282582204" rel="noopener">+1 (928) 258-2204</a></p></div>
<div><h3>Location</h3><p>Phoenix, Arizona, USA</p><h3>Language</h3><p>All training and support are in English.</p></div>
</div>
</div></section>
<section class="dark" id="host-clients"><div class="wrap">
<div class="label reveal">For businesses <span>Host clients</span></div>
<h2 class="sec-title reveal">Give a member real work to practice on.</h2>
<p class="lede reveal">Host clients are businesses that work with our members during the unpaid internship. You get a trained assistant on real tasks. The member gets real experience.</p>
<div class="btns reveal"><a class="btn" href="mailto:{EMAIL}?subject=Host%20client%20interest">Email us about hosting</a></div>
</div></section>
"""
    h += footer()
    write("/contact/", h)


def notfound():
    h = head("Page not found | " + NAME, "This page could not be found.", "/404.html", [ORG], noindex=True) + header("")
    h += """
<section class="cta-final"><div class="wrap">
<h1 style="font-size:clamp(2.4rem,6.4vw,5.4rem);max-width:12em;margin:0 auto 26px">This page is not here.</h1>
<div class="btns"><a class="btn" href="/">Go home</a><a class="btn ghost" href="/apply/">Apply now</a></div>
</div></section>
"""
    h += footer()
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(h)


def extras():
    pages = ["/", "/about/", "/services/", "/faq/", "/apply/", "/contact/"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in pages:
        sm += f"  <url><loc>{SITE}{p}</loc><lastmod>2026-10-21</lastmod></url>\n"
    sm += "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(sm)

    bots = ["GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-Web", "anthropic-ai", "PerplexityBot", "Google-Extended", "Applebot-Extended", "CCBot", "Bingbot", "Googlebot"]
    rb = "User-agent: *\nAllow: /\n\n"
    for b in bots:
        rb += f"User-agent: {b}\nAllow: /\n\n"
    rb += f"Sitemap: {SITE}/sitemap.xml\n"
    open(os.path.join(ROOT, "robots.txt"), "w").write(rb)

    llm = f"""# {NAME}

> {NAME} is an English language virtual assistant (VA) training program founded by Coach Di in Phoenix, Arizona, USA. It trains complete beginners to work as virtual assistants for international clients. Members learn core VA skills, join group coaching and practice with real businesses in an unpaid internship.

## Key facts
- Founder: Coach Di. 9+ years of digital work. Has trained 350+ virtual assistants and served 100+ clients worldwide.
- Who it is for: complete beginners, career shifters and parents going remote. No experience or portfolio needed.
- Language: English. Open to members from any country.
- Client practice: a structured, unpaid internship with real businesses.
- Tiers (one time fees in USD, no payment plans, no monthly charges): Starter $97, Spark $180, Surge $299.
- Spark includes 2 hours of coaching calls, Discord access and 3 months of portal access. Surge includes everything in Spark plus more host business practice.
- Executive Function and Vaulted VA are by invitation only.
- Community: 24K+ page followers and 2.5K+ free group members.
- Contact: {EMAIL}, {PHONE_DISPLAY}

## Pages
- [Home]({SITE}/): What the program is and how it works
- [About]({SITE}/about/): Coach Di's story and credentials
- [Membership]({SITE}/services/): Tiers, prices and what each includes
- [Questions]({SITE}/faq/): Answers to common questions
- [Apply]({SITE}/apply/): Application form
- [Contact]({SITE}/contact/): Email, phone and host client information
"""
    open(os.path.join(ROOT, "llms.txt"), "w").write(llm)
    open(os.path.join(ROOT, ".nojekyll"), "w").write("")

    logo = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 120" role="img" aria-label="VA Newbies International"><rect width="400" height="120" fill="#fff"/><text x="200" y="68" text-anchor="middle" font-family="Georgia,serif" font-weight="900" font-size="46" fill="#000">VA Newbies</text><text x="200" y="100" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="26" fill="#000">International</text></svg>'
    open(os.path.join(ROOT, "assets", "logo.svg"), "w").write(logo)
    fav = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#000"/><text x="32" y="45" text-anchor="middle" font-family="Georgia,serif" font-weight="900" font-size="36" fill="#fff">VA</text></svg>'
    open(os.path.join(ROOT, "assets", "favicon.svg"), "w").write(fav)

    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new("RGB", (1200, 630), "white")
        d = ImageDraw.Draw(img)
        d.rectangle([40, 40, 1160, 590], outline="black", width=6)
        d.rectangle([52, 52, 1148, 578], outline="black", width=2)
        def font(sz, bold=True):
            for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"]:
                if os.path.exists(p):
                    return ImageFont.truetype(p, sz)
            return ImageFont.load_default()
        d.text((600, 120), "VIRTUAL ASSISTANT TRAINING, WORLDWIDE", font=font(26), fill="black", anchor="mm")
        d.text((600, 250), "VA Newbies", font=font(120), fill="black", anchor="mm")
        d.text((600, 380), "International", font=font(100), fill="black", anchor="mm")
        d.line([200, 460, 1000, 460], fill="black", width=4)
        d.text((600, 520), "From complete beginner to member", font=font(34), fill="black", anchor="mm")
        img.save(os.path.join(ROOT, "assets", "og-cover.png"))
    except Exception as e:
        print("og image skipped:", e)


home(); about(); services(); faq(); apply(); contact(); notfound(); extras()
print("built")
