import { useEffect, useState } from 'react';
import { Navbar } from './components/Navbar';
import { CouplePortal } from './components/CouplePortal';
import { CounselorPortal } from './components/CounselorPortal';
import { PanelRegistry } from './components/PanelRegistryModal';
import {
  fetchCounselorTickets,
  fetchPanelGenes,
  initSession,
} from './services/api';
import type {
  ClinicalReferralTicket,
  SessionInitResponse,
  UAEPanelGene,
} from './types';
import { ShieldCheck, Sparkles, Building2 } from 'lucide-react';

export function App() {
  const [activeTab, setActiveTab] = useState<'couple' | 'counselor' | 'panel'>('couple');
  const [session, setSession] = useState<SessionInitResponse | null>(null);
  const [tickets, setTickets] = useState<ClinicalReferralTicket[]>([]);
  const [panelGenes, setPanelGenes] = useState<UAEPanelGene[]>([]);
  const [isPanelLoading, setIsPanelLoading] = useState(true);

  // Initialize ephemeral session
  const startNewSession = async () => {
    try {
      const sess = await initSession();
      setSession(sess);
    } catch (err) {
      console.error('Session init error:', err);
    }
  };

  // Fetch triage tickets
  const loadTickets = async () => {
    try {
      const data = await fetchCounselorTickets();
      setTickets(data);
    } catch (err) {
      console.error('Ticket fetch error:', err);
    }
  };

  // Fetch UAE panel metadata
  const loadPanel = async () => {
    setIsPanelLoading(true);
    try {
      const data = await fetchPanelGenes();
      setPanelGenes(data.genes);
    } catch (err) {
      console.error('Panel fetch error:', err);
    } finally {
      setIsPanelLoading(false);
    }
  };

  useEffect(() => {
    startNewSession();
    loadTickets();
    loadPanel();
  }, []);

  const handleTicketCreated = (newTicket: ClinicalReferralTicket) => {
    setTickets((prev) => [newTicket, ...prev.filter((t) => t.ticket_id !== newTicket.ticket_id)]);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-emerald-600 selection:text-white">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        sessionCode={session?.session_code}
        pendingTicketsCount={tickets.filter((t) => t.status !== 'COMPLETED').length}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'couple' && session && (
          <CouplePortal
            sessionId={session.session_id}
            sessionCode={session.session_code}
            onTicketCreated={handleTicketCreated}
            onRefreshSession={startNewSession}
          />
        )}

        {activeTab === 'counselor' && (
          <CounselorPortal
            tickets={tickets}
            onRefreshTickets={loadTickets}
          />
        )}

        {activeTab === 'panel' && (
          <PanelRegistry
            genes={panelGenes}
            isLoading={isPanelLoading}
          />
        )}
      </main>

      {/* Institutional Footer */}
      <footer className="mt-auto border-t border-slate-900 bg-slate-950/80 py-8 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Building2 className="w-4 h-4 text-emerald-400" />
            <span className="font-semibold text-slate-300">Amanah-Genome (أمانة للجينوم)</span>
            <span>•</span>
            <span>Future Health Digital Innovation Challenge 2026 (GITEX Abu Dhabi)</span>
          </div>

          <div className="flex items-center gap-4 text-[11px] text-slate-400">
            <span className="flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span>Zero-Knowledge PSI Standard</span>
            </span>
            <span>•</span>
            <span className="flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span>DoH Abu Dhabi Bioethics Protocol</span>
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
