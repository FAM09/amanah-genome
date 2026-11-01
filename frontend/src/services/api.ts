import type {
  ClinicalReferralTicket,
  IntersectionMatchResult,
  SessionInitResponse,
  UAEPanelGene,
  UploadReceipt,
} from '../types';

const API_BASE =
  import.meta.env.VITE_API_URL ||
  (typeof window !== 'undefined' && (window.location.port === '8020' || window.location.pathname.startsWith('/app'))
    ? ''
    : 'http://localhost:8020');

export async function initSession(): Promise<SessionInitResponse> {
  const res = await fetch(`${API_BASE}/api/session/init`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to initialize session');
  return res.json();
}

export async function uploadVcf(
  sessionId: string,
  party: 'A' | 'B',
  file: File | Blob,
  filename: string
): Promise<UploadReceipt> {
  const formData = new FormData();
  formData.append('party', party);
  formData.append('vcf_file', file, filename);

  const res = await fetch(`${API_BASE}/api/session/${sessionId}/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(err.detail || 'Upload failed');
  }
  return res.json();
}

export async function evaluateMatch(sessionId: string): Promise<IntersectionMatchResult> {
  const res = await fetch(`${API_BASE}/api/session/${sessionId}/evaluate`, { method: 'POST' });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Evaluation failed' }));
    throw new Error(err.detail || 'Evaluation failed');
  }
  return res.json();
}

export async function sendChatMessage(
  sessionId: string,
  messages: { role: string; content: string }[]
): Promise<{ response: string; match_status: string; intersecting_genes: string[] }> {
  const res = await fetch(`${API_BASE}/api/session/${sessionId}/counsel`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages }),
  });
  if (!res.ok) throw new Error('Chat failed');
  return res.json();
}

export async function createReferralTicket(sessionId: string): Promise<ClinicalReferralTicket> {
  const res = await fetch(`${API_BASE}/api/session/${sessionId}/referral`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to create referral ticket');
  return res.json();
}

export async function fetchCounselorTickets(): Promise<ClinicalReferralTicket[]> {
  const res = await fetch(`${API_BASE}/api/counselor/tickets`);
  if (!res.ok) throw new Error('Failed to fetch triage tickets');
  return res.json();
}

export async function updateTicketStatus(
  ticketId: string,
  status: string
): Promise<{ message: string; ticket: ClinicalReferralTicket }> {
  const res = await fetch(`${API_BASE}/api/counselor/tickets/${ticketId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status }),
  });
  if (!res.ok) throw new Error('Failed to update ticket');
  return res.json();
}

export async function fetchPanelGenes(): Promise<{ genes: UAEPanelGene[]; panel_count: number }> {
  const res = await fetch(`${API_BASE}/api/panel`);
  if (!res.ok) throw new Error('Failed to fetch panel metadata');
  return res.json();
}
