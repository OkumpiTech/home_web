"""
Seed the Okumpi database with full site content.

Usage:
    python manage.py seed_okumpi            # seed (skips if data exists)
    python manage.py seed_okumpi --fresh    # wipe site content and reseed
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import (
    FAQ, BlogCategory, BlogPost, Country, ForumCategory, ForumPost,
    Industry, JobPosition, KBArticle, News, Partner, Service,
    ServiceCategory, SiteSettings, Testimonial,
)

# --------------------------------------------------------------------------
# PRACTICE AREAS + SERVICES
# --------------------------------------------------------------------------
CATEGORIES = [
    {
        'name': 'Okumpi Build', 'icon': 'code', 'accent': 'violet',
        'tagline': 'Software engineered to ship',
        'description': (
            'Full-cycle software engineering — frontend, backend, mobile and '
            'the SDKs other developers build on. We design, build and scale '
            'custom platforms for enterprises, governments and startups.'),
        'services': [
            ('Custom Software Development',
             'End-to-end product engineering for web, mobile and desktop — '
             'built for African realities: intermittent connectivity, mobile-'
             'first users and multi-language audiences.',
             'Web & mobile apps, ERP & CRM systems, Offline-first design, '
             'UX research & prototyping'),
            ('SDKs & Developer Platforms',
             'We build the SDKs, client libraries and developer portals that '
             'let your partners integrate in hours instead of months.',
             'REST & gRPC SDKs, API documentation portals, Sandbox '
             'environments, Versioning & release management'),
            ('Frontend Engineering',
             'Fast, accessible interfaces your customers love — from design '
             'systems to production React, Flutter and progressive web apps.',
             'React & Next.js, Flutter cross-platform, Design systems, '
             'WCAG accessibility'),
            ('Backend & API Engineering',
             'Resilient services built on Django, FastAPI and Node — with the '
             'observability and test coverage enterprise workloads demand.',
             'Django & FastAPI, PostgreSQL & MySQL, Microservices, '
             'CI/CD pipelines'),
        ],
    },
    {
        'name': 'Okumpi Integrate', 'icon': 'plug', 'accent': 'cyan',
        'tagline': 'Every system, speaking one language',
        'description': (
            'Systems integration is our home turf. Payments, messaging, tax '
            'authorities, HR and health systems — we make them talk to each '
            'other reliably, with full audit trails.'),
        'services': [
            ('Omnichannel SMS & WhatsApp',
             'One API for SMS, WhatsApp Business, USSD, email and push. '
             'Send OTPs, payment confirmations, appointment reminders, '
             'delivery updates and marketing broadcasts — with failover '
             'routing, delivery reports and two-way conversations that '
             'flow straight into your CRM or ticketing system.',
             'WhatsApp Business API, Bulk & transactional SMS, '
             'OTPs & smart reminders, Two-way chat & chatbots, '
             'USSD menus, Delivery & read reports'),
            ('CRM & Ticketing Integration',
             'Every WhatsApp message, SMS reply and missed call becomes a '
             'lead or a ticket — automatically. We wire your messaging '
             'channels into Salesforce, HubSpot, Zoho, Odoo, Zammad or '
             'your custom helpdesk, with SLA-breach alerts pushed back to '
             'your team on WhatsApp.',
             'Salesforce · HubSpot · Zoho · Odoo, Auto-ticket from '
             'WhatsApp/SMS, SLA breach alerts, 360° customer timeline'),
            ('Mobile Money & Payments',
             'Battle-tested integrations with MTN MoMo, Airtel Money, '
             'M-Pesa and card rails — collections, disbursements and '
             'reconciliation.',
             'MTN MoMo & Airtel Money, Safaricom M-Pesa, Card gateways, '
             'Auto-reconciliation'),
            ('Tax & Government Integrations',
             'Certified integrations with revenue authorities — URA EFRIS, '
             'KRA eTIMS, TRA — backed by 10+ years of tax-systems expertise.',
             'URA EFRIS e-invoicing, KRA eTIMS, TRA VFD, e-receipting '
             'compliance'),
            ('Enterprise Middleware & APIs',
             'API gateways, event buses and ETL pipelines that connect your '
             'ERP, core banking, HRMS and legacy systems without downtime.',
             'API gateways, Message queues, HL7/FHIR health data, '
             'Legacy system bridges'),
        ],
    },
    {
        'name': 'Okumpi Cloud & AI', 'icon': 'cloud', 'accent': 'iris',
        'tagline': 'Intelligence on tap',
        'description': (
            'From cloud migration to production machine learning. We build '
            'RAG assistants, predictive models and data platforms — and run '
            'them on AWS, Azure, Google Cloud or on-prem.'),
        'services': [
            ('Cloud Migration & DevOps',
             'Move to the cloud without drama. Landing zones, Kubernetes, '
             'infrastructure-as-code and cost optimisation for African '
             'bandwidth realities.',
             'AWS · Azure · Google Cloud, Kubernetes & Docker, '
             'Terraform IaC, FinOps cost control'),
            ('Machine Learning & AI',
             'Practical AI that pays for itself — demand forecasting, fraud '
             'detection, document intelligence and computer vision.',
             'Predictive models, Fraud detection, OCR & document AI, '
             'Computer vision'),
            ('LLM & RAG Assistants',
             'Retrieval-augmented assistants trained on your policies, '
             'contracts and knowledge bases — private, cited and accurate.',
             'Private LLM deployments, Vector databases, '
             'Citation-backed answers, Multi-language support'),
            ('Local Hosting & Data Residency',
             'Host in-country when the law or your regulator says data '
             'must not leave. We run managed hosting in Ugandan and Kenyan '
             'data centres — meeting Uganda DPPA, Kenya DPA and central-'
             'bank data-residency rules — with in-region backups and '
             'hybrid links to AWS, Azure or GCP for what may travel.',
             'In-country data centres (UG · KE), Data-residency '
             'compliance, Managed VPS & colocation, In-region backups & '
             'DR, Hybrid cloud links'),
            ('Data Engineering & BI',
             'Warehouses, pipelines and dashboards that turn scattered '
             'operational data into decisions.',
             'Data warehouses, ETL pipelines, Power BI & Metabase, '
             'Executive dashboards'),
        ],
    },
    {
        'name': 'Okumpi Observe', 'icon': 'eye', 'accent': 'sky',
        'tagline': 'See it before it breaks',
        'description': (
            'Most providers stop at monitoring dashboards. We go further — '
            'mining your logs and utilisation history for capacity advisory: '
            'what to scale, what you are over-paying for, and how to stay '
            'highly available under real traffic peaks.'),
        'services': [
            ('Monitoring & Alerting',
             'Full-stack observability — metrics, logs, traces and uptime — '
             'with alerts that reach your team on WhatsApp, SMS and email '
             'before customers notice anything.',
             'Prometheus & Grafana, Log aggregation (Loki/ELK), Uptime & SSL '
             'monitoring, WhatsApp/SMS alerting'),
            ('Capacity Advisory',
             'We analyse your logs and utilisation trends to tell you exactly '
             'what to scale up, what to scale down, and where you are paying '
             'for overkill — a right-sizing report with numbers, not guesses.',
             'Utilisation & trend analysis, Right-sizing reports, Cloud cost '
             'optimisation, Growth forecasting'),
            ('High Availability & Scaling',
             'Load testing, autoscaling, failover and disaster recovery '
             'engineered so month-end peaks and campaign spikes never take '
             'you down.',
             'Load & stress testing, Autoscaling design, Failover & DR '
             'drills, Zero-downtime deploys'),
        ],
    },
    {
        'name': 'Okumpi Secure', 'icon': 'shield', 'accent': 'magenta',
        'tagline': 'African-grade security, world-class standards',
        'description': (
            'Security engineered for how African enterprises actually run — '
            'from ethical hacking and 24/7 monitoring to CCTV and blockchain '
            'integrity. Audit-ready, always.'),
        'services': [
            ('Security Audits & Ethical Hacking',
             'Penetration testing, red-team exercises and cloud security '
             'audits by certified ethical hackers — with fix-it roadmaps, '
             'not just findings.',
             'Penetration testing, Cloud security audits, Red team '
             'exercises, Remediation roadmaps'),
            ('Enterprise Security Operations',
             '24/7 security operations centre, identity and access '
             'management, and zero-trust rollouts sized for your budget.',
             '24/7 SOC monitoring, IAM & zero trust, SIEM deployment, '
             'Incident response'),
            ('CCTV & Physical Security',
             'IP camera networks, access control and alarm systems — '
             'designed, installed and monitored for local conditions and '
             'power realities.',
             'IP CCTV networks, Access control, Solar-backed systems, '
             'Remote monitoring'),
            ('Blockchain & Data Integrity',
             'Tamper-proof records for land registries, certificates and '
             'supply chains — plus compliance with ISO 27001 and African '
             'data-protection laws.',
             'Blockchain registries, Digital certificates, ISO 27001, '
             'Uganda DPPA & Kenya DPA compliance'),
        ],
    },
    {
        'name': 'Okumpi Connect', 'icon': 'network', 'accent': 'lime',
        'tagline': 'Infrastructure that stays up',
        'description': (
            'Networks, servers and data centres built for uptime where '
            'power and bandwidth fluctuate. Structured cabling to SD-WAN, '
            'we keep organisations connected.'),
        'services': [
            ('Enterprise Networking',
             'Structured cabling, enterprise Wi-Fi and SD-WAN across '
             'campuses, branches and warehouses.',
             'Structured cabling, Enterprise Wi-Fi, SD-WAN & VPN, '
             'Network monitoring'),
            ('Servers, Storage & Data Centre',
             'Server rooms and micro data centres with the redundancy your '
             'core systems need.',
             'Server deployment, SAN/NAS storage, Virtualisation, '
             'Data centre design'),
            ('Power & Continuity',
             'UPS, inverter and solar solutions that keep IT running '
             'through outages — with automated failover.',
             'UPS & inverters, Solar backup, Generator integration, '
             'Disaster recovery'),
        ],
    },
    {
        'name': 'Okumpi Care', 'icon': 'headset', 'accent': 'amber',
        'tagline': 'We stay after go-live',
        'description': (
            'Managed services, maintenance and growth support. Helpdesk, '
            'SLAs, training and the business-development muscle to win '
            'technology-driven tenders.'),
        'services': [
            ('Managed IT & Maintenance',
             'Proactive maintenance, patching and 24/7 helpdesk under clear '
             'SLAs — for systems we built and systems we inherited.',
             '24/7 helpdesk, Preventive maintenance, SLA guarantees, '
             'On-site & remote support'),
            ('Training & Capacity Building',
             'Hands-on training for your teams — from end-user onboarding '
             'to developer bootcamps and security awareness.',
             'End-user training, Developer bootcamps, Security awareness, '
             'Admin handover'),
            ('ICT Consulting & Business Development',
             'Digital strategy, technical writing and bid support for '
             'technology-driven proposals to governments and enterprises.',
             'Digital strategy, Proposal & bid support, Technical writing, '
             'ICT policy advisory'),
        ],
    },
    {
        'name': 'Okumpi Reach', 'icon': 'megaphone', 'accent': 'rose',
        'tagline': 'Be found. Be trusted. Be chosen.',
        'description': (
            'Digital marketing and social media run by the same team that '
            'builds your systems — campaigns wired to real analytics, and '
            'official platform verification that makes your brand '
            'impersonation-proof.'),
        'services': [
            ('Digital Marketing & SEO',
             'Search-first growth: SEO, Google and Meta ads, landing pages '
             'and email/SMS/WhatsApp campaigns — measured end-to-end to '
             'enquiries and sales, not vanity clicks.',
             'SEO & content strategy, Google & Meta ads, Email/SMS/WhatsApp '
             'campaigns, Conversion tracking'),
            ('Social Media Management',
             'Content calendars, community management and monthly reporting '
             'across the platforms your customers actually use — in the '
             'languages they speak.',
             'Content calendars, Community management, Short-form video, '
             'Monthly analytics'),
            ('Advertising & Media Buying',
             'Full-funnel advertising from creative to placement: Google, '
             'Meta, TikTok and LinkedIn campaigns, programmatic display, '
             'and negotiated radio and out-of-home slots — every shilling '
             'tracked to enquiries and sales.',
             'Campaign strategy & creative, Google · Meta · TikTok · '
             'LinkedIn, Programmatic display, Radio & OOH buying'),
            ('Verification & Brand Protection',
             'We shepherd official verification on Meta, X, TikTok and '
             'WhatsApp Business, lock down your handles, and monitor for '
             'impersonators and scam pages targeting your customers.',
             'Meta / X / TikTok verification, WhatsApp Business green tick, '
             'Handle security & 2FA, Impersonation takedowns'),
        ],
    },
]

# --------------------------------------------------------------------------
# INDUSTRY SOLUTIONS
# --------------------------------------------------------------------------
INDUSTRIES = [
    ('OkuHR — HRMS & Payroll', 'users',
     'One platform for people, payroll and performance',
     'A complete human-resource management system localised for African '
     'payrolls — PAYE, NSSF, local service tax — with biometric attendance, '
     'leave, appraisals and employee self-service on mobile.',
     'Localised payroll & statutory returns, Biometric attendance, '
     'Employee self-service app, Performance & leave management'),
    ('OkuMed — Hospital System', 'health',
     'From triage to theatre, one record',
     'A hospital management information system covering OPD, IPD, lab, '
     'pharmacy, billing and insurance claims — interoperable via HL7/FHIR '
     'and built to run offline when the network drops.',
     'OPD/IPD & triage workflows, Lab & pharmacy modules, Insurance & '
     'billing, HL7/FHIR interoperability'),
    ('OkuEstate — Property Management', 'building',
     'Every unit, tenant and shilling accounted for',
     'Property and facility management for landlords, agencies and malls — '
     'leases, invoicing, mobile-money rent collection, maintenance tickets '
     'and owner statements.',
     'Lease & tenant management, Mobile-money rent collection, '
     'Maintenance ticketing, Owner & agent statements'),
    ('OkuJustice — Judicial Systems', 'scale',
     'Faster case flow, full transparency',
     'Court and case management platforms for judiciaries and tribunals — '
     'e-filing, cause lists, digital evidence and public case tracking, '
     'built with the security courts demand.',
     'E-filing & registries, Cause-list scheduling, Digital evidence '
     'vault, Public case tracking'),
    ('Government & Public Sector', 'flag',
     'Citizen services that actually serve',
     'E-government portals, revenue systems and citizen service platforms '
     'for ministries, districts and agencies — accessible, auditable and '
     'built to national data-protection standards.',
     'Citizen service portals, Revenue & licensing systems, '
     'Interoperability (X-Road style), Data-protection compliance'),
    ('Banking & Fintech', 'bank',
     'Rails for the mobile-money continent',
     'Core-banking integrations, agency-banking apps, wallets and fraud '
     'monitoring for banks, SACCOs and fintechs across East Africa.',
     'Wallet & agency banking, Core-banking integration, Fraud '
     'monitoring, Regulatory reporting'),
]

# --------------------------------------------------------------------------
# TESTIMONIALS
# --------------------------------------------------------------------------
TESTIMONIALS = [
    ('Okumpi integrated M-Pesa, MoMo and our core banking in eleven weeks — '
     'reconciliation that took three days now runs in minutes.',
     'David Otieno', 'CTO', 'Pan-African Microfinance Group',
     'clutch', '5.0', 205),
    ('Their team rebuilt our hospital system and trained every department. '
     'Patient queues dropped by half in the first month.',
     'Dr. Sarah Nakato', 'Medical Director', 'Regional Referral Hospital',
     'google', '5.0', 265),
    ('The security audit was eye-opening. They found what two previous '
     'vendors missed — and stayed to fix it with us.',
     'Joseph Mwangi', 'Head of ICT', 'Government Agency, Nairobi',
     'trustpilot', '4.5', 305),
    ('WhatsApp and SMS from one dashboard changed how we talk to tenants. '
     'Rent collection via mobile money is now 94% on time.',
     'Amina Kassim', 'Operations Director', 'Skyline Properties',
     'google', '5.0', 225),
    ('Our RAG assistant answers policy questions with citations. Okumpi '
     'delivered in weeks what we budgeted a year for.',
     'Grace Tumusiime', 'HR Director', 'East African Logistics Co.',
     'linkedin', '5.0', 285),
    ('They built our SDK and developer portal — partner integrations that '
     'took months now take days. Support is genuinely 24/7.',
     'Daniel Rukundo', 'CEO', 'PayBridge Africa',
     'clutch', '4.5', 245),
]

# --------------------------------------------------------------------------
# PARTNERS & CLIENT LOGOS  (static paths under static/img/)
# --------------------------------------------------------------------------
PARTNERS = [
    # payments / banking
    ('MTN MoMo', 'payments', 'img/partners/mtn.jpg'),
    ('Airtel Money', 'payments', 'img/partners/airtel.png'),
    ('Safaricom M-Pesa', 'payments', 'img/partners/safaricom.jpg'),
    ('Vodacom M-Pesa', 'payments', 'img/partners/vodacom.jpg'),
    ('Stanbic Bank', 'payments', 'img/partners/stanbic.png'),
    ('ABSA Bank', 'payments', 'img/partners/absa.png'),
    ('Centenary Bank', 'payments', 'img/partners/centenary.jpg'),
    # cloud / tech
    ('Amazon Web Services', 'cloud', 'img/partners/aws.png'),
    ('Microsoft Azure', 'cloud', 'img/partners/azure.png'),
    ('Google Cloud', 'cloud', 'img/partners/gcloud.png'),
    # clients
    ('Bright Life', 'client', 'img/clients/brightlife.webp'),
    ('DITA', 'client', 'img/clients/dita.jpg'),
    ('Judiciary of Uganda', 'client', 'img/clients/judiciary.png'),
    ('WASSHA', 'client', 'img/clients/wassha.jpg'),
    ('First Pharmacy', 'client', 'img/clients/firstpharmacy.png'),
]

# --------------------------------------------------------------------------
# COUNTRIES
# --------------------------------------------------------------------------
COUNTRIES = [
    ('Uganda', 'UG', '🇺🇬', '+256', '+256 200 585 858', 'Kampala — HQ', True),
    ('Kenya', 'KE', '🇰🇪', '+254', '+254 200 585 858', 'Nairobi', False),
    ('Tanzania', 'TZ', '🇹🇿', '+255', '', 'Dar es Salaam', False),
    ('Rwanda', 'RW', '🇷🇼', '+250', '', 'Kigali', False),
    ('South Sudan', 'SS', '🇸🇸', '+211', '', 'Juba', False),
    ('DR Congo', 'CD', '🇨🇩', '+243', '', 'Kinshasa', False),
    ('Ethiopia', 'ET', '🇪🇹', '+251', '', 'Addis Ababa', False),
    ('Nigeria', 'NG', '🇳🇬', '+234', '', 'Lagos', False),
    ('Ghana', 'GH', '🇬🇭', '+233', '', 'Accra', False),
    ('Zambia', 'ZM', '🇿🇲', '+260', '', 'Lusaka', False),
    ('Malawi', 'MW', '🇲🇼', '+265', '', 'Lilongwe', False),
    ('South Africa', 'ZA', '🇿🇦', '+27', '', 'Johannesburg', False),
]

# --------------------------------------------------------------------------
# FAQS
# --------------------------------------------------------------------------
FAQS = [
    ('What exactly does Okumpi do?',
     'We are a full-service ICT company. One team covers software '
     'engineering (web, mobile, SDKs), systems integration (payments, '
     'SMS/WhatsApp, tax authorities), cloud and AI, observability with '
     'capacity advisory, cybersecurity and ethical hacking, networking '
     'infrastructure, managed support, and digital marketing with '
     'social-media verification. One accountable partner instead of '
     'six vendors.'),
    ('Which countries do you operate in?',
     'We are headquartered in Kampala, Uganda with an office in Nairobi, '
     'Kenya, and we deliver projects across 12+ African countries '
     'including Tanzania, Rwanda, Nigeria, Ghana, Zambia and South '
     'Africa. Remote-first delivery means your location is rarely a '
     'constraint.'),
    ('How does a project usually start?',
     'With a free discovery call. We scope your goals, audit what exists, '
     'and give you a fixed-price proposal with milestones within one '
     'week. No obligation, and you keep the audit findings either way.'),
    ('Can you integrate with mobile money and WhatsApp?',
     'Yes — it is one of our specialities. We run production integrations '
     'with MTN MoMo, Airtel Money and M-Pesa, and we are experienced with '
     'the WhatsApp Business API, bulk SMS and USSD. We also automate '
     'notifications — OTPs, reminders, payment confirmations — and pipe '
     'replies straight into your CRM or ticketing system as leads and '
     'tickets. One API, every channel your customers use.'),
    ('How do you handle security and compliance?',
     'Security is built in, not bolted on. Our certified ethical hackers '
     'test everything we ship, we align with ISO 27001, and we build to '
     'the Uganda Data Protection and Privacy Act, Kenya DPA and GDPR '
     'where applicable. We also audit third-party systems.'),
    ('Do you support systems after launch?',
     'Always. Okumpi Care provides 24/7 helpdesk, preventive maintenance '
     'and clear SLAs — for systems we built and for systems we inherit '
     'from other vendors. Most clients stay with us for years.'),
]

# --------------------------------------------------------------------------
# JOBS
# --------------------------------------------------------------------------
JOBS = [
    ('Senior Django Engineer', 'Kampala, Uganda', 'full_time',
     'Own backend services for enterprise clients — Django, PostgreSQL, '
     'DRF — and mentor mid-level engineers.',
     'Python, Django, PostgreSQL, REST APIs'),
    ('Flutter Mobile Developer', 'Kampala / Remote', 'full_time',
     'Ship cross-platform apps for fintech and health clients from a '
     'single Flutter codebase.',
     'Flutter, Dart, Firebase, CI/CD'),
    ('DevOps / Kubernetes Engineer', 'Nairobi, Kenya', 'full_time',
     'Run our multi-cloud Kubernetes platform, IaC and deployment '
     'pipelines across AWS, Azure and GCP.',
     'Kubernetes, Terraform, AWS, Azure'),
    ('Machine Learning Engineer (RAG/LLM)', 'Remote — Africa', 'full_time',
     'Build retrieval-augmented assistants and document-AI pipelines for '
     'enterprise and government clients.',
     'Python, LLMs, RAG, Vector DBs'),
    ('Penetration Tester / Ethical Hacker', 'Kampala, Uganda', 'full_time',
     'Lead offensive-security engagements: web, mobile, network and '
     'cloud, with clear remediation reporting.',
     'OSCP, Burp Suite, Cloud security, Reporting'),
    ('Network & Infrastructure Engineer', 'Kampala, Uganda', 'full_time',
     'Design and deploy enterprise networks, structured cabling and '
     'SD-WAN for campus and branch sites.',
     'CCNA/CCNP, SD-WAN, Firewalls, Wi-Fi'),
    ('Frontend Engineer (React)', 'Remote — Africa', 'full_time',
     'Craft accessible, high-performance interfaces and design systems '
     'for our product suites.',
     'React, TypeScript, Next.js, Accessibility'),
    ('Business Development Manager', 'Nairobi, Kenya', 'full_time',
     'Win technology-driven tenders with governments and enterprises; '
     'own proposals end-to-end.',
     'B2B/B2G sales, Proposals, ICT literacy'),
    ('Cloud Security Analyst', 'Remote — Africa', 'contract',
     'Audit client cloud estates, harden configurations and run '
     'compliance assessments.',
     'AWS/Azure security, ISO 27001, SIEM'),
    ('Technical Writer', 'Kampala / Remote', 'part_time',
     'Turn complex systems into clear SDK docs, user guides and winning '
     'bid documents.',
     'Documentation, API docs, Proposals'),
]

# --------------------------------------------------------------------------
# NEWS
# --------------------------------------------------------------------------
NEWS_ITEMS = [
    ('Okumpi opens Nairobi office to serve East African clients',
     'expansion',
     'Our second office puts engineers and security analysts closer to '
     'Kenyan banks, hospitals and government agencies.',
     'Okumpi has opened a fully staffed office in Nairobi, Kenya — our '
     'second on the continent after Kampala. The office hosts delivery '
     'engineers, a security operations desk and our business development '
     'team for the Kenyan market.'),
    ('Okumpi attains ISO 27001-aligned security operations',
     'award',
     'Our internal SOC and delivery processes now align with ISO 27001 '
     'controls, audited end-to-end.',
     'After a year-long programme, Okumpi\'s security operations and '
     'software delivery lifecycle now align with ISO 27001 controls, '
     'covering asset management, access control, cryptography and '
     'incident response.'),
    ('OkuHR launches: payroll built for African statutory rules',
     'announcement',
     'PAYE, NSSF and local service tax handled out of the box, with '
     'biometric attendance and mobile self-service.',
     'Our HRMS suite OkuHR is now generally available. It localises '
     'payroll for Uganda, Kenya and Tanzania out of the box and ships '
     'with biometric attendance, leave and performance modules.'),
    ('Partnership: Okumpi joins the AWS Partner Network',
     'partnership',
     'Deeper cloud expertise and funded migration assessments for '
     'qualifying enterprises.',
     'Okumpi is now a registered AWS Partner, adding funded migration '
     'assessments and well-architected reviews to our cloud practice '
     'alongside Azure and Google Cloud.'),
    ('Okumpi ships court-records integrity pilot on blockchain',
     'announcement',
     'A tamper-evident registry pilot for digital case records, built '
     'with a regional judiciary.',
     'Working with a regional judiciary, Okumpi has piloted a '
     'blockchain-anchored integrity layer for digital case records — '
     'making tampering evident while keeping records private.'),
]

# --------------------------------------------------------------------------
# BLOG
# --------------------------------------------------------------------------
BLOG_CATEGORIES = [
    ('Engineering', 'Deep dives from the Okumpi build teams'),
    ('AI & Data', 'Practical machine learning for African enterprises'),
    ('Security', 'Defensive and offensive security, explained'),
    ('Integration', 'Payments, messaging and government rails'),
]

BLOG_POSTS = [
    ('RAG in production: what enterprises get wrong', 'AI & Data',
     'Retrieval-augmented generation demos are easy; production is not. '
     'Here is our checklist after a dozen deployments.',
     'Chunking strategy, evaluation sets, citation UX and access control '
     'decide whether a RAG assistant is trusted or abandoned. We walk '
     'through the architecture we now deploy by default: hybrid search, '
     'reranking, per-document ACLs and a human feedback loop.', 7),
    ('Securing mobile money integrations end-to-end', 'Security',
     'Collections APIs are a favourite target. How we harden MoMo and '
     'M-Pesa integrations at banks and fintechs.',
     'From IP allow-listing and mutual TLS to idempotency keys, webhook '
     'signature verification and reconciliation alerts — a practical '
     'hardening guide drawn from live incident reviews.', 6),
    ('The WhatsApp Business API, minus the confusion', 'Integration',
     'Templates, sessions, pricing and the 24-hour window — explained '
     'with real flows we run for clients.',
     'We cover conversation categories, template approval strategy, '
     'session messages, opt-in design and how to fail over to SMS '
     'gracefully when a handset goes offline.', 5),
    ('Zero trust for African SMEs: a budget-honest roadmap', 'Security',
     'You do not need a Silicon Valley budget to kill implicit trust. '
     'A phased rollout that works with local realities.',
     'Start with identity: MFA everywhere, then device posture, then '
     'network segmentation. We map each phase to typical Ugandan and '
     'Kenyan SME budgets and the quick wins that fund the next phase.', 8),
    ('Django at scale: lessons from government workloads', 'Engineering',
     'Cache discipline, queue isolation and migration strategy for '
     'systems that serve millions of citizens.',
     'Read-replica routing, PgBouncer, Celery queue isolation and '
     'zero-downtime migrations — the patterns that keep our public '
     'sector Django deployments boring in the best way.', 9),
    ('Blockchain land registries: hype vs what actually ships', 'Engineering',
     'Where distributed ledgers genuinely help land and court records — '
     'and where a signed database is enough.',
     'We compare anchoring models, permissioned chains and plain '
     'append-only logs, based on our judicial and registry pilots.', 6),
]

# --------------------------------------------------------------------------
# KNOWLEDGE BASE
# --------------------------------------------------------------------------
KB_ARTICLES = [
    ('Getting started with the Okumpi Messaging SDK', 'Okumpi Integrate',
     'Install the SDK, obtain API keys, send your first SMS and WhatsApp '
     'message, and set up delivery webhooks — in under 15 minutes.'),
    ('Piping WhatsApp into your ticketing system', 'Okumpi Integrate',
     'Webhook → queue → ticket: how we map WhatsApp conversations to '
     'tickets with SLA timers, agent assignment and customer timelines — '
     'including the 24-hour session and template-message rules you must '
     'respect.'),
    ('WhatsApp webhook setup checklist', 'Okumpi Integrate',
     'Verify tokens, validate signatures, respond within timeout, queue '
     'processing — everything your endpoint must do to stay healthy.'),
    ('URA EFRIS integration checklist', 'Okumpi Integrate',
     'Device registration, invoice fiscalisation flow, error handling and '
     'the reconciliation reports auditors ask for.'),
    ('Hardening a branch VPN: our standard build', 'Okumpi Secure',
     'The firewall rules, cipher suites and monitoring we deploy on '
     'every site-to-site VPN.'),
    ('Backup policy template (3-2-1 for African bandwidth)', 'Okumpi Care',
     'A practical 3-2-1 backup policy template accounting for limited '
     'bandwidth: incremental-forever, seeded offsite copies, restore '
     'drills.'),
    ('Evaluating a RAG assistant before go-live', 'Okumpi Cloud & AI',
     'Build a golden-question set, measure faithfulness and citation '
     'accuracy, and set the thresholds that gate deployment.'),
]

# --------------------------------------------------------------------------
# FORUM
# --------------------------------------------------------------------------
FORUM_CATEGORIES = [
    ('Build vs Buy', 'chat',
     'Should you build custom or buy off-the-shelf? Compare notes with '
     'other ICT leaders.'),
    ('Integrations & APIs', 'plug',
     'Mobile money, WhatsApp, EFRIS and everything in between.'),
    ('Security Corner', 'shield',
     'Threats seen in the wild, hardening tips and audit prep.'),
    ('Cloud & AI', 'cloud',
     'Migration war stories, AI use-cases and cost control.'),
]

SETTINGS = [
    ('hero_community_count', '200+', 'Hero social-proof count'),
    ('stat_years', '10+', 'Years in business'),
    ('stat_projects', '500+', 'Projects delivered'),
    ('stat_clients', '200+', 'Clients served'),
    ('stat_team', '50+', 'Team members'),
    ('phone_ug', '+256 200 585 858', 'Uganda phone'),
    ('phone_ke', '+254 200 585 858', 'Kenya phone'),
    ('email_main', 'hello@okumpi.com', 'Primary email'),
]


class Command(BaseCommand):
    help = 'Seed the Okumpi database with demo content.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fresh', action='store_true',
            help='Delete existing site content before seeding.')

    def handle(self, *args, **options):
        if options['fresh']:
            self.stdout.write('Wiping existing content…')
            for model in (Service, ServiceCategory, Industry, Testimonial,
                          Partner, Country, FAQ, JobPosition, News,
                          BlogPost, BlogCategory, KBArticle, ForumPost,
                          ForumCategory, SiteSettings):
                model.objects.all().delete()

        if ServiceCategory.objects.exists():
            self.stdout.write(self.style.WARNING(
                'Content already present — run with --fresh to reseed.'))
            return

        # Practice areas + services
        for order, cat in enumerate(CATEGORIES):
            category = ServiceCategory.objects.create(
                name=cat['name'], icon=cat['icon'], accent=cat['accent'],
                tagline=cat['tagline'], description=cat['description'],
                order=order)
            for s_order, (name, desc, feats) in enumerate(cat['services']):
                Service.objects.create(
                    category=category, name=name, description=desc,
                    features=feats, order=s_order)

        for order, (name, icon, headline, desc, feats) in enumerate(INDUSTRIES):
            Industry.objects.create(
                name=name, icon=icon, headline=headline, description=desc,
                features=feats, order=order)

        for order, (quote, author, role, company,
                    platform, rating, hue) in enumerate(TESTIMONIALS):
            Testimonial.objects.create(
                quote=quote, author=author, role=role, company=company,
                platform=platform, rating=rating, avatar_hue=hue,
                order=order)

        for order, (name, kind, logo) in enumerate(PARTNERS):
            Partner.objects.create(
                name=name, kind=kind, logo=logo, order=order)

        for order, (name, code, flag, pcode, pnum, office,
                    is_hq) in enumerate(COUNTRIES):
            Country.objects.create(
                name=name, code=code, flag=flag, phone_code=pcode,
                phone_number=pnum, office_location=office, is_hq=is_hq,
                order=order)

        for order, (q, a) in enumerate(FAQS):
            FAQ.objects.create(question=q, answer=a, order=order)

        for title, location, jtype, desc, tags in JOBS:
            JobPosition.objects.create(
                title=title, location=location, job_type=jtype,
                description=desc, tags=tags)

        for title, ntype, excerpt, content in NEWS_ITEMS:
            News.objects.create(
                title=title, news_type=ntype, excerpt=excerpt,
                content=content)

        cat_map = {}
        for name, desc in BLOG_CATEGORIES:
            cat_map[name] = BlogCategory.objects.create(
                name=name, description=desc)

        for title, cat_name, excerpt, content, mins in BLOG_POSTS:
            BlogPost.objects.create(
                title=title, category=cat_map[cat_name], excerpt=excerpt,
                content=content, read_minutes=mins)

        svc_map = {c.name: c for c in ServiceCategory.objects.all()}
        for title, cat_name, content in KB_ARTICLES:
            KBArticle.objects.create(
                title=title, category=svc_map.get(cat_name), content=content)

        for order, (name, icon, desc) in enumerate(FORUM_CATEGORIES):
            ForumCategory.objects.create(
                name=name, icon=icon, description=desc, order=order)

        for key, value, desc in SETTINGS:
            SiteSettings.objects.update_or_create(
                key=key, defaults={'value': value, 'description': desc})

        # Dev superuser (change the password before deploying!)
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin', 'admin@okumpi.com', 'okumpi2026')
            self.stdout.write('Superuser created — admin / okumpi2026')

        self.stdout.write(self.style.SUCCESS('Okumpi content seeded.'))
