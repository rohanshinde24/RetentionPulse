export default function AboutView() {
  return (
    <>
      <div className="workspace-head">
        <p className="eyebrow">Engineering overview</p>
        <h1>An explainable churn-prediction system, built end to end.</h1>
        <p>
          RetentionPulse is a portfolio project that turns a telecom churn
          model into a deployable product: a usable React interface, a
          service-oriented Python API, explainability, tests, containers, and
          a public Render deployment.
        </p>
      </div>
      <div className="detail-grid">
        <section className="panel profile">
          <p className="eyebrow">Product scope</p>
          <h2>From model artifact to application</h2>
          <p className="explain-intro">The interface supports portfolio review, customer drill-in, single predictions with SHAP drivers, and bounded CSV batch inference with downloadable results and validation feedback.</p>
        </section>
        <section className="panel profile">
          <p className="eyebrow">Machine learning</p>
          <h2>LightGBM + SHAP</h2>
          <p className="explain-intro">The churn classifier was evaluated at 0.84 ROC-AUC on held-out telecom data. The explanation service uses Tree SHAP to return the top positive and negative drivers for every individual score.</p>
        </section>
        <section className="panel profile">
          <p className="eyebrow">Frontend</p>
          <h2>React + TypeScript</h2>
          <p className="explain-intro">The frontend uses React, TypeScript, Vite, Framer Motion, and Lucide. It is designed as an editorial risk workspace rather than a generic admin dashboard, with accessible loading and error states.</p>
        </section>
      </div>
      <div className="detail-grid" style={{ marginTop: 16 }}>
        <section className="panel profile">
          <p className="eyebrow">Backend architecture</p>
          <h2>FastAPI microservices</h2>
          <p className="explain-intro">A public gateway owns the catalogue, CSV workflow, structured errors, and API docs. It forwards scoring to the prediction service and explanations to a dedicated SHAP service using a reused asynchronous HTTP client.</p>
        </section>
        <section className="panel profile">
          <p className="eyebrow">Operational quality</p>
          <h2>Built to be run</h2>
          <p className="explain-intro">Docker Compose starts prediction, explanation, gateway, and UI services together. Batches are capped at 100 records per model request and CSV uploads at 1,000 rows to keep work bounded.</p>
        </section>
        <section className="panel profile">
          <p className="eyebrow">Verification</p>
          <h2>Tests and delivery</h2>
          <p className="explain-intro">Pytest covers prediction, explanation, and gateway contracts. GitHub Actions runs backend tests plus frontend lint/build, and the application is deployed publicly through Render.</p>
        </section>
      </div>
    </>
  );
}
