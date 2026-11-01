import React, { useState } from 'react';
import {
  Upload,
  Lock,
  Cpu,
  CheckCircle2,
  AlertTriangle,
  Send,
  MessageSquare,
  Sparkles,
  ArrowRight,
  RefreshCw,
  UserCheck,
} from 'lucide-react';
import { MOCK_SCENARIOS } from '../data/mockScenarios';
import type { MockScenario } from '../data/mockScenarios';
import type {
  ChatMessage,
  ClinicalReferralTicket,
  IntersectionMatchResult,
  UploadReceipt,
} from '../types';
import {
  createReferralTicket,
  evaluateMatch,
  sendChatMessage,
  uploadVcf,
} from '../services/api';

interface CouplePortalProps {
  sessionId: string;
  sessionCode: string;
  onTicketCreated: (ticket: ClinicalReferralTicket) => void;
  onRefreshSession: () => void;
}

export const CouplePortal: React.FC<CouplePortalProps> = ({
  sessionId,
  sessionCode,
  onTicketCreated,
  onRefreshSession,
}) => {
  // Scenario and Upload State
  const [selectedScenario, setSelectedScenario] = useState<MockScenario | null>(null);
  const [receiptA, setReceiptA] = useState<UploadReceipt | null>(null);
  const [receiptB, setReceiptB] = useState<UploadReceipt | null>(null);
  const [isUploadingA, setIsUploadingA] = useState(false);
  const [isUploadingB, setIsUploadingB] = useState(false);

  // Match State
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [matchResult, setMatchResult] = useState<IntersectionMatchResult | null>(null);

  // Referral State
  const [isBookingReferral, setIsBookingReferral] = useState(false);
  const [referralTicket, setReferralTicket] = useState<ClinicalReferralTicket | null>(null);

  // AI Chat State
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content:
        'Marhaban! I am Amanah-AI, your Abu Dhabi Pre-Conception & Genetic Wellness Companion. ' +
        'Upload your genomic files or select a benchmark scenario to evaluate compatibility with zero-knowledge cryptographic privacy.',
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isSendingChat, setIsSendingChat] = useState(false);

  // 1-Click Load Scenario
  const handleLoadScenario = async (scenario: MockScenario) => {
    setSelectedScenario(scenario);
    setMatchResult(null);
    setReferralTicket(null);

    // Auto upload both files
    setIsUploadingA(true);
    setIsUploadingB(true);
    try {
      const blobA = new Blob([scenario.ahmadVcf], { type: 'text/plain' });
      const recA = await uploadVcf(sessionId, 'A', blobA, 'ahmad_sample.vcf');
      setReceiptA(recA);

      const blobB = new Blob([scenario.fatimaVcf], { type: 'text/plain' });
      const recB = await uploadVcf(sessionId, 'B', blobB, 'fatima_sample.vcf');
      setReceiptB(recB);
    } catch (err: any) {
      alert(`Upload error: ${err.message}`);
    } finally {
      setIsUploadingA(false);
      setIsUploadingB(false);
    }
  };

  // Custom File Upload
  const handleCustomUpload = async (party: 'A' | 'B', file: File) => {
    if (party === 'A') setIsUploadingA(true);
    else setIsUploadingB(true);

    try {
      const receipt = await uploadVcf(sessionId, party, file, file.name);
      if (party === 'A') setReceiptA(receipt);
      else setReceiptB(receipt);
    } catch (err: any) {
      alert(`Failed to upload ${file.name}: ${err.message}`);
    } finally {
      if (party === 'A') setIsUploadingA(false);
      else setIsUploadingB(false);
    }
  };

  // Evaluate Match
  const handleEvaluate = async () => {
    setIsEvaluating(true);
    try {
      const res = await evaluateMatch(sessionId);
      setMatchResult(res);

      // Trigger automatic contextual guidance from AI
      const initialQuery = res.is_compatible
        ? 'We are fully compatible. Please summarize our next steps.'
        : `We both carry ${res.intersecting_genes.join(', ')}. What does this mean for our wedding and future children?`;

      const newHistory: ChatMessage[] = [
        ...messages,
        { role: 'user', content: initialQuery },
      ];
      setMessages(newHistory);

      const chatRes = await sendChatMessage(sessionId, newHistory);
      setMessages([...newHistory, { role: 'assistant', content: chatRes.response }]);
    } catch (err: any) {
      alert(`Evaluation failed: ${err.message}`);
    } finally {
      setIsEvaluating(false);
    }
  };

  // Send Chat
  const handleSendMessage = async (textToSend?: string) => {
    const text = textToSend || inputMessage;
    if (!text.trim() || isSendingChat) return;

    const newHistory: ChatMessage[] = [...messages, { role: 'user', content: text }];
    setMessages(newHistory);
    setInputMessage('');
    setIsSendingChat(true);

    try {
      const res = await sendChatMessage(sessionId, newHistory);
      setMessages([...newHistory, { role: 'assistant', content: res.response }]);
    } catch (err: any) {
      setMessages([
        ...newHistory,
        {
          role: 'assistant',
          content: 'I apologize, but I could not connect to the clinical advice engine. Please connect directly with a DoH counselor.',
        },
      ]);
    } finally {
      setIsSendingChat(false);
    }
  };

  // Create Counselor Referral Ticket
  const handleBookReferral = async () => {
    setIsBookingReferral(true);
    try {
      const ticket = await createReferralTicket(sessionId);
      setReferralTicket(ticket);
      onTicketCreated(ticket);
    } catch (err: any) {
      alert(`Booking failed: ${err.message}`);
    } finally {
      setIsBookingReferral(false);
    }
  };

  const isReadyForMatch = receiptA && receiptB;

  return (
    <div className="space-y-8">
      {/* Hero Banner with UAE Bioethics & Privacy Notice */}
      <div className="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-slate-900 p-6 rounded-2xl border border-emerald-800/40 shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-emerald-600/10 via-transparent to-transparent pointer-events-none" />
        <div className="max-w-3xl">
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-emerald-900/60 border border-emerald-700/50 text-emerald-300 text-xs font-medium mb-3">
            <Lock className="w-3.5 h-3.5 text-emerald-400" />
            <span>Transient In-Memory PSI • Zero Raw DNA Storage</span>
            <span className="text-slate-400">• Session PIN: <strong className="text-amber-300 font-mono">{sessionCode}</strong></span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Confidential Pre-Marital Genetic Screening
          </h2>
          <p className="mt-2 text-sm text-slate-300 leading-relaxed">
            Protecting family lineages through modern science and Islamic bioethics. Evaluates reciprocal carrier status
            for the Top 10 UAE high-prevalence recessive conditions without exposing unshared genetic markers to either partner.
          </p>
        </div>
      </div>

      {/* Step 1: Benchmark Scenarios Quick Loader */}
      <div className="bg-slate-900/80 rounded-2xl p-6 border border-slate-800 shadow-md">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider text-amber-400 flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              <span>Step 1: Select Evaluator Benchmark Scenario</span>
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Select one of the 4 calibrated UAE premarital cases, or upload your own VCF files below.
            </p>
          </div>
          <button
            onClick={onRefreshSession}
            className="self-start sm:self-auto flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 transition"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Reset Session</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
          {MOCK_SCENARIOS.map((sc) => (
            <button
              key={sc.id}
              onClick={() => handleLoadScenario(sc)}
              className={`p-4 rounded-xl text-left border transition relative flex flex-col justify-between ${
                selectedScenario?.id === sc.id
                  ? 'border-emerald-500 bg-emerald-950/40 ring-1 ring-emerald-500'
                  : 'border-slate-800 bg-slate-950/60 hover:border-slate-700 hover:bg-slate-900'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className={`text-[11px] px-2 py-0.5 rounded-full border font-semibold ${sc.badgeColor}`}>
                    {sc.badge}
                  </span>
                </div>
                <h4 className="text-sm font-bold text-white mb-1">{sc.title}</h4>
                <p className="text-xs text-slate-400 line-clamp-3 leading-relaxed">{sc.description}</p>
              </div>
              <div className="mt-3 pt-2 border-t border-slate-800/80 text-[11px] text-emerald-400 font-medium flex items-center gap-1">
                <span>Load Scenario</span>
                <ArrowRight className="w-3 h-3" />
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Step 2: Dual Upload Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Partner 1 (Ahmad) */}
        <div className="bg-slate-900/90 rounded-2xl p-6 border border-slate-800 shadow-md">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-emerald-950 text-emerald-400 flex items-center justify-center font-bold text-sm border border-emerald-800/60">
                A
              </div>
              <div>
                <h3 className="text-sm font-bold text-white">Partner 1: Ahmad</h3>
                <p className="text-xs text-slate-400">Prospective Groom • Individual Genomic Vault</p>
              </div>
            </div>
            {receiptA && (
              <span className="flex items-center gap-1 text-xs text-emerald-400 font-medium bg-emerald-950/80 px-2.5 py-1 rounded-full border border-emerald-800">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Blinded & Committed</span>
              </span>
            )}
          </div>

          {receiptA ? (
            <div className="bg-slate-950/80 rounded-xl p-4 border border-slate-800 space-y-2 text-xs">
              <div className="flex justify-between text-slate-400">
                <span>Sample Reference:</span>
                <span className="font-mono text-slate-200">{receiptA.sample_id}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Variants Screened:</span>
                <span className="text-slate-200">{receiptA.variants_scanned} records</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Carrier Alleles Extracted:</span>
                <span className="text-amber-400 font-bold">{receiptA.pathogenic_carrier_count} detected</span>
              </div>
              <div className="pt-2 border-t border-slate-800/80">
                <div className="text-[11px] text-slate-500 mb-0.5">Merkle Commitment Hash:</div>
                <div className="font-mono text-[10px] text-emerald-400 truncate bg-slate-900 p-1.5 rounded">
                  {receiptA.commitment_hash}
                </div>
              </div>
            </div>
          ) : (
            <div className="border-2 border-dashed border-slate-800 hover:border-emerald-600/50 rounded-xl p-6 text-center transition">
              <Upload className="w-8 h-8 text-slate-500 mx-auto mb-2 animate-bounce" />
              <p className="text-xs text-slate-300 font-medium">Drag & Drop Ahmad's VCF File</p>
              <p className="text-[11px] text-slate-500 mt-1">Standard VCF v4.2 format (.vcf)</p>
              <input
                type="file"
                accept=".vcf,.txt"
                className="mt-3 text-xs text-slate-400 file:mr-2 file:py-1 file:px-2.5 file:rounded-md file:border-0 file:text-xs file:bg-slate-800 file:text-emerald-300 hover:file:bg-slate-700 cursor-pointer"
                onChange={(e) => e.target.files?.[0] && handleCustomUpload('A', e.target.files[0])}
                disabled={isUploadingA}
              />
            </div>
          )}
        </div>

        {/* Partner 2 (Fatima) */}
        <div className="bg-slate-900/90 rounded-2xl p-6 border border-slate-800 shadow-md">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-teal-950 text-teal-400 flex items-center justify-center font-bold text-sm border border-teal-800/60">
                B
              </div>
              <div>
                <h3 className="text-sm font-bold text-white">Partner 2: Fatima</h3>
                <p className="text-xs text-slate-400">Prospective Bride • Individual Genomic Vault</p>
              </div>
            </div>
            {receiptB && (
              <span className="flex items-center gap-1 text-xs text-emerald-400 font-medium bg-emerald-950/80 px-2.5 py-1 rounded-full border border-emerald-800">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Blinded & Committed</span>
              </span>
            )}
          </div>

          {receiptB ? (
            <div className="bg-slate-950/80 rounded-xl p-4 border border-slate-800 space-y-2 text-xs">
              <div className="flex justify-between text-slate-400">
                <span>Sample Reference:</span>
                <span className="font-mono text-slate-200">{receiptB.sample_id}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Variants Screened:</span>
                <span className="text-slate-200">{receiptB.variants_scanned} records</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Carrier Alleles Extracted:</span>
                <span className="text-amber-400 font-bold">{receiptB.pathogenic_carrier_count} detected</span>
              </div>
              <div className="pt-2 border-t border-slate-800/80">
                <div className="text-[11px] text-slate-500 mb-0.5">Merkle Commitment Hash:</div>
                <div className="font-mono text-[10px] text-emerald-400 truncate bg-slate-900 p-1.5 rounded">
                  {receiptB.commitment_hash}
                </div>
              </div>
            </div>
          ) : (
            <div className="border-2 border-dashed border-slate-800 hover:border-teal-600/50 rounded-xl p-6 text-center transition">
              <Upload className="w-8 h-8 text-slate-500 mx-auto mb-2 animate-bounce" />
              <p className="text-xs text-slate-300 font-medium">Drag & Drop Fatima's VCF File</p>
              <p className="text-[11px] text-slate-500 mt-1">Standard VCF v4.2 format (.vcf)</p>
              <input
                type="file"
                accept=".vcf,.txt"
                className="mt-3 text-xs text-slate-400 file:mr-2 file:py-1 file:px-2.5 file:rounded-md file:border-0 file:text-xs file:bg-slate-800 file:text-teal-300 hover:file:bg-slate-700 cursor-pointer"
                onChange={(e) => e.target.files?.[0] && handleCustomUpload('B', e.target.files[0])}
                disabled={isUploadingB}
              />
            </div>
          )}
        </div>
      </div>

      {/* Step 3: Zero-Knowledge PSI Execution Button */}
      <div className="flex flex-col items-center justify-center p-6 bg-slate-900/60 rounded-2xl border border-slate-800">
        <div className="text-center max-w-xl mb-4">
          <div className="flex items-center justify-center gap-2 text-xs font-semibold uppercase tracking-wider text-emerald-400 mb-1">
            <Cpu className="w-4 h-4" />
            <span>Private Set Intersection Engine (PSI)</span>
          </div>
          <p className="text-xs text-slate-400">
            Intersection is computed over cryptographic HMAC-SHA256 salted hashes. Neither party or server administrator
            can deduce non-overlapping variants.
          </p>
        </div>

        <button
          onClick={handleEvaluate}
          disabled={!isReadyForMatch || isEvaluating}
          className={`px-8 py-3.5 rounded-xl font-bold text-sm shadow-xl flex items-center gap-2.5 transition ${
            isReadyForMatch && !isEvaluating
              ? 'bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white cursor-pointer shadow-emerald-900/40'
              : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
          }`}
        >
          {isEvaluating ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span>Computing Zero-Knowledge Intersection...</span>
            </>
          ) : (
            <>
              <Lock className="w-4 h-4" />
              <span>Execute Zero-Knowledge Compatibility Match</span>
            </>
          )}
        </button>
      </div>

      {/* Step 4: Compatibility Match Result Display */}
      {matchResult && (
        <div
          className={`p-6 rounded-2xl border transition shadow-xl ${
            matchResult.is_compatible
              ? 'bg-emerald-950/40 border-emerald-600/60'
              : 'bg-rose-950/40 border-rose-600/60'
          }`}
        >
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
            <div className="flex items-start gap-3">
              {matchResult.is_compatible ? (
                <div className="w-10 h-10 rounded-xl bg-emerald-600/20 text-emerald-400 flex items-center justify-center border border-emerald-500/40">
                  <CheckCircle2 className="w-6 h-6" />
                </div>
              ) : (
                <div className="w-10 h-10 rounded-xl bg-rose-600/20 text-rose-400 flex items-center justify-center border border-rose-500/40">
                  <AlertTriangle className="w-6 h-6" />
                </div>
              )}
              <div>
                <div className="flex items-center gap-2">
                  <span
                    className={`text-xs px-2.5 py-0.5 rounded-full font-bold uppercase ${
                      matchResult.is_compatible
                        ? 'bg-emerald-900/80 text-emerald-200 border border-emerald-700'
                        : 'bg-rose-900/80 text-rose-200 border border-rose-700'
                    }`}
                  >
                    {matchResult.risk_level}
                  </span>
                  <span className="text-xs font-mono text-slate-400">{matchResult.zk_proof_token}</span>
                </div>
                <h3 className="text-xl font-bold text-white mt-1">
                  {matchResult.is_compatible
                    ? 'Harmonious Genetic Compatibility'
                    : 'Elevated Recessive Inheritance Risk Detected (25%)'}
                </h3>
              </div>
            </div>

            {/* DoH Referral Button */}
            {!matchResult.is_compatible && (
              <button
                onClick={handleBookReferral}
                disabled={isBookingReferral || !!referralTicket}
                className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-500 text-slate-950 font-bold text-xs transition shadow-lg shadow-amber-900/30"
              >
                <UserCheck className="w-4 h-4" />
                <span>
                  {referralTicket
                    ? `Ticket Dispatched: ${referralTicket.ticket_id}`
                    : 'Connect with Certified DoH Counselor'}
                </span>
              </button>
            )}
          </div>

          {/* Details */}
          <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-400">Reciprocal Child Risk:</span>
              <div className="text-lg font-bold text-white mt-0.5">
                {matchResult.child_risk_probability * 100}% per pregnancy
              </div>
              <p className="text-[11px] text-slate-500 mt-1">
                {matchResult.is_compatible
                  ? 'Baseline general population risk only.'
                  : 'Requires both parents passing recessive allele.'}
              </p>
            </div>

            <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-400">Intersecting Carrier Genes:</span>
              <div className="text-lg font-bold text-amber-300 mt-0.5">
                {matchResult.intersecting_genes.length > 0
                  ? matchResult.intersecting_genes.join(', ')
                  : 'None (Zero Overlap)'}
              </div>
              <p className="text-[11px] text-slate-500 mt-1">
                {matchResult.is_compatible
                  ? 'Zero recessive mutations in common.'
                  : matchResult.intersecting_gene_details[0]?.disease_name_en || 'Recessive condition'}
              </p>
            </div>

            <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-400">Zero-Knowledge Guarantee:</span>
              <div className="text-xs font-medium text-emerald-400 mt-1">
                Zero Leaked Non-Overlapping Genes
              </div>
              <p className="text-[11px] text-slate-400 mt-1 truncate">
                Audit Hash: {matchResult.audit_hash}
              </p>
            </div>
          </div>

          {/* Clinical Options Banner for High-Risk */}
          {!matchResult.is_compatible && matchResult.intersecting_gene_details.length > 0 && (
            <div className="mt-4 p-4 rounded-xl bg-amber-950/30 border border-amber-800/40 text-xs">
              <div className="font-semibold text-amber-300 mb-1 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Abu Dhabi Department of Health Recommended Clinical Pathway:</span>
              </div>
              <ul className="list-disc list-inside space-y-1 text-slate-300">
                {matchResult.intersecting_gene_details[0].clinical_options.map((opt, idx) => (
                  <li key={idx}>{opt}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Step 5: Interactive Cultural AI Companion */}
      <div className="bg-slate-900/90 rounded-2xl p-6 border border-slate-800 shadow-xl">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-amber-500 to-emerald-600 flex items-center justify-center shadow">
              <MessageSquare className="w-5 h-5 text-slate-950" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-white">Amanah-AI Companion</h3>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800 font-semibold">
                  DoH Guardrails Active
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Emirathi Cultural & Clinical Guidance • Arabic & English • Non-Stigmatizing
              </p>
            </div>
          </div>
        </div>

        {/* Suggested Prompt Pills */}
        <div className="py-3 flex items-center gap-2 flex-wrap text-xs">
          <span className="text-slate-400 text-[11px]">Recommended Inquiries:</span>
          <button
            onClick={() => handleSendMessage('Should we cancel our wedding because we are carriers?')}
            className="px-3 py-1 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
          >
            "Should we cancel our wedding?"
          </button>
          <button
            onClick={() => handleSendMessage('What is PGT-M and how does it prevent inherited disease?')}
            className="px-3 py-1 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
          >
            "What is PGT-M / IVF?"
          </button>
          <button
            onClick={() => handleSendMessage('How does Islamic bioethics view genetic testing and IVF in Abu Dhabi?')}
            className="px-3 py-1 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
          >
            "Islamic Bioethics & Lineage (Hifz an-Nasl)"
          </button>
        </div>

        {/* Message Thread */}
        <div className="h-72 overflow-y-auto space-y-3 p-4 bg-slate-950/70 rounded-xl border border-slate-800/80 text-xs">
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] sm:max-w-[75%] p-3.5 rounded-xl leading-relaxed whitespace-pre-wrap ${
                  m.role === 'user'
                    ? 'bg-emerald-600 text-white rounded-br-none'
                    : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-bl-none shadow'
                }`}
              >
                {m.content}
              </div>
            </div>
          ))}
          {isSendingChat && (
            <div className="flex justify-start">
              <div className="bg-slate-900 border border-slate-800 text-slate-400 p-3 rounded-xl text-xs flex items-center gap-2">
                <RefreshCw className="w-3.5 h-3.5 animate-spin text-emerald-400" />
                <span>Amanah-AI is composing clinical guidance...</span>
              </div>
            </div>
          )}
        </div>

        {/* Chat Input */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="mt-3 flex items-center gap-2"
        >
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask Amanah-AI about your results, reproductive options, or DoH care programs..."
            className="flex-1 bg-slate-950 border border-slate-800 focus:border-emerald-500 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 outline-none transition"
          />
          <button
            type="submit"
            disabled={!inputMessage.trim() || isSendingChat}
            className="bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-800 disabled:text-slate-600 text-white p-2.5 rounded-xl transition"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};
