import SwiftUI
import SubscriptionTrackerCore
import Combine

/// SwiftUI wrapper for SubscriptionManager that conforms to ObservableObject
public class ObservableSubscriptionManager: ObservableObject {
    @Published public var subscriptions: [Subscription] = []
    
    private let manager: SubscriptionManager
    
    public init(manager: SubscriptionManager = SubscriptionManager()) {
        self.manager = manager
        self.subscriptions = manager.subscriptions
    }
    
    // MARK: - CRUD Operations
    
    public func addSubscription(_ subscription: Subscription) {
        manager.addSubscription(subscription)
        subscriptions = manager.subscriptions
    }
    
    public func updateSubscription(_ subscription: Subscription) {
        manager.updateSubscription(subscription)
        subscriptions = manager.subscriptions
    }
    
    public func deleteSubscription(_ subscription: Subscription) {
        manager.deleteSubscription(subscription)
        subscriptions = manager.subscriptions
    }
    
    public func deleteSubscriptions(at offsets: IndexSet) {
        manager.deleteSubscriptions(at: Array(offsets))
        subscriptions = manager.subscriptions
    }
    
    public func getSubscription(byId id: UUID) -> Subscription? {
        manager.getSubscription(byId: id)
    }
    
    // MARK: - Analytics
    
    public var totalMonthlyCost: Double {
        manager.totalMonthlyCost
    }
    
    public var totalYearlyCost: Double {
        manager.totalYearlyCost
    }
    
    public var subscriptionsByCategory: [String: [Subscription]] {
        manager.subscriptionsByCategory
    }
    
    public var activeSubscriptionsCount: Int {
        manager.activeSubscriptionsCount
    }
    
    public func clearAllSubscriptions() {
        manager.clearAllSubscriptions()
        subscriptions = manager.subscriptions
    }
}
