import React from 'react';
import { ShieldCheck, Dna, Stethoscope, BookOpen, KeyRound } from 'lucide-react';

interface NavbarProps {
  activeTab: 'couple' | 'counselor' | 'panel';
  setActiveTab: (tab: 'couple' | 'counselor' | 'panel') => void;
  sessionCode?: string;
  pendingTicketsCount: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  sessionCode,
  pendingTicketsCount,
}) => {
  return (
    <header className="border-b border-emerald-950/80 bg-slate-950/90 backdrop-blur sticky top-0 z-50">
      {/* Top institutional strip */}
      <div className="bg-gradient-to-r from-emerald-950 via-slate-900 to-emerald-950 border-b border-emerald-900/40 px-4 py-1.5 text-xs text-emerald-300/90 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <span className="font-semibold tracking-wider text-amber-300">FUTURE HEALTH DIGITAL INNOVATION CHALLENGE 2026</span>
          <span className="text-slate-500">•</span>
          <span className="hidden sm:inline text-slate-300">Department of Health Abu Dhabi • Inception (G42) • MBZUAI • Microsoft</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 rounded text-[11px] bg-emerald-900/50 text-emerald-200 border border-emerald-700/50">
            GITEX Abu Dhabi Track 01
          </span>
        </div>
      </div>

      {/* Main navigation header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-600 to-teal-800 p-2 flex items-center justify-center shadow-lg shadow-emerald-900/40 border border-emerald-500/40">
            <Dna className="w-6 h-6 text-white animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                Amanah-Genome <span className="font-serif text-amber-300 text-lg">أمانة للجينوم</span>
              </h1>
              <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800 font-mono">
                ZK-PSI v1.0
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Zero-Knowledge Pre-Marital Genetic Compatibility & Cultural Care Bridge
            </p>
          </div>
        </div>

        {/* Tab Buttons & Session PIN */}
        <div className="flex items-center gap-2 sm:gap-3 flex-wrap">
          {sessionCode && (
            <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900/90 border border-slate-800 text-xs text-slate-300">
              <KeyRound className="w-3.5 h-3.5 text-amber-400" />
              <span>Session PIN:</span>
              <span className="font-mono font-bold text-amber-300 tracking-wider">{sessionCode}</span>
            </div>
          )}

          <div className="bg-slate-900/90 p-1 rounded-xl border border-slate-800 flex items-center gap-1">
            <button
              onClick={() => setActiveTab('couple')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                activeTab === 'couple'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <ShieldCheck className="w-4 h-4" />
              <span>Couple Portal</span>
            </button>

            <button
              onClick={() => setActiveTab('counselor')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition relative ${
                activeTab === 'counselor'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <Stethoscope className="w-4 h-4" />
              <span>Counselor Triage</span>
              {pendingTicketsCount > 0 && (
                <span className="ml-1 px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-amber-500 text-slate-950">
                  {pendingTicketsCount}
                </span>
              )}
            </button>

            <button
              onClick={() => setActiveTab('panel')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                activeTab === 'panel'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              <span>UAE Panel</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};
