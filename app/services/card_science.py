from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable

from ..schemas import CardInsight, CycleInsight, PersonalBlueprint


@dataclass(frozen=True)
class CardDefinition:
    name: str
    keywords: str
    advice: str


# Simplified 52-card deck for card science interpretations.
DECK: list[CardDefinition] = [
    CardDefinition("Ace of Hearts", "Birth of passion and emotional renewal.", "Lead with compassion and allow yourself to begin again."),
    CardDefinition("Two of Hearts", "Connection and heartfelt alliances.", "Nurture intimate bonds through honest conversation."),
    CardDefinition("Three of Hearts", "Creative expression of love.", "Experiment with new ways to communicate affection."),
    CardDefinition("Four of Hearts", "Emotional stability and home.", "Create rituals that remind you of emotional safety."),
    CardDefinition("Five of Hearts", "Emotional adventure.", "Travel, learn, and keep your heart curious."),
    CardDefinition("Six of Hearts", "Karmic balance in relationships.", "Choose forgiveness and live your values consistently."),
    CardDefinition("Seven of Hearts", "Spiritual tests of love.", "Trust the unseen and move beyond fear of loss."),
    CardDefinition("Eight of Hearts", "Magnetic charisma.", "Use your influence to inspire, not control."),
    CardDefinition("Nine of Hearts", "Emotional fulfillment.", "Release attachments that block your joy."),
    CardDefinition("Ten of Hearts", "Celebration and community.", "Host gatherings that keep your heart open."),
    CardDefinition("Jack of Hearts", "Devotional creativity.", "Serve with humility and playful spirit."),
    CardDefinition("Queen of Hearts", "Sacred nurturer.", "Set boundaries so your care is sustainable."),
    CardDefinition("King of Hearts", "Emotional mastery.", "Lead with emotional intelligence and kindness."),
    CardDefinition("Ace of Clubs", "Curiosity and mental sparks.", "Follow the question that lights you up."),
    CardDefinition("Two of Clubs", "Shared ideas.", "Collaborate with someone who mirrors your brilliance."),
    CardDefinition("Three of Clubs", "Creative mind.", "Channel mental restlessness into art."),
    CardDefinition("Four of Clubs", "Mental foundation.", "Design systems that let you feel secure."),
    CardDefinition("Five of Clubs", "Quest for truth.", "Study diverse viewpoints to grow."),
    CardDefinition("Six of Clubs", "Messenger of inspiration.", "Speak up; your ideas change lives."),
    CardDefinition("Seven of Clubs", "Faith in your voice.", "Silence doubt with spiritual practice."),
    CardDefinition("Eight of Clubs", "Mental focus.", "Discipline your genius to achieve breakthroughs."),
    CardDefinition("Nine of Clubs", "Completion of ideas.", "Share your wisdom freely and move on."),
    CardDefinition("Ten of Clubs", "Mastermind success.", "Teach what you know to elevate others."),
    CardDefinition("Jack of Clubs", "Inventive storyteller.", "Gamify learning to keep curiosity alive."),
    CardDefinition("Queen of Clubs", "Intuitive intellect.", "Trust inner knowing when logic is noisy."),
    CardDefinition("King of Clubs", "Visionary leadership.", "Strategize, delegate, and empower minds."),
    CardDefinition("Ace of Diamonds", "Manifestation spark.", "Initiate ventures aligned with your values."),
    CardDefinition("Two of Diamonds", "Values partnerships.", "Invest with allies who share your mission."),
    CardDefinition("Three of Diamonds", "Creative enterprise.", "Prototype boldly and learn from iteration."),
    CardDefinition("Four of Diamonds", "Financial foundation.", "Budget with intention and gratitude."),
    CardDefinition("Five of Diamonds", "Freedom with resources.", "Experiment with new revenue channels."),
    CardDefinition("Six of Diamonds", "Karmic balance in value.", "Pay it forward and settle open accounts."),
    CardDefinition("Seven of Diamonds", "Faith in prosperity.", "Release scarcity patterns with trust."),
    CardDefinition("Eight of Diamonds", "Magnetic value creator.", "Elevate your skills through disciplined focus."),
    CardDefinition("Nine of Diamonds", "Completion and generosity.", "Donate or invest to expand collective wealth."),
    CardDefinition("Ten of Diamonds", "Legacy of abundance.", "Scale what works and celebrate milestones."),
    CardDefinition("Jack of Diamonds", "Creative investor.", "Pitch imaginative offers with heart."),
    CardDefinition("Queen of Diamonds", "Resourceful mentor.", "Curate experiences that feel luxurious and wise."),
    CardDefinition("King of Diamonds", "Regal commerce.", "Lead enterprises with integrity."),
    CardDefinition("Ace of Spades", "Spiritual initiation.", "Embrace transformation with courage."),
    CardDefinition("Two of Spades", "Sacred allies.", "Partner with those who mirror your work ethic."),
    CardDefinition("Three of Spades", "Creative work-life blend.", "Invent careers that fit your soul."),
    CardDefinition("Four of Spades", "Stability in purpose.", "Guard your energy with healthy structures."),
    CardDefinition("Five of Spades", "Adventure in purpose.", "Make brave pivots that honour your truth."),
    CardDefinition("Six of Spades", "Karmic destiny.", "Stay consistent; the universe is taking notes."),
    CardDefinition("Seven of Spades", "Faith in purpose.", "Transcend worry through spiritual discipline."),
    CardDefinition("Eight of Spades", "Powerhouse worker.", "Channel intensity into sustainable routines."),
    CardDefinition("Nine of Spades", "Completion of cycles.", "Release what is ending with reverence."),
    CardDefinition("Ten of Spades", "Mastery of craft.", "Build systems that hold your ambitious visions."),
    CardDefinition("Jack of Spades", "Mystic artisan.", "Blend sacred practice with practical magic."),
    CardDefinition("Queen of Spades", "Soulful authority.", "Lead through embodiment and devotion."),
    CardDefinition("King of Spades", "Master teacher.", "Share the blueprint that transformed you."),
]

SPECIAL_FAMILY_DATES = {(1, 1), (12, 31)}


def day_of_year_with_leap(birthday: date) -> int:
    start_of_year = date(birthday.year, 1, 1)
    return (birthday - start_of_year).days + 1


def pick_card_by_offset(birthday: date, offset: int = 0) -> CardDefinition:
    index = (day_of_year_with_leap(birthday) - 1 + offset) % len(DECK)
    return DECK[index]


def derive_personal_blueprint(birthday: date) -> PersonalBlueprint:
    life_card = pick_card_by_offset(birthday)
    ruling_card = pick_card_by_offset(birthday, offset=7)
    is_special_family = (birthday.month, birthday.day) in SPECIAL_FAMILY_DATES

    soul_resource_card = None
    soul_challenge_card = None
    if not is_special_family:
        soul_resource_card = pick_card_by_offset(birthday, offset=14)
        soul_challenge_card = pick_card_by_offset(birthday, offset=21)

    return PersonalBlueprint(
        life_card=_to_insight("生命牌", life_card),
        ruling_card=_to_insight("守护牌", ruling_card),
        soul_resource_card=_to_insight("灵魂资源牌", soul_resource_card)
        if soul_resource_card
        else None,
        soul_challenge_card=_to_insight("灵魂挑战牌", soul_challenge_card)
        if soul_challenge_card
        else None,
        is_special_family=is_special_family,
    )


def build_yearly_cycles(birthday: date, cycle_count: int = 7) -> list[CycleInsight]:
    start_year = date.today().year
    start_reference = date(start_year, birthday.month, birthday.day)
    cycles: list[CycleInsight] = []
    for index in range(cycle_count):
        cycle_start = start_reference + timedelta(days=index * 52)
        cycle_end = cycle_start + timedelta(days=51)
        card = pick_card_by_offset(birthday, offset=index * 5)
        cycles.append(
            CycleInsight(
                cycle_index=index + 1,
                cycle_start=cycle_start,
                cycle_end=cycle_end,
                theme=f"{card.name} 的周期主题",
                advice=card.advice,
            )
        )
    return cycles


def draw_today_card(birthday: date) -> CardInsight:
    today = date.today()
    days_since_birthday = (today - birthday).days
    card = pick_card_by_offset(birthday, offset=days_since_birthday)
    return _to_insight("今日牌", card)


def compatibility_score(primary: date, partner: date) -> int:
    difference = abs(day_of_year_with_leap(primary) - day_of_year_with_leap(partner))
    return 100 - (difference % 52) * 2


def compatibility_lessons(primary: date, partner: date) -> list[str]:
    base_messages = [
        "共同探索信任与亲密的节奏。",
        "学习在彼此的价值观之间找到平衡。",
        "彼此鼓励坚持灵魂使命。",
        "激励对方更深刻地表达爱与愿景。",
    ]
    offset = (day_of_year_with_leap(primary) + day_of_year_with_leap(partner)) % len(
        base_messages
    )
    return rotate(base_messages, offset)


def rotate(items: Iterable[str], offset: int) -> list[str]:
    items_list = list(items)
    if not items_list:
        return []
    offset = offset % len(items_list)
    return items_list[offset:] + items_list[:offset]


def build_compatibility_theme(primary: date, partner: date) -> str:
    card = pick_card_by_offset(primary, offset=day_of_year_with_leap(partner) % len(DECK))
    return f"关系的核心能量来自 {card.name}"


def _to_insight(title: str, card: CardDefinition | None) -> CardInsight:
    if card is None:
        raise ValueError("Card definition is required")
    return CardInsight(title=f"{title} · {card.name}", description=card.keywords, advice=card.advice)
