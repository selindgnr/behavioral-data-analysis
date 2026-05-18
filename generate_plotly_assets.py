from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go


SEED = 42
N_PARTICIPANTS = 30
CONDITIONS = ["baseline", "adaptation"]
MIN_TRIALS = 90
OUTPUT_DIR = Path("assets")


def simulate_data() -> pd.DataFrame:
    """Create the same simulated repeated-measures dataset used in the notebook."""
    np.random.seed(SEED)
    rows = []

    for participant_id in range(1, N_PARTICIPANTS + 1):
        for condition in CONDITIONS:
            mean_rate = 5.0 if condition == "baseline" else 6.5
            rows.append(
                {
                    "participant_id": participant_id,
                    "condition": condition,
                    "switch_rate": np.random.normal(loc=mean_rate, scale=1.0),
                    "trials_completed": np.random.randint(low=85, high=101),
                }
            )

    return pd.DataFrame(rows)


def prepare_summary() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply quality control and return long and wide participant summaries."""
    df = simulate_data()
    participant_trial_min = df.groupby("participant_id")["trials_completed"].min()
    valid_participants = participant_trial_min[participant_trial_min >= MIN_TRIALS].index
    df_valid = df[df["participant_id"].isin(valid_participants)].copy()

    summary = (
        df_valid.groupby(["participant_id", "condition"])["switch_rate"]
        .mean()
        .reset_index()
    )
    summary_pivot = summary.pivot(
        index="participant_id",
        columns="condition",
        values="switch_rate",
    ).reset_index()

    return summary, summary_pivot


def build_condition_means_figure(summary: pd.DataFrame) -> go.Figure:
    """Plot condition means with standard error bars."""
    stats_by_condition = (
        summary.groupby("condition")["switch_rate"]
        .agg(["mean", "sem"])
        .reindex(CONDITIONS)
        .reset_index()
    )

    fig = go.Figure(
        data=[
            go.Bar(
                x=stats_by_condition["condition"],
                y=stats_by_condition["mean"],
                error_y=dict(type="data", array=stats_by_condition["sem"]),
                marker_color=["#3d5a80", "#ee6c4d"],
                text=[f"{value:.2f}" for value in stats_by_condition["mean"]],
                textposition="outside",
                hovertemplate=(
                    "Condition=%{x}<br>"
                    "Mean switch rate=%{y:.2f}<br>"
                    "SEM=%{error_y.array:.2f}<extra></extra>"
                ),
            )
        ]
    )
    fig.update_layout(
        title="Mean Switch Rate by Condition",
        xaxis_title="Condition",
        yaxis_title="Mean Switch Rate",
        template="plotly_white",
        width=900,
        height=550,
        margin=dict(l=60, r=40, t=80, b=60),
    )
    return fig


def build_participant_comparison_figure(summary_pivot: pd.DataFrame) -> go.Figure:
    """Plot within-subject change from baseline to adaptation for each participant."""
    fig = go.Figure()

    for row in summary_pivot.itertuples(index=False):
        fig.add_trace(
            go.Scatter(
                x=CONDITIONS,
                y=[row.baseline, row.adaptation],
                mode="lines+markers",
                line=dict(color="rgba(61, 90, 128, 0.35)", width=1.5),
                marker=dict(size=8, color=["#3d5a80", "#ee6c4d"]),
                hovertemplate=(
                    f"Participant {row.participant_id}"
                    "<br>Condition=%{x}<br>Switch rate=%{y:.2f}<extra></extra>"
                ),
                showlegend=False,
            )
        )

    mean_values = summary_pivot[["baseline", "adaptation"]].mean()
    fig.add_trace(
        go.Scatter(
            x=CONDITIONS,
            y=mean_values.values,
            mode="lines+markers+text",
            line=dict(color="#101418", width=4),
            marker=dict(size=12, color="#101418"),
            text=[f"{value:.2f}" for value in mean_values.values],
            textposition="top center",
            name="Group mean",
            hovertemplate="Group mean<br>Condition=%{x}<br>Switch rate=%{y:.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        title="Participant-Level Change Across Conditions",
        xaxis_title="Condition",
        yaxis_title="Switch Rate",
        template="plotly_white",
        width=900,
        height=550,
        margin=dict(l=60, r=40, t=80, b=60),
    )
    return fig


def export_figure(fig: go.Figure, stem: str) -> None:
    """Write both interactive HTML and static PNG outputs for README usage."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    fig.write_html(OUTPUT_DIR / f"{stem}.html", include_plotlyjs="cdn")
    fig.write_image(OUTPUT_DIR / f"{stem}.png", scale=2)


def main() -> None:
    summary, summary_pivot = prepare_summary()
    figures = {
        "plotly-condition-means": build_condition_means_figure(summary),
        "plotly-participant-comparison": build_participant_comparison_figure(summary_pivot),
    }

    for stem, figure in figures.items():
        export_figure(figure, stem)

    print(f"Saved {len(figures)} Plotly figures to {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
