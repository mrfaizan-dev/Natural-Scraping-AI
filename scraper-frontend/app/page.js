"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";
import { 
  Plus, 
  Trash2, 
  Play, 
  Loader2, 
  CheckCircle2, 
  XCircle, 
  Download, 
  ExternalLink, 
  RefreshCw, 
  Globe, 
  Layers, 
  Sparkles, 
  Search, 
  FileSpreadsheet, 
  FileText,
  ShoppingCart,
  Building2,
  Terminal,
  ShieldCheck,
  Cpu,
  CheckCircle,
  Clock,
  Database,
  BarChart3,
  Activity
} from "lucide-react";

const API_BASE_URL = "http://127.0.0.1:8800";

export default function Home() {
  const [urls, setUrls] = useState(["https://www.amazon.com/s?k=watch"]);
  const [scrapeType, setScrapeType] = useState("ecommerce"); // 'ecommerce' or 'real_estate'
  const [loading, setLoading] = useState(false);
  const [taskId, setTaskId] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [taskStatus, setTaskStatus] = useState(null); 
  const [statusMessage, setStatusMessage] = useState("System ready for execution.");
  const [scrapedData, setScrapedData] = useState([]);
  const [errorDetails, setErrorDetails] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [executionTime, setExecutionTime] = useState(0);

  const pollingRef = useRef(null);
  const canvasRef = useRef(null);
  const timerRef = useRef(null);
  const terminalEndRef = useRef(null);

  // High-Density Neural Wire Network Background Canvas Effect
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let animationFrameId;

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", handleResize);

    const mouse = { x: width / 2, y: height / 2, radius: 180 };
    const handleMouseMove = (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    };
    window.addEventListener("mousemove", handleMouseMove);

    const particleCount = Math.min(Math.floor((width * height) / 9000), 120);
    const particles = [];
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 1.1,
        vy: (Math.random() - 0.5) * 1.1,
        radius: Math.random() * 2.2 + 1.2,
      });
    }

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(52, 211, 153, 0.75)";
        ctx.shadowBlur = 8;
        ctx.shadowColor = "rgba(16, 185, 129, 0.5)";
        ctx.fill();
        ctx.shadowBlur = 0;

        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 160) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(6, 182, 212, ${0.4 * (1 - dist / 160)})`;
            ctx.lineWidth = 1.4; 
            ctx.stroke();
          }
        }

        const mdx = p.x - mouse.x;
        const mdy = p.y - mouse.y;
        const mdist = Math.sqrt(mdx * mdx + mdy * mdy);

        if (mdist < mouse.radius) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.strokeStyle = `rgba(16, 185, 129, ${0.5 * (1 - mdist / mouse.radius)})`;
          ctx.lineWidth = 1.7;
          ctx.stroke();
        }
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("mousemove", handleMouseMove);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  // Timer effect for execution duration tracking
  useEffect(() => {
    if (loading) {
      setExecutionTime(0);
      timerRef.current = setInterval(() => {
        setExecutionTime((prev) => prev + 1);
      }, 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [loading]);

  // Cleanup polling on unmount
  useEffect(() => {
    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, []);

  const handleUrlChange = (index, value) => {
    const updated = [...urls];
    updated[index] = value;
    setUrls(updated);
  };

  const addUrlField = () => {
    if (urls.length < 10) {
      setUrls([...urls, ""]);
    }
  };

  const removeUrlField = (index) => {
    if (urls.length > 1) {
      setUrls(urls.filter((_, i) => i !== index));
    }
  };

  // Start Scraping Job
  const startScraping = async () => {
    const validUrls = urls.map((u) => u.trim()).filter((u) => u.length > 0);
    if (validUrls.length === 0) {
      alert("Please provide at least one valid target URL.");
      return;
    }

    setLoading(true);
    setTaskId(null);
    setSessionId(null);
    setTaskStatus("QUEUED");
    setStatusMessage("Initializing background extraction task queue...");
    setScrapedData([]);
    setErrorDetails(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/scrape`, {
        urls: validUrls,
        scrape_type: scrapeType, 
      });

      if (response.data && response.data.task_id) {
        const receivedTaskId = response.data.task_id;
        setTaskId(receivedTaskId);
        setStatusMessage("Task successfully queued. Establishing live telemetry stream...");
        
        pollTaskStatus(receivedTaskId);
      }
    } catch (err) {
      setLoading(false);
      setTaskStatus("FAILURE");
      setStatusMessage("Failed to dispatch execution payload.");
      setErrorDetails(err.response?.data?.detail || err.message);
    }
  };

  // Poll FastAPI Status Endpoint
  const pollTaskStatus = (id) => {
    if (pollingRef.current) clearInterval(pollingRef.current);

    pollingRef.current = setInterval(async () => {
      try {
        const res = await axios.get(`${API_BASE_URL}/scrape/status/${id}`);
        const data = res.data;

        setTaskStatus(data.status);
        if (data.message) setStatusMessage(data.message);

        if (data.status === "SUCCESS") {
          clearInterval(pollingRef.current);
          setLoading(false);

          const resultObj = data.data || {};
          if (resultObj.user_session_id) {
            setSessionId(resultObj.user_session_id);
          }

          let allItems = [];
          if (Array.isArray(resultObj.raw_data)) {
            resultObj.raw_data.forEach((batchRes) => {
              if (batchRes?.status === "Success" && batchRes?.clean_data?.Clean_Data) {
                const cleanList = batchRes.clean_data.Clean_Data;
                if (Array.isArray(cleanList)) {
                  allItems = [...allItems, ...cleanList];
                }
              }
            });
          }
          setScrapedData(allItems);
        } else if (data.status === "FAILURE") {
          clearInterval(pollingRef.current);
          setLoading(false);
          setErrorDetails(data.error || "Task Execution Pipeline Failed");
        }
      } catch (err) {
        console.error("Telemetry polling exception:", err);
      }
    }, 2500);
  };

  const handleDownload = (format) => {
    if (!sessionId) {
      alert("Active session identifier not found.");
      return;
    }
    const downloadUrl = `${API_BASE_URL}/scrape/downloads/${sessionId}/${format}`;
    window.open(downloadUrl, "_blank");
  };

  // Computed Analytics Metrics
  const totalItems = scrapedData.length;
  const activeSources = [...new Set(scrapedData.map(item => item.source))].filter(Boolean).length;
  const averagePrice = totalItems > 0 ? (() => {
    const prices = scrapedData.map(item => {
      const num = parseFloat(String(item.price || "").replace(/[^0-9.]/g, ""));
      return isNaN(num) ? 0 : num;
    }).filter(p => p > 0);
    if (prices.length === 0) return "N/A";
    const avg = prices.reduce((a, b) => a + b, 0) / prices.length;
    return `$${avg.toFixed(2)}`;
  })() : "N/A";

  const filteredData = scrapedData.filter((item) =>
    (item.title || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (item.source || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (item.location || "").toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-emerald-500 selection:text-white flex flex-col justify-between relative overflow-x-hidden">
      
      {/* Background Neural Wire Canvas */}
      <canvas
        ref={canvasRef}
        className="fixed inset-0 pointer-events-none z-0 opacity-90"
      />

      {/* Professional Dark Ambiance Glow Lights */}
      <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
        <div className="absolute -top-48 -left-48 w-[600px] h-[600px] bg-emerald-900/15 rounded-full blur-[140px]" />
        <div className="absolute top-1/3 -right-48 w-[600px] h-[600px] bg-cyan-900/15 rounded-full blur-[140px]" />
      </div>

      <div className="relative z-10 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-8 flex-1">
        
        {/* Header Section */}
        <header className="flex flex-col md:flex-row items-center justify-between gap-4 border-b border-slate-800/80 pb-6 mb-8 backdrop-blur-sm">
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-2xl bg-slate-900/90 border border-slate-700/60 shadow-lg shadow-emerald-950/30 flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-emerald-400" />
            </div>
            <div>
              <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
                Agentic Web Scraper Pro
              </h1>
              <p className="text-xs sm:text-sm text-slate-400 flex items-center gap-2 mt-0.5">
                <Cpu className="w-3.5 h-3.5 text-cyan-400" /> Enterprise-Grade Automated Data Extraction Engine
              </p>
            </div>
          </div>

          {/* System Telemetry Badges */}
          <div className="flex items-center gap-3 bg-slate-900/90 backdrop-blur-md p-2 rounded-xl border border-slate-800 text-xs shadow-lg">
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-950/60 text-emerald-400 border border-emerald-500/30 shadow-sm">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse shadow-md shadow-emerald-400" />
              Celery Worker Online
            </div>
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyan-950/60 text-cyan-400 border border-cyan-500/30 shadow-sm">
              <Layers className="w-3.5 h-3.5" />
              Redis Active
            </div>
          </div>
        </header>

        {/* Core Control Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          
          {/* Left Column: Extraction Mode & URL Input Console */}
          <div className="lg:col-span-2 bg-slate-900/90 border border-slate-800/90 backdrop-blur-xl rounded-2xl p-6 shadow-2xl space-y-6 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/5 rounded-full blur-2xl pointer-events-none" />

            {/* Scrape Type Selection Toggle */}
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2.5 flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-400" /> Target Extraction Domain
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setScrapeType("ecommerce")}
                  className={`flex items-center justify-center gap-2.5 py-3 px-4 rounded-xl text-sm font-semibold transition border transform active:scale-95 ${
                    scrapeType === "ecommerce"
                      ? "bg-emerald-600/20 text-emerald-300 border-emerald-500/60 shadow-lg shadow-emerald-950/50 ring-1 ring-emerald-500/30"
                      : "bg-slate-950/80 text-slate-400 border-slate-800 hover:border-slate-700 hover:text-slate-200"
                  }`}
                >
                  <ShoppingCart className="w-4 h-4 text-emerald-400" />
                  E-Commerce Scraper
                </button>

                <button
                  type="button"
                  onClick={() => setScrapeType("real_estate")}
                  className={`flex items-center justify-center gap-2.5 py-3 px-4 rounded-xl text-sm font-semibold transition border transform active:scale-95 ${
                    scrapeType === "real_estate"
                      ? "bg-cyan-600/20 text-cyan-300 border-cyan-500/60 shadow-lg shadow-cyan-950/50 ring-1 ring-cyan-500/30"
                      : "bg-slate-950/80 text-slate-400 border-slate-800 hover:border-slate-700 hover:text-slate-200"
                  }`}
                >
                  <Building2 className="w-4 h-4 text-cyan-400" />
                  Real Estate Scraper
                </button>
              </div>
            </div>

            {/* Target URLs Input Section */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <label className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
                  <Globe className="w-4 h-4 text-cyan-400" /> Target URLs Repository
                </label>
                <span className="text-xs font-mono text-slate-300 bg-slate-950 px-2.5 py-1 rounded-md border border-slate-800 shadow-inner">
                  {urls.length} / 10 URLs Active
                </span>
              </div>

              <div className="space-y-3 mb-4 max-h-52 overflow-y-auto pr-1">
                {urls.map((url, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="flex items-center gap-2"
                  >
                    <input
                      type="url"
                      value={url}
                      onChange={(e) => handleUrlChange(idx, e.target.value)}
                      placeholder={
                        scrapeType === "ecommerce"
                          ? "https://www.amazon.com/s?k=... or eBay, Walmart, Daraz"
                          : "https://www.propertyfinder.ae/... or Zameen, Zillow, Rightmove"
                      }
                      className="flex-1 bg-slate-950 border border-slate-800/80 rounded-xl px-4 py-2.5 text-sm text-slate-100 placeholder-slate-600 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/40 transition shadow-inner"
                    />
                    {urls.length > 1 && (
                      <button
                        onClick={() => removeUrlField(idx)}
                        className="p-2.5 text-slate-500 hover:text-red-400 hover:bg-red-500/10 rounded-xl transition border border-transparent hover:border-red-500/20"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    )}
                  </motion.div>
                ))}
              </div>

              <div className="flex items-center justify-between pt-3 border-t border-slate-800/80">
                <button
                  onClick={addUrlField}
                  disabled={urls.length >= 10 || loading}
                  className="flex items-center gap-1.5 text-xs font-semibold text-emerald-400 hover:text-emerald-300 bg-emerald-950/40 hover:bg-emerald-900/40 px-3.5 py-2 rounded-xl transition border border-emerald-500/30 disabled:opacity-50 shadow-sm"
                >
                  <Plus className="w-4 h-4" /> Add Target URL
                </button>

                <button
                  onClick={startScraping}
                  disabled={loading}
                  className="flex items-center gap-2 bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 hover:opacity-95 text-white font-bold px-6 py-2.5 rounded-xl text-sm shadow-lg shadow-emerald-950/60 transition transform active:scale-95 disabled:opacity-50 border border-emerald-400/30"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" /> Processing Engine...
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4 fill-current" /> Execute Scraping
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Feature 2: Advanced Progress Steps Bar */}
            <div className="pt-4 border-t border-slate-800/80">
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
                Execution Pipeline Progress
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px]">
                <div className={`p-2.5 rounded-xl border flex flex-col gap-1 transition ${
                  taskStatus ? "bg-emerald-950/30 border-emerald-500/40 text-emerald-300" : "bg-slate-950 border-slate-800 text-slate-500"
                }`}>
                  <span className="font-bold flex items-center gap-1">1. URL Validation</span>
                  <span className="text-[10px] opacity-80">{taskStatus ? "Passed" : "Waiting"}</span>
                </div>
                <div className={`p-2.5 rounded-xl border flex flex-col gap-1 transition ${
                  taskStatus === "STARTED" || taskStatus === "SUCCESS" ? "bg-cyan-950/30 border-cyan-500/40 text-cyan-300" : "bg-slate-950 border-slate-800 text-slate-500"
                }`}>
                  <span className="font-bold flex items-center gap-1">2. Playwright & Proxy</span>
                  <span className="text-[10px] opacity-80">{taskStatus === "STARTED" || taskStatus === "SUCCESS" ? "Active" : "Pending"}</span>
                </div>
                <div className={`p-2.5 rounded-xl border flex flex-col gap-1 transition ${
                  taskStatus === "STARTED" || taskStatus === "SUCCESS" ? "bg-teal-950/30 border-teal-500/40 text-teal-300" : "bg-slate-950 border-slate-800 text-slate-500"
                }`}>
                  <span className="font-bold flex items-center gap-1">3. Parsing & Pydantic</span>
                  <span className="text-[10px] opacity-80">{taskStatus === "SUCCESS" ? "Completed" : "Pending"}</span>
                </div>
                <div className={`p-2.5 rounded-xl border flex flex-col gap-1 transition ${
                  taskStatus === "SUCCESS" ? "bg-emerald-950/30 border-emerald-500/40 text-emerald-300" : "bg-slate-950 border-slate-800 text-slate-500"
                }`}>
                  <span className="font-bold flex items-center gap-1">4. Excel / CSV Export</span>
                  <span className="text-[10px] opacity-80">{taskStatus === "SUCCESS" ? "Ready" : "Pending"}</span>
                </div>
              </div>
            </div>

          </div>

          {/* Right Column: Live Session & Task Monitor + Live Agent Terminal */}
          <div className="bg-slate-900/90 border border-slate-800/90 backdrop-blur-xl rounded-2xl p-6 shadow-2xl flex flex-col justify-between">
            <div>
              <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4 flex items-center gap-2">
                <Terminal className={`w-4 h-4 text-emerald-400 ${loading ? "animate-spin" : ""}`} /> Telemetry & Session Monitor
              </h2>

              <div className="space-y-3 text-xs">
                <div className="flex justify-between items-center p-3 bg-slate-950 rounded-xl border border-slate-800 shadow-inner">
                  <span className="text-slate-400">Task UUID:</span>
                  <span className="font-mono text-cyan-400 font-medium truncate max-w-[150px]">
                    {taskId || "Not Initialized"}
                  </span>
                </div>

                <div className="flex justify-between items-center p-3 bg-slate-950 rounded-xl border border-slate-800 shadow-inner">
                  <span className="text-slate-400">Session Identifier:</span>
                  <span className="font-mono text-emerald-400 font-medium truncate max-w-[150px]">
                    {sessionId || "Awaiting Completion"}
                  </span>
                </div>

                {/* Status Indicator Card */}
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-2 shadow-inner">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400">Pipeline State:</span>
                    {taskStatus === "PENDING" && (
                      <span className="px-2 py-0.5 rounded bg-amber-950/60 text-amber-300 font-semibold border border-amber-500/30">
                        Queued
                      </span>
                    )}
                    {taskStatus === "STARTED" && (
                      <span className="px-2 py-0.5 rounded bg-blue-950/60 text-blue-300 font-semibold flex items-center gap-1 border border-blue-500/30">
                        <Loader2 className="w-3 h-3 animate-spin" /> Active
                      </span>
                    )}
                    {taskStatus === "SUCCESS" && (
                      <span className="px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-300 font-semibold flex items-center gap-1 border border-emerald-500/30">
                        <CheckCircle2 className="w-3.5 h-3.5" /> Completed
                      </span>
                    )}
                    {taskStatus === "FAILURE" && (
                      <span className="px-2 py-0.5 rounded bg-red-950/60 text-red-300 font-semibold flex items-center gap-1 border border-red-500/30">
                        <XCircle className="w-3.5 h-3.5" /> Failed
                      </span>
                    )}
                    {!taskStatus && <span className="text-slate-500 font-mono">Idle</span>}
                  </div>
                  <p className="text-slate-300 text-xs italic font-mono truncate">{statusMessage}</p>
                </div>

                {/* Feature 1: Live Agent Activity Terminal */}
                <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 font-mono text-[11px] shadow-inner">
                  <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-800/80 text-slate-400">
                    <span className="flex items-center gap-1.5 text-emerald-400">
                      <Activity className="w-3.5 h-3.5" /> Live Agent Stream
                    </span>
                    <span className={`w-2 h-2 rounded-full ${loading ? "bg-emerald-400 animate-ping" : "bg-slate-600"}`} />
                  </div>
                  <div className="space-y-1 text-slate-300 max-h-28 overflow-y-auto pr-1">
                    <p className="text-slate-500">[00:00] System initialized successfully...</p>
                    {loading && (
                      <p className="text-cyan-400">[{`00:${executionTime < 10 ? '0' + executionTime : executionTime}`}] Launching async Playwright & Celery worker node...</p>
                    )}
                    {taskStatus === "STARTED" && (
                      <p className="text-teal-400">[Agent] Rotating headers, moving human mouse cursor & scrolling DOM...</p>
                    )}
                    {taskStatus === "SUCCESS" && (
                      <p className="text-emerald-300 font-bold">[Success] Extracted {scrapedData.length} structured items successfully.</p>
                    )}
                    {taskStatus === "FAILURE" && (
                      <p className="text-red-400 font-bold">[Error] Execution pipeline encountered a timeout or block.</p>
                    )}
                    <div ref={terminalEndRef} />
                  </div>
                </div>

              </div>
            </div>

            {/* Quick Export Downloads Section */}
            {sessionId && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 pt-4 border-t border-slate-800/80 space-y-2"
              >
                <p className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-1">Export Scraped Results:</p>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    onClick={() => handleDownload("excel")}
                    className="flex items-center justify-center gap-1.5 bg-emerald-950/40 hover:bg-emerald-900/50 text-emerald-300 border border-emerald-500/30 py-2.5 px-3 rounded-xl text-xs font-semibold transition shadow-md transform active:scale-95"
                  >
                    <FileSpreadsheet className="w-3.5 h-3.5" /> Excel (.xlsx)
                  </button>
                  <button
                    onClick={() => handleDownload("csv")}
                    className="flex items-center justify-center gap-1.5 bg-cyan-950/40 hover:bg-cyan-900/50 text-cyan-300 border border-cyan-500/30 py-2.5 px-3 rounded-xl text-xs font-semibold transition shadow-md transform active:scale-95"
                  >
                    <FileText className="w-3.5 h-3.5" /> CSV Data
                  </button>
                </div>
              </motion.div>
            )}
          </div>
        </div>

        {/* Error Notification Banner */}
        {errorDetails && (
          <div className="mb-8 p-4 bg-red-950/50 border border-red-500/40 rounded-2xl flex items-start gap-3 text-red-300 text-sm shadow-xl backdrop-blur-md">
            <XCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
            <div>
              <p className="font-bold">Execution Error Encountered</p>
              <p className="text-xs text-red-400 font-mono mt-1">{String(errorDetails)}</p>
            </div>
          </div>
        )}

        {/* Feature 4: Quick Analytics Summary Header */}
        {scrapedData.length > 0 && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6"
          >
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-lg flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-emerald-950/60 text-emerald-400 border border-emerald-500/20">
                <Database className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-slate-400 font-medium">Total Items</p>
                <p className="text-lg font-bold text-slate-100 font-mono">{totalItems}</p>
              </div>
            </div>

            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-lg flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-cyan-950/60 text-cyan-400 border border-cyan-500/20">
                <BarChart3 className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-slate-400 font-medium">Average Price</p>
                <p className="text-lg font-bold text-emerald-400 font-mono">{averagePrice}</p>
              </div>
            </div>

            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-lg flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-teal-950/60 text-teal-400 border border-teal-500/20">
                <Globe className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-slate-400 font-medium">Active Sources</p>
                <p className="text-lg font-bold text-slate-100 font-mono">{activeSources}</p>
              </div>
            </div>

            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-lg flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-blue-950/60 text-blue-400 border border-blue-500/20">
                <Clock className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-slate-400 font-medium">Execution Time</p>
                <p className="text-lg font-bold text-slate-100 font-mono">{executionTime}s</p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Feature 3: Skeleton Loading Shimmer Cards when loading */}
        {loading && scrapedData.length === 0 && (
          <div className="space-y-4 pb-12">
            <div className="bg-slate-900/90 p-4 rounded-2xl border border-slate-800 shadow-xl flex items-center justify-between">
              <div className="h-6 w-48 bg-slate-800 rounded animate-pulse" />
              <div className="h-9 w-64 bg-slate-800 rounded animate-pulse" />
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {[1, 2, 3, 4, 5, 6, 7, 8].map((n) => (
                <div key={n} className="bg-slate-900/60 border border-slate-800/80 rounded-2xl p-4 space-y-3 animate-pulse">
                  <div className="w-full h-40 bg-slate-800/60 rounded-xl" />
                  <div className="h-4 bg-slate-800/80 rounded w-5/6" />
                  <div className="h-4 bg-slate-800/60 rounded w-1/2" />
                  <div className="pt-2 border-t border-slate-800 flex justify-between">
                    <div className="h-5 bg-slate-800 rounded w-1/3" />
                    <div className="h-7 bg-slate-800 rounded w-1/3" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Extracted Data Showcase Section */}
        {scrapedData.length > 0 && (
          <section className="space-y-4 pb-12">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900/90 p-4 rounded-2xl border border-slate-800 shadow-xl backdrop-blur-md">
              <div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  Extracted Data Items <span className="text-xs font-mono bg-emerald-950/80 text-emerald-300 px-2.5 py-0.5 rounded-full border border-emerald-500/30">{scrapedData.length} records parsed</span>
                </h3>
              </div>

              {/* Filter Search */}
              <div className="relative min-w-[260px]">
                <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-400" />
                <input
                  type="text"
                  placeholder="Filter by title, location or source..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-slate-200 focus:outline-none focus:border-emerald-500/60 shadow-inner"
                />
              </div>
            </div>

            {/* Results Grid Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              <AnimatePresence>
                {filteredData.map((item, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    transition={{ duration: 0.2 }}
                    className="bg-slate-900/90 border border-slate-800 hover:border-emerald-500/40 rounded-2xl p-4 flex flex-col justify-between transition group shadow-xl hover:shadow-2xl hover:shadow-emerald-950/40 relative overflow-hidden"
                  >
                    <div>
                      {/* Thumbnail Container */}
                      <div className="w-full h-40 bg-slate-950 rounded-xl overflow-hidden mb-3 border border-slate-800 flex items-center justify-center relative shadow-inner">
                        {item.image_url && item.image_url !== "N/A" ? (
                          <img
                            src={item.image_url}
                            alt={item.title}
                            className="w-full h-full object-contain group-hover:scale-105 transition duration-300"
                            onError={(e) => { e.currentTarget.style.display = 'none'; }}
                          />
                        ) : (
                          <span className="text-xs text-slate-600 font-mono">No Preview Available</span>
                        )}
                        {item.source && (
                          <span className="absolute top-2 right-2 bg-slate-950/90 backdrop-blur-md text-cyan-300 text-[10px] font-bold px-2 py-0.5 rounded-md border border-cyan-500/30 shadow">
                            {item.source}
                          </span>
                        )}
                      </div>

                      {/* Title */}
                      <h4 className="text-xs font-semibold text-slate-200 line-clamp-2 mb-2 group-hover:text-emerald-300 transition">
                        {item.title || "Untitled Item"}
                      </h4>
                    </div>

                    {/* Price and Details */}
                    <div className="pt-2 border-t border-slate-800 mt-2 space-y-2">
                      <div className="flex items-baseline justify-between">
                        <span className="text-base font-extrabold text-emerald-400 font-mono">
                          {item.price && item.price !== "N/A" ? item.price : "N/A"}
                        </span>
                        {item.rating && item.rating !== "N/A" && (
                          <span className="text-[11px] text-amber-400 font-semibold bg-amber-950/40 px-1.5 py-0.5 rounded border border-amber-500/20">
                            ⭐ {item.rating}
                          </span>
                        )}
                      </div>

                      {/* Real Estate Specs summary if present */}
                      {(item.bedrooms || item.bathrooms || item.area_size) && (
                        <div className="text-[11px] text-slate-300 flex gap-2 flex-wrap font-mono bg-slate-950/60 p-1.5 rounded-lg border border-slate-800/80">
                          {item.bedrooms && item.bedrooms !== "N/A" && <span>🛏️ {item.bedrooms}</span>}
                          {item.bathrooms && item.bathrooms !== "N/A" && <span>🛁 {item.bathrooms}</span>}
                          {item.area_size && item.area_size !== "N/A" && <span>📐 {item.area_size}</span>}
                        </div>
                      )}

                      {/* Link Button */}
                      {(item.product_url || item.property_url) && (
                        <a
                          href={item.product_url || item.property_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center justify-center gap-1 w-full bg-slate-950 hover:bg-emerald-600/30 text-slate-300 hover:text-emerald-300 py-1.5 rounded-lg text-[11px] font-semibold transition border border-slate-800 hover:border-emerald-500/40 shadow-sm"
                        >
                          View Source Link <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          </section>
        )}

      </div>

      {/* Footer */}
      <footer className="relative z-10 py-4 text-center text-xs text-slate-500 border-t border-slate-800/80 bg-slate-950/90 backdrop-blur-md">
        <p className="flex items-center justify-center gap-1.5 font-medium">
          <span>Designed & Developed for</span>
          <span className="font-semibold text-cyan-400">Mr Faizan</span>
          <span>| Agentic Web Scraper Pro</span>
        </p>
      </footer>

    </div>
  );
}



