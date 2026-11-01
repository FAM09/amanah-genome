import React from 'react';
import { BookOpen, Dna, Check } from 'lucide-react';
import type { UAEPanelGene } from '../types';

interface PanelRegistryProps {
  genes: UAEPanelGene[];
  isLoading: boolean;
}

export const PanelRegistry: React.FC<PanelRegistryProps> = ({ genes, isLoading }) => {
  return (
    <div className="space-y-6">
      {/* Registry Header */}
      <div className="bg-gradient-to-r from-emerald-950 via-slate-900 to-slate-900 p-6 rounded-2xl border border-emerald-800/40 shadow-xl">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-amber-400 mb-1">
          <BookOpen className="w-4 h-4" />
          <span>Department of Health Abu Dhabi (DoH) Reference Standard</span>
        </div>
        <h2 className="text-2xl font-bold text-white tracking-tight">
          UAE Priority Premarital Screening Panel (10 Genetic Disorders)
        </h2>
        <p className="text-xs text-slate-300 mt-1 max-w-3xl leading-relaxed">
          High-penetrance autosomal recessive conditions selected based on regional epidemiological prevalence and
          actionability under modern reproductive care pathways in the United Arab Emirates.
        </p>
      </div>

      {isLoading ? (
        <div className="py-20 text-center text-slate-500 text-xs">
          <Dna className="w-8 h-8 mx-auto mb-2 animate-spin text-emerald-400" />
          <span>Loading UAE Panel Registry from API...</span>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {genes.map((gene) => (
            <div
              key={gene.gene_symbol}
              className="bg-slate-900/80 rounded-2xl p-5 border border-slate-800 shadow-md flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between pb-3 border-b border-slate-800/80 mb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-mono font-bold text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800">
                      {gene.gene_symbol}
                    </span>
                    <span className="text-[11px] text-slate-400">Chr {gene.chromosome} • OMIM {gene.omim_id}</span>
                  </div>
                  <span className="text-[10px] font-semibold text-amber-400 bg-amber-950/60 px-2 py-0.5 rounded-full border border-amber-800/60">
                    {gene.inheritance}
                  </span>
                </div>

                <h3 className="text-base font-bold text-white mb-0.5">{gene.disease_name_en}</h3>
                <h4 className="text-xs font-serif text-amber-300/80 mb-3">{gene.disease_name_ar}</h4>

                <p className="text-xs text-slate-300 leading-relaxed mb-3">
                  {gene.description_en}
                </p>

                <div className="text-[11px] text-slate-400 mb-3 bg-slate-950/60 p-2.5 rounded-xl border border-slate-800/60">
                  <span className="text-slate-500 font-medium">Regional Prevalence: </span>
                  <span className="text-slate-200">{gene.prevalence_uae}</span>
                </div>
              </div>

              <div>
                <div className="pt-3 border-t border-slate-800/80">
                  <span className="text-[11px] font-semibold text-emerald-400 flex items-center gap-1 mb-1.5">
                    <Check className="w-3.5 h-3.5" />
                    <span>Abu Dhabi Certified Clinical Interventions:</span>
                  </span>
                  <ul className="text-[11px] space-y-1 text-slate-300">
                    {gene.clinical_options.map((opt, i) => (
                      <li key={i} className="flex items-start gap-1.5">
                        <span className="text-emerald-500 font-bold">•</span>
                        <span>{opt}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
