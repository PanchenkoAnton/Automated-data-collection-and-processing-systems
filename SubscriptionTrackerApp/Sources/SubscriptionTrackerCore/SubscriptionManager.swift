import Foundation

/// Manages subscriptions with persistence
public class SubscriptionManager {
    public private(set) var subscriptions: [Subscription] = []
    
    private let storageKey = "subscriptions"
    private let userDefaults: UserDefaults
    
    public init(userDefaults: UserDefaults = .standard) {
        self.userDefaults = userDefaults
        loadSubscriptions()
    }
    
    // MARK: - CRUD Operations
    
    /// Add a new subscription
    public func addSubscription(_ subscription: Subscription) {
        subscriptions.append(subscription)
        saveSubscriptions()
    }
    
    /// Update an existing subscription
    public func updateSubscription(_ subscription: Subscription) {
        if let index = subscriptions.firstIndex(where: { $0.id == subscription.id }) {
            subscriptions[index] = subscription
            saveSubscriptions()
        }
    }
    
    /// Delete a subscription
    public func deleteSubscription(_ subscription: Subscription) {
        subscriptions.removeAll { $0.id == subscription.id }
        saveSubscriptions()
    }
    
    /// Delete subscriptions at specific indices
    public func deleteSubscriptions(at indices: [Int]) {
        let sortedIndices = indices.sorted(by: >)
        for index in sortedIndices {
            if index < subscriptions.count {
                subscriptions.remove(at: index)
            }
        }
        saveSubscriptions()
    }
    
    /// Get subscription by ID
    public func getSubscription(byId id: UUID) -> Subscription? {
        subscriptions.first { $0.id == id }
    }
    
    // MARK: - Analytics
    
    /// Calculate total monthly cost of all active subscriptions
    public var totalMonthlyCost: Double {
        subscriptions
            .filter { $0.isActive }
            .reduce(0) { $0 + $1.monthlyCost }
    }
    
    /// Calculate total yearly cost of all active subscriptions
    public var totalYearlyCost: Double {
        subscriptions
            .filter { $0.isActive }
            .reduce(0) { $0 + $1.yearlyCost }
    }
    
    /// Get subscriptions grouped by category
    public var subscriptionsByCategory: [String: [Subscription]] {
        Dictionary(grouping: subscriptions) { $0.category }
    }
    
    /// Get active subscriptions count
    public var activeSubscriptionsCount: Int {
        subscriptions.filter { $0.isActive }.count
    }
    
    // MARK: - Persistence
    
    private func saveSubscriptions() {
        do {
            let encoder = JSONEncoder()
            encoder.dateEncodingStrategy = .iso8601
            let data = try encoder.encode(subscriptions)
            userDefaults.set(data, forKey: storageKey)
        } catch {
            print("Error saving subscriptions: \(error)")
        }
    }
    
    private func loadSubscriptions() {
        guard let data = userDefaults.data(forKey: storageKey) else { return }
        
        do {
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            subscriptions = try decoder.decode([Subscription].self, from: data)
        } catch {
            print("Error loading subscriptions: \(error)")
        }
    }
    
    /// Clear all subscriptions (useful for testing)
    public func clearAllSubscriptions() {
        subscriptions.removeAll()
        saveSubscriptions()
    }
}
