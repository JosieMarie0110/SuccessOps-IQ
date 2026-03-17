import gradio as gr
from study_content import STUDY_TOPICS

APP_TITLE = "SuccessOps IQ"
APP_SUBTITLE = (
    "Customer Success study workspace for onboarding, adoption, engagement, "
    "escalations, renewals, and strategic account management."
)

CUSTOM_CSS = """
body {
    background: linear-gradient(180deg, #dbe4ff 0%, #e2e8f0 100%);
    font-family: Inter, system-ui, sans-serif;
}

.gradio-container {
    max-width: 95vw !important;
    margin: auto !important;
}

.hero {
    background: linear-gradient(135deg, #4c1d95 0%, #2563eb 58%, #64748b 100%);
    border-radius: 20px;
    padding: 22px 24px;
    margin-bottom: 18px;
    box-shadow: 0 10px 28px rgba(37, 99, 235, 0.18);
}

.hero-title {
    font-size: 2rem;
    font-weight: 800;
    color: white;
}

.hero-subtitle {
    font-size: 1rem;
    color: rgba(255,255,255,0.92);
}

.card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 16px;
    padding: 20px;
    min-height: 500px;
    box-shadow: 0 6px 18px rgba(71, 85, 105, 0.08);
}

.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 10px;
    color: #1e3a8a;
}

h1, h2, h3 {
    color: #1e3a8a;
}

.markdown {
    padding: 4px 8px;
}

.markdown h2 {
    margin-top: 14px;
    margin-bottom: 10px;
    padding-bottom: 4px;
    border-bottom: 1px solid #cbd5e1;
}

.markdown h1 {
    margin-bottom: 14px;
}

.markdown p {
    margin-bottom: 10px;
}

.markdown ul {
    padding-left: 22px;
    margin-top: 8px;
    margin-bottom: 12px;
}

.markdown li {
    margin-bottom: 8px;
    line-height: 1.6;
}

.talking-points-list {
    margin: 10px 0 14px 0;
    padding-left: 0;
    list-style: none;
}

.talking-points-list li {
    position: relative;
    padding-left: 24px;
    margin-bottom: 12px;
    line-height: 1.65;
    color: #1f2937;
}

.talking-points-list li::before {
    content: "•";
    position: absolute;
    left: 0;
    top: 0;
    color: #1e3a8a;
    font-weight: 700;
}

p, li {
    color: #1f2937;
    line-height: 1.6;
}

footer {
    display: none !important;
}
"""


def bullets(items):
    if not items:
        return "- None listed"
    return "\n".join([f"- {item}" for item in items])


def html_bullet_list(items, class_name="clean-list"):
    if not items:
        return f'<ul class="{class_name}"><li>None listed</li></ul>'
    return f'<ul class="{class_name}">' + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def get_topic(topic_name):
    topic = STUDY_TOPICS[topic_name]

    return {
        "definition": topic.get("definition", ""),
        "why_it_matters": topic.get("why_it_matters", ""),
        "good_looks_like": topic.get("good_looks_like", []),
        "risk_signals": topic.get("risk_signals", []),
        "metrics": topic.get("metrics", []),
        "scenario": topic.get("scenario", ""),
        "talking_points": topic.get("interview_talking_points", ""),
        "business_context": (
            topic.get("business_context")
            or topic.get("context")
            or topic.get("overview")
            or ""
        ),
    }


def build_left_panel(topic_name):
    topic = get_topic(topic_name)

    return f"""
# {topic_name}

## Definition
{topic["definition"]}

## Why It Matters
{topic["why_it_matters"]}

## What Good Looks Like
{bullets(topic["good_looks_like"])}

## Risk Signals
{bullets(topic["risk_signals"])}

## Metrics
{bullets(topic["metrics"])}
"""


def build_dynamic_scenario(topic_name, topic):
    if topic["scenario"]:
        return topic["scenario"]

    definition = topic["definition"] or f"{topic_name} is a key Customer Success capability."
    why = topic["why_it_matters"] or "This topic directly affects customer outcomes and long-term retention."

    return (
        f"A Customer Success team is evaluating **{topic_name}** in a customer account where leadership wants stronger outcomes, "
        f"clearer adoption signals, and better operational alignment.\n\n"
        f"**Context:** {definition}\n\n"
        f"**Why this matters in practice:** {why}"
    )


def build_dynamic_talking_points(topic_name, topic):
    points = []

    if topic["why_it_matters"]:
        points.append(
            f"Explain why <strong>{topic_name}</strong> matters to retention, adoption, and long-term customer value."
        )

    if topic["good_looks_like"]:
        points.append(
            f"Describe what strong execution looks like, including: {', '.join(topic['good_looks_like'][:3])}."
        )

    if topic["risk_signals"]:
        points.append(
            f"Call out the main warning signs, such as: {', '.join(topic['risk_signals'][:3])}."
        )

    if topic["metrics"]:
        points.append(
            f"Reference measurable indicators like: {', '.join(topic['metrics'][:3])}."
        )

    if topic["definition"]:
        points.append(
            f"Frame the topic clearly: {topic['definition']}"
        )

    if not points:
        points.append(
            f"Discuss how <strong>{topic_name}</strong> helps Customer Success teams operate more proactively and strategically."
        )

    return html_bullet_list(points, class_name="talking-points-list")


def build_dynamic_key_takeaway(topic_name, topic):
    if topic["why_it_matters"] and topic["metrics"]:
        return (
            f"**{topic_name}** creates the most value when teams connect strategy to measurable outcomes, "
            f"using signals such as {', '.join(topic['metrics'][:2])} to guide action."
        )

    if topic["why_it_matters"] and topic["risk_signals"]:
        return (
            f"The real value of **{topic_name}** is recognizing early signals like "
            f"{', '.join(topic['risk_signals'][:2])} before they become larger customer risks."
        )

    if topic["good_looks_like"]:
        return (
            f"Strong execution in **{topic_name}** means consistently demonstrating behaviors such as "
            f"{', '.join(topic['good_looks_like'][:2])}."
        )

    return (
        f"**{topic_name}** is most effective when Customer Success teams turn customer signals into clear action, "
        f"measurable outcomes, and stronger stakeholder confidence."
    )


def build_right_panel(topic_name):
    topic = get_topic(topic_name)

    scenario_text = build_dynamic_scenario(topic_name, topic)
    talking_points_text = build_dynamic_talking_points(topic_name, topic)
    key_takeaway_text = build_dynamic_key_takeaway(topic_name, topic)

    business_context_section = f"""
## Business Context

{topic["business_context"]}

---
""" if topic["business_context"] else ""

    return f"""
{business_context_section}
## Example Scenario

{scenario_text}

---

## Interview Talking Points

{talking_points_text}

---

## Key Takeaway

{key_takeaway_text}
"""


def update_topic(topic_name):
    return build_left_panel(topic_name), build_right_panel(topic_name)


with gr.Blocks(title=APP_TITLE) as demo:
    gr.HTML(
        f"""
        <div class="hero">
            <div class="hero-title">{APP_TITLE}</div>
            <div class="hero-subtitle">{APP_SUBTITLE}</div>
        </div>
        """
    )

    default_topic = list(STUDY_TOPICS.keys())[0]

    topic_dropdown = gr.Dropdown(
        choices=list(STUDY_TOPICS.keys()),
        value=default_topic,
        label="Customer Success Topic",
    )

    with gr.Row():
        left_panel = gr.Markdown(
            value=build_left_panel(default_topic),
            elem_classes=["card"],
        )

        right_panel = gr.Markdown(
            value=build_right_panel(default_topic),
            elem_classes=["card"],
        )

    topic_dropdown.change(
        fn=update_topic,
        inputs=topic_dropdown,
        outputs=[left_panel, right_panel],
    )

demo.launch(css=CUSTOM_CSS)
