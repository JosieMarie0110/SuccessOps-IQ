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

.interview-card {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 6px 18px rgba(71, 85, 105, 0.08);
    margin-top: 14px;
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

.markdown h3 {
    margin-top: 12px;
    margin-bottom: 6px;
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


def get_topic(topic_name):
    topic = STUDY_TOPICS[topic_name]

    return {
        "definition": topic.get("definition", ""),
        "why_it_matters": topic.get("why_it_matters", ""),
        "good_looks_like": topic.get("good_looks_like", []),
        "risk_signals": topic.get("risk_signals", []),
        "metrics": topic.get("metrics", []),
        "scenario": topic.get("scenario", ""),
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
        f"A Customer Success team is navigating **{topic_name}** within an active customer relationship. "
        f"The goal is to keep the customer progressing toward value while identifying any risks early.\n\n"
        f"**Context:** {definition}\n\n"
        f"**Why this matters in practice:** {why}"
    )


def build_dynamic_talking_points(topic_name, topic):
    points = []

    if topic["good_looks_like"]:
        points.append(
            f"Start by describing what strong {topic_name} execution looks like: {', '.join(topic['good_looks_like'][:3])}."
        )

    if topic["risk_signals"]:
        points.append(
            f"Then highlight warning signs such as: {', '.join(topic['risk_signals'][:3])}."
        )

    if topic["metrics"]:
        points.append(
            f"Anchor your answer in measurable indicators like: {', '.join(topic['metrics'][:3])}."
        )

    if topic["definition"]:
        points.append(
            f"Close by framing the concept clearly: {topic['definition']}"
        )

    if not points:
        points.append(
            f"Explain how {topic_name} connects to customer outcomes and execution across the lifecycle."
        )

    return bullets(points)


def build_dynamic_key_takeaway(topic_name, topic):
    if topic["why_it_matters"] and topic["metrics"]:
        return (
            f"**{topic_name}** is strongest when teams connect lifecycle execution to measurable outcomes, "
            f"using indicators such as {', '.join(topic['metrics'][:2])} to guide action."
        )

    if topic["why_it_matters"] and topic["risk_signals"]:
        return (
            f"The value of **{topic_name}** comes from recognizing early signals like "
            f"{', '.join(topic['risk_signals'][:2])} before they become larger customer risks."
        )

    if topic["good_looks_like"]:
        return (
            f"Strong **{topic_name}** execution shows up through behaviors such as "
            f"{', '.join(topic['good_looks_like'][:2])}."
        )

    return (
        f"**{topic_name}** matters most when Customer Success teams translate signals into action, "
        f"clear communication, and stronger customer outcomes."
    )


def build_interview_qa(topic_name, topic):
    good = ", ".join(topic["good_looks_like"][:2]) if topic["good_looks_like"] else "clear ownership and aligned goals"
    risks = ", ".join(topic["risk_signals"][:2]) if topic["risk_signals"] else "low engagement or unclear value"
    metrics = ", ".join(topic["metrics"][:2]) if topic["metrics"] else "adoption and engagement metrics"

    q1 = f"How do you approach {topic_name.lower()} in a Customer Success role?"
    a1 = (
        f"I focus on where {topic_name.lower()} shows up in the lifecycle and whether the customer is progressing toward value. "
        f"That usually means making sure things like {good} are in place early."
    )

    q2 = f"How do you know if {topic_name.lower()} is not going well?"
    a2 = (
        f"I look for warning signs such as {risks}. "
        f"Those usually signal misalignment, stalled progress, or growing risk if not addressed early."
    )

    q3 = f"What metrics would you use to evaluate {topic_name.lower()}?"
    a3 = (
        f"I would look at measures like {metrics}, because they help show whether the customer is actually moving toward value."
    )

    return f"""
# Interview Questions & Answers

**Q: {q1}**  
**A:** {a1}

**Q: {q2}**  
**A:** {a2}

**Q: {q3}**  
**A:** {a3}
"""


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
## Real-World Scenario

{scenario_text}

---

## Interview Talking Points

{talking_points_text}

---

## Key Takeaway

{key_takeaway_text}
"""


def update_topic(topic_name):
    topic = get_topic(topic_name)
    return (
        build_left_panel(topic_name),
        build_right_panel(topic_name),
        build_interview_qa(topic_name, topic),
    )


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
    default_topic_data = get_topic(default_topic)

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

    with gr.Row():
        interview_qa_panel = gr.Markdown(
            value=build_interview_qa(default_topic, default_topic_data),
            elem_classes=["interview-card"],
        )

    topic_dropdown.change(
        fn=update_topic,
        inputs=topic_dropdown,
        outputs=[left_panel, right_panel, interview_qa_panel],
    )

demo.launch(css=CUSTOM_CSS)
