type Shap = { name: string; abs_shap: number; shap: number };

function ShapBars({ items }: { items?: Shap[] }) {
  if (!items) {
    return (
      <div className="text-sm text-gray-500">
        Run Explain to see feature contributions.
      </div>
    );
  }
  return (
    <ul className="space-y-2">
      {items.map((f, i) => (
        <li key={i} className="grid grid-cols-12 gap-2 items-center">
          <div className="col-span-5 truncate text-sm font-medium">
            {f.name}
          </div>
          <div className="col-span-5">
            <div className="h-2 w-full bg-gray-100 rounded">
              <div
                className="h-2 bg-gray-900 rounded"
                style={{
                  width: `${Math.min(100, Math.abs(f.abs_shap) * 100)}%`,
                }}
              />
            </div>
          </div>
          <div className="col-span-2 text-right text-xs text-gray-600">
            {f.shap.toFixed(4)}
          </div>
        </li>
      ))}
    </ul>
  );
}

export default ShapBars;
