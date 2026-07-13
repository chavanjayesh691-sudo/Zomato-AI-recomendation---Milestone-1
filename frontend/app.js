/**
 * CraveAI - AI Restaurant Recommendation Frontend Logic
 */

document.addEventListener("DOMContentLoaded", () => {
    // Dynamic API Base URL (priority: localStorage -> window.API_BASE_URL -> default "" relative path)
    function getApiBaseUrl() {
        const saved = localStorage.getItem("CRAVEAI_API_BASE_URL");
        if (saved !== null && saved.trim() !== "") {
            return saved.trim().replace(/\/+$/, "");
        }
        return window.API_BASE_URL || (window.CONFIG && window.CONFIG.API_BASE_URL) || "";
    }


    // State
    const state = {
        location: "Indiranagar",
        budget_tier: "medium",
        cuisines: ["Italian"],
        min_rating: 4.0,
        dietary_preferences: "",
        top_k: 10
    };

    // DOM elements
    const locationSelect = document.getElementById("location-select");
    const budgetSelector = document.getElementById("budget-selector");
    const cuisineChips = document.getElementById("cuisine-chips");
    const ratingSelector = document.getElementById("rating-selector");
    const aiPromptInput = document.getElementById("ai-prompt");
    const findBtn = document.getElementById("find-btn");
    const themeToggle = document.getElementById("theme-toggle");

    const resultsContainer = document.getElementById("results-container");
    const loadingState = document.getElementById("loading-state");
    const emptyState = document.getElementById("empty-state");
    const resultsTitle = document.getElementById("results-title");
    const activeLocationDisplay = document.getElementById("active-location-display");
    const activeFiltersTags = document.getElementById("active-filters-tags");

    // Theme Toggle
    themeToggle.addEventListener("click", () => {
        document.documentElement.classList.toggle("dark");
        const icon = themeToggle.querySelector("span");
        icon.textContent = document.documentElement.classList.contains("dark") ? "dark_mode" : "light_mode";
    });

    // Fetch Metadata on Load
    async function loadMetadata() {
        try {
            const response = await fetch(`${getApiBaseUrl()}/api/v1/metadata`);
            if (response.ok) {
                const data = await response.json();
                if (data.available_locations && data.available_locations.length > 0) {
                    locationSelect.innerHTML = "";
                    // Prioritize popular areas at the top
                    const priority = ["indiranagar", "koramangala 5th block", "whitefield", "hsr", "bellandur", "jayanagar", "mg road", "btm"];
                    const locs = data.available_locations;
                    
                    locs.forEach(loc => {
                        const opt = document.createElement("option");
                        opt.value = loc;
                        opt.textContent = loc.charAt(0).toUpperCase() + loc.slice(1);
                        if (loc.toLowerCase() === "indiranagar") {
                            opt.selected = true;
                            state.location = loc;
                        }
                        locationSelect.appendChild(opt);
                    });
                }
            }
        } catch (err) {
            console.warn("Could not load metadata from API, using default locations.", err);
        }
    }

    // Event Listeners for Filters
    locationSelect.addEventListener("change", (e) => {
        state.location = e.target.value;
        fetchRecommendations();
    });

    budgetSelector.addEventListener("click", (e) => {
        const btn = e.target.closest("button[data-budget]");
        if (!btn) return;
        budgetSelector.querySelectorAll("button").forEach(b => {
            b.classList.remove("border-2", "border-primary", "bg-primary/5", "text-primary", "font-bold");
            b.classList.add("border", "border-surface-container-highest", "bg-white", "text-on-surface");
        });
        btn.classList.remove("border", "border-surface-container-highest", "bg-white", "text-on-surface");
        btn.classList.add("border-2", "border-primary", "bg-primary/5", "text-primary", "font-bold");
        state.budget_tier = btn.getAttribute("data-budget");
        fetchRecommendations();
    });

    cuisineChips.addEventListener("click", (e) => {
        const chip = e.target.closest("button[data-cuisine]");
        if (!chip) return;
        const cuisine = chip.getAttribute("data-cuisine");
        const idx = state.cuisines.indexOf(cuisine);
        if (idx > -1) {
            state.cuisines.splice(idx, 1);
            chip.classList.remove("bg-primary", "text-white", "font-semibold");
            chip.classList.add("bg-white", "border", "border-surface-container-highest", "text-on-surface");
        } else {
            state.cuisines.push(cuisine);
            chip.classList.remove("bg-white", "border", "border-surface-container-highest", "text-on-surface");
            chip.classList.add("bg-primary", "text-white", "font-semibold");
        }
        fetchRecommendations();
    });

    ratingSelector.addEventListener("click", (e) => {
        const btn = e.target.closest("button[data-rating]");
        if (!btn) return;
        ratingSelector.querySelectorAll("button").forEach(b => {
            b.classList.remove("border-2", "border-primary", "bg-primary/5", "text-primary", "font-bold");
            b.classList.add("border", "border-surface-container-highest", "bg-white");
        });
        btn.classList.remove("border", "border-surface-container-highest", "bg-white");
        btn.classList.add("border-2", "border-primary", "bg-primary/5", "text-primary", "font-bold");
        state.min_rating = parseFloat(btn.getAttribute("data-rating")) || 0.0;
        fetchRecommendations();
    });

    findBtn.addEventListener("click", () => {
        state.dietary_preferences = aiPromptInput.value.trim() || null;
        fetchRecommendations();
    });

    aiPromptInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            state.dietary_preferences = aiPromptInput.value.trim() || null;
            fetchRecommendations();
        }
    });

    // Fetch and Render Recommendations
    async function fetchRecommendations() {
        resultsContainer.innerHTML = "";
        emptyState.classList.add("hidden");
        loadingState.classList.remove("hidden");
        activeLocationDisplay.textContent = state.location.charAt(0).toUpperCase() + state.location.slice(1);

        // Update active filter pill badges
        renderActiveFilterTags();

        const payload = {
            location: state.location,
            budget_tier: state.budget_tier,
            cuisines: state.cuisines.length > 0 ? state.cuisines.join(", ") : "",
            min_rating: state.min_rating,
            dietary_preferences: aiPromptInput.value.trim() || null,
            top_k: state.top_k
        };

        try {
            const res = await fetch(`${getApiBaseUrl()}/api/v1/recommend`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            loadingState.classList.add("hidden");

            if (!res.ok) {
                let errDetail = `API Error ${res.status}`;
                if (res.status === 502) {
                    errDetail = "HTTP 502 Bad Gateway: Railway backend container is initializing or warming up.";
                }
                throw new Error(errDetail);
            }

            const data = await res.json();
            renderRecommendations(data);
        } catch (err) {
            loadingState.classList.add("hidden");
            console.error("Recommendation fetch error:", err);
            renderErrorState(err.message);
        }
    }

    function renderActiveFilterTags() {
        activeFiltersTags.innerHTML = "";
        
        const budgetLabels = {
            "low": "Low (≤ ₹500)",
            "medium": "Medium (₹501–1500)",
            "high": "High (> ₹1500)",
            "$": "Low (≤ ₹500)",
            "$$": "Medium (₹501–1500)",
            "$$$": "High (> ₹1500)"
        };

        const budgetText = budgetLabels[state.budget_tier.toLowerCase()] || `Budget: ${state.budget_tier}`;
        activeFiltersTags.appendChild(createTagPill("currency_rupee", budgetText));

        if (state.cuisines.length > 0) {
            activeFiltersTags.appendChild(createTagPill("restaurant", state.cuisines.join(", ")));
        }
        if (state.min_rating > 0) {
            activeFiltersTags.appendChild(createTagPill("star", `${state.min_rating}+ ★`));
        }
        activeFiltersTags.appendChild(createTagPill("auto_awesome", "AI Curated"));
    }

    function createTagPill(iconName, text) {
        const span = document.createElement("span");
        span.className = "glass-panel px-3.5 py-1.5 rounded-full text-xs font-semibold text-primary flex items-center gap-1.5 shadow-sm";
        span.innerHTML = `<span class="material-symbols-outlined text-sm">${iconName}</span><span>${text}</span>`;
        return span;
    }

    function renderRecommendations(data) {
        const recs = data.recommendations || [];
        const count = recs.length;
        resultsTitle.textContent = count === 1 ? "1 Top Match for you" : `${count} Matches for you`;

        if (count === 0) {
            emptyState.classList.remove("hidden");
            return;
        }

        recs.forEach((rec, idx) => {
            const card = document.createElement("div");
            card.className = "relative group bg-white dark:bg-surface-dim/40 rounded-2xl overflow-hidden shadow-sm hover:shadow-md border border-surface-container-high transition-all duration-300 p-6";

            const rankNum = rec.rank || (idx + 1);
            const badgeClass = rankNum === 1 
                ? "bg-primary text-white" 
                : "bg-surface-container-high text-on-surface";

            card.innerHTML = `
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-4">
                    <div>
                        <div class="flex items-center gap-3 mb-1.5">
                            <span class="${badgeClass} font-bold text-xs px-3 py-1 rounded-full uppercase tracking-wider">
                                #${rankNum} AI Match
                            </span>
                            <span class="inline-flex items-center gap-1 bg-amber-50 text-amber-700 border border-amber-200 px-2.5 py-0.5 rounded-full text-xs font-bold">
                                <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
                                ${Number(rec.rating || 0).toFixed(1)} / 5
                            </span>
                            ${data.fallback_used ? `<span class="text-[10px] text-on-surface-variant bg-surface-container px-2 py-0.5 rounded">Rule-based Match</span>` : ''}
                        </div>
                        <h2 class="text-2xl font-bold text-on-surface group-hover:text-primary transition-colors">${escapeHtml(rec.name)}</h2>
                        <p class="text-sm font-medium text-on-surface-variant mt-1">${escapeHtml(rec.cuisine)}</p>
                    </div>

                    <div class="flex flex-wrap items-center gap-3">
                        <div class="glass-panel px-4 py-2 rounded-xl flex items-center gap-2 text-on-surface">
                            <span class="material-symbols-outlined text-primary text-lg">currency_rupee</span>
                            <span class="text-sm font-bold">${escapeHtml(rec.estimated_cost || "Cost info not available")}</span>
                        </div>
                    </div>
                </div>

                <!-- AI Insight Explanation Banner -->
                <div class="glass-panel p-4 rounded-xl bg-surface-bright/70 border-l-4 border-l-primary relative overflow-hidden my-4">
                    <div class="flex items-center gap-2 mb-1 text-primary font-bold text-sm">
                        <span class="material-symbols-outlined text-base">auto_awesome</span>
                        <span>AI Recommendation Insight</span>
                    </div>
                    <p class="text-sm text-on-surface leading-relaxed">${escapeHtml(rec.explanation)}</p>
                </div>

                <div class="flex items-center justify-between pt-3 border-t border-surface-container-high mt-4">
                    <span class="text-xs text-on-surface-variant flex items-center gap-1">
                        <span class="material-symbols-outlined text-sm">location_on</span>
                        ${escapeHtml(state.location)}
                    </span>
                    <div class="flex gap-3">
                        <button class="px-5 py-2 rounded-full bg-primary hover:bg-primary-container text-white text-xs font-bold transition-colors shadow-sm">
                            Reserve Table
                        </button>
                        <button class="px-5 py-2 rounded-full bg-surface-container hover:bg-surface-container-high text-on-surface text-xs font-semibold transition-colors">
                            View Menu
                        </button>
                    </div>
                </div>
            `;
            resultsContainer.appendChild(card);
        });
    }

    function renderErrorState(message) {
        resultsTitle.textContent = "Error loading recommendations";
        const is502 = message.includes("502") || message.includes("Failed to fetch");
        resultsContainer.innerHTML = `
            <div class="p-6 rounded-xl bg-red-50 border border-red-200 text-red-700 text-center max-w-xl mx-auto shadow-sm">
                <span class="material-symbols-outlined text-4xl mb-2">error</span>
                <h3 class="font-bold text-lg">Unable to generate recommendations</h3>
                <p class="text-sm mt-1">${escapeHtml(message)}</p>
                ${is502 ? `
                    <div class="mt-4 pt-4 border-t border-red-200 text-xs text-red-800 text-left space-y-2">
                        <p class="font-semibold">Why did this happen?</p>
                        <p>Your Railway container (` + "<code>web-production-016d9.up.railway.app</code>" + `) is warming up and downloading the ~149MB dataset on cold boot. Once loaded, requests complete in under 1 second.</p>
                        <div class="pt-3 flex justify-center">
                            <button onclick="location.reload()" class="px-5 py-2 rounded-xl bg-primary text-white font-bold hover:bg-primary-container transition-all shadow-sm flex items-center gap-1.5">
                                <span class="material-symbols-outlined text-base">refresh</span>
                                Retry Now
                            </button>
                        </div>
                    </div>
                ` : ""}
            </div>
        `;
    }

    function escapeHtml(str) {
        if (!str) return "";
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Initialize
    loadMetadata().then(() => {
        fetchRecommendations();
    });
});
