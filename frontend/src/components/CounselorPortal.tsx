import React, { useState } from 'react';
import {
  Stethoscope,
  Clock,
  CheckCircle2,
  Calendar,
  AlertCircle,
  FileCheck,
  Shield,
  RefreshCw,
} from 'lucide-react';
import type { ClinicalReferralTicket } from '../types';
import { updateTicketStatus } from '../services/api';

interface CounselorPortalProps {
  tickets: ClinicalReferralTicket[];
  onRefreshTickets: () => void;
}

export const CounselorPortal: React.FC<CounselorPortalProps> = ({
  tickets,
  onRefreshTickets,
}) => {
  const [selectedTicket, setSelectedTicket] = useState<ClinicalReferralTicket | null>(
    tickets.length > 0 ? tickets[0] : null
  );
  const [isUpdating, setIsUpdating] = useState(false);

  const handleStatusChange = async (ticketId: string, newStatus: string) => {
    setIsUpdating(true);
    try {
      const res = await updateTicketStatus(ticketId, newStatus);
      setSelectedTicket(res.ticket);
      onRefreshTickets();
    } catch (err: any) {
      alert(`Failed to update status: ${err.message}`);
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Counselor Header */}
      <div className="bg-gradient-to-r from-emerald-950 via-slate-900 to-slate-900 p-6 rounded-2xl border border-emerald-800/40 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-amber-400 mb-1">
            <Stethoscope className="w-4 h-4" />
            <span>DoH Genetic Counseling Triage Station</span>
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            Abu Dhabi Premarital Clinical Intake & Care Network
          </h2>
          <p className="text-xs text-slate-300 mt-1 max-w-2xl">
            Licensed genetic counselors review sanitized Zero-Knowledge clinical tickets, conduct confidential teleconsultations,
            and facilitate sponsored PGT-M/IVF referrals across Abu Dhabi healthcare centers.
          </p>
        </div>

        <button
          onClick={onRefreshTickets}
          className="self-start md:self-auto flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-200 transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Queue</span>
        </button>
      </div>

      {/* Main Grid: Triage Queue on Left, Detailed Clinical Brief on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Triage Queue List */}
        <div className="lg:col-span-1 bg-slate-900/80 rounded-2xl p-5 border border-slate-800 shadow-md flex flex-col">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
              <Clock className="w-3.5 h-3.5 text-amber-400" />
              <span>Incoming Triage Tickets ({tickets.length})</span>
            </h3>
          </div>

          {tickets.length === 0 ? (
            <div className="py-12 text-center text-slate-500 text-xs">
              <AlertCircle className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p>No active referral tickets in queue.</p>
              <p className="text-[11px] text-slate-600 mt-1">
                Evaluate a high-risk match in the Couple Portal and click "Connect with DoH Counselor" to generate one.
              </p>
            </div>
          ) : (
            <div className="space-y-2.5 overflow-y-auto max-h-[550px] pr-1">
              {tickets.map((t) => (
                <button
                  key={t.ticket_id}
                  onClick={() => setSelectedTicket(t)}
                  className={`w-full text-left p-3.5 rounded-xl border transition ${
                    selectedTicket?.ticket_id === t.ticket_id
                      ? 'border-emerald-500 bg-emerald-950/40 ring-1 ring-emerald-500'
                      : 'border-slate-800 bg-slate-950/50 hover:bg-slate-900 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="font-mono text-[11px] font-bold text-amber-300">{t.ticket_id}</span>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${
                        t.status === 'COMPLETED'
                          ? 'bg-emerald-900/80 text-emerald-300'
                          : t.status === 'TELECONSULT_SCHEDULED'
                          ? 'bg-blue-900/80 text-blue-300'
                          : 'bg-amber-900/80 text-amber-300'
                      }`}
                    >
                      {t.status.replace(/_/g, ' ')}
                    </span>
                  </div>
                  <div className="text-xs font-medium text-white truncate">
                    {t.affected_diseases_en.length > 0
                      ? t.affected_diseases_en.join(', ')
                      : 'Carrier Evaluation'}
                  </div>
                  <div className="text-[11px] text-slate-400 mt-1 flex items-center justify-between">
                    <span>Risk: {t.child_risk_probability * 100}% recessive</span>
                    <span className="font-mono text-[10px] text-slate-500">{t.session_id}</span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Detailed Sanitized Clinical Brief */}
        <div className="lg:col-span-2 bg-slate-900/80 rounded-2xl p-6 border border-slate-800 shadow-md">
          {selectedTicket ? (
            <div className="space-y-6">
              {/* Ticket Top bar */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-800">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800">
                      {selectedTicket.ticket_id}
                    </span>
                    <span className="text-xs text-slate-400">
                      Session Code: <span className="font-mono text-slate-300">{selectedTicket.session_id}</span>
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-white mt-1">
                    Sanitized Pre-Conception Clinical Summary Brief
                  </h3>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-400">Status:</span>
                  <span className="text-xs px-2.5 py-1 rounded-lg font-bold bg-slate-800 text-amber-300 border border-slate-700 uppercase">
                    {selectedTicket.status.replace(/_/g, ' ')}
                  </span>
                </div>
              </div>

              {/* Privacy Shield Seal */}
              <div className="p-3.5 rounded-xl bg-slate-950/70 border border-emerald-900/50 flex items-center gap-3 text-xs text-emerald-300">
                <Shield className="w-5 h-5 text-emerald-400 shrink-0" />
                <p>
                  <strong>Zero-Knowledge Privacy Protection:</strong> Patient names and non-overlapping variants are cryptographically
                  redacted. Only actionable reciprocal recessive risk biomarkers are made accessible to counselors.
                </p>
              </div>

              {/* Medical Findings Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800">
                  <div className="text-slate-400 font-medium">Reciprocal Risk Gene:</div>
                  <div className="text-base font-bold text-amber-400 mt-1">
                    {selectedTicket.intersecting_genes.join(', ') || 'N/A'}
                  </div>
                  <div className="text-slate-300 text-xs mt-1">
                    {selectedTicket.affected_diseases_en.join(', ')}
                  </div>
                  <div className="text-[11px] text-slate-500 mt-0.5 font-serif">
                    {selectedTicket.affected_diseases_ar.join(', ')}
                  </div>
                </div>

                <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800">
                  <div className="text-slate-400 font-medium">Childhood Transmission Risk:</div>
                  <div className="text-base font-bold text-rose-400 mt-1">
                    {selectedTicket.child_risk_probability * 100}% per pregnancy
                  </div>
                  <div className="text-slate-400 text-xs mt-1">
                    Autosomal Recessive Pattern (25% affected, 50% healthy carrier, 25% unaffected non-carrier).
                  </div>
                </div>
              </div>

              {/* Clinical Referral Pathway Guidance */}
              <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-xs space-y-2">
                <div className="text-slate-400 font-semibold uppercase tracking-wider text-[11px]">
                  Recommended Abu Dhabi Reproductive Care Protocol:
                </div>
                <div className="text-white font-medium text-sm">
                  {selectedTicket.recommended_pathway}
                </div>
                <p className="text-slate-300 leading-relaxed text-xs">
                  Counselors initiate teleconsultation to introduce pre-implantation embryo diagnosis (PGT-M)
                  sponsored under Abu Dhabi Government healthcare subsidies, eliminating disease transmission without marriage disruption.
                </p>
                <div className="text-[11px] text-slate-500 flex items-center gap-1.5 pt-1">
                  <span>Authorizing Network:</span>
                  <span className="text-emerald-400 font-medium">{selectedTicket.doh_clinic_reference}</span>
                </div>
              </div>

              {/* Counselor Action Handlers */}
              <div className="pt-4 border-t border-slate-800 flex items-center justify-between flex-wrap gap-3">
                <div className="text-xs text-slate-400">Update Clinical Case Disposition:</div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleStatusChange(selectedTicket.ticket_id, 'TELECONSULT_SCHEDULED')}
                    disabled={isUpdating}
                    className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-medium text-xs transition"
                  >
                    <Calendar className="w-3.5 h-3.5" />
                    <span>Schedule Teleconsultation</span>
                  </button>

                  <button
                    onClick={() => handleStatusChange(selectedTicket.ticket_id, 'COMPLETED')}
                    disabled={isUpdating}
                    className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs transition"
                  >
                    <FileCheck className="w-3.5 h-3.5" />
                    <span>Authorize PGT-M Referral</span>
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="py-24 text-center text-slate-500 text-xs">
              <CheckCircle2 className="w-10 h-10 mx-auto mb-2 opacity-40 text-emerald-500" />
              <p className="text-sm font-semibold text-slate-300">Select a Ticket to View Clinical Summary</p>
              <p className="text-xs text-slate-500 mt-1">All clinical summaries follow strict Zero-Knowledge anonymization standards.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
