import { useState, useEffect, useRef } from "react"
import { Bell, X, CheckCheck } from "lucide-react"
import { Link } from "react-router-dom"
import api from "../../api/axios"

function NotificationBell() {
  const [count, setCount] = useState(0)
  const [notifications, setNotifications] = useState([])
  const [open, setOpen] = useState(false)
  const ref = useRef(null)

  async function fetchCount() {
    try {
      const res = await api.get("/notifications/unread-count")
      setCount(res.data?.data?.unread_count || 0)
    } catch {}
  }

  async function fetchNotifs() {
    try {
      const res = await api.get("/notifications?page=1&page_size=8")
      setNotifications(res.data?.data?.notifications || [])
    } catch {}
  }

  useEffect(() => {
    fetchCount()
    const id = setInterval(fetchCount, 30000)
    return () => clearInterval(id)
  }, [])

  useEffect(() => {
    if (open) fetchNotifs()
  }, [open])

  useEffect(() => {
    function outside(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener("mousedown", outside)
    return () => document.removeEventListener("mousedown", outside)
  }, [])

  async function markAll() {
    try {
      await api.put("/notifications/read-all")
      setCount(0)
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })))
    } catch {}
  }

  async function markOne(id) {
    try {
      await api.put(`/notifications/${id}/read`)
      setNotifications(prev => prev.map(n => n.id === id ? { ...n, is_read: true } : n))
      setCount(c => Math.max(0, c - 1))
    } catch {}
  }

  return (
    <div className="relative" ref={ref}>
      <button onClick={() => setOpen(!open)} className="relative p-2.5 rounded-full border border-border bg-white hover:bg-cream transition-colors">
        <Bell size={18} className="text-navy" />
        {count > 0 && (
          <span className="absolute -top-1 -right-1 w-5 h-5 bg-accent-orange text-white text-[10px] font-bold rounded-full flex items-center justify-center">
            {count > 9 ? "9+" : count}
          </span>
        )}
      </button>

      {open && (
        <div className="absolute right-0 mt-3 w-[380px] bg-white rounded-3xl border border-border shadow-[0_20px_60px_rgba(0,0,0,.10)] overflow-hidden z-50">
          <div className="flex items-center justify-between p-5 border-b border-border">
            <h3 className="font-serif text-lg text-navy">Notifications</h3>
            <div className="flex items-center gap-3">
              <button onClick={markAll} className="text-xs text-body hover:text-navy flex items-center gap-1"><CheckCheck size={14} />Mark all read</button>
              <button onClick={() => setOpen(false)} className="p-1 hover:bg-cream rounded-full"><X size={16} /></button>
            </div>
          </div>

          <div className="max-h-[420px] overflow-y-auto">
            {notifications.length === 0 ? (
              <div className="p-10 text-center">
                <div className="w-12 h-12 bg-cream rounded-full flex items-center justify-center mx-auto mb-3"><Bell size={20} className="text-body/50" /></div>
                <p className="text-body text-sm">No notifications</p>
                <p className="text-body/50 text-xs mt-1">New engineering jobs will appear here</p>
              </div>
            ) : (
              notifications.map(n => (
                <div key={n.id} className={`p-4 border-b border-border/50 hover:bg-cream/50 transition-colors ${!n.is_read ? "bg-orange-50/30" : ""}`}>
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-navy line-clamp-1">{n.title}</p>
                      <p className="text-xs text-body mt-1 line-clamp-2">{n.message}</p>
                      <div className="flex items-center gap-2 mt-2">
                        <span className={`text-[10px] px-2 py-1 rounded-full border ${n.hybrid_score > 0.6 ? "bg-emerald-50 text-emerald-600 border-emerald-100" : "bg-cream text-body border-border"}`}>
                          {Math.round(n.hybrid_score * 100)}% match
                        </span>
                        <span className="text-[10px] text-body/50">{new Date(n.created_at).toLocaleTimeString()}</span>
                      </div>
                    </div>
                    {!n.is_read && <button onClick={() => markOne(n.id)} className="w-2 h-2 bg-accent-orange rounded-full mt-2 shrink-0" />}
                  </div>
                  {n.job && <a href={n.job.apply_link} target="_blank" rel="noreferrer" className="mt-3 inline-flex text-xs text-accent-orange hover:text-orange-600 font-medium">Apply Now →</a>}
                </div>
              ))
            )}
          </div>

          <div className="p-3 bg-cream/50 border-t border-border text-center">
            <Link to="/jobs" onClick={() => setOpen(false)} className="text-xs font-medium text-navy hover:text-accent-orange">View all jobs →</Link>
          </div>
        </div>
      )}
    </div>
  )
}

export default NotificationBell