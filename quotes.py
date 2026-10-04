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


def saved_quote(value):
    """Accept complete saved excerpts with one of the checked publisher/author links."""
    if not isinstance(value, dict) or not all(isinstance(value.get(k), str) for k in QUOTE_BANK[0]):
        return None
    if value["source_url"] not in {q["source_url"] for q in QUOTE_BANK}:
        return None
    return dict(value)
