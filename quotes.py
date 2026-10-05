# Copyright (c) 2025-2026 Eduardo Correia <ecorreia@apliant.com.br>
#
# This file is part of E-Tutor. It is free software, licensed under the GNU
# Lesser General Public License v3.0 or later. See COPYING.LESSER and COPYING
# for details.
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Short, source-checked excerpts. Applications are our own notes.

Sources were checked on 2026-10-04. Rotate locally: no invented model attributions,
extra API calls, or additional tokens. Book headings are identified as such.
"""

from urllib.parse import urlencode

QUOTE_BANK = (
    {
        "id": "clear-systems",
        "text": "You do not rise to the level of your goals. You fall to the level of your systems.",
        "author": "James Clear",
        "work": "Author's quote collection — habits and systems",
        "source_url": "https://jamesclear.com/quotes/you-do-not-rise-to-the-level-of-your-goals-you-fall-to-the-level-of-your-systems",
        "application_en": "Turn an ambition into a repeatable routine with a clear trigger.",
        "application_pt": "Transforme uma ambição em uma rotina repetível, com um gatilho claro.",
    },
    {
        "id": "covey-understand",
        "text": "Seek first to understand, then to be understood.",
        "author": "Stephen R. Covey",
        "work": "The 7 Habits of Highly Effective People — Habit 5",
        "source_url": "https://mp.franklincovey.com/habit-5/",
        "application_en": "Before pitching your solution, summarize the other person's concern and check your understanding.",
        "application_pt": "Antes de apresentar sua solução, resuma a preocupação da outra pessoa e confirme se entendeu.",
    },
    {
        "id": "greene-boldness",
        "text": "Enter Action with Boldness",
        "author": "Robert Greene",
        "work": "The 48 Laws of Power — Law 28 (heading)",
        "source_url": "https://www.penguinrandomhouse.com/books/330912/the-48-laws-of-power-by-robert-greene/",
        "application_en": "State your recommendation clearly, while keeping the risks and uncertainties visible.",
        "application_pt": "Apresente sua recomendação com clareza, sem esconder riscos e incertezas.",
    },
    {
        "id": "bezos-commit",
        "text": "disagree and commit",
        "author": "Jeff Bezos",
        "work": "2016 Letter to Shareholders — phrase advocated in the letter",
        "source_url": "https://www.aboutamazon.com/news/company-news/2016-letter-to-shareholders",
        "application_en": "Raise objections during the decision; once it is settled, make your support explicit.",
        "application_pt": "Apresente objeções durante a decisão; depois de definida, deixe explícito seu compromisso com a execução.",
    },
    {
        "id": "mckeown-essential",
        "text": "We can discern what's essential, eliminate what's not essential",
        "author": "Greg McKeown",
        "work": "Essentialism — author interview, To Do Things Better, Stop Doing So Much (excerpt)",
        "source_url": "https://gregmckeown.com/to-do-things-better-stop-doing-so-much/",
        "application_en": "When accepting a new priority, name what you will postpone to make room for it.",
        "application_pt": "Ao aceitar uma nova prioridade, diga o que será adiado para abrir espaço para ela.",
    },
    {
        "id": "covey-end",
        "text": "Begin With the End in Mind",
        "author": "Stephen R. Covey",
        "work": "The 7 Habits of Highly Effective People — Habit 2 (heading)",
        "source_url": "https://mp.franklincovey.com/habit-5/",
        "application_en": "Open a meeting by naming the decision or outcome you want to leave with.",
        "application_pt": "Abra uma reunião dizendo qual decisão ou resultado você quer obter ao final.",
    },
    {
        "id": "greene-master",
        "text": "Never Outshine the Master",
        "author": "Robert Greene",
        "work": "The 48 Laws of Power — Law 1 (heading)",
        "source_url": "https://www.penguinrandomhouse.com/books/330912/the-48-laws-of-power-by-robert-greene/",
        "application_en": "A lens on hierarchy, not a universal rule: make your contribution clear and acknowledge other people's work.",
        "application_pt": "Uma perspectiva sobre hierarquia, não uma regra universal: mostre sua contribuição e reconheça o trabalho dos outros.",
    },
    {
        "id": "covey-proactive",
        "text": "Be Proactive",
        "author": "Stephen R. Covey",
        "work": "The 7 Habits of Highly Effective People — Habit 1 (heading)",
        "source_url": "https://mp.franklincovey.com/habit-5/",
        "application_en": "Pair a problem statement with the next step you can take yourself.",
        "application_pt": "Ao apresentar um problema, acrescente o próximo passo que você mesmo pode tomar.",
    },
)


def quote_for(index):
    return dict(QUOTE_BANK[index % len(QUOTE_BANK)])


def _saved(value, bank):
    """Accept complete saved excerpts with one of the checked publisher/author links."""
    if not isinstance(value, dict) or not all(isinstance(value.get(k), str) for k in bank[0]):
        return None
    if value["source_url"] not in {q["source_url"] for q in bank}:
        return None
    return dict(value)


def saved_quote(value):
    return _saved(value, QUOTE_BANK)


def book_search(title, author):
    """Open Library search, never an invented catalog entry."""
    return "https://openlibrary.org/search?" + urlencode({"title": title, "author": author})


# Public-domain passages for a 30-second read, checked word for word against the Project
# Gutenberg texts on 2026-10-05 (Franklin's original spellings kept; italics dropped).
# "notice" points at one piece of language in the passage; "application" is our own note.
PUBLIC_DOMAIN_EXCERPTS = (
    {
        "id": "strunk-needless",
        "kind": "excerpt",
        "text": "Vigorous writing is concise. A sentence should contain no unnecessary words, a paragraph no "
                "unnecessary sentences, for the same reason that a drawing should have no unnecessary lines "
                "and a machine no unnecessary parts.",
        "author": "William Strunk Jr.",
        "work": "The Elements of Style (1918) — Rule 13, Omit needless words",
        "source_url": "https://www.gutenberg.org/ebooks/37134",
        "notice_en": "Ellipsis: after the first clause, “should contain” is understood (“a paragraph [should contain] "
                     "no unnecessary sentences”). It keeps parallel lists tight.",
        "notice_pt": "Elipse: depois da primeira oração, “should contain” fica subentendido (“a paragraph [should "
                     "contain] no unnecessary sentences”). Isso deixa listas paralelas enxutas.",
        "application_en": "Before sending, cut one word per sentence that adds nothing, such as just or actually.",
        "application_pt": "Antes de enviar, corte de cada frase uma palavra que não acrescenta nada, como just ou actually.",
    },
    {
        "id": "strunk-positive",
        "kind": "excerpt",
        "text": "Put statements in positive form. Make definite assertions. Avoid tame, colorless, hesitating, "
                "non-committal language.",
        "author": "William Strunk Jr.",
        "work": "The Elements of Style (1918) — Put statements in positive form",
        "source_url": "https://www.gutenberg.org/ebooks/37134",
        "notice_en": "Non-committal: avoiding a clear position. Useful in feedback: “Her answer was non-committal.”",
        "notice_pt": "Non-committal: evasivo, que não se compromete com uma posição. Útil em feedback: “Her answer was non-committal.”",
        "application_en": "Say “We’ll probably finish next week” rather than “It’s not very likely that we won’t finish”: "
                          "the same certainty, stated positively.",
        "application_pt": "Diga “We’ll probably finish next week” em vez de “It’s not very likely that we won’t finish”: "
                          "a mesma certeza, dita de forma positiva.",
    },
    {
        "id": "strunk-emphatic",
        "kind": "excerpt",
        "text": "The proper place in the sentence for the word, or group of words, which the writer desires to make "
                "most prominent is usually the end.",
        "author": "William Strunk Jr.",
        "work": "The Elements of Style (1918) — Rule 18, Place the emphatic words of a sentence at the end",
        "source_url": "https://www.gutenberg.org/ebooks/37134",
        "notice_en": "Make + object + adjective: make something prominent, make it clear, make it easy.",
        "notice_pt": "Make + objeto + adjetivo: make something prominent, make it clear, make it easy.",
        "application_en": "End a status update with what people must remember: “The fix is ready; what we still need is QA sign-off.”",
        "application_pt": "Termine um status com o que as pessoas precisam lembrar: “The fix is ready; what we still need is QA sign-off.”",
    },
    {
        "id": "thoreau-detail",
        "kind": "excerpt",
        "text": "Our life is frittered away by detail. An honest man has hardly need to count more than his ten "
                "fingers, or in extreme cases he may add his ten toes, and lump the rest. Simplicity, simplicity, "
                "simplicity!",
        "author": "Henry David Thoreau",
        "work": "Walden (1854) — Where I Lived, and What I Lived For",
        "source_url": "https://www.gutenberg.org/ebooks/205",
        "notice_en": "Fritter away (phrasal verb): waste time or money little by little. “I frittered away the afternoon on email.”",
        "notice_pt": "Fritter away (phrasal verb): desperdiçar tempo ou dinheiro aos poucos. “I frittered away the afternoon on email.”",
        "application_en": "Cap a meeting update at three points and lump the rest into a follow-up note.",
        "application_pt": "Limite sua atualização em reunião a três pontos e agrupe o resto em uma nota de follow-up.",
    },
    {
        "id": "thoreau-deliberately",
        "kind": "excerpt",
        "text": "I went to the woods because I wished to live deliberately, to front only the essential facts of "
                "life, and see if I could not learn what it had to teach, and not, when I came to die, discover "
                "that I had not lived.",
        "author": "Henry David Thoreau",
        "work": "Walden (1854) — Where I Lived, and What I Lived For",
        "source_url": "https://www.gutenberg.org/ebooks/205",
        "notice_en": "Deliberately means with careful intention here. Front is an old use of confront; today say face.",
        "notice_pt": "Deliberately aqui significa com intenção cuidadosa. Front é um uso antigo de confront; hoje diga face.",
        "application_en": "Before a long explanation, ask yourself: what is the essential fact my listener needs?",
        "application_pt": "Antes de uma explicação longa, pergunte-se: qual é o fato essencial de que meu ouvinte precisa?",
    },
    {
        "id": "franklin-fixed-opinion",
        "kind": "excerpt",
        "text": "I even forbid myself, agreeably to the old laws of our Junto, the use of every word or expression "
                "in the language that imported a fix'd opinion, such as certainly, undoubtedly, etc., and I "
                "adopted, instead of them, I conceive, I apprehend, or I imagine a thing to be so or so; or it so "
                "appears to me at present.",
        "author": "Benjamin Franklin",
        "work": "Autobiography of Benjamin Franklin — on the virtue of humility",
        "source_url": "https://www.gutenberg.org/ebooks/20203",
        "notice_en": "Hedging. Modern equivalents: “It seems to me”, “As far as I can tell”, “My sense is”. "
                     "Spellings such as fix'd are 18th-century.",
        "notice_pt": "Hedging (atenuação). Equivalentes modernos: “It seems to me”, “As far as I can tell”, "
                     "“My sense is”. Grafias como fix'd são do século XVIII.",
        "application_en": "When you disagree, replace “That’s wrong” with “My sense is that… Am I missing something?”",
        "application_pt": "Ao discordar, troque “That’s wrong” por “My sense is that… Am I missing something?”",
    },
    {
        "id": "franklin-precepts",
        "kind": "excerpt",
        "text": "Silence. Speak not but what may benefit others or yourself; avoid trifling conversation. … "
                "Resolution. Resolve to perform what you ought; perform without fail what you resolve.",
        "author": "Benjamin Franklin",
        "work": "Autobiography of Benjamin Franklin — the thirteen virtues (2 and 4)",
        "source_url": "https://www.gutenberg.org/ebooks/20203",
        "notice_en": "“Speak not but what…” is archaic for “Speak only what…”. Trifling means trivial.",
        "notice_pt": "“Speak not but what…” é forma arcaica de “Speak only what…”. Trifling significa trivial, sem importância.",
        "application_en": "In a meeting, commit only to what you will deliver, then deliver it.",
        "application_pt": "Numa reunião, comprometa-se apenas com o que vai entregar e, depois, entregue.",
    },
    {
        "id": "emerson-consistency",
        "kind": "excerpt",
        "text": "A foolish consistency is the hobgoblin of little minds, adored by little statesmen and "
                "philosophers and divines. With consistency a great soul has simply nothing to do.",
        "author": "Ralph Waldo Emerson",
        "work": "Self-Reliance, in Essays: First Series (1841)",
        "source_url": "https://www.gutenberg.org/ebooks/2944",
        "notice_en": "Often misquoted without “foolish”. Hobgoblin: a mischievous spirit, so a needless fear. "
                     "Divines: clergy. Have nothing to do with: stay out of.",
        "notice_pt": "Muitas vezes citado sem “foolish”. Hobgoblin: duende travesso, ou seja, um medo desnecessário. "
                     "Divines: clérigos. Have nothing to do with: não ter relação com.",
        "application_en": "It is fine to say “Given the new data, I’ve changed my mind”; explain the reason, not just the reversal.",
        "application_pt": "Tudo bem dizer “Given the new data, I’ve changed my mind”; explique o motivo, não só a mudança.",
    },
)


# Our own paraphrases of ideas from current books: no sentences are reproduced from the books, and the
# app labels them as tutor summaries. Concept names (Level 5, Radical Candor) are attributed to their authors.
BOOK_SUMMARIES = (
    {
        "id": "greene-mastery",
        "kind": "summary",
        "text": "Robert Greene argues that mastery owes less to innate genius than to a long, deliberate apprenticeship. First you identify the work that genuinely draws you in, what he calls your Life's Task. Then you submit to years of observation and practice, ideally under a mentor, absorbing the unwritten rules of your field before you try to bend them. Greene insists that the tedium of this phase is the point: people who seem intuitively brilliant late in their careers have usually put in the hours that others avoided.",
        "author": 'Robert Greene',
        "work": 'Mastery (2012)',
        "source_url": book_search('Mastery', 'Robert Greene'),
        "notice_en": 'Submit to: accept the discipline or authority of something. “She submitted to two years of training.”',
        "notice_pt": 'Submit to: aceitar a disciplina ou autoridade de algo. “She submitted to two years of training.”',
        "application_en": 'Treat your first months in a US team as an apprenticeship: learn the unwritten rules of its meetings before trying to change them.',
        "application_pt": 'Trate seus primeiros meses num time americano como um aprendizado: aprenda as regras não escritas das reuniões antes de tentar mudá-las.',
    },
    {
        "id": "greene-human-nature",
        "kind": "summary",
        "text": 'Greene contends that people are far less rational than they believe, and that the first person you should study is yourself. Envy, grandiosity and short-term thinking do not disappear because we ignore them; they leak out in our tone, our choices and our blind spots. He calls this hidden side of personality the shadow. His advice is to judge people by patterns of behavior rather than by their words or a single incident, and to treat empathy as a practical skill for reading others, not as a sentimental gesture.',
        "author": 'Robert Greene',
        "work": 'The Laws of Human Nature (2018)',
        "source_url": book_search('The Laws of Human Nature', 'Robert Greene'),
        "notice_en": 'Leak out: become visible without your intention. “His frustration leaked out in the email.”',
        "notice_pt": 'Leak out: transparecer sem querer. “His frustration leaked out in the email.”',
        "application_en": 'Before sending a message you wrote while annoyed, reread it only for tone.',
        "application_pt": 'Antes de enviar uma mensagem escrita com irritação, releia-a só para checar o tom.',
    },
    {
        "id": "greene-war",
        "kind": "summary",
        "text": 'Greene treats everyday conflict as a contest of minds, drawing on centuries of military history. One recurring idea is that people keep fighting the previous battle: they repeat the tactics that worked last time even after the terrain has changed. Another is that emotion is the enemy of strategy, because anger narrows your vision exactly when you need the widest view. He recommends stepping back, seeing the whole field and choosing your battles. Read it as a lens on rivalry, not as a script for treating colleagues as enemies.',
        "author": 'Robert Greene',
        "work": 'The 33 Strategies of War (2006)',
        "source_url": book_search('The 33 Strategies of War', 'Robert Greene'),
        "notice_en": 'Choose your battles (idiom): only fight over what really matters.',
        "notice_pt": 'Choose your battles (expressão): só brigar pelo que realmente importa.',
        "application_en": 'Before a tense discussion, decide which single point is worth winning and let the minor ones go.',
        "application_pt": 'Antes de uma discussão tensa, decida qual ponto vale a pena defender e deixe os menores de lado.',
    },
    {
        "id": "holiday-obstacle",
        "kind": "summary",
        "text": 'Drawing on Stoic philosophy, Ryan Holiday argues that obstacles are not interruptions to the work; they are the work. He organizes his approach into three disciplines. Perception means seeing a setback calmly and without exaggeration. Action means applying steady, creative effort to the part you can actually move. Will means accepting with equanimity what cannot be changed. The point is not to pretend that problems are pleasant, but to stop spending energy on outrage and redirect it toward the next useful step.',
        "author": 'Ryan Holiday',
        "work": 'The Obstacle Is the Way (2014)',
        "source_url": book_search('The Obstacle Is the Way', 'Ryan Holiday'),
        "notice_en": 'Equanimity: calm and balance under pressure. Formal, but common in leadership writing.',
        "notice_pt": 'Equanimity: serenidade, equilíbrio sob pressão. Formal, mas comum em textos sobre liderança.',
        "application_en": 'In an incident update, separate what happened, what you are doing now and what is outside your control.',
        "application_pt": 'Num update de incidente, separe o que aconteceu, o que você está fazendo agora e o que está fora do seu controle.',
    },
    {
        "id": "holiday-ego",
        "kind": "summary",
        "text": "Holiday describes ego as an unhealthy belief in our own importance and traces how it sabotages us at every stage. When we aspire, it tempts us to talk about our plans instead of working on them. When we succeed, it makes us complacent and defensive. When we fail, it turns an ordinary setback into wounded pride. His remedy is to remain a permanent student, to let results speak louder than announcements, and to measure yourself against your own standards rather than other people's applause.",
        "author": 'Ryan Holiday',
        "work": 'Ego Is the Enemy (2016)',
        "source_url": book_search('Ego Is the Enemy', 'Ryan Holiday'),
        "notice_en": 'Complacent: too satisfied with yourself to keep improving. A false friend of the Portuguese complacente (lenient).',
        "notice_pt": 'Complacent: acomodado, satisfeito demais para continuar melhorando. Falso cognato de complacente (que seria lenient).',
        "application_en": 'Share progress with evidence rather than promises, and ask for critique on the work you are proudest of.',
        "application_pt": 'Compartilhe progresso com evidências, não promessas, e peça críticas justamente sobre o trabalho de que mais se orgulha.',
    },
    {
        "id": "duckworth-grit",
        "kind": "summary",
        "text": 'Psychologist Angela Duckworth argues that talent alone predicts surprisingly little about long-term achievement. What distinguishes high achievers in her research is grit: passion and perseverance sustained over years toward a single, high-level goal. She stresses that effort matters twice, first in building a skill and then in turning that skill into results. Grit is not mere stubbornness; it grows through deliberate practice, a purpose larger than yourself, and the hope that comes from believing you can improve.',
        "author": 'Angela Duckworth',
        "work": 'Grit (2016)',
        "source_url": book_search('Grit', 'Angela Duckworth'),
        "notice_en": 'Perseverance: continuing despite difficulty. Stick with it is the everyday spoken equivalent.',
        "notice_pt": 'Perseverance: perseverança, continuar apesar das dificuldades. Na fala do dia a dia: stick with it.',
        "application_en": 'Pick one English skill, such as word stress in long words, and practice it daily for a month instead of switching topics.',
        "application_pt": 'Escolha uma habilidade em inglês, como a sílaba tônica de palavras longas, e pratique todo dia por um mês em vez de trocar de tema.',
    },
    {
        "id": "dweck-mindset",
        "kind": "summary",
        "text": "Carol Dweck's research contrasts a fixed mindset, the belief that ability is a set amount you either have or lack, with a growth mindset, the belief that ability develops through effort, good strategies and feedback. People with a fixed mindset tend to avoid challenges that might expose their limits, while people with a growth mindset treat the same challenges as useful information. Dweck has also warned that the idea is often oversimplified: praising effort alone does not help if the strategy itself is not working.",
        "author": 'Carol S. Dweck',
        "work": 'Mindset (2006)',
        "source_url": book_search('Mindset', 'Carol S. Dweck'),
        "notice_en": "Yet at the end of a sentence turns a verdict into a stage: “I'm not comfortable presenting in English yet.”",
        "notice_pt": "Yet no fim da frase transforma um veredito em uma etapa: “I'm not comfortable presenting in English yet.”",
        "application_en": "Replace “I'm bad at small talk” with “I'm not great at small talk yet, so I'm practicing a few openers.”",
        "application_pt": "Troque “I'm bad at small talk” por “I'm not great at small talk yet, so I'm practicing a few openers.”",
    },
    {
        "id": "newport-deep-work",
        "kind": "summary",
        "text": 'Cal Newport distinguishes deep work, cognitively demanding tasks done in long, distraction-free stretches, from shallow work, the logistical tasks you can do while distracted. He argues that the ability to concentrate is becoming rarer at the very moment it is becoming more valuable. Instead of relying on willpower, Newport recommends routines: scheduled blocks for focus, clear rules about when to check messages, and accepting that being a little less responsive is a fair price for doing your best work.',
        "author": 'Cal Newport',
        "work": 'Deep Work (2016)',
        "source_url": book_search('Deep Work', 'Cal Newport'),
        "notice_en": 'Stretch (noun): a continuous period of time. “I worked for a three-hour stretch.”',
        "notice_pt": 'Stretch (substantivo): um período contínuo de tempo. “I worked for a three-hour stretch.”',
        "application_en": "Tell your team: “I'm blocking nine to eleven for focused work; I'll catch up on messages right after.”",
        "application_pt": "Diga ao time: “I'm blocking nine to eleven for focused work; I'll catch up on messages right after.”",
    },
    {
        "id": "collins-good-to-great",
        "kind": "summary",
        "text": 'Jim Collins and his research team studied companies that made a lasting leap from average to outstanding results. Their leaders were rarely charismatic celebrities. Collins calls them Level 5 leaders: a paradoxical blend of personal humility and intense professional will. They credited others when things went well and took responsibility when things went badly. These companies also put the right people in place before settling on a strategy, and they confronted unpleasant facts honestly instead of explaining them away.',
        "author": 'Jim Collins',
        "work": 'Good to Great (2001)',
        "source_url": book_search('Good to Great', 'Jim Collins'),
        "notice_en": 'Explain away: give reasons so that a problem seems unimportant. Often critical in tone.',
        "notice_pt": 'Explain away: dar justificativas para que um problema pareça sem importância. Costuma ter tom crítico.',
        "application_en": 'In a project review, credit the team for the win and own the miss yourself.',
        "application_pt": 'Numa revisão de projeto, dê o crédito da vitória ao time e assuma você mesmo o que deu errado.',
    },
    {
        "id": "sinek-why",
        "kind": "summary",
        "text": 'Simon Sinek argues that inspiring leaders and organizations communicate from the inside out. Most of us explain what we do, sometimes how we do it, and rarely why. His Golden Circle reverses that order: begin with the purpose or belief behind the work, then the approach, and only then the product or task. His claim is that people commit more readily to a cause they understand than to a list of features, and that a clear purpose helps a team make consistent decisions when nobody is checking.',
        "author": 'Simon Sinek',
        "work": 'Start with Why (2009)',
        "source_url": book_search('Start with Why', 'Simon Sinek'),
        "notice_en": 'From the inside out: starting from the core and moving outward. Also: know something inside out (very well).',
        "notice_pt": 'From the inside out: do centro para fora. Também: know something inside out (conhecer muito bem).',
        "application_en": 'Open a proposal with one sentence on why it matters to the customer before any technical detail.',
        "application_pt": 'Abra uma proposta com uma frase sobre por que ela importa para o cliente, antes de qualquer detalhe técnico.',
    },
    {
        "id": "scott-candor",
        "kind": "summary",
        "text": 'Kim Scott, a former executive at Google and Apple, built her approach on two dimensions: caring personally and challenging directly. Challenging without caring comes across as obnoxious aggression; caring without challenging becomes ruinous empathy, where a manager stays quiet to be nice and the person never improves. The goal is to do both at once. Scott also advises asking for criticism before giving it, praising in public and criticizing in private, and keeping feedback specific, timely and about the work, not the person.',
        "author": 'Kim Scott',
        "work": 'Radical Candor (2017)',
        "source_url": book_search('Radical Candor', 'Kim Scott'),
        "notice_en": "Come across as: give a certain impression. “I don't want to come across as rude.”",
        "notice_pt": "Come across as: passar uma certa impressão. “I don't want to come across as rude.”",
        "application_en": "Before giving feedback, ask for it: “What's one thing I could do to make our syncs more useful?”",
        "application_pt": "Antes de dar feedback, peça: “What's one thing I could do to make our syncs more useful?”",
    },
    {
        "id": "horowitz-hard-things",
        "kind": "summary",
        "text": "Ben Horowitz, a venture capitalist and former CEO, notes that management books explain how to build a great company but say little about what to do when everything is going wrong. Drawing on his own company's near-collapses, he argues that the hardest part of leadership is psychological: making decisions with incomplete information while staying steady in front of the team. He contrasts a peacetime leader, who widens opportunities and encourages broad creativity, with a wartime leader, who focuses relentlessly on one existential threat.",
        "author": 'Ben Horowitz',
        "work": 'The Hard Thing About Hard Things (2014)',
        "source_url": book_search('The Hard Thing About Hard Things', 'Ben Horowitz'),
        "notice_en": "Existential threat: a danger to something's very survival. Common in business: an existential threat to the company.",
        "notice_pt": 'Existential threat: uma ameaça à própria sobrevivência. Comum em negócios: an existential threat to the company.',
        "application_en": 'In a crisis, name the one priority clearly and say explicitly what is paused.',
        "application_pt": 'Numa crise, diga claramente qual é a prioridade e deixe explícito o que fica pausado.',
    },
    {
        "id": "grove-high-output",
        "kind": "summary",
        "text": "Andy Grove, the longtime Intel leader, defined a manager's output not as personal activity but as the output of their team plus the teams they influence. That shifts the question from how busy you are to which of your actions has the most leverage. Grove valued regular one-on-one meetings in which the direct report sets the agenda, because an hour of focused attention can improve weeks of someone else's work. He also urged managers to plan around measurable outputs rather than effort.",
        "author": 'Andrew S. Grove',
        "work": 'High Output Management (1983)',
        "source_url": book_search('High Output Management', 'Andrew S. Grove'),
        "notice_en": 'Leverage (noun): the power to get a large effect from a small action. In US offices it is also a verb.',
        "notice_pt": 'Leverage (substantivo): poder de obter grande efeito com pouca ação. Em escritórios americanos, também é verbo.',
        "application_en": "In a one-on-one, ask: “What's slowing you down that I could remove?”",
        "application_pt": "Num one-on-one, pergunte: “What's slowing you down that I could remove?”",
    },
    {
        "id": "willink-ownership",
        "kind": "summary",
        "text": 'Jocko Willink and Leif Babin, former Navy SEAL officers, argue that leaders must own everything in their world, including the mistakes of the people they lead. When a mission fails, blaming others or circumstances may be partly accurate, but it blocks learning; taking full ownership invites the team to do the same. Their other principles include keeping plans simple, believing in the mission, and, when overwhelmed, choosing the single highest priority, executing it, and only then moving to the next.',
        "author": 'Jocko Willink and Leif Babin',
        "work": 'Extreme Ownership (2015)',
        "source_url": book_search('Extreme Ownership', 'Jocko Willink and Leif Babin'),
        "notice_en": "Own (verb): take full responsibility for. “I own this decision.” “That's on me” is the spoken equivalent.",
        "notice_pt": "Own (verbo): assumir total responsabilidade por. “I own this decision.” Na fala: “That's on me.”",
        "application_en": "When something you led goes wrong, say “That's on me” and follow it with the one thing you will change.",
        "application_pt": "Quando algo que você liderou dá errado, diga “That's on me” e emende com a única coisa que você vai mudar.",
    },
    {
        "id": "voss-negotiation",
        "kind": "summary",
        "text": "Chris Voss, a former FBI hostage negotiator, argues that negotiation is driven much more by emotion than by logic. His toolkit centers on tactical empathy: showing that you understand the other side's perspective without necessarily agreeing with it. Techniques include labeling the emotion you hear, repeating the last few words someone said to invite them to elaborate, and asking open questions that begin with how or what, which let the other person feel in control while you work on the problem together.",
        "author": 'Chris Voss',
        "work": 'Never Split the Difference (2016)',
        "source_url": book_search('Never Split the Difference', 'Chris Voss'),
        "notice_en": 'Split the difference: agree on a point halfway between two positions. Voss argues it often leaves both sides unhappy.',
        "notice_pt": 'Split the difference: chegar a um meio-termo. Voss argumenta que isso costuma deixar os dois lados insatisfeitos.',
        "application_en": 'Instead of a flat no, ask: “How am I supposed to deliver that by Friday?”',
        "application_pt": 'Em vez de um não seco, pergunte: “How am I supposed to deliver that by Friday?”',
    },
    {
        "id": "lencioni-dysfunctions",
        "kind": "summary",
        "text": "Patrick Lencioni's leadership fable describes five problems that build on one another. At the base is an absence of trust: people are unwilling to be vulnerable with each other. Without trust, teams avoid productive conflict; without honest debate, members never truly commit to decisions; without commitment, they hesitate to hold one another accountable; and without accountability, ego and personal status crowd out attention to collective results. His practical message is that healthy conflict signals trust rather than a lack of it.",
        "author": 'Patrick Lencioni',
        "work": 'The Five Dysfunctions of a Team (2002)',
        "source_url": book_search('The Five Dysfunctions of a Team', 'Patrick Lencioni'),
        "notice_en": 'Hold someone accountable: make someone answer for their commitments. Very common in US workplaces.',
        "notice_pt": 'Hold someone accountable: cobrar de alguém o que foi combinado. Muito comum em empresas americanas.',
        "application_en": "Invite disagreement in meetings: “What's the strongest argument against this plan?”",
        "application_pt": "Convide a discordância nas reuniões: “What's the strongest argument against this plan?”",
    },
    {
        "id": "frankl-meaning",
        "kind": "summary",
        "text": 'Viktor Frankl, a psychiatrist who survived Nazi concentration camps, observed that prisoners who held on to a sense of meaning, such as a person to return to or work to complete, often found more strength to endure. The experience reinforced logotherapy, the approach he had begun developing before the war, which treats the search for meaning as a primary human drive. His central claim about resilience is that even when outward freedom is taken away, people keep the freedom to choose their attitude toward their circumstances.',
        "author": 'Viktor E. Frankl',
        "work": "Man's Search for Meaning (1946)",
        "source_url": book_search("Man's Search for Meaning", 'Viktor E. Frankl'),
        "notice_en": 'Hold on to: keep, refuse to let go of. “Hold on to that idea for the next meeting.”',
        "notice_pt": 'Hold on to: manter, não largar. “Hold on to that idea for the next meeting.”',
        "application_en": 'When a project gets rough, say out loud who benefits when it ships.',
        "application_pt": 'Quando um projeto ficar difícil, diga em voz alta quem se beneficia quando ele for entregue.',
    },
    {
        "id": "duhigg-habit",
        "kind": "summary",
        "text": "Journalist Charles Duhigg popularized the habit loop: a cue that triggers a behavior, the routine that follows, and a reward that makes the brain want to repeat it. He argues that you rarely erase a bad habit; you change it by keeping the cue and the reward while swapping in a new routine. He also describes keystone habits, small changes such as regular exercise or family dinners that set off a chain reaction in other areas of a person's life or of an organization.",
        "author": 'Charles Duhigg',
        "work": 'The Power of Habit (2012)',
        "source_url": book_search('The Power of Habit', 'Charles Duhigg'),
        "notice_en": 'Set off a chain reaction: start a series of events, each causing the next.',
        "notice_pt": 'Set off a chain reaction: desencadear uma série de eventos, um provocando o outro.',
        "application_en": 'Attach English practice to an existing cue: after your first coffee, rehearse one sentence aloud.',
        "application_pt": 'Associe a prática de inglês a um gatilho que já existe: depois do primeiro café, ensaie uma frase em voz alta.',
    },
)


def _interleave(summaries, excerpts):
    """One public-domain passage after every two summaries."""
    remaining = iter(excerpts)
    readings = []
    for number, item in enumerate(summaries, 1):
        readings.append(item)
        if number % 2 == 0:
            readings.append(next(remaining, None))
    readings.extend(remaining)
    return tuple(r for r in readings if r)


BOOK_EXCERPTS = _interleave(BOOK_SUMMARIES, PUBLIC_DOMAIN_EXCERPTS)


def excerpt_for(index):
    return dict(BOOK_EXCERPTS[index % len(BOOK_EXCERPTS)])


def saved_excerpt(value):
    return _saved(value, BOOK_EXCERPTS)
