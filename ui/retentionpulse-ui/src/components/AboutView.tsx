export default function AboutView() {
  return (
    <>
      <div className="workspace-head">
        <p className="eyebrow">About RetentionPulse</p>
        <h1>Prediction is a signal. Retention is the decision.</h1>
        <p>
          RetentionPulse helps teams identify customers who may be at risk of
          churn, understand the drivers behind each score, and prioritize a
          thoughtful follow-up.
        </p>
      </div>
      <div className="detail-grid">
        <section className="panel profile">
          <p className="eyebrow">What it does</p>
          <h2>Customer-level focus</h2>
          <p className="explain-intro">The portfolio view surfaces risk, while each profile gives a specific probability and the model factors that most influenced it.</p>
        </section>
        <section className="panel profile">
          <p className="eyebrow">How it works</p>
          <h2>Model + explanation</h2>
          <p className="explain-intro">A LightGBM churn model was evaluated at 0.84 ROC-AUC on held-out telecom data. SHAP values describe the strongest positive and negative influences for an individual prediction.</p>
        </section>
        <section className="panel profile">
          <p className="eyebrow">Use with care</p>
          <h2>Start a conversation</h2>
          <p className="explain-intro">Risk is not a verdict about a customer. Use it to guide outreach and offers, then pair it with context, consent, and human judgment.</p>
        </section>
      </div>
    </>
  );
}
