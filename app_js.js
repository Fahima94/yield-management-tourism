/**
 * ===================================
 * YIELD MANAGEMENT TOURISM - APP MAIN
 * Application principale du système
 * ===================================
 */

// État global de l'application
class YieldManagementApp {
    constructor() {
        this.yieldEngine = new YieldManagementEngine();
        this.currentTab = 'dashboard';
        this.data = this.initializeData();
        this.isInitialized = false;
        
        // Bind des méthodes
        this.showTab = this.showTab.bind(this);
        this.updateAllocations = this.updateAllocations.bind(this);
        this.applyYieldStrategy = this.applyYieldStrategy.bind(this);
    }

    /**
     * Initialisation des données de démonstration
     */
    initializeData() {
        return {
            weeklyPerf: [
                {week: 'S22', clicks: 2847, conversions: 98, rate: 3.4, ca: 247500, margin: 18.2, status: 'good'},
                {week: 'S23', clicks: 3156, conversions: 112, rate: 3.5, ca: 289600, margin: 19.1, status: 'good'},
                {week: 'S24', clicks: 2734, conversions: 87, rate: 3.2, ca: 228900, margin: 16.8, status: 'warning'},
                {week: 'S25', clicks: 3892, conversions: 143, rate: 3.7, ca: 378200, margin: 21.3, status: 'good'},
                {week: 'S26', clicks: 2189, conversions: 67, rate: 3.1, ca: 187400, margin: 15.2, status: 'critical'}
            ],
            flights: [
                {flight: 'AF738', dest: 'Maldives', allocated: 45, sold: 38, remaining: 7, buyPrice: 890, sellPrice: 1245, margin: 39.8, status: 'good'},
                {flight: 'TG947', dest: 'Thaïlande', allocated: 35, sold: 31, remaining: 4, buyPrice: 675, sellPrice: 985, margin: 45.9, status: 'good'},
                {flight: 'QR834', dest: 'Maldives', allocated: 25, sold: 18, remaining: 7, buyPrice: 920, sellPrice: 1189, margin: 29.2, status: 'warning'},
                {flight: 'EK405', dest: 'Dubai', allocated: 30, sold: 29, remaining: 1, buyPrice: 540, sellPrice: 789, margin: 46.1, status: 'good'},
                {flight: 'GA715', dest: 'Bali', allocated: 45, sold: 32, remaining: 13, buyPrice: 780, sellPrice: 1098, margin: 40.8, status: 'warning'}
            ],
            hotels: [
                {name: 'Oberoi Beach Resort', chain: 'Oberoi Hotels', type: 'Ferme', rooms: 25, price: 320, commission: 12, usage: 92, perf: 'Excellent'},
                {name: 'Mercure Koh Samui', chain: 'Mercure', type: 'Allotement', rooms: 40, price: 185, commission: 15, usage: 87, perf: 'Très Bon'},
                {name: 'TBH Luxury Maldives', chain: 'TBH Hotels', type: 'Ferme', rooms: 20, price: 450, commission: 10, usage: 95, perf: 'Excellent'},
                {name: 'Hilton Dubai Creek', chain: 'Hilton', type: 'Allotement', rooms: 35, price: 240, commission: 18, usage: 78, perf: 'Bon'},
                {name: 'Novotel Bali Benoa', chain: 'Accor', type: 'Ferme', rooms: 30, price: 165, commission: 16, usage: 83, perf: 'Bon'},
                {name: 'Shangri-La Bangkok', chain: 'Shangri-La', type: 'Allotement', rooms: 28, price: 285, commission: 14, usage: 91, perf: 'Très Bon'},
                {name: 'Conrad Maldives', chain: 'Hilton', type: 'Ferme', rooms: 15, price: 680, commission: 8, usage: 97, perf: 'Excellent'},
                {name: 'Sofitel Dubai Palm', chain: 'Accor', type: 'Allotement', rooms: 32, price: 295, commission: 17, usage: 89, perf: 'Très Bon'},
                {name: 'Four Seasons Bali', chain: 'Four Seasons', type: 'Ferme', rooms: 18, price: 520, commission: 9, usage: 94, perf: 'Excellent'}
            ],
            yieldData: [
                {product: 'Maldives Premium', clickRate: 2.8, stock: 12, currentPrice: 1890, suggestedPrice: 1795, action: 'Réduction', impact: '+15%'},
                {product: 'Thailand Beach', clickRate: 4.2, stock: 8, currentPrice: 1245, suggestedPrice: 1345, action: 'Augmentation', impact: '+8%'},
                {product: 'Dubai Luxury', clickRate: 3.1, stock: 15, currentPrice: 985, suggestedPrice: 985, action: 'Maintien', impact: '0%'},
                {product: 'Bali Culture', clickRate: 3.8, stock: 5, currentPrice: 1156, suggestedPrice: 1225, action: 'Augmentation', impact: '+6%'}
            ],
            risks: [
                {indicator: 'Taux de Remplissage', value: '87%', target: '90%', gap: '-3%', trend: '↗️', action: 'Optimiser pricing'},
                {indicator: 'Stock Résiduel', value: '32 places', target: '< 20', gap: '+12', trend: '⚠️', action: 'Promotion flash'},
                {indicator: 'Marge Globale', value: '18.9%', target: '20%', gap: '-1.1%', trend: '↘️', action: 'Réviser achats'},
                {indicator: 'Conversion Rate', value: '3.4%', target: '3.5%', gap: '-0.1%', trend: '↗️', action: 'A/B test landing'}
            ]
        };
    }

    /**
     * Initialisation de l'application
     */
    init() {
        if (this.isInitialized) return;
        
        console.log('🚀 Initialisation Yield Management System...');
        
        // Populate data
        this.populateAllTables();
        
        // Event listeners
        this.attachEventListeners();
        
        // Initial setup
        this.showTab('dashboard');
        
        // Auto-refresh des données
        this.startAutoRefresh();
        
        this.isInitialized = true;
        console.log('✅ Système initialisé avec succès');
    }

    /**
     * Affichage des onglets
     */
    showTab(tabName) {
        // Masquer tous les contenus
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Désactiver tous les boutons
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Activer l'onglet sélectionné
        const selectedTab = document.getElementById(tabName);
        const selectedButton = document.querySelector(`[onclick="showTab('${tabName}')"]`);
        
        if (selectedTab) {
            selectedTab.classList.add('active');
            this.currentTab = tabName;
        }
        
        if (selectedButton) {
            selectedButton.classList.add('active');
        }
        
        // Actions spécifiques par onglet
        this.handleTabSpecificActions(tabName);
        
        console.log(`📊 Onglet actif: ${tabName}`);
    }

    /**
     * Actions spécifiques selon l'onglet
     */
    handleTabSpecificActions(tabName) {
        switch (tabName) {
            case 'hotels':
                setTimeout(() => this.drawHotelChart(), 100);
                break;
            case 'yield':
                this.updateYieldRecommendations();
                break;
            case 'analytics':
                this.updateAnalytics();
                break;
        }
    }

    /**
     * Population de tous les tableaux
     */
    populateAllTables() {
        this.populateWeeklyPerformance();
        this.populateFlightAllocations();
        this.populateHotelContracts();
        this.populateYieldStrategy();
        this.populateRiskAnalysis();
    }

    /**
     * Performance hebdomadaire
     */
    populateWeeklyPerformance() {
        const tbody = document.getElementById('weeklyPerformance');
        if (!tbody) return;
        
        tbody.innerHTML = this.data.weeklyPerf.map(week => `
            <tr class="animate-slide-up">
                <td><strong>${week.week}</strong></td>
                <td>${week.clicks.toLocaleString()}</td>
                <td><strong>${week.conversions}</strong></td>
                <td>${week.rate}%</td>
                <td class="profit-positive"><strong>€${week.ca.toLocaleString()}</strong></td>
                <td>${week.margin}%</td>
                <td><span class="status-${week.status}">${this.getStatusText(week.status)}</span></td>
            </tr>
        `).join('');
    }

    /**
     * Allocations de vol
     */
    populateFlightAllocations() {
        const tbody = document.getElementById('flightAllocations');
        if (!tbody) return;
        
        tbody.innerHTML = this.data.flights.map(flight => `
            <tr class="animate-slide-up">
                <td><strong>${flight.flight}</strong></td>
                <td>${flight.dest}</td>
                <td>${flight.allocated}</td>
                <td><strong>${flight.sold}</strong></td>
                <td>${flight.remaining}</td>
                <td>€${flight.buyPrice}</td>
                <td><strong>€${flight.sellPrice}</strong></td>
                <td class="profit-positive"><strong>${flight.margin}%</strong></td>
                <td><span class="status-${flight.status}">${this.getStatusText(flight.status)}</span></td>
            </tr>
        `).join('');
    }

    /**
     * Contrats hôteliers
     */
    populateHotelContracts() {
        const tbody = document.getElementById('hotelContracts');
        if (!tbody) return;
        
        tbody.innerHTML = this.data.hotels.map(hotel => `
            <tr class="animate-slide-up">
                <td><strong>${hotel.name}</strong></td>
                <td>${hotel.chain}</td>
                <td><span class="font-bold ${hotel.type === 'Ferme' ? 'status-good' : 'status-warning'}">${hotel.type}</span></td>
                <td>${hotel.rooms}</td>
                <td><strong>€${hotel.price}</strong></td>
                <td>${hotel.commission}%</td>
                <td><strong>${hotel.usage}%</strong></td>
                <td><span class="status-${this.getPerformanceStatus(hotel.perf)}">${hotel.perf}</span></td>
            </tr>
        `).join('');
    }

    /**
     * Stratégie yield
     */
    populateYieldStrategy() {
        const tbody = document.getElementById('yieldStrategy');
        if (!tbody) return;
        
        tbody.innerHTML = this.data.yieldData.map(item => `
            <tr class="animate-slide-up">
                <td><strong>${item.product}</strong></td>
                <td>${item.clickRate}%</td>
                <td>${item.stock}</td>
                <td>€${item.currentPrice}</td>
                <td><strong>€${item.suggestedPrice}</strong></td>
                <td><span class="font-bold ${this.getActionClass(item.action)}">${item.action}</span></td>
                <td class="${item.impact.includes('+') ? 'profit-positive' : 'profit-negative'}"><strong>${item.impact}</strong></td>
            </tr>