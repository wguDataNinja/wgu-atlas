import Link from "next/link";

export default function Footer({ dataDate }: { dataDate?: string }) {
  return (
    <footer className="border-t border-slate-200 bg-slate-50 mt-16">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm text-slate-500">
          <div>
            <p className="font-semibold text-slate-700 mb-1">WGU Atlas</p>
            <p>Created by WGU-DataNinja</p>
            <p className="mt-1">
              An independent community project. Not affiliated with WGU.
            </p>
          </div>
          <div>
            <p className="font-semibold text-slate-700 mb-1">Data</p>
            <p>Catalog coverage: 2017-01 → 2026-03</p>
            {dataDate && <p>Data through: {dataDate}</p>}
            <p className="mt-1">
              <Link href="/methods" className="underline hover:text-slate-700">
                Methods
              </Link>
              {" · "}
              <Link href="/data" className="underline hover:text-slate-700">
                Download datasets
              </Link>
            </p>
          </div>
          <div>
            <p className="font-semibold text-slate-700 mb-1">Disclaimer</p>
            <p>
              All data is derived from WGU&apos;s publicly available course catalog.
              Catalog dates reflect publication, not student rollout timing.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
